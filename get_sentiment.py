from __future__ import print_function

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg


def nltk_sentiment(sentence):
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    nltk_sentiment = SentimentIntensityAnalyzer()
    score = nltk_sentiment.polarity_scores(sentence)
    return score['compound']


"""  This es deprecated for being too naive :3
def get_sentiment_dict(hdfs_path):
    cat = subprocess.Popen(["hadoop", "dfs", "-cat", hdfs_path],
                           stdout=subprocess.PIPE)
    sentiment_dict = json.loads(cat.stdout.read())
    return sentiment_dict


def get_word_sentiment(word, sentiment_dict):
    word = word.lower()
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
    
"""


if __name__ == '__main__':
    spark = SparkSession \
        .builder \
        .appName("BuildSentimentWP") \
        .getOrCreate()

    spark.sparkContext.addPyFile('vendor.zip')

    df = spark.read.option('header', 'true') \
        .option("delimiter", ",") \
        .option('quote', '"') \
        .option('multiLine', 'true') \
        .option('parserLib', 'univocity') \
        .csv("hdfs://cm:9000/uhadoop2019/dpi/CommentsApril2017.csv.gz")

    print(df.take(1))


    def callback(row):
        if None in row:
            return []
        return (row[0],  # commentBody
                row[1],  # commentID
                row[2],  # createDate
                row[3],  # articleID
                str(nltk_sentiment(row[0])))

    df = df.select('commentBody', 'commentId', 'createDate', 'articleID')
    df = df.na.drop()
    df = df.rdd.map(callback)\
        .toDF(['commentBody', 'commentId', 'createDate', 'articleID', 'sentimentScore'])
    df.show()
    df.write.csv("hdfs://cm:9000/uhadoop2019/dpi/test2")

    df.cache()

    # get avg score per article
    article_df = spark.read.option('header', 'true') \
        .option("delimiter", ",") \
        .option('quote', '"') \
        .option('multiLine', 'true') \
        .option('parserLib', 'univocity') \
        .csv("hdfs://cm:9000/uhadoop2019/dpi/ArticlesApril2017.csv.gz")

    joined_df = article_df.join(df, 'articleID')
    joined_df = joined_df.groupBy('articleID').agg(avg('SentimentScore').alias('avg_score'))

    joined_df.write.csv("hdfs://cm:9000/uhadoop2019/dpi/avg_score_article")
    print(joined_df.show())
