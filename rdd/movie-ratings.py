from pyspark import SparkConf, SparkContext

if __name__ == "__main__":
  """
    Usage: movie-ratings
    Example using basic RDD operations
  """
  conf = SparkConf().setAppName("movie-ratings")
  sc = SparkContext(conf=conf)
  lines = sc.textFile("./dataset/movie-ratings.data") #RDD

  ratings = lines.map(lambda x: x.split()[2])
  result = ratings.countByValue().items()
  print(result)

