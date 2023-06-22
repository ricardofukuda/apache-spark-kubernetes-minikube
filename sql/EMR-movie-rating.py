from random import random
from pyspark import SparkConf, SparkContext
from pyspark.sql import functions as func


# spark-submit --executor-memory 1g EMR-movie-rating.py
if __name__ == "__main__":
  """
    movie rating using DF on EMR
  """
  conf = SparkConf()
  sc = SparkContext(conf = conf)

  data = sc.textFile("s3n://fukuda-movie-lens/ratings.dat", 10)

  ratings = data.map(lambda l: l.split("::")).map(lambda l: (int(l[0]), (int(l[1]), float(l[2]))))
  results = ratings.map(lambda l: (l[0], l[0]))

  print(f"count: {ratings.count()}")

  sc.stop()
