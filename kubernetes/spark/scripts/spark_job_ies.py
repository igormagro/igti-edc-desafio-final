from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import os

aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']

# set conf
conf = (
SparkConf()
    .set("spark.hadoop.fs.s3a.access.key", aws_access_key_id)
    .set("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key)
    .set("spark.hadoop.fs.s3a.fast.upload", True)
    .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:2.7.3')
)

# apply config
sc = SparkContext(conf=conf).getOrCreate()
    

if __name__ == "__main__":

    # init spark session
    spark = SparkSession\
            .builder\
            .appName("Save as Parquet")\
            .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")
    
    df4 = (
        spark
        .read
        .format("csv")
        .options(header='true', inferSchema='true', delimiter=';')
        .load("s3a://370799417405-raw-zone/inep/SUP_IES/")
    )
    
    

    df4.show()
    df4.printSchema()

    (
        df4
        .write
        .mode("overwrite")
        .format("parquet")
        .save("s3a://370799417405-processing-zone/inep/SUP_IES/")
    )

    print("*****************")
    print("Escrito com sucesso!")
    print("*****************")

    spark.stop()