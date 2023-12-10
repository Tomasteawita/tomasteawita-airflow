class PostgresConfig:
    def __init__(self, postgres_host, postgres_port, postgres_db, postgres_user, postgres_password, postgres_driver, postgres_url = 'jbdc'): 
        self.POSTGRES_HOST = postgres_host
        self.POSTGRES_PORT = postgres_port
        self.POSTGRES_DB = postgres_db
        self.POSTGRES_USER = postgres_user
        self.POSTGRES_PASSWORD = postgres_password
        self.POSTGRES_DRIVER = postgres_driver
        if postgres_url == 'jbdc':
            self.POSTGRES_URL = f"jdbc:postgresql://{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        else:
            self.POSTGRES_URL = postgres_url