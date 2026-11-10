# Odoo Community AI Assistant & Copilot (`odoo_community_ai`)

[![Odoo Version](https://img.shields.io/badge/Odoo-19.0%20Community-714B67?logo=odoo&logoColor=white)](https://www.odoo.com)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![OWL 2](https://img.shields.io/badge/Frontend-OWL%202-017E84)](https://github.com/odoo/owl)

> 🌍 **Languages / Idiomas:** [🇺🇸 English](#-english) | [🇧🇷 Português (BR)](#-português-br) | [🇪🇸 Español](#-español)

---

## 🇺🇸 English

**`odoo_community_ai`** brings Enterprise-grade Agentic AI, Voice Dictation, Multi-LLM Orchestration, and Computer Vision Form Drafting to **Odoo 19 Community Edition**. Designed under the *Single Responsibility Principle* and strict *Human-in-the-Loop* safety, it depends only on `base`, `web`, and `mail`, while dynamically introspecting optional modules (`sale`, `stock`, `account`, `hr`) when installed.

### Key Features
1. **Interactive Systray Drawer & Floating Action Button (OWL 2):**
   - Accessible from any screen in Odoo 19.
   - Persistent conversation threads (`llm.conversation` & `llm.message`) with real-time search, inline rename, favorites, and deletion.
   - **Native Voice Dictation ("Talk to Odoo"):** Built-in Web Speech API integration that automatically adapts to the user's browser language.
   - **Interactive Action Cards:** Suggests and opens pre-filled Odoo forms directly from the chat.
2. **Multi-Provider LLM Engine (`llm.config`):**
   - **100% Free & Private Local LLMs:** Native support for **Ollama** (`llama3.2`) and **LM Studio** (`qwen2.5-coder`).
   - **Cloud Providers:** **Google Gemini** (`gemini-3.5-flash`, `gemini-3.8-flash`), **OpenAI** (`gpt-4o-mini`, `gpt-4o`), **DeepSeek** (`deepseek-chat`, `deepseek-reasoner`), **Anthropic Claude**, and **MCP Proxy**.
   - One-click **Model Auto-Discovery** and connection tester with built-in **SSRF security validation**.
   - **Personal API Key per User (`res.users`):** Allows users to configure their own private API key while keeping global keys restricted to `AI Administrators`.
3. **AI Form Copilot Wizard (OCR & Vision):**
   - Upload photos or PDFs (business cards, invoices, product labels, resumes) to extract structured JSON via Vision LLMs.
   - Displays an HTML verification table and opens the official Odoo form pre-filled in **Draft mode** (*Human-in-the-Loop*).
4. **Extensible `@aitool` Framework (OCA Standard):**
   - Expose any Odoo ORM method to the AI Assistant using the `@aitool` decorator.

### Quick Start (Docker Compose)
```bash
git clone https://github.com/mailsonm/odoo-community-ai.git
cd odoo-community-ai
docker compose up -d
```
Then install **Odoo Community AI Assistant & Copilot** (`odoo_community_ai`) from the Apps menu.

---

## 🇧🇷 Português (BR)

O **`odoo_community_ai`** leva recursos de Inteligência Artificial Agêntica, Ditado por Voz, Orquestração Multi-LLM e Preenchimento de Formulários por Visão Computacional para o **Odoo 19 Community Edition**. Projetado com segurança *Human-in-the-Loop* estrita, depende apenas de `base`, `web` e `mail`, detectando automaticamente módulos opcionais (`sale`, `stock`, `account`, `hr`) quando instalados.

### Principais Funcionalidades
1. **Gaveta Lateral no Systray & Botão Flutuante (OWL 2):**
   - Acessível de qualquer tela do Odoo 19.
   - Histórico de conversas persistido com busca em tempo real, renomeação inline, favoritos com estrela e exclusão.
   - **Ditado por Voz Nativo ("Talk to Odoo"):** Integração com Web Speech API que detecta automaticamente o idioma do usuário.
   - **Action Cards Interativos:** Botões no chat que abrem formulários do Odoo pré-preenchidos.
2. **Motor Multiprovedor LLM (`llm.config`):**
   - **LLMs Locais (Custo Zero / 100% Privado):** Suporte nativo a **Ollama** (`llama3.2`) e **LM Studio** (`qwen2.5-coder`).
   - **Nuvem:** **Google Gemini** (`gemini-3.5-flash`, `gemini-3.8-flash`), **OpenAI** (`gpt-4o-mini`, `gpt-4o`), **DeepSeek**, **Anthropic Claude** e **MCP Proxy**.
   - Botão para **Auto-Descoberta de Modelos da API**, teste de conexão e proteção nativa contra **SSRF**.
   - **Chave Pessoal por Usuário (`res.users`):** Permite que cada usuário utilize sua própria cota de API com isolamento de segurança RBAC.
3. **AI Form Copilot Wizard (OCR & Visão Computacional):**
   - Envie fotos ou PDFs (cartões de visita, cabeçalhos de notas, rótulos de produtos, currículos) para extrair dados estruturados.
   - Confira o resumo em HTML e abra o formulário oficial do Odoo pré-preenchido em modo **Rascunho** (*Human-in-the-Loop*).
4. **Framework `@aitool` Extensível (Padrão OCA):**
   - Exponha qualquer método do ORM para a IA utilizando o decorator `@aitool`.

---

## 🇪🇸 Español

**`odoo_community_ai`** incorpora Inteligencia Artificial Agéntica, Dictado por Voz, Orquestación Multi-LLM y Relleno de Formularios por Visión Artificial a **Odoo 19 Community Edition**. Diseñado bajo el principio *Human-in-the-Loop*, depende únicamente de `base`, `web` y `mail`, detectando dinámicamente módulos adicionales (`sale`, `stock`, `account`, `hr`).

### Características Principales
1. **Panel Lateral en Systray y Botón Flotante (OWL 2):**
   - Gestión completa de conversaciones con búsqueda instantánea, renombrado en línea y favoritos.
   - **Dictado por Voz ("Talk to Odoo"):** Reconocimiento de voz nativo adaptable al idioma del navegador.
   - **Action Cards Interactivos:** Apertura de formularios de Odoo pre-rellenados directamente desde el chat.
2. **Orquestador Multi-Proveedor (`llm.config`):**
   - **Modelos Locales (Costo Cero / 100% Privado):** **Ollama** (`llama3.2`) y **LM Studio** (`qwen2.5-coder`).
   - **Nube:** **Google Gemini**, **OpenAI**, **DeepSeek**, **Anthropic Claude** y **MCP Proxy**.
   - Auto-detección de modelos, prueba de conexión y protección contra **SSRF**.
3. **AI Form Copilot Wizard (OCR y Visión):**
   - Extrae datos de fotos o PDFs (tarjetas comerciales, facturas, etiquetas, currículums) y abre el formulario oficial en modo **Borrador**.

---

## 👨‍💻 Author / Autor
- **Mailson Maia Alves** — [GitHub @mailsonm](https://github.com/mailsonm)
- **License:** LGPL-3.0
