import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import input_file_name, regexp_extract, col

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load from Glue Catalog table
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="iot_database",
    table_name="group1_temp001"
)

# Convert to Spark DataFrame for transformation
df = datasource.toDF()

# Extract metadata from S3 path (group/device info)
df = df.withColumn("s3_path", input_file_name())
df = df.withColumn("group", regexp_extract("s3_path", r"group(\d+)", 1))
df = df.withColumn("device_id", regexp_extract("s3_path", r"/(temp-\d+)/", 1))

# Filter invalid or extreme temperature values
df_clean = df.filter((df.temperature < 85) & (df.temperature > -40))

# Write as Parquet to new S3 location
df_clean.write.mode("overwrite").partitionBy("group", "device_id").parquet("s3://your-cleaned-bucket/cleaned/")

job.commit()
