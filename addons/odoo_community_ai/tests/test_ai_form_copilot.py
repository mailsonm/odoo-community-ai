# -*- coding: utf-8 -*-
import base64
import json
from odoo.tests.common import TransactionCase
from odoo.addons.odoo_community_ai.controllers.main import OdooCommunityAIController


class TestAIFormCopilot(TransactionCase):

    def test_01_copilot_wizard_json_parsing_and_draft_action(self):
        """Validates JSON extraction, HTML summary generation, and draft form action."""
        wizard = self.env['ai.form.copilot.wizard'].create({
            'target_model': 'res.partner',
            'document_image': base64.b64encode(b'fakeimagebytes'),
            'image_filename': 'business_card.jpg',
        })
        self.assertEqual(wizard.state, 'draft')

        prompts = wizard._get_copilot_model_prompts()
        self.assertIn('res.partner', prompts)

        sample_json = """
        ```json
        {
          "name": "Acme Innovation Corp",
          "vat": "US-99887766",
          "email": "hello@acme.example.com",
          "phone": "+1 415-555-0100",
          "is_company": true
        }
        ```
        """
        parsed = wizard._clean_and_parse_json(sample_json)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.get('name'), 'Acme Innovation Corp')

        summary_html = wizard._build_summary_html(parsed)
        self.assertIn('Acme Innovation Corp', summary_html)

        wizard.write({
            'state': 'extracted',
            'extracted_json': json.dumps(parsed),
            'extracted_summary': summary_html,
        })

        action = wizard.action_apply_to_form()
        self.assertEqual(action.get('res_model'), 'res.partner')
        self.assertEqual(action.get('context', {}).get('default_name'), 'Acme Innovation Corp')
        self.assertTrue(action.get('context', {}).get('default_is_company'))

    def test_02_action_card_extraction_in_controller(self):
        """Validates extraction of interactive Action Cards from LLM responses."""
        controller = OdooCommunityAIController()
        reply_with_card = """
        Here is the draft contact ready for review:
        ```json
        {
          "copilot_form": "res.partner",
          "action_label": "Open Customer Draft",
          "data": {
            "name": "Wayne Enterprises",
            "phone": "+1 212-555-0144"
          }
        }
        ```
        """
        card = controller._extract_action_card(reply_with_card)
        self.assertIsNotNone(card)
        self.assertEqual(card.get('model'), 'res.partner')
        self.assertEqual(card.get('defaults', {}).get('name'), 'Wayne Enterprises')
        self.assertEqual(card.get('label'), 'Open Customer Draft')
