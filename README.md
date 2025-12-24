# 📝 Gerador de Relatórios Operacionais - Brasfort

Sistema automatizado para geração de relatórios técnicos e operacionais em PDF. Desenvolvido para padronizar a identidade visual, agilizar o preenchimento de dados e automatizar cálculos de ocorrências.

## 🚀 Funcionalidades

O sistema possui uma arquitetura modular que suporta atualmente três tipos de relatórios:

### 1. Ocorrência LPR (Leitura de Placa)
* **Cálculo Automático:** Calcula o "Delta T" (tempo decorrido) entre a chegada do veículo, leitura da placa e abertura do portão.
* **Evidências:** Organização automática das 3 fotos (Chegada, Leitura, Abertura).
* **Análise:** Destaca em vermelho se o tempo exceder o padrão.

### 2. Laudo de Avaria de Equipamento
* **Estrutura Técnica:** Campos para N/S, defeito relatado e diagnóstico.
* **Conclusão Visual:** Destaque automático para diagnósticos de "Troca Imediata".
* **Foto:** Espaço para evidência fotográfica da avaria ou etiqueta.

### 3. Vistoria Técnica / Levantamento
* **Checklist:** Campo de texto livre que se converte automaticamente em tópicos (bullet points) no PDF.
* **Galeria de Fotos:** Suporte para upload múltiplo de imagens do local, gerando páginas extras conforme necessário.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **[Streamlit](https://streamlit.io/):** Interface web interativa e rápida.
* **[FPDF2](https://py-pdf.github.io/fpdf2/):** Geração e desenho dos PDFs pixel-perfect.

---

## 📂 Estrutura do Projeto

```text
/projeto_relatorios
│
├── app.py                  # Arquivo principal (Menu e Roteamento)
├── requirements.txt        # Lista de dependências
├── README.md               # Documentação
│
├── modules/                # Módulos de cada relatório
│   ├── __init__.py
│   ├── lpr.py              # Lógica do relatório LPR
│   ├── equipamento.py      # Lógica do laudo de equipamento
│   └── visita.py           # Lógica da vistoria técnica
│
├── utils/                  # Utilitários globais
│   └── brasfort_pdf.py     # Classe Base (Header, Footer, Fontes)
│
└── assets/                 # Recursos estáticos
    ├── logo.png (ou .svg)  # Logotipo da empresa
    └── fonts/              # Fontes obrigatórias
        ├── Barlow-Regular.ttf
        └── Barlow-Bold.ttf
```

## ⚙️ Instalação e Uso
### 1. Pré-requisitos
Certifique-se de ter o Python instalado. Recomenda-se o uso de um ambiente virtual.

### 2. Instalação das dependências
No terminal, execute:

```Bash
pip install -r requirements.txt
```
### 3. Configuração de Assets
Para que o PDF seja gerado corretamente com a identidade visual:

* Crie uma pasta assets/fonts/.

* Baixe a fonte Barlow (Regular e Bold) e coloque na pasta.

* Coloque o logo da empresa em assets/logo.png (ou .svg).

### 4. Executando a Aplicação
Rode o comando abaixo na raiz do projeto:

```Bash
streamlit run app.py
```
O navegador abrirá automaticamente com a interface.

## 🎨 Personalização
Toda a identidade visual (Cabeçalho, Rodapé, Fontes) está centralizada no arquivo: utils/brasfort_pdf.py

Alterando este único arquivo, todos os módulos de relatório serão atualizados automaticamente.
