# Vaga-de-Estagio

Descrição do Projeto
Solução completa para coleta, processamento e análise de dados da Agência Nacional de Saúde Suplementar (ANS), composta por três módulos principais:

Web Scraping: Coleta automatizada de documentos oficiais

Transformação de Dados: Conversão de PDFs para dados estruturados

Banco de Dados: Armazenamento e análise de informações financeiras das operadoras

# Módulo 1: Web Scraping
Funcionalidades
Acesso automatizado ao portal da ANS

Download dos Anexos I e II em PDF

Compactação dos arquivos em formato ZIP

Tecnologias
Python com BeautifulSoup e requests

Manipulação de arquivos PDF e ZIP

# Módulo 2: Transformação de Dados
Processamento
Extração de tabelas de PDF para CSV

Normalização de abreviações (OD → Odontológico, AMB → Ambulatorial)

Compactação do resultado final

Saídas
Arquivo Teste_Edson_Carvalho.zip contendo:

Dados estruturados em CSV

Metadados da transformação

# Módulo 3: Banco de Dados
Estrutura
Tabela de Operadoras: Dados cadastrais

Tabela de Demonstrações Contábeis: Dados financeiros

Consultas Analíticas
Top 10 operadoras com maiores despesas médico-hospitalares (trimestral)

Ranking anual de despesas médico-hospitalares

Requisitos Técnicos
Dependências
Python 3.8+

MySQL 8+ ou PostgreSQL 10+

Bibliotecas Python:

BeautifulSoup4, requests, PyPDF2, pandas

SQLAlchemy 

Dados de Entrada
PDFs dos Anexos I e II da ANS

Arquivos CSV das demonstrações contábeis (2 anos)

Dados cadastrais das operadoras ativas
