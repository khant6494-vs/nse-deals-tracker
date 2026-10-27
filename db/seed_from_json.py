"""
Seed the MySQL `deals` table from public/deals.json (the bundled dataset).

Usage: python db/seed_from_json.py [path/to/deals.json]

Safe to re-run: uses INSERT IGNORE, so existing deals are skipped.
"""
import json
import os
import sys

import mysql.connector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_JSON = os.path.join(ROOT, "public", "deals.json")


def load_env():
    env = dict(os.environ)
    env_path = os.path.join(ROOT, ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env.setdefault(k.strip(), v.strip())
    return env


_env = load_env()
DB_CONFIG = {
    "host":     _env.get("DB_HOST",     "127.0.0.1"),
    "port":     int(_env.get("DB_PORT", "3306")),
    "user":     _env.get("DB_USER",     "nse_user"),
    "password": _env.get("DB_PASSWORD", "nse_pass"),
    "database": _env.get("DB_NAME",     "nse_deals"),
}


def to_row(d):
    """DD-MM-YYYY JSON deal -> DB tuple, or None if the date is malformed."""
    parts = str(d.get("date", "")).split("-")
    if len(parts) != 3:
        return None
    dd, mm, yyyy = parts
    return (
        d.get("id") or "",
        f"{yyyy}-{mm}-{dd}",
        d.get("symbol", ""),
        d.get("client", ""),
        str(d.get("buy_sell", "")).upper(),
        int(d.get("quantity") or 0),
        float(d.get("price") or 0),
        float(d.get("value_cr") or 0),
        d.get("type", ""),
    )


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_JSON
    with open(path, encoding="utf-8") as f:
        deals = json.load(f)

    rows = [r for r in map(to_row, deals) if r]
    skipped = len(deals) - len(rows)

    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    sql = """
        INSERT IGNORE INTO deals
            (deal_id, deal_date, symbol, client, buy_sell, quantity, price, value_cr, deal_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    inserted = 0
    for i in range(0, len(rows), 2000):
        cur.executemany(sql, rows[i:i + 2000])
        inserted += cur.rowcount
        conn.commit()
    cur.close()
    conn.close()

    print(f"Read {len(deals)} deals; inserted {inserted}, "
          f"{len(rows) - inserted} already present, {skipped} skipped (bad date).")


if __name__ == "__main__":
    main()
