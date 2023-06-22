from random import random
from pyspark.sql import SparkSession, Row, functions as func
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    FloatType,
    IntegerType,
)

if __name__ == "__main__":
    """
    Usage: temperature
    Calculate the min temperature by stationID using DataFrames
    """
    session = (SparkSession)(SparkSession.builder.appName("temperature").getOrCreate())

    schema = StructType(
        [
            StructField("stationID", StringType(), True),
            StructField("date", IntegerType(), True),
            StructField("measure_type", StringType(), True),
            StructField("temperature", FloatType(), True),
        ]
    )

    df = session.read.schema(schema).csv("dataset/1800.csv")

    minTemps = df.filter(df.measure_type == "TMIN")

    stationTemps = minTemps.select("stationID", "temperature")

    minTempByStation = stationTemps.groupBy("stationID").min("temperature")
    minTempByStation.show()

    for r in minTempByStation.collect():
        print(r)
