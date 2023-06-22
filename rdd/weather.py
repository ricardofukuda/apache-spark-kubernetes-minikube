from pyspark import SparkConf, SparkContext

def parseLine(line):
  fields = line.split(',')
  station = fields[0]
  entryType = fields[2]
  temperature = float(fields[3])
  return (station, entryType, temperature)

if __name__ == "__main__":
  """
    Usage: weather
    Example using Filters on RDD
  """
  conf = SparkConf().setAppName("weather")
  sc = SparkContext(conf=conf)

  lines = sc.textFile("./dataset/1800.csv")
  rdd = lines.map(parseLine)

  minTemps = rdd.filter(lambda x: "TMIN" in x[1])
  stationMinTemps = minTemps.map(lambda x: (x[0], x[2]))
  minTempByStation = stationMinTemps.reduceByKey(lambda x, y: min(x, y))

  results = minTempByStation.collect()
  for r in results:
    print(r)
  
  maxTemps = rdd.filter(lambda x: "TMAX" in x[1])
  stationMaxTemps = maxTemps.map(lambda x: (x[0], x[2]))
  maxTempByStation = stationMaxTemps.reduceByKey(lambda x, y: max(x, y))

  results = maxTempByStation.collect()
  for r in results:
    print(r)
  

  
  