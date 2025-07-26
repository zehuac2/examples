import sys
from pyspark.sql import SparkSession


def main() -> None:
    spark = SparkSession.builder.getOrCreate()
    text = spark.sparkContext.textFile(sys.argv[1])
    words = text.flatMap(lambda line: line.split(" "))

    word_counts = words.map(lambda word: (word, 1))
    counts = word_counts.reduceByKey(lambda a, b: a + b)

    counts.saveAsTextFile(sys.argv[2])


if __name__ == "__main__":
    main()
