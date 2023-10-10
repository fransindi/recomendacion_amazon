from pyspark.sql import SparkSession #PySpark sera nuestra opcion para el manejo de grandes volumenes de datos


# Crea una sesión de Spark
spark = SparkSession.builder \
    .appName("MiAplicacionSpark") \
    .getOrCreate()

# Importamos las funciones de sql de pyspark para manejar mejor las columnas
from pyspark.sql.functions import col, sum, when, size, length, to_date, from_unixtime, year, count


from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType, BooleanType


   

def etl_reviews(archivo):
    """
    crea un dataframe con pyspark que hara un proceso
    sencillo de etl, con transformaciones de columnas,
    eliminacion de duplicados y tratamiento de valores nulos.
    parametros: 
    Archivo: un archivo tipo json que provenga de la fuente de Amazon.
    """
    try:
        df = spark.read.json(archivo)
    except:
        custom_schema = StructType([
        StructField("asin", StringType(), nullable=True),
        StructField("image", StringType(), nullable=True),
        StructField("overall", FloatType(), nullable=True),
        StructField("reviewText", StringType(), nullable=True),
        StructField("reviewTime", StringType(), nullable=True),
        StructField("reviewerID", StringType(), nullable=True),
        StructField("reviewerName", StringType(), nullable=True),
        StructField("style", StringType(), nullable=True),
        StructField("summary", StringType(), nullable=True),
        StructField("unixReviewTime", IntegerType(), nullable=True),
        StructField("verified", BooleanType(), nullable=True),
        StructField("vote", StringType(), nullable=True)
        ])
        df = spark.read.json(archivo, schema=custom_schema)

    # Eliminamos los duplicados donde esten todas las filas
    df = df.dropDuplicates()

    # Eliminamos las columnas que no nos haran falta
    columnas_a_eliminar = ['image', 'style', 'summary', 'vote', 'reviewTime']
    df = df.drop(*columnas_a_eliminar)
    
    # Eliminamos valores faltantes en las siguientes columnas
    df = df.na.drop(subset=['reviewText'])
    df = df.na.drop(subset=['reviewerName'])
    df = df.na.fill("N/D", ['reviewerName'])
    
    # Transformamos las columnas para un mejor entendimiento.
    df = df.withColumn("review_date", from_unixtime(df["unixreviewtime"]))
    df = df.withColumn("review_year", year(df["review_date"]))
    df = df.drop("unixreviewtime")
    return df

