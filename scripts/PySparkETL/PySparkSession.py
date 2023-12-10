from os import environ as env
from pyspark.sql import SparkSession

class PySparkSession:
    def __init__(self, app_name: str):
        self.DRIVER_PATH = env['DRIVER_PATH']
        
        env['PYSPARK_SUBMIT_ARGS'] = f'--driver-class-path {self.DRIVER_PATH} --jars {self.DRIVER_PATH} pyspark-shell'
        env['SPARK_CLASSPATH'] = self.DRIVER_PATH
        
        self.spark = SparkSession.builder \
            .master("local[1]") \
            .appName(app_name) \
            .config("spark.jars", self.DRIVER_PATH) \
            .config("spark.executor.extraClassPath", self.DRIVER_PATH) \
            .getOrCreate()