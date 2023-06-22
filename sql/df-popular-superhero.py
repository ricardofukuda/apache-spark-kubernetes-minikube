from random import random
from pyspark.sql import SparkSession, Row, functions as func, DataFrame
from pyspark.sql.types import StructType, StructField, IntegralType, StringType, IntegerType

if __name__ == "__main__":
  """
    popular super hero using DataFrames
  """
  session = (SparkSession)(SparkSession.builder.appName("popuar-superhero").getOrCreate())

  schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True)
  ])

  names = session.read.option("sep", " ").schema(schema).csv("dataset/Marvel-Names")
  
  lines = session.read.text("dataset/Marvel-Graph")
  connections = lines.withColumn("id", func.split(func.col("value"), " ")[0]) \
    .withColumn("connections", func.size(func.split(func.col("value"), " ")) - 1) \
    .groupBy("id").agg(func.sum("connections").alias("numConnections"))
  
  connections = connections.sort("numConnections", ascending=False)

  connections = connections.filter(func.col("numConnections") > 1000)

  connections.show()

  session.stop()
