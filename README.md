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