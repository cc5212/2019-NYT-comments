import json
import re
import string
import ast
import subprocess

from pyspark.sql import SparkSession
from pyspark.sql.functions import approx_count_distinct, sum, avg, desc


def mapper(line):
    split_keywords = ast.literal_eval(line[1])
    return [(keyword, line[2]) for keyword in split_keywords]


if __name__ == '__main__':
    spark = SparkSession\
        .builder\
        .appName("keywordsPop")\
        .getOrCreate()

    df = spark.read.csv("hdfs://cm:9000/uhadoop2019/dpi/tags_number/part-00000-ba6063ed-3744-43d1-903f-d25d3b2513bf.csv")
    keyword_map = df.rdd.flatMap(mapper)\
        .toDF(("keyword", "comments"))

    keyword_reduced = keyword_map.groupBy("keyword").agg(sum("comments").alias("sum"))
    keyword_reduced = keyword_reduced.orderBy(desc("sum"))
    keyword_map.show()
    keyword_reduced.repartition(1).write.csv("hdfs://cm:9000/uhadoop2019/dpi/keywords_number")
