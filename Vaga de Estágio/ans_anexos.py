import os
import requests
import zipfile
from bs4 import BeautifulSoup

def baixar_e_compactar_anexos():
    # Configurações
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    pasta_downloads = os.path.join(diretorio_base, "anexos_ans")
    zip_nome = os.path.join(diretorio_base, "anexos_ans.zip")
    
    try:
        # 1. Criar pasta de downloads se não existir
        os.makedirs(pasta_downloads, exist_ok=True)
        print(f"Pasta de downloads criada em: {pasta_downloads}")

        # 2. Acessar o site
        print("\nConectando ao portal da ANS...")
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        # 3. Buscar os anexos
        print("Localizando os anexos na página...")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Padrões de busca melhorados
        padroes = {
            'Anexo I': ['anexo i', 'i - anexo', 'rol i'],
            'Anexo II': ['anexo ii', 'ii - anexo', 'rol ii']
        }
        
        arquivos_baixados = []

        # 4. Download dos anexos
        for anexo, termos in padroes.items():
            encontrado = False
            for link in soup.find_all('a'):
                href = link.get('href', '').lower()
                texto = link.text.strip().lower()
                
                if any(termo in texto or termo in href for termo in termos) and href.endswith('.pdf'):
                    try:
                        print(f"\nIniciando download do {anexo}...")
                        pdf_url = link['href'] if link['href'].startswith('http') else f"https://www.gov.br{link['href']}"
                        
                        pdf_response = requests.get(pdf_url, timeout=20)
                        pdf_response.raise_for_status()
                        
                        nome_arquivo = f"{anexo.replace(' ', '_')}.pdf"
                        caminho_arquivo = os.path.join(pasta_downloads, nome_arquivo)
                        
                        with open(caminho_arquivo, 'wb') as f:
                            f.write(pdf_response.content)
                        
                        arquivos_baixados.append(caminho_arquivo)
                        print(f"✅ {anexo} baixado com sucesso!")
                        encontrado = True
                        break
                    
                    except Exception as e:
                        print(f"⚠️ Erro ao baixar {anexo}: {str(e)}")
            
            if not encontrado:
                print(f"❌ {anexo} não encontrado na página")

        # 5. Compactação dos arquivos
        if arquivos_baixados:
            print("\nIniciando compactação dos arquivos...")
            try:
                with zipfile.ZipFile(zip_nome, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for arquivo in arquivos_baixados:
                        if os.path.exists(arquivo):
                            zipf.write(arquivo, os.path.basename(arquivo))
                            print(f"Adicionado ao ZIP: {os.path.basename(arquivo)}")
                        else:
                            print(f"Arquivo não encontrado para compactação: {arquivo}")
                
                print(f"\n✅ Compactação concluída! Arquivo ZIP criado em: {zip_nome}")
            except Exception as e:
                print(f"❌ Erro durante a compactação: {str(e)}")
        else:
            print("\n❌ Nenhum arquivo foi baixado para compactação.")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Erro de conexão: {str(e)}")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")

if __name__ == "__main__":
    print("=== Download e Compactação de Anexos da ANS ===")
    baixar_e_compactar_anexos()
    print("\nProcesso finalizado.")