from typing import List
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType
from pyspark.sql import SparkSession, Row


def main() -> None:
    spark = SparkSession.builder.appName("rdd").getOrCreate()
    data = []  # type: List[Row]

    with open("input.txt") as input_file:
        for line in input_file.readlines():
            fields = line.split(" ")
            row = Row(
                student_id=int(fields[0]),
                first_name=fields[1],
                last_name=fields[2],
                department_name=fields[3],
                origin_country=fields[4],
                gpa=float(fields[5]),
            )

            data.append(row)


    schema = StructType([
        StructField("student_id", IntegerType(), False),
        StructField("first_name", StringType(), False),
        StructField("last_name", StringType(), False),
        StructField("department_name", StringType(), False),
        StructField("origin_country", StringType(), False),
        StructField("gpa", FloatType(), False)
    ])

    df = spark.createDataFrame(data=data, schema=schema)
    df.show()



if __name__ == "__main__":
    main()
