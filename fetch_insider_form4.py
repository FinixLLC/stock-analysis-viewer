#!/usr/bin/env python3
"""
Fetch SEC Form 4 insider transactions for S&P 500 pipeline BUY/WATCH tickers.
Run from repo root:  python3 fetch_insider_form4.py
Outputs:            insider-activity.json
"""
import json, re, time, xml.etree.ElementTree as ET, urllib.request, urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path

UA         = "EVCDM Research evcdm@test.com"
DAYS_BACK  = 90          # look-back window for all transactions
CLUSTER_DAYS = 30        # window for cluster-buy detection
CLUSTER_MIN  = 3         # min distinct insiders buying to be "cluster buy"
MAX_FILINGS  = 25        # max Form 4 filings to parse per ticker
RESULTS_PATH = "sp500-results.json"
OUT_PATH     = "insider-activity.json"


# ── helpers ────────────────────────────────────────────────────────────────────

def http_get(url, retries=3):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (404, 400): return None
            time.sleep(2 ** attempt)
        except Exception:
            time.sleep(2 ** attempt)
    return None


def cik_for_ticker(ticker, tickers_data):
    for v in tickers_data.values():
        if v["ticker"].upper() == ticker.upper():
            return str(v["cik_str"]).zfill(10)
    return None


def get_form4_accessions(cik, cutoff_date):
    """Return list of (accession_nodash, filing_date, primary_doc) for Form 4s after cutoff."""
    raw = http_get(f"https://data.sec.gov/submissions/CIK{cik}.json")
    if not raw: return []
    data = json.loads(raw)
    recent = data.get("filings", {}).get("recent", {})
    forms   = recent.get("form", [])
    accs    = recent.get("accessionNumber", [])
    dates   = recent.get("filingDate", [])
    primaries = recent.get("primaryDocument", [])
    results = []
    for i, f in enumerate(forms):
        if f != "4": continue
        filing_date = dates[i] if i < len(dates) else ""
        if filing_date < cutoff_date: break  # filings are newest-first
        acc = accs[i].replace("-", "") if i < len(accs) else ""
        prim = primaries[i] if i < len(primaries) else ""
        if acc:
            results.append((acc, filing_date, prim))
        if len(results) >= MAX_FILINGS:
            break
    return results


def _text(el, path):
    node = el.find(path)
    return node.text.strip() if node is not None and node.text else ""


def parse_form4_xml(xml_bytes):
    """
    Parse Form 4 XML. Returns dict:
      {"filer": str, "title": str, "is_officer": bool, "is_director": bool,
       "transactions": [{"date","code","shares","price","acquired"}]}
    """
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return None

    ns = ""  # Form 4 XML rarely uses namespace prefix

    # Reporting owner info — can be multiple owners; take first
    owner_el = root.find(".//reportingOwner")
    if owner_el is None:
        return None
    filer     = _text(owner_el, "reportingOwnerIdentity/rptOwnerName")
    title     = _text(owner_el, "reportingOwnerRelationship/officerTitle")
    is_officer  = _text(owner_el, "reportingOwnerRelationship/isOfficer") == "1"
    is_director = _text(owner_el, "reportingOwnerRelationship/isDirector") == "1"
    is_10pct    = _text(owner_el, "reportingOwnerRelationship/isTenPercentOwner") == "1"

    transactions = []
    for txn in root.findall(".//nonDerivativeTransaction"):
        code = _text(txn, "transactionCoding/transactionCode")
        if code not in ("P", "S"):   # only open-market purchase or sale
            continue
        date   = _text(txn, "transactionDate/value")
        shares_str = _text(txn, "transactionAmounts/transactionShares/value")
        price_str  = _text(txn, "transactionAmounts/transactionPricePerShare/value")
        acq_str    = _text(txn, "transactionAmounts/transactionAcquiredDisposedCode/value")

        try:   shares = abs(float(shares_str.replace(",","")))
        except: shares = 0
        try:   price  = float(price_str.replace(",",""))
        except: price  = 0.0

        if shares > 0 and date:
            transactions.append({
                "date":     date,
                "code":     code,       # P = purchase, S = sale
                "shares":   int(shares),
                "price":    round(price, 2),
                "acquired": acq_str,    # A or D
            })

    return {
        "filer":       filer.title(),
        "title":       title,
        "is_officer":  is_officer,
        "is_director": is_director,
        "is_10pct":    is_10pct,
        "transactions": transactions,
    }


def fetch_form4_xml(cik_int, accession, primary_doc):
    """Fetch Form 4 XML bytes. Falls back to scanning the index."""
    base = f"https://www.sec.gov/Archives/edgar/data/{cik_int}/{accession}/"

    # Try primary_doc first if it looks like XML
    if primary_doc and (primary_doc.endswith(".xml") or primary_doc.endswith(".XML")):
        raw = http_get(base + primary_doc)
        if raw and raw.strip().startswith(b"<"): return raw

    # Fall back: scan the index for an XML file
    idx = http_get(f"https://data.sec.gov/Archives/edgar/data/{cik_int}/{accession}/{accession}-index.json")
    if idx:
        try:
            files = json.loads(idx).get("files", [])
            for f in files:
                name = f.get("name","")
                if name.endswith(".xml") and "xsd" not in name.lower():
                    raw = http_get(base + name)
                    if raw and raw.strip().startswith(b"<"): return raw
        except Exception:
            pass

    return None


def compute_signal(all_txns, cutoff_dt, cluster_cutoff_dt):
    """
    all_txns: list of {"filer", "title", "date", "code", "shares"}
    Returns (signal, buy_count, sell_count, net_shares, distinct_buyers_30d)
    """
    buy_shares = sell_shares = 0
    distinct_buyers_30d = set()

    for t in all_txns:
        try:
            tdate = datetime.strptime(t["date"], "%Y-%m-%d").date()
        except ValueError:
            continue
        if t["code"] == "P":
            buy_shares += t["shares"]
            if tdate >= cluster_cutoff_dt:
                distinct_buyers_30d.add(t["filer"])
        elif t["code"] == "S":
            sell_shares += t["shares"]

    net = buy_shares - sell_shares
    n_buyers = len(distinct_buyers_30d)

    if n_buyers >= CLUSTER_MIN:
        signal = "cluster_buy"
    elif net > 0:
        signal = "net_buy"
    elif sell_shares > 0 and net < -5000:
        signal = "net_sell"
    else:
        signal = "neutral"

    return signal, buy_shares, sell_shares, net, n_buyers


# ── main ───────────────────────────────────────────────────────────────────────

def main():
    # Load pipeline results to identify tickers
    results_path = Path(RESULTS_PATH)
    if not results_path.exists():
        print(f"[insider] {RESULTS_PATH} not found — run from repo root")
        return
    with open(results_path) as f:
        results = json.load(f).get("results", [])

    tickers = sorted({
        r["ticker"] for r in results
        if r.get("verdict") in ("BUY", "WATCH") or r.get("entry_override") == "WATCH_ENTRY"
    })
    print(f"[insider] {len(tickers)} BUY/WATCH tickers: {tickers}")

    # Load SEC company tickers (CIK lookup)
    print("[insider] loading SEC company_tickers.json...")
    raw = http_get("https://www.sec.gov/files/company_tickers.json")
    tickers_data = json.loads(raw) if raw else {}

    now_utc  = datetime.now(timezone.utc)
    cutoff   = (now_utc - timedelta(days=DAYS_BACK)).strftime("%Y-%m-%d")
    cutoff_dt         = datetime.strptime(cutoff, "%Y-%m-%d").date()
    cluster_cutoff_dt = (now_utc - timedelta(days=CLUSTER_DAYS)).date()

    output = {}

    for ticker in tickers:
        print(f"\n  [{ticker}]", flush=True)
        cik = cik_for_ticker(ticker, tickers_data)
        if not cik:
            print(f"  [{ticker}] CIK not found, skipping")
            output[ticker] = {"signal": "no_data", "transactions": []}
            continue
        cik_int = int(cik)

        accessions = get_form4_accessions(cik, cutoff)
        print(f"  [{ticker}] CIK={cik}  Form 4 filings (90d): {len(accessions)}", flush=True)
        if not accessions:
            output[ticker] = {"signal": "no_data", "transactions": []}
            continue

        all_txns = []
        for acc, filing_date, primary in accessions:
            xml_bytes = fetch_form4_xml(cik_int, acc, primary)
            if not xml_bytes:
                continue
            parsed = parse_form4_xml(xml_bytes)
            if not parsed:
                continue
            for t in parsed["transactions"]:
                all_txns.append({
                    "date":   t["date"],
                    "filer":  parsed["filer"],
                    "title":  parsed["title"],
                    "code":   t["code"],
                    "shares": t["shares"],
                    "price":  t["price"],
                    "value":  int(t["shares"] * t["price"]),
                })
            time.sleep(0.15)

        # Only keep P and S within the 90d window
        all_txns = [t for t in all_txns if t["date"] >= cutoff]
        all_txns.sort(key=lambda t: t["date"], reverse=True)

        signal, buy_sh, sell_sh, net_sh, n_buyers = compute_signal(
            all_txns, cutoff_dt, cluster_cutoff_dt
        )
        buys_  = [t for t in all_txns if t["code"] == "P"]
        sells_ = [t for t in all_txns if t["code"] == "S"]

        print(f"  [{ticker}] signal={signal}  buys={len(buys_)} sells={len(sells_)} net={net_sh:+,}  buyers_30d={n_buyers}", flush=True)

        output[ticker] = {
            "signal":       signal,
            "buy_txns":     len(buys_),
            "sell_txns":    len(sells_),
            "net_shares_90d": net_sh,
            "buyers_30d":   n_buyers,
            "transactions": all_txns[:20],  # cap at 20 rows for display
        }

    with open(OUT_PATH, "w") as f:
        json.dump({"generated_at": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"), "data": output}, f, indent=2)
    print(f"\n[insider] written to {OUT_PATH} ({len(output)} tickers)")


if __name__ == "__main__":
    main()
