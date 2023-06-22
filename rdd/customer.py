from pyspark import SparkConf, SparkContext

def parseLine(line):
  fields = line.split(',')
  customer = fields[0]
  price = float(fields[2])
  return (customer, price)

if __name__ == "__main__":
  """
    Usage: customer.py
    Example using reduceByKey on key/value data
  """
  conf = SparkConf().setAppName("weather")
  sc = SparkContext(conf=conf)

  lines = sc.textFile("./dataset/customer-orders.csv")
  rdd = lines.map(parseLine)

  sumByCustomer = rdd.reduceByKey(lambda x, y: (x + y))
  flip = sumByCustomer.map(lambda p: (p[1], p[0]))
  results = flip.sortByKey().collect()
  for r in results:
    print(r)
  

  
  