from __future__ import print_function

import json
import re
import string
import subprocess

from pyspark.sql import SparkSession
from pyspark.sql.functions import approx_count_distinct
from stopwords import ENGLISH_STOP_WORDS


def get_sentiment_dict(hdfs_path):
    cat = subprocess.Popen(["hadoop", "dfs", "-cat", hdfs_path],
                           stdout=subprocess.PIPE)
    sentiment_dict = json.loads(cat.stdout.read())
    return sentiment_dict


def get_word_sentiment(word, sentiment_dict):
    if word not in ENGLISH_STOP_WORDS:
        try:
            score = sentiment_dict[word]['value']
            return score
        except KeyError:
            # try to stem the word
            for i in range(1, len(word)):
                score = sentiment_dict.get(word[:-i])
                if score is not None:
                    return score['value']
    return 0


def get_sentiment_score(comment, sentiment_dict):
    # remove punctuation and get words
    words = re.sub('['+string.punctuation+']', '', comment).split()

    score = sum([get_word_sentiment(word, sentiment_dict) for word in words])

    return score


if __name__ == '__main__':
    spark = SparkSession \
        .builder \
        .appName("BuildSentimentWP") \
        .getOrCreate()

    sentiment_dict = get_sentiment_dict("/uhadoop2019/dpi/sentiment-dict.json")
    print(sentiment_dict.keys())

    comments = spark.read.option('header', 'true').option("delimiter", ",").option('quote', '"').option('escape', '"')
    df = spark.read.option('header', 'true') \
        .option("delimiter", ",") \
        .option('quote', '"') \
        .option('multiLine', 'true') \
        .option('parserLib', 'univocity') \
        .csv("hdfs://cm:9000/uhadoop2019/dpi/CommentsApril2017.csv.gz")

    # df.rdd.map(lambda x: )
    print(df.take(1))


    def callback(row):
        if None in row:
            return []
        return (row[0],  # commentBody
                row[1],  # commentID
                row[2],  # createDate
                row[3],  # articleID
                str(get_sentiment_score(row[0], sentiment_dict)))

    df = df.select('commentBody', 'commentId', 'createDate', 'articleID')
    df = df.na.drop()
    df = df.rdd.map(callback)\
        .toDF(['commentBody', 'commentId', 'createDate', 'articleID', 'sentimentScore'])
    df.write.csv("hdfs://cm:9000/uhadoop2019/dpi/test2")
    print(df.take(1))
