import csv, json, random, sys
from datetime import datetime, date, timedelta

from pathlib import Path

random.seed(42)
RAW = Path("data/raw")
CITIES = ["Lahore", "Austin", "Berlin", "Nairobi", "Lima", "Osaka"]
CATS = {"Electronics": (40, 900), "Books": (8, 60), "Home": (15, 300), "Sports": (20, 400)}

def products():
    rows = []
    for i in range(1, 41):
        cat = random.choice(list(CATS))
        lo, hi = CATS[cat]
        rows.append({"product_id": f"P{i:03d}", "name": f"{cat} item {i}", "category": cat, "price": round(random.uniform(lo, hi), 2)})
    return rows


def customers(n=2000):
    rows = []
    for i in range(1, n + 1):
        signup = date(2025, 1, 1) + timedelta(days=random.randrange(600))
        rows.append([i, f"Customer {i}", random.choice(CITIES), signup.isoformat()])
    rows += random.sample(rows, 20)
    return rows


def orders(day, n, start_id, history):
    rows = []
    midnight = datetime.combine(day, datetime.min.time())
    for k in range(n):
        ts = midnight + timedelta(seconds=random.randrange(86400))
        cust = random.randint(1, 2000) if random.random() > 0.02 else ""
        qty = random.choice([1, 1, 1, 2, 2, 3, 4]) if random.random() > 0.01 else -1
        status = random.choices(["paid", "shipped"], [75, 25])[0]
        rows.append([start_id + k, ts, cust, f"P{random.randint(1, 41):03d}", qty, status, ts])
    for old in random.sample(history, min(100, len(history))):
        rows.append(old[:5] + ["refunded", midnight + timedelta(hours=random.randint(1, 23))])
    rows += random.sample(rows, 50)
    return rows


if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    (RAW / "orders").mkdir(parents=True, exist_ok=True)
    with open(RAW / "products.jsonl", "w") as f:
        for p in products():
            f.write(json.dumps(p) + "\n")
    with open(RAW / "customers.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["customer_id", "name", "city", "signup_date"])
        w.writerows(customers())
    history, next_id = [], 1
    for i in range(days):
        day = date(2026, 10, 1) + timedelta(days=i)
        rows = orders(day, 20000, next_id, history)
        history += [r for r in rows if r[5] != "refunded"]
        next_id += 20000
        with open(RAW / "orders" / f"orders_{day}.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["order_id", "order_ts", "customer_id", "product_id", "quantity", "status", "updated_at"])
            w.writerows(rows)
    print(f"wrote {days} days, {next_id - 1} new orders")