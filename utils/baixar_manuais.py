import os
import time
import re
import requests
import streamlit as st
from duckduckgo_search import DDGS

# Pastas
PASTA_EQUIPAMENTOS = "estudo_equipamentos"
PASTA_OS = "estudo_os"
PASTA_MANUAIS = "estudo_manuais"

def identificar_marca_modelo(texto):
    """
    Analisa o texto e retorna (Marca, Modelo).
    """
    texto = texto.upper().strip()
    
    # 1. Padrões HIKVISION (DS-XXXX)
    match_hik = re.search(r'\b(DS-[A-Z0-9-]+)\b', texto)
    if match_hik:
        return "Hikvision", match_hik.group(1)

    # 2. Padrões PPA (Motores)
    # Ex: DZ Rio, 800 Fast, Jet Flex
    match_ppa = re.search(r'\b(DZ\s?[A-Z0-9]+|[0-9]{3,4}\s?FAST|[0-9]{3,4}\s?JET\s?FLEX)\b', texto)
    if match_ppa:
        return "PPA", match_ppa.group(1)

    # 3. Padrões INTELBRAS (Padrão Geral: Letras + Números)
    # Ex: MHDX 3004, AMT 2018, VIP 1230
    match_intel = re.search(r'\b([A-Z]{2,5}\s?-?\s?[0-9]{2,4}[A-Z0-9\s\/]*)\b', texto)
    if match_intel:
        # Limpeza extra para Intelbras
        modelo = match_intel.group(1).strip()
        # Remove sufixos que atrapalham a busca as vezes
        return "Intelbras", modelo
        
    return "Genérico", texto

def descobrir_equipamentos_alvo():
    """Varre as pastas e monta lista de (Marca, Modelo) para buscar."""
    alvos = set() # Usa set para evitar duplicatas de (Marca, Modelo)
    
    print("🔍 Varrendo arquivos...")
    
    # Função interna para processar linhas
    def processar_linha(linha_texto):
        if len(linha_texto) < 3: return
        marca, modelo = identificar_marca_modelo(linha_texto)
        if marca != "Genérico" and len(modelo) > 3:
            alvos.add((marca, modelo))

    # 1. Varre Inventário (Limpo)
    if os.path.exists(PASTA_EQUIPAMENTOS):
        for arq in os.listdir(PASTA_EQUIPAMENTOS):
            try:
                with open(os.path.join(PASTA_EQUIPAMENTOS, arq), 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                    for linha in conteudo.split('\n'):
                        if "MODELO TÉCNICO:" in linha:
                            processar_linha(linha.split(":")[1])
            except: pass

    # 2. Varre OSs (Sujo)
    if os.path.exists(PASTA_OS):
        for arq in os.listdir(PASTA_OS):
            try:
                with open(os.path.join(PASTA_OS, arq), 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                    for linha in conteudo.split('\n'):
                        if "EQUIPAMENTO:" in linha:
                            processar_linha(linha.split(":")[1])
            except: pass
            
    # Ordena alfabeticamente
    return sorted(list(alvos))

def baixar_pdf_real(url, nome_arquivo):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        r = requests.get(url, headers=headers, stream=True, timeout=15)
        
        ct = r.headers.get('Content-Type', '').lower()
        
        # Aceita PDF ou stream binário
        if r.status_code == 200 and ('pdf' in ct or 'octet-stream' in ct):
            caminho = os.path.join(PASTA_MANUAIS, nome_arquivo)
            with open(caminho, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            if os.path.getsize(caminho) < 5000: # < 5kb é erro
                os.remove(caminho)
                return False
            return True
    except:
        return False
    return False

def caçar_manuais():
    if not os.path.exists(PASTA_MANUAIS): os.makedirs(PASTA_MANUAIS)

    log = st.expander("📝 Log de Busca Detalhado", expanded=True)
    status = st.empty()
    
    lista_alvos = descobrir_equipamentos_alvo()
    status.info(f"📋 Lista de busca: {len(lista_alvos)} equipamentos identificados.")
    
    sucessos = 0
    ddgs = DDGS()

    for marca, modelo in lista_alvos:
        # Nome do arquivo seguro
        nome_safe = modelo.replace(' ', '_').replace('/', '-').replace('\\', '-')
        nome_arquivo = f"Manual_{marca}_{nome_safe}.pdf"
        
        if os.path.exists(os.path.join(PASTA_MANUAIS, nome_arquivo)):
            log.write(f"⏩ Já existe: **{modelo}**")
            continue

        log.markdown(f"🔎 **{marca} {modelo}**...")
        
        # Estratégia de Busca em Níveis
        queries = [
            f"{marca} {modelo} manual pdf",           # Busca 1: Específica
            f"{marca} {modelo} datasheet pdf",        # Busca 2: Datasheet
            f"{marca} {modelo.split()[0]} manual pdf" # Busca 3: Genérica (ex: só "AMT 2018")
        ]
        
        encontrou = False
        for q in queries:
            if encontrou: break
            try:
                # Tenta baixar dos primeiros resultados
                results = ddgs.text(q, region='br-pt', max_results=4)
                if not results: continue

                for r in results:
                    url = r['href']
                    if any(x in url for x in ['youtube', 'facebook', 'mercadolivre']): continue
                    
                    if baixar_pdf_real(url, nome_arquivo):
                        log.success(f"✅ Baixado: {modelo} (Fonte: {q})")
                        st.toast(f"Novo manual: {modelo}")
                        sucessos += 1
                        encontrou = True
                        break
            except Exception as e:
                print(f"Erro busca: {e}")
            
            time.sleep(1) # Respiro

        if not encontrou:
            log.error(f"❌ Não encontrado: {modelo}")

    if sucessos > 0:
        status.success(f"🎉 Finalizado! {sucessos} novos manuais salvos.")
    else:
        status.warning("Varredura finalizada. Nenhum novo manual encontrado desta vez.")

if __name__ == "__main__":
    caçar_manuais()