# Importing necessary libraries
import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime, to_date
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType, BooleanType

# Initialize SparkSession
spark = SparkSession.builder.appName("ETL reviews Process").config("spark.hadoop.fs.defaultFS", "file:///").getOrCreate()

# Define file_path as command line argument
file_path = sys.argv[1]

# Define schema
schema = StructType([
    StructField("asin", StringType(), nullable=True),
    StructField("overall", FloatType(), nullable=True),
    StructField("reviewText", StringType(), nullable=True),
    StructField("reviewerID", StringType(), nullable=True),
    StructField("reviewerName", StringType(), nullable=True),
    StructField("unixReviewTime", IntegerType(), nullable=True),
    StructField("verified", BooleanType(), nullable=True)
    ])

# Read JSON or CSV file
df = spark.read.schema(schema).json(file_path)

# ETL Process
df = df.dropDuplicates() \
    .na.drop(subset=["reviewText", "reviewerName"]) \
    .withColumn("unixReviewTime", to_date(from_unixtime(col("unixReviewTime")))) \
    .withColumn("overall", col("overall").cast("int")) \
    .na.fill('N/D', ["reviewerName"]) \
    .withColumnRenamed("overall", "Overall") \
    .withColumnRenamed("verified", "Verified") \
    .withColumnRenamed("reviewerID", "CodigoUsuario") \
    .withColumnRenamed("asin", "CodigoProducto") \
    .withColumnRenamed("reviewerName", "NombreUsuario") \
    .withColumnRenamed("unixReviewTime", "Fecha") \
    .withColumnRenamed("reviewText", "Review")

# Repartition the DataFrame to a single partition
df = df.repartition(1)

# Define output path and file name
output_dir = os.path.dirname(file_path)
output_name = os.path.basename(file_path).replace(".json", "_Processed")

# Define full output path
output_path = os.path.join(output_dir, output_name)

# Save as JSON file
df.write.mode("overwrite").json(output_path)

# Stop SparkSession
spark.stop()