import env
from pyspark.sql import SparkSession, Row
import requests
import json
import datetime

class MicrowavesETL:
    def __init__(self):
        self.DRIVER_PATH = env['DRIVER_PATH']
        
        env['PYSPARK_SUBMIT_ARGS'] = f'--driver-class-path {self.DRIVER_PATH} --jars {self.DRIVER_PATH} pyspark-shell'
        env['SPARK_CLASSPATH'] = self.DRIVER_PATH
        
        self.spark = SparkSession.builder \
            .master("local[1]") \
            .appName("Spark y Postgres") \
            .config("spark.jars", self.DRIVER_PATH) \
            .config("spark.executor.extraClassPath", self.DRIVER_PATH) \
            .getOrCreate()
    
    def extract(self, category):
        url = f"https://api.mercadolibre.com/sites/MLA/search?category={category}#json"
        response = requests.get(url).text
        json_response = json.loads(response)
        data = json_response["results"]
        
        return data
    
    

    def transform(self, data):
        
        def clean_string(string) -> str:
            return str(string).replace(' ', '').strip()
        
        today = datetime.date.today()
        rows = [Row(
            id = clean_string(item['id']),
            title = clean_string(item['title']),
            price = float(item['price']),
            thumbnail = clean_string(item['thumbnail']),
            create_date = today) for item in data]
        
        return self.spark.createDataFrame(rows)
    
    def load(self, df, table, config: dict):
        """
        Carga un DataFrame de pandas en Postgres.

        Parameters:
        df (pandas.DataFrame): El DataFrame de pandas a cargar.
        table (str): El nombre de la tabla en Postgres donde se cargará el DataFrame.

        """
        
        print("Cargar el PySpark DataFrame en Postgres") 
        try:
            df.write \
                .format("jdbc") \
                .option("url", config["url"]) \
                .option("dbtable", table) \
                .option("user", config["user"]) \
                .option("password", config["password"]) \
                .option("driver", self.DRIVER_PATH) \
                .mode("overwrite") \
                .save()

            print("Dataframe subido")
        except Exception as e:
            print("Se produjo excepción:", e)
        