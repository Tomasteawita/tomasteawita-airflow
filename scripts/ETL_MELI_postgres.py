from pyspark.sql import Row
import requests
import json
import datetime
from PySparkETL.PySparkETL import PySparkETL



    def get_most_relevant_items_for_category(self, category):
        url = f"https://api.mercadolibre.com/sites/MLA/search?category={category}#json"
        response = requests.get(url).text
        json_response = json.loads(response)
        data = json_response["results"]
        return data

def clean_string(string) -> str:
    return str(string).replace(' ', '').strip()

if __name__ == '__main__':
    spark = PySparkSession().spark
    
    postgres_dict = {
        "postgres_host": "postgres",
        "postgres_port": "5432",
        "postgres_db": "tecnica_db",
        "postgres_user": "tecnica",
        "postgres_password": "tecnica_password",
        "postgres_driver": "org.postgresql.Driver",
    }
    
    postgres_config = PostgresConfig(postgres_dict)
    CATEGORY = "MLA1577"
    TABLE = "tecnica_ml"
    DATE = str(datetime.date.today())
    
    etl = ETL_MELI_postgres(spark, postgres_config)
    
    print("Obtener los 10 items más relevantes para la categoría 'MLA5725'")
    data = etl.get_most_relevant_items_for_category(CATEGORY)
    
    print("Limpiar los datos")
    rows = [Row(
        id=clean_string(item['id']),
        title=clean_string(item['title']),
        price=float(item['price']),
        thumbnail=clean_string(item['thumbnail']),
        create_date=DATE) for item in data]
    
    df = spark.createDataFrame(rows)
    
    df.show()
    etl.load_to_postgres(df, TABLE, postgres_config)