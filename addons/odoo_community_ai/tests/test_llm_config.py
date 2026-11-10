# -*- coding: utf-8 -*-
from unittest.mock import patch, MagicMock
from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError, ValidationError
from odoo.addons.odoo_community_ai.controllers.main import OdooCommunityAIController


class TestLLMConfig(TransactionCase):

    def test_01_llm_config_creation_and_default_switch(self):
        """Validates LLM configuration creation and single active default enforcement."""
        Config = self.env['llm.config']
        cfg1 = Config.create({
            'name': 'Gemini Cloud Test',
            'provider': 'gemini',
            'model_name': 'gemini-3.5-flash',
            'is_default': True,
        })
        cfg2 = Config.create({
            'name': 'Ollama Local Test',
            'provider': 'ollama',
            'model_name': 'llama3.2',
            'is_default': False,
        })

        self.assertTrue(cfg1.is_default)
        self.assertFalse(cfg2.is_default)

        cfg2.action_set_as_default()
        self.assertTrue(cfg2.is_default)
        cfg1.invalidate_recordset()
        self.assertFalse(cfg1.is_default)

        active = Config.get_active_config()
        self.assertEqual(active.id, cfg2.id)

    def test_02_ssrf_protection_on_api_base_url(self):
        """Validates that cloud metadata IP addresses and invalid URL schemes are blocked."""
        Config = self.env['llm.config']

        with self.assertRaises(ValidationError):
            Config.create({
                'name': 'Malicious SSRF Metadata',
                'provider': 'openai',
                'api_base_url': 'http://169.254.169.254/latest/meta-data/',
                'model_name': 'gpt-4o-mini',
            })

        with self.assertRaises(ValidationError):
            Config.create({
                'name': 'Invalid Scheme FTP',
                'provider': 'openai',
                'api_base_url': 'ftp://api.openai.com/v1',
                'model_name': 'gpt-4o-mini',
            })

    def test_03_api_key_security_and_personal_key_override(self):
        """Validates that regular users cannot read global api_key or modify another user's personal key."""
        group_user = self.env.ref('odoo_community_ai.group_ai_user')
        regular_user = self.env['res.users'].create({
            'name': 'Regular AI Operator',
            'login': 'regular_ai_operator@example.com',
            'email': 'regular_ai_operator@example.com',
            'group_ids': [(6, 0, [group_user.id, self.env.ref('base.group_user').id])],
        })

        config = self.env['llm.config'].create({
            'name': 'Global Confidential Gemini',
            'provider': 'gemini',
            'api_key': 'AIzaSyGlobalSecretKey999',
            'model_name': 'gemini-3.5-flash',
            'is_default': True,
        })

        # Regular user cannot read api_key directly
        with self.assertRaises(AccessError):
            config.with_user(regular_user).read(['name', 'api_key'])

        # Regular user cannot create or modify global LLM config
        with self.assertRaises(AccessError):
            self.env['llm.config'].with_user(regular_user).create({
                'name': 'Unauthorized Config',
                'provider': 'ollama',
                'model_name': 'llama3.2',
            })

        # Effective key falls back to global key via internal sudo
        effective = self.env['llm.config'].with_user(regular_user)._get_effective_api_key()
        self.assertEqual(effective, 'AIzaSyGlobalSecretKey999')

        # Regular user sets their own personal key
        regular_user.with_user(regular_user).write({
            'ai_use_personal_key': True,
            'ai_personal_api_key': 'AIzaSyPersonalUserKey111',
        })
        effective_personal = self.env['llm.config'].with_user(regular_user)._get_effective_api_key()
        self.assertEqual(effective_personal, 'AIzaSyPersonalUserKey111')

    def test_04_mocked_multi_provider_dispatch_and_auto_discovery(self):
        """Validates provider HTTP adapters and model auto-discovery using isolated HTTP mocks."""
        controller = OdooCommunityAIController()
        messages = [{'role': 'user', 'content': 'Hello Odoo AI'}]

        # 1. Mock Gemini
        gemini_cfg = self.env['llm.config'].create({
            'name': 'Mock Gemini',
            'provider': 'gemini',
            'api_key': 'fake-gemini-key',
            'model_name': 'gemini-3.5-flash',
        })
        with patch('odoo.addons.odoo_community_ai.controllers.main.requests.post') as mock_post:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {
                'candidates': [{'content': {'parts': [{'text': 'Hello from Gemini Mock'}]}}],
            }
            mock_post.return_value = mock_resp
            reply = controller._call_provider(gemini_cfg, messages)
            self.assertEqual(reply, 'Hello from Gemini Mock')

        # 2. Mock OpenAI-compatible (Ollama / LM Studio / OpenAI / DeepSeek)
        ollama_cfg = self.env['llm.config'].create({
            'name': 'Mock Ollama',
            'provider': 'ollama',
            'api_base_url': 'http://localhost:11434/v1',
            'model_name': 'llama3.2',
        })
        with patch('odoo.addons.odoo_community_ai.controllers.main.requests.post') as mock_post:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {
                'choices': [{'message': {'content': 'Hello from Ollama Mock'}}],
            }
            mock_post.return_value = mock_resp
            reply = controller._call_provider(ollama_cfg, messages)
            self.assertEqual(reply, 'Hello from Ollama Mock')

        # 3. Mock Auto-Discovery (action_fetch_models)
        with patch('odoo.addons.odoo_community_ai.models.llm_config.requests.get') as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {
                'models': [{'name': 'llama3.3-70b'}, {'name': 'qwen2.5-coder'}],
            }
            mock_get.return_value = mock_resp
            ollama_cfg.action_fetch_models()
            self.assertEqual(ollama_cfg.model_name, 'llama3.3-70b')
            self.assertIn('qwen2.5-coder', ollama_cfg.compatible_models_json)
