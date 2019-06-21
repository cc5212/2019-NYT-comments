import json
import re
import string
import ast
import subprocess
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import approx_count_distinct, sum, avg, desc


def mapper(line):
    split_keywords = ast.literal_eval(line[1])
    return [(keyword, line[2]) for keyword in split_keywords]


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('error de arguments')
        sys.exit(2)
    else:
        input_data = sys.argv[1]
        output_path = sys.argv[2]

    spark = SparkSession\
        .builder\
        .appName("keywordsPop")\
        .getOrCreate()

    df = spark.read.csv(str(input_data))
    keyword_map = df.rdd.flatMap(mapper)\
        .toDF(("keyword", "comments"))

    keyword_reduced = keyword_map.groupBy("keyword").agg(sum("comments").alias("sum"))
    keyword_reduced = keyword_reduced.orderBy(desc("sum"))
    keyword_map.show()
    keyword_reduced.repartition(1).write.csv(str(output_path))
