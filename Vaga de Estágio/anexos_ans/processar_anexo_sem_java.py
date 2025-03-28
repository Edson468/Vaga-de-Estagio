import os
import csv
import zipfile
import pdfplumber

def extrair_tabelas_pdf(pdf_path):
    """Extrai tabelas de um PDF usando pdfplumber"""
    todas_tabelas = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extrai tabelas da página atual
            tabelas = page.extract_tables()
            
            # Para cada tabela na página
            for tabela in tabelas:
                if tabela:  # Verifica se a tabela não está vazia
                    # Adiciona apenas linhas com dados válidos
                    linhas_validas = [linha for linha in tabela if any(campo for campo in linha)]
                    if linhas_validas:
                        todas_tabelas.extend(linhas_validas)
    
    return todas_tabelas

def processar_anexo_i():
    # Configurações
    pdf_path = "Anexo_I.pdf"
    csv_output = "Rol_Procedimentos.csv"
    zip_output = "Teste_Edson_Carvalho.zip"
    
    try:
        # 2.1 Extrair dados do PDF
        print("Extraindo tabelas do PDF (sem Java)...")
        dados = extrair_tabelas_pdf(pdf_path)
        
        if not dados:
            print("Nenhuma tabela encontrada no PDF.")
            return
        
        print(f"Total de registros extraídos: {len(dados)-1}")  # Subtrai o cabeçalho
        
        # 2.2 Salvar em CSV com tratamento das colunas
        print("Processando e salvando dados em CSV...")
        with open(csv_output, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            
            # Escreve cabeçalho (ajustar conforme estrutura real do PDF)
            writer.writerow(['CODIGO', 'DESCRICAO', 'TIPO_ATENDIMENTO', 'PORTE', 'PRAZO'])
            
            # Processa cada linha de dados
            for linha in dados[1:]:  # Pula o cabeçalho se já estiver nos dados
                if len(linha) >= 5:  # Verifica se tem colunas suficientes
                    # 2.4 Substitui abreviações
                    tipo_atendimento = linha[2].replace('OD', 'Seg. Odontológico').replace('AMB', 'Seg. Ambulatorial')
                    
                    # Escreve linha processada
                    writer.writerow([
                        linha[0],       # CODIGO
                        linha[1],      # DESCRICAO
                        tipo_atendimento,  # TIPO_ATENDIMENTO (já convertido)
                        linha[3],       # PORTE
                        linha[4]        # PRAZO
                    ])
        
        # 2.3 Compactar o CSV
        print("Criando arquivo ZIP...")
        with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_output)
        
        print(f"\nProcesso concluído com sucesso!")
        print(f"Arquivo ZIP gerado: {zip_output}")
        
        # Opcional: remover o CSV após compactar
        os.remove(csv_output)
        
    except Exception as e:
        print(f"\nOcorreu um erro: {str(e)}")

if __name__ == "__main__":
    print("=== Processamento do Anexo I (sem Java) ===")
    processar_anexo_i()