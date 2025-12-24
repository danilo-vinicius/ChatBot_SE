import requests
import os
import json

# URL da sua Base de Conhecimento (PerformanceLab)
URL_API = "https://sla.performancelab.com.br/v3/powerbi/rest/fieldlab_oss/5c50b4df4b176845cd235b6a510c6903/.json"
PASTA_DESTINO = "estudo_os"

def limpar_texto(texto):
    """Remove None ou textos vazios"""
    if not texto:
        return "Não informado"
    return str(texto).strip()

def baixar_e_salvar_os():
    print(f"🔄 Conectando à API PerformanceLab...")
    
    try:
        response = requests.get(URL_API)
        
        if response.status_code == 200:
            dados = response.json()
            print(f"✅ Dados recebidos! Total de registros encontrados: {len(dados)}")
            
            if not os.path.exists(PASTA_DESTINO):
                os.makedirs(PASTA_DESTINO)
            
            salvos = 0
            ignorado_sem_info = 0

            for os_item in dados:
                # Mapeamento dos campos do seu JSON
                id_os = os_item.get('id')
                cliente = limpar_texto(os_item.get('site_nome'))
                equipamento = f"{limpar_texto(os_item.get('equipamento_nome'))} - {limpar_texto(os_item.get('equipamento_modelo'))}"
                tecnico = limpar_texto(os_item.get('tecnico_nome'))
                
                # Onde está o problema? (Concatena Necessidade + Problema específico)
                problema_desc = limpar_texto(os_item.get('necessidade'))
                if os_item.get('problema'):
                    problema_desc += f"\nDetalhe do Defeito: {os_item.get('problema')}"

                # Onde está a solução? (Concatena Observações + Última Ação)
                # A IA vai usar isso para aprender o que foi feito
                solucao = ""
                obs = os_item.get('observacoes')
                acao = os_item.get('ultima_acao_realizada')
                
                if obs: solucao += f"Notas: {obs}\n"
                if acao: solucao += f"Status/Ação Final: {acao}"

                # Filtro de Qualidade: Só salvamos se tiver alguma descrição de solução/ação útil
                # Ignoramos OSs que só dizem "OS Resolvida" sem detalhes, a menos que a 'necessidade' seja rica
                if len(problema_desc) > 10: 
                    nome_arquivo = f"OS_{id_os}.txt"
                    caminho_arquivo = os.path.join(PASTA_DESTINO, nome_arquivo)
                    
                    conteudo_arquivo = f"""
========================================
ORDEM DE SERVIÇO: {id_os}
CLIENTE: {cliente}
EQUIPAMENTO: {equipamento}
TÉCNICO: {tecnico}
========================================
[PROBLEMA / SOLICITAÇÃO]
{problema_desc}

[HISTÓRICO E SOLUÇÃO TÉCNICA]
{solucao}
========================================
"""
                    with open(caminho_arquivo, "w", encoding="utf-8") as f:
                        f.write(conteudo_arquivo)
                    salvos += 1
                else:
                    ignorado_sem_info += 1
            
            print(f"🚀 Concluído! {salvos} OSs salvas na pasta '{PASTA_DESTINO}'.")
            print(f"⚠️ {ignorado_sem_info} OSs ignoradas por falta de informação relevante.")
            
        else:
            print(f"❌ Erro na API: Código {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    baixar_e_salvar_os()