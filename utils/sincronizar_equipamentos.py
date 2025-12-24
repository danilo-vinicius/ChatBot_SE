import requests
import os
import json

# URL da API de Equipamentos
URL_API = "https://sla.performancelab.com.br/v3/powerbi/rest/fieldlab_equipamentos/5c50b4df4b176845cd235b6a510c6903/.json"
PASTA_DESTINO = "estudo_equipamentos"

def limpar(texto):
    if not texto or str(texto).lower() in ['none', 'null', 'geral', 'genérico']:
        return ""
    return str(texto).strip()

def baixar_equipamentos():
    print(f"🔄 Baixando inventário de equipamentos...")
    
    try:
        response = requests.get(URL_API)
        
        if response.status_code == 200:
            dados = response.json()
            print(f"✅ Recebido! Processando {len(dados)} equipamentos...")
            
            if not os.path.exists(PASTA_DESTINO):
                os.makedirs(PASTA_DESTINO)
            
            salvos = 0
            for item in dados:
                # Pega dados limpos
                id_eq = item.get('id')
                nome = item.get('nome')
                marca = limpar(item.get('marca_nome'))
                modelo = limpar(item.get('modelo'))
                produto = item.get('produto_nome')
                local = item.get('local_nome')
                
                # Só salva se tiver Marca E Modelo (informação útil pra manual)
                # Ou se tiver pelo menos um nome específico
                if marca and modelo:
                    nome_arquivo = f"EQ_{id_eq}_{marca}_{modelo}.txt".replace("/", "-")
                    caminho = os.path.join(PASTA_DESTINO, nome_arquivo)
                    
                    conteudo = f"""
                    --- FICHA DE EQUIPAMENTO INSTALADO ---
                    ID: {id_eq}
                    LOCAL/CLIENTE: {local}
                    NOME NO SISTEMA: {nome}
                    TIPO: {produto}
                    
                    MARCA: {marca}
                    MODELO TÉCNICO: {modelo}
                    
                    SITUAÇÃO: {item.get('situacao_nome')}
                    GARANTIA (Meses): {item.get('garantia')}
                    """
                    
                    with open(caminho, "w", encoding="utf-8") as f:
                        f.write(conteudo)
                    salvos += 1
            
            print(f"🚀 Sucesso! {salvos} equipamentos catalogados em '{PASTA_DESTINO}'.")
            
        else:
            print(f"❌ Erro API: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    baixar_equipamentos()