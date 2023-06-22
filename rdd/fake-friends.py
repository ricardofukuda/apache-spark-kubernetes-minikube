from pyspark import SparkConf, SparkContext

def parseLine(line):
  fields = line.split(',')
  age = int(fields[2])
  numFriends = int(fields[3])
  return (age, numFriends)

if __name__ == "__main__":
  """
    Usage: fake-friends
    Example using Key/Value operations RDD
  """
  conf = SparkConf().setAppName("fake-friends")
  sc = SparkContext(conf=conf)

  lines = sc.textFile("./dataset/fakefriends.csv")
  rdd = lines.map(parseLine)

  totalsByAge = rdd.mapValues(lambda x: (x, 1)).reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
  averagesByAge = totalsByAge.mapValues(lambda x: x[0] / x[1])
  avgByAge = averagesByAge.collect()
  avgByAge.sort()
  for r in avgByAge:
    print(r)
