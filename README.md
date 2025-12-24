markdown
# 🛡️ ChatBot Técnico - Brasfort (Mentor Virtual)

> Assistente de Inteligência Artificial para suporte técnico, formalização de relatórios e consulta de base de conhecimento.

O **ChatBot SE** é uma aplicação web desenvolvida em **Python** com **Streamlit**, que utiliza a IA do **Google Gemini (Flash)** para auxiliar a equipe técnica da Brasfort. Ele funciona como um "Mentor Virtual", utilizando RAG (Retrieval-Augmented Generation) para consultar manuais técnicos e histórico de Ordens de Serviço reais.

---

## 🚀 Funcionalidades

* **✍️ Formalização de Texto:** Transforma relatos informais (ex: "fio solto", "bateria arriada") em textos técnicos padronizados para relatórios.
* **🧠 Base de Conhecimento Híbrida:**
    * Lê **Manuais Técnicos (PDF)** para responder dúvidas de especificação e configuração.
    * Lê **Histórico de OSs (TXT)** para sugerir soluções baseadas em problemas passados.
* **🔄 Sincronização Automática:** Conecta-se à API da **PerformanceLab** para baixar e aprender com as novas Ordens de Serviço fechadas pela equipe.
* **📱 Mobile-First:** Interface otimizada para uso em celulares via navegador.

---

## 🛠️ Tecnologias Utilizadas

* [Streamlit](https://streamlit.io/) - Interface Web
* [Google Generative AI](https://ai.google.dev/) - Modelo Gemini 1.5 Flash
* [PyPDF](https://pypi.org/project/pypdf/) - Leitura de arquivos PDF
* [Requests](https://pypi.org/project/requests/) - Integração com API REST

---

## 📂 Estrutura do Projeto

```text
/ChatBot_SE
│
├── app.py                  # Aplicação Principal (Frontend)
├── requirements.txt        # Lista de dependências
│
├── utils/
│   ├── cerebro_ia.py       # Lógica de leitura de arquivos e montagem de contexto
│   └── sincronizar_api.py  # Script que baixa OSs da API PerformanceLab
│
├── estudo_os/              # Pasta onde ficam as OSs (TXT) baixadas automaticamente
└── estudo_manuais/         # Pasta para colocar Manuais (PDF) manualmente

```

---

## 📦 Instalação e Execução Local

Se você quiser rodar o projeto no seu computador:

1. **Clone o repositório:**
```bash
git clone [https://github.com/danilo-vinicius/ChatBot_SE.git](https://github.com/danilo-vinicius/ChatBot_SE.git)
cd ChatBot_SE

```


2. **Instale as dependências:**
```bash
pip install -r requirements.txt

```


3. **Configure a Chave de API:**
* Crie uma pasta chamada `.streamlit` na raiz.
* Crie um arquivo `secrets.toml` dentro dela.
* Cole sua chave do Google AI Studio:
```toml
GOOGLE_API_KEY = "Sua-Chave-AIza-Aqui..."

```




4. **Execute o sistema:**
```bash
streamlit run app.py

```



---

## ☁️ Deploy (Streamlit Community Cloud)

Este projeto está configurado para rodar na nuvem do Streamlit.

1. Suba o código para o GitHub.
2. Conecte sua conta no [share.streamlit.io](https://share.streamlit.io).
3. Crie um novo App apontando para este repositório.
4. **Importante:** Nas configurações do App na nuvem, vá em **Settings > Secrets** e adicione a `GOOGLE_API_KEY` manualmente, pois ela não é enviada para o GitHub por segurança.

---

## 🔄 Como Atualizar a Base de Conhecimento

### 1. Histórico de OSs (Automático)

No menu lateral do aplicativo, clique no botão **"🔄 Atualizar Base de Dados"**.

* O sistema irá conectar na API da PerformanceLab.
* Baixará as últimas OSs com solução técnica preenchida.
* Salvará arquivos `.txt` na pasta `estudo_os`.
* A IA aprenderá o novo conteúdo imediatamente.

### 2. Manuais Técnicos (Manual)

Para ensinar a IA sobre um novo equipamento:

1. Baixe o PDF do manual.
2. Coloque o arquivo na pasta `estudo_manuais` localmente.
3. Faça o **Commit** e **Push** para o GitHub.
4. O Streamlit Cloud atualizará automaticamente.

---

## 📝 Licença e Autoria

Desenvolvido para uso interno da **Brasfort Segurança Eletrônica**.

* **Desenvolvedor:** Danilo Vinícius Bastos Torres
* **Foco:** Otimização de processos técnicos e gestão do conhecimento.