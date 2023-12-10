# Levantate ese airflow con docker papaaa
## ¡ATENCIOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOON!

No clones este repositorio, en lugar de eso, hacete los scripts siguientes y ejecutalos en tu consola:

* Para Windows
```PowerShell
# Crear directorios
mkdir drivers,dags,plugins,logs,config,scripts

# URL base del repositorio
$base_url = "https://raw.githubusercontent.com/Tomasteawita/tomasteawita-airflow/main"

# Lista de archivos a descargar
$files = @("docker-compose.yml", "Dockerfile.airflow", "Dockerfile.spark", "drivers/postgresql-42.5.2.jar", "requirements.txt", "README.md", "config/airflow.cfg", ".env")

# Descargar cada archivo
foreach ($file in $files) {
    echo "Descargando $file"
    Invoke-WebRequest -Uri "$base_url/$file" -OutFile "./$file"
    echo "Descargado $file"
}
```

* Para MacOS o Linux

```Bash
#!/bin/bash

# Crear directorios
mkdir -p drivers dags plugins logs config scripts

# URL base del repositorio
base_url="https://raw.githubusercontent.com/Tomasteawita/tomasteawita-airflow/main"

# Lista de archivos a descargar
files=("docker-compose.yml" "Dockerfile.airflow" "Dockerfile.spark" "drivers/postgresql-42.5.2.jar" "requirements.txt" "README.md" "config/airflow.cfg" ".env")

# Descargar cada archivo
for file in "${files[@]}"; do
    echo "Descargando $file"
    curl -o "./$file" "$base_url/$file"
    echo "Descargado $file"
done
```

Una vez ejecutado el script y te hayas llevado todos los archivos de este repo a tu directorio raiz, ejecutá
```PowerShell
docker-compose up --build
```
Y ya vas a poder levantar airflow con operadores de Spark funcionando :) .

## Crea base de datos Postgre
Si vas a utilizar la base de datos del servicio postgre, crea una base de datos, un usuario y una contraseña, en el directorio `scripts/sql` tienes un ejemplo.

## Configuraciones de Airflow
Una vez que los servicios estén levantados, ingresar a Airflow en http://localhost:8080/ con usuario "airflow" y contraseña "airflow".

En la pestaña `Admin -> Connections` crear una nueva conexión con los siguientes datos para Redshift:
    * Conn Id: `postgres_connection`
    * Conn Type: `Postgres`
    * Host: `postgres`
    * Database: `nombre_db`
    * Schema: `esquema de redshift`
    * User: `usuario`
    * Password: `contraseña`
    * Port: `5432`

Ahora hacemos el mismo proceso para utilizar los SparkOperators
    * Conn Id: `spark_default`
    * Conn Type: `Spark`
    * Host: `spark://spark`
    * Port: `7077`
    * Extra: `{"queue": "default"}`

En la pestaña `Admin -> Variables` crear las siguientes variables con los siguientes datos:
1. Variables para la ruta del Driver de Postgre:
    * Key: `driver_class_path`
    * Value: `/tmp/drivers/postgresql-42.5.2.jar`
2. Variable para la ruta con los scripts para los DAGs que utilizan operadores de Spark:
    * Key: `spark_scripts_dir`
    * Value: `/opt/airflow/scripts`

Para el envío de Emails con SMTP, es necesario que la cuenta desde donde se va a enviar el email sea de tipo `gmail` y se genera una contraseña de aplicación. Posteriormente creamos las siguientes variables:
1. Email de origen:
    * Key: `smtp_from`
    * Value: `tu_email@gmail.com`
2. Contraseña de aplicación:    
    * Key: `smtp_password`
    * Value: `<contraseña de aplicación creada en gmail>`
3. Email destinatario:
    * Key: `smtp_to`
    * Value: `el email al cual deseas enviar tus reportes diarios(puede ser @gmail, @yahoo o cualquier otro).`

Si no aparecen los dags una vez agregadas las conexiones y las variables, detener el contenedor con `ctrl + c` en la misma consola (si por alguna razon usaste un `docker-compose up -d` utiliza en comando `docker-compose down` dentro del mismo directorio) y ejecuta denuevo el comando `docker-compose up`.

Ejecutar los DAGs `etl_top_tokens` y `etl_market_chart`, si es la primera vez que ejecutas los dags, espera a que finalice el DAG `etl_market_chart` para poder ejecutar el DAG `trigger_bitcoin`.
