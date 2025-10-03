import argparse, os, sqlite3, random
from datetime import datetime, timedelta
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")
REPORT_SQL_PATH = os.path.join(os.path.dirname(__file__), "report.sql")

def seed():
    # fresh DB
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # --- Schema mirrors your query shape
    cur.executescript("""
    DROP TABLE IF EXISTS "order";
    DROP TABLE IF EXISTS orderdetail;
    DROP TABLE IF EXISTS orderdetailunit;

    CREATE TABLE "order"(
        id INTEGER PRIMARY KEY,
        createdonutc TEXT,           -- ISO8601
        iscancelled INTEGER,         -- 0/1
        type TEXT,                   -- e.g., 'standard','reprint'
        CustomPartnerId TEXT
    );

    CREATE TABLE orderdetail(
        id INTEGER PRIMARY KEY,
        orderid INTEGER,
        IsCancelled INTEGER,         -- 0/1
        ismugprint INTEGER,          -- 0/1
        isstickerprint INTEGER,      -- 0/1
        FOREIGN KEY(orderid) REFERENCES "order"(id)
    );

    CREATE TABLE orderdetailunit(
        id INTEGER PRIMARY KEY,
        orderdetailid INTEGER,
        iscancelled INTEGER,         -- 0/1
        FOREIGN KEY(orderdetailid) REFERENCES orderdetail(id)
    );
    """)

    random.seed(21)
    start = datetime(2024, 3, 15)   # a bit before April
    partners = ["teepublicvip", "printify", "acme"]
    types = ["standard", "standard", "reprint"]  # skew toward standard

    oid = 1
    odid = 1
    u_id = 1

    # ~75 days of data; 10–40 orders per day
    for day in range(0, 75):
        d = start + timedelta(days=day)
        for _ in range(random.randint(10, 40)):
            partner = random.choice(partners)
            otype   = random.choice(types)
            ocancel = 1 if random.random() < 0.05 else 0

            cur.execute("""
                INSERT INTO "order"(id, createdonutc, iscancelled, type, CustomPartnerId)
                VALUES (?, ?, ?, ?, ?)
            """, (oid, d.isoformat(), ocancel, otype, partner))

            # 1–4 orderdetails per order
            for _od in range(random.randint(1, 4)):
                d_cancel = 1 if random.random() < 0.03 else 0
                is_mug   = 1 if random.random() < 0.10 else 0
                is_stkr  = 1 if random.random() < 0.06 else 0

                cur.execute("""
                    INSERT INTO orderdetail(id, orderid, IsCancelled, ismugprint, isstickerprint)
                    VALUES (?, ?, ?, ?, ?)
                """, (odid, oid, d_cancel, is_mug, is_stkr))

                # 1–5 units per detail
                for _u in range(random.randint(1, 5)):
                    u_cancel = 1 if random.random() < 0.04 else 0
                    cur.execute("""
                        INSERT INTO orderdetailunit(id, orderdetailid, iscancelled)
                        VALUES (?, ?, ?)
                    """, (u_id, odid, u_cancel))
                    u_id += 1

                odid += 1

            oid += 1

    conn.commit()
    conn.close()
    print("Seeded fake audit data into app.db")

def run_report(start, end, partner, out_csv=None):
    # ensure db
    if not os.path.exists(DB_PATH):
        seed()

    conn = sqlite3.connect(DB_PATH)
    with open(REPORT_SQL_PATH, "r") as f:
        sql = f.read()
    params = {"start": start, "end": end, "partner": partner}
    df = pd.read_sql_query(sql, conn, params=params)
    conn.close()

    print("\n=== Parameters ===")
    print(params)
    print("\n=== Audit Result ===")
    if df.empty:
        # For a COUNT query, empty result means no rows matched — produce zeros
        out = {"numOrdersRecv": 0, "numUnitsRecv": 0, "TotalRebate": 0.0}
        print(out)
        result = pd.DataFrame([out])
    else:
        print(df.to_string(index=False))
        result = df

    if out_csv:
        result.to_csv(out_csv, index=False)
        print(f"\nSaved CSV to {out_csv}")

def main():
    ap = argparse.ArgumentParser(description="Order Units & Rebate Audit")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("seed", help="Create/refresh SQLite DB with fake audit data.")

    r = sub.add_parser("report", help="Run the audit for a date window and partner.")
    r.add_argument("--start", default="2024-04-01")
    r.add_argument("--end",   default="2024-05-01")
    r.add_argument("--partner", default="teepublicvip")
    r.add_argument("--out", dest="out_csv", default="audit_rebate.csv")

    args = ap.parse_args()
    if args.cmd == "seed":
        seed()
    elif args.cmd == "report":
        run_report(args.start, args.end, args.partner, args.out_csv)

if __name__ == "__main__":
    main()
