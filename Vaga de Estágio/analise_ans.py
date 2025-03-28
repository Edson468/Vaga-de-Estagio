# -*- coding: utf-8 -*-
"""
Script completo para análise de dados da ANS
Execução passo-a-passo diretamente no VS Code
"""

import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import zipfile
import pdfplumber

def configurar_ambiente():
    """Cria a estrutura de pastas e verifica dependências"""
    os.makedirs('dados_ans', exist_ok=True)
    os.makedirs('resultados', exist_ok=True)
    
    print("✅ Ambiente configurado - pastas criadas")

def baixar_dados():
    """Baixa os arquivos necessários diretamente dos portais da ANS"""
    base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/"
    
    # 1. Dados cadastrais das operadoras
    url_operadoras = f"{base_url}operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
    try:
        r = requests.get(url_operadoras, timeout=30)
        with open('dados_ans/operadoras.csv', 'wb') as f:
            f.write(r.content)
        print("✅ Dados das operadoras baixados")
    except Exception as e:
        print(f"❌ Erro ao baixar operadoras: {e}")

    # 2. Demonstrações contábeis (últimos 2 anos)
    ano_atual = datetime.now().year
    for ano in [ano_atual - 1, ano_atual]:
        for mes in range(1, 13):
            arquivo = f"demonstracao_{ano}{mes:02d}.csv"
            try:
                r = requests.get(f"{base_url}demonstracoes_contabeis/{arquivo}", timeout=30)
                with open(f'dados_ans/{arquivo}', 'wb') as f:
                    f.write(r.content)
                print(f"✅ {arquivo} baixado")
            except:
                continue  # Alguns meses podem não ter arquivo

def processar_dados():
    """Processa os arquivos baixados e prepara para análise"""
    # 1. Processar operadoras
    try:
        df_operadoras = pd.read_csv('dados_ans/operadoras.csv', sep=';', encoding='utf-8')
        df_operadoras.to_parquet('dados_ans/operadoras.parquet', index=False)
        print("✅ Dados das operadoras processados")
    except Exception as e:
        print(f"❌ Erro ao processar operadoras: {e}")

    # 2. Processar demonstrações contábeis
    arquivos = [f for f in os.listdir('dados_ans') if f.startswith('demonstracao_')]
    dfs = []
    
    for arquivo in arquivos:
        try:
            df = pd.read_csv(f'dados_ans/{arquivo}', sep=';', encoding='utf-8', decimal=',')
            dfs.append(df)
        except Exception as e:
            print(f"❌ Erro ao processar {arquivo}: {e}")
    
    if dfs:
        df_contabil = pd.concat(dfs)
        df_contabil.to_parquet('dados_ans/demonstracoes.parquet', index=False)
        print(f"✅ {len(dfs)} arquivos contábeis processados")

def analisar_dados():
    """Realiza as análises solicitadas e gera relatórios"""
    try:
        # Carregar dados processados
        df_operadoras = pd.read_parquet('dados_ans/operadoras.parquet')
        df_contabil = pd.read_parquet('dados_ans/demonstracoes.parquet')
        
        # Converter datas
        df_contabil['DATA'] = pd.to_datetime(df_contabil['DATA'], format='%Y%m')
        
        # 1. Análise do último trimestre
        data_corte = datetime.now() - timedelta(days=90)
        df_trimestre = df_contabil[df_contabil['DATA'] >= data_corte]
        
        despesas_trimestre = df_trimestre[
            df_trimestre['DESCRICAO'].str.contains('EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR', case=False)
        ].merge(df_operadoras, on='REGISTRO_ANS')
        
        top10_trimestre = despesas_trimestre.groupby('RAZAO_SOCIAL')['VALOR'].sum().nlargest(10)
        
        # 2. Análise do último ano
        data_corte_ano = datetime.now() - timedelta(days=365)
        df_ano = df_contabil[df_contabil['DATA'] >= data_corte_ano]
        
        despesas_ano = df_ano[
            df_ano['DESCRICAO'].str.contains('EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR', case=False)
        ].merge(df_operadoras, on='REGISTRO_ANS')
        
        top10_ano = despesas_ano.groupby('RAZAO_SOCIAL')['VALOR'].sum().nlargest(10)
        
        # Salvar resultados
        with pd.ExcelWriter('resultados/analise_ans.xlsx') as writer:
            top10_trimestre.to_excel(writer, sheet_name='Top10 Trimestre')
            top10_ano.to_excel(writer, sheet_name='Top10 Ano')
        
        print("✅ Análise concluída - resultados salvos em 'resultados/analise_ans.xlsx'")
        
        # Gerar gráficos
        plt.figure(figsize=(12, 6))
        top10_trimestre.plot(kind='barh')
        plt.title('Top 10 Operadoras - Maiores Despesas (Último Trimestre)')
        plt.tight_layout()
        plt.savefig('resultados/top10_trimestre.png')
        
        plt.figure(figsize=(12, 6))
        top10_ano.plot(kind='barh')
        plt.title('Top 10 Operadoras - Maiores Despesas (Último Ano)')
        plt.tight_layout()
        plt.savefig('resultados/top10_ano.png')
        
        print("✅ Gráficos gerados na pasta 'resultados'")
        
    except Exception as e:
        print(f"❌ Erro na análise: {e}")

def main():
    print("=== ANÁLISE DE DADOS DA ANS ===")
    print("1. Configurando ambiente...")
    configurar_ambiente()
    
    print("\n2. Baixando dados...")
    baixar_dados()
    
    print("\n3. Processando dados...")
    processar_dados()
    
    print("\n4. Analisando dados...")
    analisar_dados()
    
    print("\nProcesso concluído! Verifique a pasta 'resultados'.")

if __name__ == "__main__":
    main()