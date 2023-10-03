import pandas as pd #utilizaremos pandas para el mejor manejo de tablas
import numpy as np #utilizaremos numpy para un mejor tratamiento de los datos
import matplotlib.pyplot as plt
import seaborn as sns # matplotlib y seaborn seran usados para graficar
from pyspark.sql import SparkSession #pyspark lo usaremos como opcion al gran requerimiento de procesamiento de datos

# Crea una sesión de Spark
spark = SparkSession.builder \
    .appName("MiAplicacionSpark") \
    .getOrCreate()
#importamos las funciones sql de pyspark para el manejo de columnas y valores
from pyspark.sql.functions import col, sum, when, size, length, to_date, from_unixtime, year, regexp_replace, avg, lit, coalesce, array, concat_ws, isnull
from pyspark.ml.feature import Imputer



def etl_metadata(archivo):
    """
    crea un dataframe con pyspark que hara un proceso
    sencillo de etl, con transformaciones de columnas,
    eliminacion de duplicados y tratamiento de valores nulos.
    parametros: 
    validador: solo en caso de ser True, se hace el proceso.
    """
    df = spark.read.json(archivo)
    df = df.dropDuplicates()
    # Lista de nombres de columnas que deseas eliminar
    columnas_a_eliminar = ["imageURL", "imageUrlHighRes", "tech1", 'tech2', 'category', 'date', 'feature', 'fit', 'similar_item']

    # Elimina las columnas especificadas
    df = df.drop(*columnas_a_eliminar)


    # eliminamos los valores nulos
    df = df.na.drop(subset=['title'])
    df = df.na.drop(subset=['details'])

    #Convertimos las columnas a su tipo de dato y trasnformamos
    df = df.withColumn('main_cat', lit('Digital Music'))
    
    # Utiliza regexp_replace para eliminar todos los caracteres que no sean números
    df = df.withColumn('rank', regexp_replace(df['rank'], '[^0-9]', ''))
    df = df.withColumn("rank", when(df["rank"] == '', 'N/D').otherwise(df["rank"]))
    df = df.fillna({'brand': 'N/D'})

    df = df.withColumn("also_buy", concat_ws(", ", col("also_buy")))
    df = df.withColumn("also_view", concat_ws(", ", col("also_view")))
    df = df.withColumn("description", concat_ws(", ", col("description")))

    df = df.withColumn("also_buy", when(col("also_buy") == '', 'N/D').otherwise(col("also_buy")))
    df = df.withColumn("also_view", when(col("also_view") == '', 'N/D').otherwise(col("also_view")))
    df = df.withColumn("description", when(col("description") == '', 'N/D').otherwise(col("description")))
        
    df = df.withColumn("price", regexp_replace(col("price"), "\\$", "").cast("float"))
    
    # Crea un imputador para reemplazar los valores nulos en la columna 'price' con la moda
    imputer = Imputer(strategy="mode", inputCol="price", outputCol="price")

    # Ajusta el imputador al conjunto de datos y reemplaza los valores nulos
    model = imputer.fit(df)
    df = model.transform(df)
    return df
