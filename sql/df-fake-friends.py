from random import random

from pyspark.sql import SparkSession, Row, functions as func

if __name__ == "__main__":
  """
      Usage: df-fake-friends
  """
  session = (SparkSession)(SparkSession.builder.appName("df-fake-friends").getOrCreate())
  
  people = session.read.option("header", "true").option("inferSchema", "true").csv("dataset/fakefriends.csv").cache() # cache as Dataframe in memory
  people.createOrReplaceTempView("people") # creates a view to query as a database table

  people.printSchema()
  people.select("name").show()
  people.filter(people.age < 21).show()

  teenagers = session.sql("SELECT * FROM people WHERE age >= 13 AND age <= 19")
  for r in teenagers.collect():
    print(r)

  friendsByAge = people.select("age", "friends")
  friendsByAge.groupBy("age").avg("friends").sort("age").show()
  friendsByAge.groupBy("age").agg(func.round(func.avg("friends"), 2)).show()

  session.stop()