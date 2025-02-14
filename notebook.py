def read_csv(spark, caminho_csv):

    rdd = spark.sparkContext.textFile(caminho_csv)

    rdd_data = rdd.zipWithIndex().filter(lambda x: x[1] > 1).map(lambda x: x[0])

    rdd_cleaned = rdd_data.map(lambda line: [field.replace('"', '') for field in line.split(";")])

    return rdd_cleaned

def create_colunas(spark, caminho_csv):
    df = (spark.read.option("header", "false").csv(caminho_csv))
    # Obter a segunda linha como cabeçalho
    novo_header = df.collect()[1]  
    colunas = [str(c).replace('"', '').strip() for c in novo_header[0].split(";")]
    return colunas

def creat_dataframe(rdd_cleaned, colunas):
    df = rdd_cleaned.toDF(colunas)
    return df

def create_table_voos(df):
    from pyspark.sql import functions as F
    from pyspark.sql.functions import concat
    from pyspark.sql.functions import col
    # Filtro
    df_filtrado = df.filter(
        (df["EMPRESA_SIGLA"] == "GLO") &
        (df["GRUPO_DE_VOO"] == "REGULAR") &
        (df["NATUREZA"] == "DOMÉSTICA")
    )
    df_prep = df_filtrado.withColumn("MERCADO",
            concat(
                F.least(F.col("AEROPORTO_DE_ORIGEM_SIGLA"), F.col("AEROPORTO_DE_DESTINO_SIGLA")),
                F.greatest(F.col("AEROPORTO_DE_ORIGEM_SIGLA"), F.col("AEROPORTO_DE_DESTINO_SIGLA"))
            )) \
        .select("MES", "ANO", "RPK", "MERCADO") \


    df_DB = df_prep.withColumn("mes", col("mes").cast("int")) \
             .withColumn("ano", col("ano").cast("int")) \
             .withColumn("rpk", col("rpk").cast("double"))

    df_DB = df_DB.na.drop()

    return df_DB

def conect_psql():
    from pyspark.sql import SparkSession

    jdbc_driver_path = "C:/Users/User/AppData/Local/Programs/Python/Python311/Lib/site-packages/pyspark/jars/postgresql-42.7.5.jar"

    spark = SparkSession.builder \
        .appName("PostgreSQL Connection") \
        .config("spark.jars", jdbc_driver_path) \
        .config("spark.driver.extraClassPath", jdbc_driver_path) \
        .getOrCreate()

def write_db(df_DB, database_url):

    df_DB.write \
        .format("jdbc") \
        .option("url", database_url) \
        .option("dbtable", "voos") \
        .option("user", "root") \
        .option("password", "root") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

def write_csv(df_DB):
    import csv
    novo_caminho_csv = "dados/populate.csv"

    dados_lista = df_DB.rdd.map(lambda row: row.asDict()).collect()
    colunas = df_DB.columns
    with open(novo_caminho_csv, "w", encoding="utf-8", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=colunas)
        writer.writeheader() 
        writer.writerows(dados_lista)

if __name__ == "__main__":
    import findspark
    import shutil
    import glob
    import os
    findspark.init()
    from pyspark.sql import SparkSession

    # Criar a sessão Spark de forma mais simples
    spark = SparkSession.builder \
        .appName("TestePySpark") \
        .master("local[*]") \
        .getOrCreate()

    caminho_csv = "dados/dados_gol.csv"
    database_url = "jdbc:postgresql://localhost:5432/anac"

    rdd_cleaned = read_csv(spark,caminho_csv)
    colunas = create_colunas(spark, caminho_csv)
    df = creat_dataframe(rdd_cleaned, colunas)

    df_DB = create_table_voos(df)

    conect_psql()
    write_db(df_DB,database_url)