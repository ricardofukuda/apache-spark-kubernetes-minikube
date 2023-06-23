from random import random
from pyspark.sql import SparkSession, functions as func
from pyspark.sql.types import StructType, StructField, StringType, LongType, IntegerType

if __name__ == "__main__":
  """
    movie rating partition using DF
  """
  session = (SparkSession)(SparkSession.builder.appName("movie-rating").getOrCreate())

  schema = StructType([
    StructField("userID", IntegerType(), True),
    StructField("movieID", IntegerType(), True),
    StructField("rating", IntegerType(), True),
    StructField("timestamp", LongType(), True)
  ])

  df = session.read.option("sep", "\t").schema(schema).csv("dataset/movie-ratings.data")
  df = df.repartition(10, "movieID").groupBy("movieID").avg("rating")
  
  df.show()

  print(f"count: {df.count()}")
