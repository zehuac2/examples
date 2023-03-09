from os import path
from pyspark.sql import SparkSession, Row


def upper_case_name(row: Row) -> Row:
    # row columns can be obtained by accessing properties
    first_name = row.first_name.upper()
    last_name = row.last_name.upper()

    return Row(name=f"{first_name} {last_name}")


def main() -> None:
    folder = path.dirname(__file__)
    purchases_filename = path.join(folder, "purchases.csv")

    spark = SparkSession.builder.appName("rdd").getOrCreate()
    purchases_df = spark.read.csv(purchases_filename, header=True)
    purchases_rdd = purchases_df.rdd

    upper_names = purchases_rdd.map(upper_case_name)

    # convert rdd back to data frame
    upper_names.toDF().show()


if __name__ == "__main__":
    main()
