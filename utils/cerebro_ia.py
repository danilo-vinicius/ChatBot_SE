import os
import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import random

# --- CONFIGURAÇÃO ---
# Adicione aqui todas as pastas que você quer que a IA leia
PASTAS_CONHECIMENTO = [
    "estudo_os",                  # Dados da API (Dia a dia)
    "estudo_manuais",             # Manuais e PDFs técnicos (Referência)
    "estudo_seguranca_eletronica" # A pasta que você mencionou
]

# Configura API
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel("gemini-flash-latest") 
    else:
        model = None
except:
    model = None

def ler_arquivo_pdf(caminho):
    """Extrai texto de um PDF"""
    texto = ""
    try:
        reader = PdfReader(caminho)
        # Lê até 10 páginas para não ficar gigante (ajuste conforme necessário)
        limit_paginas = min(len(reader.pages), 10)
        for i in range(limit_paginas):
            page = reader.pages[i]
            if page.extract_text():
                texto += page.extract_text() + "\n"
        return f"\n--- FONTE: {os.path.basename(caminho)} (PDF) ---\n{texto}\n"
    except Exception as e:
        print(f"Erro ao ler PDF {caminho}: {e}")
        return ""

def ler_arquivo_txt(caminho):
    """Extrai texto de um TXT"""
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return f"\n--- FONTE: {os.path.basename(caminho)} (TXT) ---\n{f.read()}\n"
    except Exception as e:
        print(f"Erro ao ler TXT {caminho}: {e}")
        return ""

def carregar_conhecimento():
    """Varre todas as pastas configuradas e monta a base de conhecimento."""
    texto_consolidado = ""
    total_arquivos = []

    # 1. Coleta todos os arquivos de todas as pastas
    for pasta in PASTAS_CONHECIMENTO:
        if os.path.exists(pasta):
            arquivos = [os.path.join(pasta, f) for f in os.listdir(pasta) if f.lower().endswith(('.pdf', '.txt'))]
            total_arquivos.extend(arquivos)
    
    if not total_arquivos:
        return ""

    # 2. Seleção Inteligente
    # Vamos pegar até 10 arquivos aleatórios para dar contexto variado
    # (O Gemini 1.5 Flash aguenta bastante texto, então aumentamos o limite)
    amostra = random.sample(total_arquivos, min(len(total_arquivos), 10))

    # 3. Leitura
    for caminho in amostra:
        if caminho.lower().endswith('.pdf'):
            texto_consolidado += ler_arquivo_pdf(caminho)
        elif caminho.lower().endswith('.txt'):
            texto_consolidado += ler_arquivo_txt(caminho)
            
    return texto_consolidado