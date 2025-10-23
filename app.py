#!/usr/bin/env python3
"""
app.py
Lightweight Flask API wrapper for OSINT-Phone-Tool (Light).
- Endpoint /run  : proses file numbers.txt -> hasil CSV + JSON summary
- Endpoint /report : lihat summary JSON terakhir
- Endpoint /download : download CSV hasil
Security:
- Optional API token via env var OSINT_API_TOKEN (recommended for Termux use)
- Only reads local numbers.txt and writes to osint_output/
- Does NOT perform any deanonymization, location/IP lookups, or private-data scraping.
"""

import os
import csv
import time
import hmac
import hashlib
from urllib.parse import quote_plus
from flask import Flask, request, jsonify, send_from_directory, abort
import phonenumbers

# Configuration
OUTPUT_DIR = "osint_output"
OUT_CSV = os.path.join(OUTPUT_DIR, "osint_phone_report.csv")
INPUT_FILE = "numbers.txt"
API_TOKEN = os.getenv("OSINT_API_TOKEN", "")  # Set in environment for basic auth-like protection
DEFAULT_REGION = os.getenv("OSINT_DEFAULT_REGION", "ID")

SEARCH_TEMPLATES = {
    "google": "https://www.google.com/search?q={q}",
    "duckduckgo": "https://duckduckgo.com/?q={q}",
    "bing": "https://www.bing.com/search?q={q}",
    "whatsapp": "https://wa.me/{plain}",
    "truecaller": "https://www.truecaller.com/search/{country_code}/{plain}",
    "telegram": "https://t.me/s/{plain}",
    "facebook": "https://www.facebook.com/search/top/?q={q}",
    "twitter": "https://twitter.com/search?q={q}",
    "youtube": "https://www.youtube.com/results?search_query={q}"
}

app = Flask(__name__)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Simple token check helper (constant-time compare)
def _check_token(req):
    if not API_TOKEN:
        # no token configured -> allow local access
        return True
    token = req.headers.get("X-API-Token", "")
    # use hmac.compare_digest for timing-safe comparison
    return hmac.compare_digest(token, API_TOKEN)


def normalize_number(number, default_region=DEFAULT_REGION):
    try:
        pn = phonenumbers.parse(number, default_region)
        e164 = phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
        international = phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        national = phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.NATIONAL)
        country_code = str(pn.country_code)
        valid = phonenumbers.is_valid_number(pn)
        return {
            "input": number,
            "e164": e164,
            "international": international,
            "national": national,
            "country_code": country_code,
            "valid": valid
        }
    except Exception as e:
        return {"input": number, "error": str(e)}


def build_links(norm):
    if "e164" not in norm or not norm.get("e164"):
        return {}
    q = quote_plus(norm.get("e164", "") + " phone")
    plain = norm.get("e164", "").replace("+", "")
    cc = norm.get("country_code", "")
    links = {}
    for k, tpl in SEARCH_TEMPLATES.items():
        try:
            links[k] = tpl.format(q=q, plain=plain, country_code=cc)
        except Exception:
            links[k] = ""
    return links


def process_input_file(input_path=INPUT_FILE):
    if not os.path.exists(input_path):
        return {"error": "input file not found", "path": input_path}
    rows = []
    with open(input_path, "r", encoding="utf-8") as f:
        for raw in f:
            num = raw.strip()
            if not num:
                continue
            norm = normalize_number(num)
            links = build_links(norm) if "e164" in norm and norm.get("e164") else {}
            row = {
                "input": norm.get("input", ""),
                "e164": norm.get("e164", ""),
                "international": norm.get("international", ""),
                "national": norm.get("national", ""),
                "country_code": norm.get("country_code", ""),
                "valid": norm.get("valid", False),
                "error": norm.get("error", "")
            }
            # flatten links
            for k, v in links.items():
                row[f"link_{k}"] = v
            rows.append(row)
    # write CSV
    if rows:
        fieldnames = list(rows[0].keys())
        with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)
            writer.writeheader()
            for r in rows:
                writer.writerow(r)
    return {"rows": len(rows), "csv": OUT_CSV, "timestamp": int(time.time())}


# Store last summary in memory (simple)
_last_summary = {}

@app.route("/run", methods=["POST"])
def run():
    if not _check_token(request):
        return jsonify({"error": "unauthorized"}), 401
    result = process_input_file()
    if result.get("error"):
        return jsonify(result), 400
    # store minimal summary
    _last_summary.update(result)
    _last_summary["human_time"] = time.ctime(result["timestamp"])
    return jsonify({"status": "ok", "detail": result}), 200


@app.route("/report", methods=["GET"])
def report():
    if not _check_token(request):
        return jsonify({"error": "unauthorized"}), 401
    if not _last_summary:
        return jsonify({"error": "no report generated yet"}), 404
    return jsonify(_last_summary), 200


@app.route("/download", methods=["GET"])
def download():
    if not _check_token(request):
        return jsonify({"error": "unauthorized"}), 401
    if not os.path.exists(OUT_CSV):
        return jsonify({"error": "report not found, run /run first"}), 404
    # serve file from OUTPUT_DIR
    return send_from_directory(OUTPUT_DIR, os.path.basename(OUT_CSV), as_attachment=True)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "time": time.ctime()})


if __name__ == "__main__":
    # For Termux: run with `python3 app.py` and access via localhost:5000
    # Optional: set OSINT_API_TOKEN env var for basic protection
    bind_addr = os.getenv("OSINT_BIND", "127.0.0.1")
    port = int(os.getenv("OSINT_PORT", "5000"))
    print(f"Starting OSINT API on {bind_addr}:{port} (token={'set' if API_TOKEN else 'not set'})")
    app.run(host=bind_addr, port=port)
