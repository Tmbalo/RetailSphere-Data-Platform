"""
RetailSphere synthetic POS sales generator.

Creates fake transaction lines shaped like an Oracle MICROS POS export,
plus an answer key used by the reconciliation tests (TST-001 Section 5).
All data is synthetic (MET-001 rule): no real customers or products.
"""
import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Same seed = same data every run, so tests are repeatable
SEED = 42
random.seed(SEED)

# Size and shape of the data
NUM_TRANSACTIONS = 200          # about 500 lines at 1-4 lines each
START_DATE = datetime(2026, 10, 1)
DAYS = 30
ANONYMOUS_SHARE = 0.66          # 66% of in-store sales are anonymous (BPA-001)

# Reference data: stores, products and loyalty customers
STORE_IDS = [101, 102, 103, 104, 105]
PRODUCTS = {
    f"60012345{n:05d}": round(random.uniform(25, 1500), 2)
    for n in range(1, 21)
}
CUSTOMER_IDS = [f"RS-CUST-{n:07d}" for n in range(1, 301)]

# Build the transaction lines
lines = []
for t in range(1, NUM_TRANSACTIONS + 1):
    # Transaction header: one per sale
    transaction_id = f"POS-2026-{t:06d}"
    store_id = random.choice(STORE_IDS)
    timestamp = START_DATE + timedelta(
        days=random.randrange(DAYS),
        hours=random.randint(8, 20),
        minutes=random.randint(0, 59),
    )
    is_anonymous = random.random() < ANONYMOUS_SHARE
    customer_id = "" if is_anonymous else random.choice(CUSTOMER_IDS)

    # Transaction lines: 1 to 4 products per sale
    for line_number in range(1, random.randint(1, 4) + 1):
        barcode = random.choice(list(PRODUCTS))
        unit_price = PRODUCTS[barcode]
        quantity = random.randint(1, 3)
        has_discount = random.random() < 0.15
        discount_amount = round(unit_price * quantity * 0.10, 2) if has_discount else 0.00

        lines.append({
            "transaction_id": transaction_id,
            "line_number": line_number,
            "transaction_timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "store_id": store_id,
            "barcode": barcode,
            "customer_id": customer_id,
            "quantity": quantity,
            "unit_price": unit_price,
            "discount_amount": discount_amount,
        })

# Output locations
repo_root = Path(__file__).resolve().parents[2]
seed_dir = repo_root / "src" / "dbt" / "retailsphere" / "seeds" / "bronze"
output_dir = repo_root / "data" / "generated"
seed_dir.mkdir(parents=True, exist_ok=True)
output_dir.mkdir(parents=True, exist_ok=True)

# 1. The sales file: lands in dbt's seeds as the Bronze stand-in
sales_file = seed_dir / "pos_sales.csv"

with open(sales_file, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=lines[0].keys())
    writer.writeheader()
    writer.writerows(lines)

# 2. The answer key: totals the pipeline must reproduce
answer_key = {
    "seed": SEED,
    "row_count": len(lines),
    "transaction_count": NUM_TRANSACTIONS,
    "total_quantity": sum(line["quantity"] for line in lines),
    "total_gross_value": round(sum(line["quantity"] * line["unit_price"] for line in lines), 2),
    "total_discount": round(sum(line["discount_amount"] for line in lines), 2),
}
key_file = output_dir / "pos_sales_answer_key.json"
with open(key_file, "w") as f:
    json.dump(answer_key, f, indent=2)

print(f"Wrote {len(lines)} lines to {sales_file}")
print(json.dumps(answer_key, indent=2))