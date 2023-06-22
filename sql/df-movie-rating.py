from random import random
from pyspark.sql import SparkSession, functions as func
from pyspark.sql.types import StructType, StructField, StringType, LongType, IntegerType

if __name__ == "__main__":
  """
    movie rating using DF
  """
  session = (SparkSession)(SparkSession.builder.appName("movie-rating").getOrCreate())

  schema = StructType([
    StructField("userID", IntegerType(), True),
    StructField("movieID", IntegerType(), True),
    StructField("rating", IntegerType(), True),
    StructField("timestamp", LongType(), True)
  ])

  df = session.read.option("sep", "\t").schema(schema).csv("dataset/movie-ratings.data")

  schema = StructType([
    StructField("movieID", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("category", StringType(), True)
  ])

  dfNames = session.read.option("sep", "::").schema(schema).csv("dataset/movies.dat")

  topMovies = df.groupBy("movieID").avg("rating")

  topMovies = topMovies.join(dfNames, on = "movieID").sort("movieID")
  topMovies.show()
