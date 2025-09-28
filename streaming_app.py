from pyspark.sql import SparkSession
#from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("K8sPySparkStreaming") \
    .config("spark.ui.port", "4040") \
    .getOrCreate()

# Input folder inside the pod
folder_path = "/data"

# Checkpoint directory (you've already created /data/checkpoint on the host)
checkpoint_path = f"{folder_path}/checkpoint"

# Read schema from an existing file
schema = spark.read.parquet(f"{folder_path}/yellow_tripdata_2025-01.parquet").schema

# Set up streaming reader
df_stream = spark.readStream \
    .schema(schema) \
    .format("parquet") \
    .load(folder_path)

# Group by PULocationID (stateful aggregation)
agg_df = df_stream.groupBy("PULocationID").count()

# Output to console with safe checkpoint path
query = agg_df.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("checkpointLocation", checkpoint_path) \
    .start()

query.awaitTermination()
