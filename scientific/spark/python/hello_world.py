"""Load hello_world.py, print lines and then count lines
"""
from pyspark.sql import SparkSession


def main() -> None:
    spark = SparkSession.builder \
        .master("local") \
        .appName("hello_world") \
        .getOrCreate()

    df = spark.read.text("hello_world.py")
    df.show()

    print(f"# of lines {df.count()}")


if __name__ == "__main__":
    main()
