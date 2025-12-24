import streamlit as st
from utils.cerebro_ia import carregar_conhecimento
import google.generativeai as genai

st.set_page_config(page_title="Mentor Técnico Brasfort", page_icon="🛡️")

st.title("🛡️ Mentor Técnico Brasfort")
st.caption("Base de conhecimento alimentada via API PerformanceLab.")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Sincronização")
    if st.button("🔄 Atualizar Base de Dados"):
        with st.spinner("Baixando novas OSs da API..."):
            # Importa e roda o script de sincronização na hora
            from utils.sincronizar_api import baixar_e_salvar_os
            baixar_e_salvar_os()
            st.cache_resource.clear() # Limpa a memória da IA para ler os novos arquivos
            st.success("Base atualizada com sucesso!")
    
    st.info("Clique acima para baixar as últimas OSs do sistema.")

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