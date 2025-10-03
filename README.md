# 🧮 Order Units & Rebate Audit Report (SQLite + Python)

> This project showcases how **SQL + Python automation** can power real-world **audit and rebate validation** workflows.  
> This demo uses **fake but realistic data** to simulate a **finance & operations audit report**:
>
> _Order Units & Rebate Audit — verifies all valid units received and rebate amounts for a specific partner within a date range._

---

### 🔍 Why this matters
Finance, Operations, and Auditing teams often need to confirm **rebate eligibility** for partner orders.  
This report helps:
- Audit total orders and shipped units during a given time window  
- Exclude cancelled or ineligible orders (mugs, stickers, reprints)  
- Calculate total rebates based on a fixed rate per unit  

---

### ⚙️ How it works
This small pipeline combines:
- 🗃️ **SQLite** (lightweight fake database)
- 💡 **SQL** report (`report.sql`)
- 🐍 **Python CLI** (`app.py`) to:
  - seed fake data  
  - execute the audit query  
  - export the results to a CSV file  
- ⚡ **GitHub Actions workflow** for one-click audit generation directly in GitHub  

---

## 🚀 How to run (in GitHub)

### Option 1 — Codespaces (interactive)
1. Click **Code → Create codespace on main**  
2. In the terminal, run:
   ```bash
   pip install -r requirements.txt
   python app.py seed
   python app.py report --start 2024-04-01 --end 2024-05-01 --partner teepublicvip --out audit_rebate.csv```

---

### Option 2 — Workflows (interactive)
Run the below Workflow:

[![Run Audit](https://github.com/CarlosJordan-AI/audit-rebate/actions/workflows/run-audit.yml/badge.svg)](https://github.com/CarlosJordan-AI/audit-rebate/actions/workflows/run-audit.yml)


Run the workflow:

<img width="378" height="512" alt="image" src="https://github.com/user-attachments/assets/602f50ad-337a-46df-a46e-38d2840e7a72" />

After it completes (about 15 seg), enter in the workflow and download the file for preview:

<img width="1545" height="549" alt="image" src="https://github.com/user-attachments/assets/be1c09d7-635b-4d48-b5b0-b72c1435d644" />

Output preview:

<img width="473" height="693" alt="image" src="https://github.com/user-attachments/assets/847d4996-7d2d-41ee-ba6a-a57d90d3c507" />

### 🧠 Key highlights
- Parameterized SQL query (`:partner`, `:factory`, `:start`)  
- Reproducible fake dataset seeded automatically  
- Outputs `audit_rebate.csv` with order, carrier, and invoice data  
- Optional: run interactively in **Codespaces**, or trigger via **GitHub Actions**  

