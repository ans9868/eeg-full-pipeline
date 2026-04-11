from pyspark.sql import SparkSession


def get_spark_session() -> SparkSession:
    print("[standard] Building SparkSession")

    return (
        SparkSession.builder.appName("simplified-pyspark-standard")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.pyspark.python", "python3")
        .config("spark.pyspark.driver.python", "python3")
        .getOrCreate()
    )
