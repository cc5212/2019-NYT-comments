from __future__ import print_function

import json
import pickle
import re
import string
import subprocess
import sys
from operator import add

from pyspark.sql import SparkSession
from pyspark.sql.functions import approx_count_distinct, sum, avg, desc

def get_sentiment_dict(hdfs_path):
    cat = subprocess.Popen(["hadoop", "dfs", "-cat", hdfs_path],
                           stdout=subprocess.PIPE)
    sentiment_dict = json.loads(cat.stdout.read())
    return sentiment_dict


def get_word_sentiment(word, sentiment_dict):
    try:
        score = sentiment_dict[word]['values']
    except KeyError:
        # try to stem the word
        for i in range(1, len(word)):
            score = sentiment_dict.get(word[:-i])
            if score is not None:
                return score['value']
    return 0


# stem word



def get_sentiment_score(comment, sentiment_dict):
    # remove punctuation and get words
    words = re.sub('['+string.punctuation+']', '', comment).split()

    for word in words:
        pass


##"hdfs://cm:9000/uhadoop2019/dpi/ArticlesMay2017.csv.gz"
##hdfs://cm:9000/uhadoop2019/dpi/CommentsMay2017.csv.gz
##hdfs://cm:9000/uhadoop2019/dpi/count/may
if __name__ == '__main__':
    if len(sys.argv)!=4:        
        print("comentarios, articulos, output")
        sys.exit
    else:
        commentcsv=sys.argv[2]
        articlecsv=sys.argv[1]
        outputcsv=sys.argv[3]

    
    spark = SparkSession\
        .builder\
        .appName("BuildSentimentWP")\
        .getOrCreate()


    comments = spark.read.option('header', 'true').option("delimiter",",").option('quote', '"').option('escape', '"').option('multiline','true').csv(commentcsv)
    comments=comments.select('commentBody', 'commentId', 'createDate', 'articleID')
    comments = comments.na.drop()
    grupitos=comments.groupby(comments.articleID).count()


    articles = spark.read.option('header', 'true').option("delimiter",",").option('quote', '"').option('escape', '"').csv(articlecsv)
    articles=articles.select('articleID','keywords')
    ta = articles.alias('ta')
    tg = grupitos.alias('tg')
    inner_join = ta.join(tg, on= 'articleID')
    inner_join=inner_join.orderBy(desc('count'))
    inner_join.repartition(1).write.csv(outputcsv)