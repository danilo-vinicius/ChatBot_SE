import streamlit as st
from utils.cerebro_ia import carregar_conhecimento
import google.generativeai as genai
import os
import requests
from urllib.parse import unquote

st.set_page_config(page_title="Técnico SEIA | Brasfort", page_icon="🛡️")

st.title("🛡️ Técnico SEIA Brasfort")
st.caption("Base de conhecimento alimentada via API e Equipe SE.")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Sincronização")
    
    # Botão 1: Atualizar OSs (que já tínhamos)
    if st.button("🔄 Atualizar Base de OSs"):
        with st.spinner("Baixando novas OSs da API..."):
            from utils.sincronizar_api import baixar_e_salvar_os
            baixar_e_salvar_os()
            st.cache_resource.clear()
            st.success("Base de OSs atualizada!")
            
    # Botão 2: Atualizar Equipamentos (NOVO - Se você criou o script de equipamentos)
    if st.button("🏭 Atualizar Inventário"):
        with st.spinner("Baixando lista de equipamentos..."):
            from utils.sincronizar_equipamentos import baixar_equipamentos
            baixar_equipamentos()
            st.success("Inventário atualizado!")

    # Botão 3: Baixar Manuais (O QUE VOCÊ PEDIU AGORA)
    st.markdown("---")
    st.header("📚 Manuais Técnicos")
    if st.button("🔎 Baixar Manuais Faltantes"):
        with st.spinner("O Robô está caçando manuais no Google..."):
            from utils.baixar_manuais import caçar_manuais
            caçar_manuais()
            st.success("Busca finalizada!")

    st.markdown("---")
    st.header("🔗 Adicionar Manual via Link")
    
    # Campo para colar o link
    link_manual = st.text_input("Cole o link do PDF aqui:")
    
    if st.button("⬇️ Baixar e Aprender"):
        if len(link_manual) > 10:
            with st.spinner("Baixando arquivo..."):
                try:
                    # 1. Configura a pasta
                    pasta_manuais = "estudo_manuais"
                    if not os.path.exists(pasta_manuais):
                        os.makedirs(pasta_manuais)
                    
                    # 2. Tenta extrair um nome bonito do link
                    # Ex: .../Datasheet%20-%20iMHDX.pdf -> Datasheet - iMHDX.pdf
                    nome_arquivo = unquote(link_manual.split("/")[-1])
                    
                    # Se o nome não terminar em pdf, força a extensão
                    if not nome_arquivo.lower().endswith(".pdf"):
                        nome_arquivo += ".pdf"
                        
                    caminho_final = os.path.join(pasta_manuais, nome_arquivo)
                    
                    # 3. Baixa o arquivo (Fingindo ser um navegador para não ser bloqueado)
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                    response = requests.get(link_manual, headers=headers, timeout=15)
                    
                    if response.status_code == 200:
                        with open(caminho_final, "wb") as f:
                            f.write(response.content)
                        
                        st.success(f"✅ Sucesso! Manual salvo: {nome_arquivo}")
                        st.cache_resource.clear() # Limpa a memória para a IA ler o novo arquivo na próxima pergunta
                    else:
                        st.error(f"Erro ao baixar: Código {response.status_code}")
                        
                except Exception as e:
                    st.error(f"Erro: {e}")
        else:
            st.warning("Cole um link válido primeiro.")

# --- CARREGA MEMÓRIA ---
@st.cache_resource
def get_memoria():
    return carregar_conhecimento()

conhecimento = get_memoria()

# --- CHAT ---
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [{"role": "assistant", "content": "Olá! Pode descrever o problema ou colar seu rascunho. Vou consultar nosso histórico."}]

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escreva aqui..."):
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analisando histórico técnico..."):
            # Prompt de Mentor com Habilidade de Vídeo
            instrucao = f"""
            Você é o Supervisor Técnico Sênior da Brasfort (nível do Técnico Silvano).
            Sua base de conhecimento é HÍBRIDA: histórico de OSs reais e Manuais Técnicos.
            
            BASE DE CONHECIMENTO:
            {conhecimento[:30000]}
            
            SUA TAREFA:
            1. Responda a dúvida técnica com precisão, usando o histórico ou manuais.
            2. Se for um procedimento prático (instalação, configuração, manutenção), GERE UM LINK DE BUSCA DO YOUTUBE no final.
            
            COMO GERAR O LINK:
            - Crie uma URL de busca usando os termos técnicos principais.
            - Formato: https://www.youtube.com/results?search_query=TERMOS+TECNICOS
            - Exiba no texto assim: "🎥 [Ver vídeos sugeridos sobre XXXXX](URL_AQUI)"
            
            Exemplo: Se a dúvida for "resetar senha DVR Intelbras", gere:
            "🎥 [Ver vídeos sobre Reset Senha DVR Intelbras](https://www.youtube.com/results?search_query=reset+senha+dvr+intelbras)"
            
            MENSAGEM DO USUÁRIO:
            "{prompt}"
            """
            
            try:
                if "GOOGLE_API_KEY" in st.secrets:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel("gemini-flash-latest")
                    resp = model.generate_content(instrucao)
                    texto = resp.text
                else:
                    texto = "Erro: Chave de API não configurada."
                
                st.markdown(texto)
                st.session_state.mensagens.append({"role": "assistant", "content": texto})
            except Exception as e:
                st.error(f"Erro: {e}")