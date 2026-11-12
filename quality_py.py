import sys
from pyspark.sql import functions as F

def check(name, ok, detail):
    print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    return ok

def run_checks(orders, products):
    s = orders.agg(
        F.count("*").alias("rows"),
        F.count_distinct("order_id").alias("ids"),
        F.expr("count_if(order_id IS NULL OR order_ts IS NULL OR product_id IS NULL)").alias("nulls"),
        F.expr("count_if(quantity IS NULL OR quantity <=0)").alias("bad_qty"),
        F.expr("count_if(status NOT IN ('paid', 'shipped', 'refunded'))").alias("bad_status"),
        F.max("order_ts").alias("latest")).first()
    orphans = orders.join(products, "product_id", "left_anti").count()
    results = [
        check("not empty", s.rows > 0, f"{s.rows} rows"),
        check("unique order_id", s.rows == s.ids, f"{s.rows - s.ids} duplicates"),
        check("required not null", s.nulls == 0, f"{s.nulls} rows"),
        check("quantity positive", s.bad_qty == 0, f"{s.bad_qty} rows"),
        check("known status", s.bad_status == 0, f"{s.bad_status} rows"),
        check("product exists", orphans == 0, f"{orphans} rows"),
    ]
    print("latest orders: ", s.latest)
    return all(results)


if __name__ == "__main__":
    from spark_session import get_spark
    import sources
    spark = get_spark("quality")
    path = sys.argv[1]
    df = sources.orders(spark, path) if path.startswith("data/raw") else spark.read.parquet(path)
    ok = run_checks(df, sources.products(spark))
    
    print("QUALITY GATE:", "PASSED" if ok else "FAILED")
    sys.exit(0 if ok else 1)
    
# python quality_py.py data/lake/orders; echo "exit code: $?"