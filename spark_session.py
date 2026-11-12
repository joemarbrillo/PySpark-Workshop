from pyspark.sql import SparkSession

def get_spark(app='course'):
    spark = (SparkSession.builder
        .master("local[*]")
        .appName(app)
        .config("spark.ui.showConsoleProgress", "false")
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate())
    
    spark.sparkContext.setLogLevel("ERROR")
    
    return spark