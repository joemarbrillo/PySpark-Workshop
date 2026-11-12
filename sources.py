import import_ipynb # Added to read the ipynb as regular module
from schemas import ORDERS, CUSTOMERS, PRODUCTS

import os
import glob

os.environ["HADOOP_HOME"] = "D:\\hadoop"
os.environ["PATH"] += os.pathsep + "D:\\hadoop\\bin"


def orders(spark, path="data/raw/orders"):
    return spark.read.csv(path, header=True, schema=ORDERS)

def orders_glob(spark, path="data/raw/orders"):
    if os.path.isdir(path):
        path = glob.glob(os.path.join(path, "*.csv"))
    return spark.read.csv(path, header=True, schema=ORDERS)

def customers(spark):
    return spark.read.csv("data/raw/customers.csv", header=True, schema=CUSTOMERS)

def products(spark):
    return spark.read.schema(PRODUCTS).json("data/raw/products.jsonl")
