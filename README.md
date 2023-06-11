# About
This repository contains instructions and files to use **pyspark** to submit and execute Spark Applications on kubernetes (minikube). The Submit can be done using the spark-submit cli utility, or using K8S Spark Operator with SparkApplication (CRD).

# About pyspark
'This Python packaged version of Spark is suitable for interacting with an existing cluster (be it Spark standalone, YARN, or Mesos) - but does not contain the tools required to set up your own standalone Spark cluster. By default, it is going to launch the driver program locally.'

'Pyspark is a connection between Apache Spark and Python. It is a Spark Python API and helps you connect with Resilient Distributed Datasets (RDDs) to Apache Spark and Python. Through PySpark, you can write applications by using Python APIs. This interface also allows you to use PySpark Shell to analyze data in a distributed environment interactively.'

# Install
```
pipenv install
pipenv shell
```

# Submit Spark App using spark-submit
```
# For local run:
spark-submit ./main.py 10

# For standalone cluster:
spark-submit --master spark://fukuda:7077 ./main.py 10

# Access Application UI:
http://fukuda.hitronhub.home:4040
```



# Submit Spark App using spark-submit on Minikube
## Initial Setup
```
minikube start
kubectl create namespace apache-spark
kubectl apply -f ./kubernetes/spark-pi-minikube.yaml
```

## Build Spark Application Driver Image
Required to copy the Spark Application into the Docker image.
```
docker build --tag spark-pi:latest -f kubernetes/Dockerfile .
minikube image load spark-pi:latest
```

## Submit Spark App
```
kubectl cluster-info

./spark-submit --master k8s://https://192.168.49.2:8443 --deploy-mode cluster --name spark-pi --conf spark.executor.instances=3 --conf spark.kubernetes.container.image=spark-pi:latest --conf spark.kubernetes.namespace=apache-spark --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark-pi --conf spark.kubernetes.executor.request.cores=100m --conf spark.kubernetes.executor.limit.cores=100m local:///app/main.py 100
```

### Notes
- The "local://" scheme references dependencies in custom-built Docker images in spark-submit.
- We support dependencies from the submission client’s local file system using the "file://" scheme or without a scheme (using a full path), where the destination should be a Hadoop compatible filesystem (exmple s3).


# Submit Spark App using K8S Spark Operator on Minikube
More info: https://github.com/GoogleCloudPlatform/spark-on-k8s-operator

## Initial Setup
```
minikube start
kubectl create namespace apache-spark
kubectl apply -f ./kubernetes/spark-pi-k8s-operator.yaml
```

## Build Spark Application Driver Image
Required to copy the Spark Application into the Docker image.
```
docker build --tag spark-pi:latest -f kubernetes/Dockerfile .
minikube image load spark-pi:latest
```

## Submit Spark App
```
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator

helm install spark-operator spark-operator/spark-operator --namespace spark-operator --create-namespace --set sparkJobNamespace=apache-spark

kubectl apply -f kubernetes/spark-pi-k8s-operator.yaml
```

# Run pyspark interactive shell
```
# For local run:
pyspark

# For standalone cluster:
pyspark --master spark://fukuda:7077

# Access Application UI:
http://fukuda.hitronhub.home:4040
```