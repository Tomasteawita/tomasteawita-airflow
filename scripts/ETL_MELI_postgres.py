from .ETLs.MicrowavesETL import MicrowavesETL
if __name__ == '__main__':
    
    postgres_config = {
            'host' : "postgres",
            'port' : "5432",
            'db' : "tecnica_db",
            'user' : "tecnica",
            'password' : "tecnica_password",
            'driver' : "org.postgresql.Driver",
            'url' : "jdbc:postgresql://postgres:5432/tecnica_db"
        }
    category = 'MLA1577'
    table = 'tecnica_ml'
    
    etl = MicrowavesETL()
    
    data = etl.extract(category)
        
    df = etl.transform(data)
    
    df.show()
    
    etl.load(df, table, postgres_config)