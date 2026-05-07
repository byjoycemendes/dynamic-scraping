# WebScrapper FrenquLab - Dynamic Scraping Analyzer

Este projeto é um webscraper desenvolvido para analisar e interagir com páginas protegidas por **hCaptcha**, utilizando uma abordagem de **Scraping Dinâmico** com automação de navegador e interceptação de tráfego HTTP.

## 🚀 Objetivo
Criar um webscrapper capaz de acessar a página protegida `https://frenqulabi.com/ig/atlas`, analisar o fluxo anti-bot implementado via hCaptcha e identificar ferramentas capazes de concluir as etapas de defesa.

## 🛠 Tecnologias e Ferramentas
- **Python 3.12+**: Linguagem principal do projeto.
- **Playwright**: Framework de automação de navegadores modernos.
- **Playwright Stealth**: Técnicas de evasão básica de automação.
- **Chromium**: Navegador utilizado na automação.
- **Tracing do Playwright**: Captura visual e temporal da execução.
- **POO (Programação Orientada a Objetos)**: Arquitetura baseada em classes e separação de responsabilidades.

## 🏗 Arquitetura do Projeto
A solução foi dividida em módulos simples e organizados para facilitar manutenção, debugging e análise do fluxo:

1. **`main.py`**
   - Orquestração da execução;
   - Criação da sessão inicial;
   - Navegação até rota protegida;
   - Geração de screenshot;
   - Controle do fluxo principal.

2. **`browser.py`**
   - Inicialização do navegador;
   - Configuração do contexto;
   - Aplicação de Stealth;
   - Configuração de locale/timezone;
   - Geração de tracing.

3. **`monitor.py`**
   - Interceptação de requests;
   - Interceptação de responses;
   - Captura de headers;
   - Captura de payloads POST;
   - Persistência de respostas em JSON.


   A execução do scraper gera automaticamente:

- **`trace.zip`**
  - Trace completo da execução do navegador;
  - Timeline;
  - Screenshots;
  - Requests;
  - DOM snapshots.

- **`resultado.png`**
  - Screenshot final da página.

- **`responses.json`**
  - Persistência das responses interceptadas;
  - Headers;
  - Payloads relevantes.

## 🔍 Fluxo Identificado
Durante a análise do ambiente protegido, foi possível mapear o seguinte fluxo do hCaptcha:

1. Criação da sessão inicial;
2. Carregamento do `api.js`;
3. Execução do endpoint `checksiteconfig`;
4. Carregamento do script `hsw.js`;
5. Execução do endpoint `getcaptcha`;
6. Renderização dinâmica do challenge;
7. Carregamento das imagens do captcha.

Além disso, foram identificados:
- headers específicos;
- cookies de sessão;
- assets do challenge;
- endpoints internos do hCaptcha;
- fluxo de renderização dinâmica.

## ⚙️ Configuração

1.  Crie um ambiente virtual: `python -m venv venv`
2.  Ative o ambiente e instale as dependências: `pip install -r requirements.txt`

## 📈 Análises e Sugestões
Foi um prazer atuar com esse projeto e suas sugestões de melhoria são muito bem-vindas!
