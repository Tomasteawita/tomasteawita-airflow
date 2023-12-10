from .PySparkSession import PySparkSession


class PySparkETL:
    def __init__(self, app_name, db_config_dict: dict):
        self.spark = PySparkSession(app_name).spark
        self.db_config_dict = db_config_dict
    
    def load(self, df, table: str):
        
        print("Cargar el PySpark DataFrame en Base de datos") 
        try:
            df.write \
                .format("jdbc") \
                .option("url", self.db_config_dict['url']) \
                .option("dbtable", table) \
                .option("user", self.db_config_dict['user']) \
                .option("password", self.db_config_dict['password']) \
                .option("driver", self.db_config_dict['driver']) \
                .mode("overwrite") \
                .save()

            print("Dataframe subido")
        except Exception as e:
            print("Se produjo excepción:", e)