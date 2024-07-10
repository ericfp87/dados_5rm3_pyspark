from pyspark.sql import SparkSession
from pyspark.sql.functions import count
import os
import shutil

# Inicialize a sessão Spark
spark = SparkSession.builder.appName('ProcessarArquivosTXT').getOrCreate()

# Defina o caminho da pasta de entrada e de processados
pasta_entrada = r'C:\Files\Leitura\Dados\5RM3\Fases'
pasta_processados = r'C:\Files\Leitura\Dados\5RM3\Fases\PROCESSADOS'

# Lista todos os arquivos .txt na pasta de entrada
arquivos = [f for f in os.listdir(pasta_entrada) if f.endswith('.txt')]

for arquivo in arquivos:
    # Construa o caminho completo do arquivo
    caminho_arquivo = os.path.join(pasta_entrada, arquivo)
    
    # Leia o arquivo .txt no DataFrame
    df = spark.read.option("delimiter", ";").csv(caminho_arquivo, header=True)
    
    # Selecione as colunas necessárias e renomeie a coluna 'OCORRENCIA'
    df = df.select("REFER", "UNIDADE", "GERENCIA", "OCORRENCIA").withColumnRenamed("OCORRENCIA", "COD_OCORRENCIA")
    
    # Agregue os valores da contagem da coluna 'COD_OCORRENCIA'
    df = df.groupBy("REFER", "UNIDADE", "GERENCIA", "COD_OCORRENCIA").agg(count("COD_OCORRENCIA").alias("QTD_LEITURAS"))

    df = df.select("REFER", "UNIDADE", "GERENCIA", "QTD_LEITURAS", "COD_OCORRENCIA")

    # Coalesce o DataFrame em uma única partição
    df = df.coalesce(1)
    
    # Escreva o DataFrame em um arquivo .parquet
    df.write.mode('append').parquet(r'C:\Files\INDICADORES DE LEITURAS - COPASA\DATABASE\indicadores_leituras.parquet')

    # Escreva o DataFrame em um arquivo .csv
    df.write.mode('append').csv(r'C:\Files\INDICADORES DE LEITURAS - COPASA\DATABASE\indicadores_leituras.csv')
    
    # Mova o arquivo .txt processado para a pasta 'Processados'
    shutil.move(caminho_arquivo, os.path.join(pasta_processados, arquivo))

    print(f'{caminho_arquivo} concluído!')

print("Tarefa Concluída!")
