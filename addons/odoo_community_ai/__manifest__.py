# -*- coding: utf-8 -*-
{
    'name': 'Odoo Community AI Assistant & Copilot',
    'version': '19.0.1.0.0',
    'category': 'Productivity/AI',
    'summary': 'Interactive AI Assistant Drawer, Multi-LLM Orchestrator, Voice Dictation, and Human-in-the-Loop Form Copilot for Odoo 19 Community.',
    'description': """
Odoo Community AI Assistant & Copilot
=====================================
Open-source agentic AI suite designed to bring Enterprise-grade AI capabilities to Odoo 19 Community Edition:
- Interactive Systray Drawer and Floating Action Button (FAB) built with OWL 2.
- Native Voice Dictation ("Talk to Odoo") via Web Speech API with automatic user language detection.
- Multi-Provider LLM support: Local (Ollama, LM Studio) and Cloud (Google Gemini, OpenAI, DeepSeek, Anthropic Claude, MCP Proxy).
- AI Form Copilot Wizard: Extract structured data from images/PDFs (Vision/OCR) and open pre-filled Odoo forms in draft mode (Human-in-the-Loop).
- Extensible OCA @aitool framework for real-time PostgreSQL ORM RAG (Contacts, Inventory, Sales, Invoicing).
- Strict RBAC security, SSRF protection, and per-user conversation isolation.
    """,
    'author': 'Mailson Maia Alves',
    'website': 'https://github.com/mailsonm/odoo-community-ai',
    'depends': [
        'base',
        'web',
        'mail',
    ],
    'data': [
        'security/ai_security.xml',
        'security/ir.model.access.csv',
        'security/ir_rule_data.xml',
        'data/llm_default_config.xml',
        'data/ai_tools_data.xml',
        'wizard/ai_form_copilot_wizard_views.xml',
        'views/llm_config_views.xml',
        'views/llm_conversation_views.xml',
        'views/ai_tool_views.xml',
        'views/res_users_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'odoo_community_ai/static/src/js/ai_assistant_systray.js',
            'odoo_community_ai/static/src/js/ai_assistant_drawer.js',
            'odoo_community_ai/static/src/xml/ai_assistant_templates.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
