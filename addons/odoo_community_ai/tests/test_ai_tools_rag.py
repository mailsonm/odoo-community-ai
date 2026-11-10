# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.addons.odoo_community_ai.controllers.main import OdooCommunityAIController


class TestAIToolsRAG(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Global Tech Solutions Ltd',
            'email': 'contact@globaltech.example.com',
            'phone': '+1 800-555-0199',
            'is_company': True,
        })

    def test_01_search_partners_tool(self):
        """Validates execution of the OCA @aitool search_partners method."""
        AiTool = self.env['ai.tool']
        res = AiTool.action_tool_search_partners(query='Global Tech')
        self.assertTrue(res.get('success'))
        self.assertGreaterEqual(res.get('count', 0), 1)
        found = any(p['id'] == self.partner.id for p in res.get('partners', []))
        self.assertTrue(found)

    def test_02_business_insights_and_rag_search(self):
        """Validates real-time business insights and RAG search on res.partner."""
        controller = OdooCommunityAIController()
        insights = controller._search_business_insights(self.env, "How many contacts do we have?")
        self.assertIn("Contacts Registry", insights)

        rag = controller._rag_search(self.env, "Tell me about Global Tech Solutions")
        self.assertIn("Global Tech Solutions Ltd", rag)
