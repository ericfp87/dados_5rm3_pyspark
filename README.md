Aqui está um exemplo de como poderia ser o `README.md` para o seu código:

```markdown
# Processamento de Arquivos TXT com PySpark

Este repositório contém um script Python que utiliza PySpark para processar arquivos `.txt` de uma pasta, realiza transformações e agrega dados, e salva os resultados em formatos `.parquet` e `.csv`.

## Requisitos

- Python 3.x
- PySpark
- Os pacotes `os` e `shutil` (nativos do Python)

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd seu-repositorio
   ```
3. Instale as dependências necessárias:
   ```bash
   pip install pyspark
   ```

## Uso

1. Defina os caminhos das pastas de entrada e de processados no script conforme necessário.
2. Coloque seus arquivos `.txt` na pasta de entrada especificada.
3. Execute o script:
   ```bash
   python seu_script.py
   ```

## Descrição do Script

O script realiza as seguintes operações:

1. **Inicialização da Sessão Spark**:
   ```python
   spark = SparkSession.builder.appName('ProcessarArquivosTXT').getOrCreate()
   ```

2. **Definição dos Caminhos das Pastas**:
   ```python
   pasta_entrada = r'C:\Files\Leitura\Dados\5RM3\Fases'
   pasta_processados = r'C:\Files\Leitura\Dados\5RM3\Fases\PROCESSADOS'
   ```

3. **Listagem dos Arquivos `.txt` na Pasta de Entrada**:
   ```python
   arquivos = [f for f in os.listdir(pasta_entrada) if f.endswith('.txt')]
   ```

4. **Processamento de Cada Arquivo**:
   - Leitura do arquivo `.txt` no DataFrame:
     ```python
     df = spark.read.option("delimiter", ";").csv(caminho_arquivo, header=True)
     ```
   - Seleção e renomeação das colunas:
     ```python
     df = df.select("REFER", "UNIDADE", "GERENCIA", "OCORRENCIA").withColumnRenamed("OCORRENCIA", "COD_OCORRENCIA")
     ```
   - Agregação dos valores da contagem da coluna `COD_OCORRENCIA`:
     ```python
     df = df.groupBy("REFER", "UNIDADE", "GERENCIA", "COD_OCORRENCIA").agg(count("COD_OCORRENCIA").alias("QTD_LEITURAS"))
     ```
   - Seleção das colunas finais:
     ```python
     df = df.select("REFER", "UNIDADE", "GERENCIA", "QTD_LEITURAS", "COD_OCORRENCIA")
     ```
   - Coalescência do DataFrame em uma única partição:
     ```python
     df = df.coalesce(1)
     ```
   - Escrita do DataFrame em arquivos `.parquet` e `.csv`:
     ```python
     df.write.mode('append').parquet(r'C:\Files\INDICADORES DE LEITURAS - COPASA\DATABASE\indicadores_leituras.parquet')
     df.write.mode('append').csv(r'C:\Files\INDICADORES DE LEITURAS - COPASA\DATABASE\indicadores_leituras.csv')
     ```
   - Movimentação do arquivo `.txt` processado para a pasta 'Processados':
     ```python
     shutil.move(caminho_arquivo, os.path.join(pasta_processados, arquivo))
     ```
   - Impressão de mensagem de conclusão para cada arquivo:
     ```python
     print(f'{caminho_arquivo} concluído!')
     ```

5. **Mensagem de Conclusão Geral**:
   ```python
   print("Tarefa Concluída!")
   ```

## Contribuição

1. Faça um fork do projeto
2. Crie uma nova branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Envie para a branch (`git push origin feature/nova-funcionalidade`)
5. Crie um novo Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
```

Adapte conforme necessário, especialmente as partes onde menciona o caminho dos arquivos e o repositório do GitHub.