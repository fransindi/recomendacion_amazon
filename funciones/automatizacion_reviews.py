import numpy as np #importamos numpy para un mejor manejo de matrizes, filas y valores
import matplotlib.pyplot as plt #esta libreria la usaremos para graficar
from pyspark.sql import SparkSession #PySpark sera nuestra opcion para el manejo de grandes volumenes de datos
import os

# Crea una sesión de Spark
spark = SparkSession.builder \
    .appName("MiAplicacionSpark") \
    .getOrCreate()

# Importamos las funciones de sql de pyspark para manejar mejor las columnas
from pyspark.sql.functions import col, sum, when, size, length, to_date, from_unixtime, year, count


   

def etl_reviews(archivo):
    """
    crea un dataframe con pyspark que hara un proceso
    sencillo de etl, con transformaciones de columnas,
    eliminacion de duplicados y tratamiento de valores nulos.
    parametros: 
    validador: solo en caso de ser True, se hace el proceso.
    """
   
    df = spark.read.json(archivo)
   
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
