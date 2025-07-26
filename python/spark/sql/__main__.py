"""
"""
from os import path
from pyspark.sql import SparkSession, Row


def to_upper(row: Row):
    print(row)

    return row


def main() -> None:
    spark = SparkSession.builder \
        .master("local") \
        .appName("sql") \
        .getOrCreate()

    folder = path.dirname(__file__)
    purchases_filename = path.join(folder, "purchases.csv")
    purchases_df = spark.read.csv(purchases_filename, inferSchema=True, header=True)
    purchases_df.show()

    names_items = purchases_df.select(["first_name", "item", "value"])
    names_items.show()

    total_cost_by_name = names_items.groupBy("first_name").sum("value")
    total_cost_by_name.show()


if __name__ == "__main__":
    main()
