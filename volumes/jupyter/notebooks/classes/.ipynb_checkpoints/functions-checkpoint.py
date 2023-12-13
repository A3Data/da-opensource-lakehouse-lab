import os
import pyspark
from pyspark.sql import SparkSession
import boto3
from botocore.config import Config
import psycopg2

def getOrCreateSparkSession(app_name, uri, aws_endpoint, access_key, secret_key, bucket) -> pyspark.sql.SparkSession:
    """Get or create a Spark session."""
    conf = (
        pyspark.SparkConf()
            .setAppName(app_name)
            .set(
                "spark.jars.packages",
                "software.amazon.awssdk:bundle:2.17.178,software.amazon.awssdk:url-connection-client:2.17.178,org.apache.iceberg:iceberg-spark-runtime-3.2_2.12:1.4.2,org.projectnessie.nessie-integrations:nessie-spark-extensions-3.2_2.12:0.74.0,org.apache.hadoop:hadoop-aws:3.3.1",
            )
            .set("spark.sql.execution.pyarrow.enabled", "true")
            .set('spark.sql.catalog.nessie', 'org.apache.iceberg.spark.SparkCatalog')
            .set('spark.sql.catalog.nessie.uri', uri)
            .set('spark.sql.catalog.nessie.ref', 'main')
            .set('spark.sql.catalog.nessie.authentication.type', 'NONE')
            .set('spark.sql.catalog.nessie.catalog-impl', 'org.apache.iceberg.nessie.NessieCatalog')
            .set('spark.sql.catalog.nessie.s3.endpoint', aws_endpoint)
            .set('spark.sql.catalog.nessie.warehouse', bucket)
            .set('spark.sql.catalog.nessie.io-impl', 'org.apache.iceberg.aws.s3.S3FileIO')
            .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
            .set('spark.hadoop.fs.s3a.access.key', access_key)
            .set('spark.hadoop.fs.s3a.secret.key', secret_key)
            .set("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
            .set("spark.hadoop.fs.s3a.path.style.access", True)
            .set(
                "spark.sql.extensions",
                "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions,org.projectnessie.spark.extensions.NessieSparkSessionExtensions",
            )
    )
    
    return SparkSession.builder.config(conf=conf).getOrCreate()

class minio:
    def __init__(self, endpoint_url, access_key, secret_key):
        self.endpoint_url = endpoint_url
        self.access_key = access_key
        self.secret_key = secret_key

        self.minio_client = self.create_minio_client()

    def create_minio_client(self):
        return boto3.client(
            's3', 
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
            )

    def list_buckets(self):
        response = self.minio_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        return buckets

    def upload_file(self, bucket_name, object_name, local_file_path):
        self.minio_client.upload_file(local_file_path, bucket_name, object_name)

    def download_file(self, bucket_name, object_name, local_file_path):
        self.minio_client.download_file(bucket_name, object_name, local_file_path)

    def read_file_from_minio(self, bucket_name, file):
    # Configurando o cliente do MinIO
        obj = self.minio_client.get_object(Bucket=bucket_name, Key=file)
    # Lendo o conteúdo do arquivo
        file_content = obj['Body'].read()
        
        return file_content

class postgres:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def conectar(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("Conectado com sucesso!")
        except Exception as e:
            print(f"Erro ao conectar: {e}")

    def desconectar(self):
        if self.connection:
            self.connection.close()
            print("Conexão encerrada!")

    def query(self, query):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query)
                self.connection.commit()
                cursor.close()
                print("Query executada com sucesso!")
            except Exception as e:
                print(f"Erro ao executar: {e}")
        else:
            print("Conect-se Primeiro")