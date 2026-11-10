# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, AccessError


class TestAIThreads(TransactionCase):

    def test_01_conversation_and_message_persistence(self):
        """Validates conversation creation, message ordering, and token estimation."""
        conv = self.env['llm.conversation'].create({
            'name': 'ERP Inventory Inquiry',
            'user_id': self.env.user.id,
        })
        self.assertTrue(conv.id)

        msg_user = self.env['llm.message'].create({
            'conversation_id': conv.id,
            'role': 'user',
            'content': 'How many units of Product X are in stock?',
        })
        msg_ai = self.env['llm.message'].create({
            'conversation_id': conv.id,
            'role': 'assistant',
            'content': 'There are 42 units available in the main warehouse.',
        })

        self.assertEqual(len(conv.message_ids), 2)
        self.assertEqual(conv.message_ids[0].id, msg_user.id)
        self.assertEqual(conv.message_ids[1].id, msg_ai.id)
        self.assertGreater(msg_user.tokens_used, 0)
        self.assertGreater(msg_ai.tokens_used, 0)

    def test_02_rename_favorite_and_ownership_protection(self):
        """Validates renaming, toggling favorite, and ownership protection across users."""
        user_a = self.env['res.users'].create({
            'name': 'User A',
            'login': 'user_a_threads@example.com',
            'group_ids': [(6, 0, [self.env.ref('base.group_user').id])],
        })
        user_b = self.env['res.users'].create({
            'name': 'User B',
            'login': 'user_b_threads@example.com',
            'group_ids': [(6, 0, [self.env.ref('base.group_user').id])],
        })

        conv_a = self.env['llm.conversation'].with_user(user_a).create({
            'name': 'Original Title',
            'user_id': user_a.id,
        })

        # Toggle favorite
        self.assertFalse(conv_a.is_favorite)
        conv_a.with_user(user_a).action_toggle_favorite()
        self.assertTrue(conv_a.is_favorite)

        # Rename conversation
        conv_a.with_user(user_a).action_rename('Updated Thread Title')
        self.assertEqual(conv_a.name, 'Updated Thread Title')

        with self.assertRaises(UserError):
            conv_a.with_user(user_a).action_rename('   ')

        # User B cannot rename or delete User A's conversation
        with self.assertRaises(AccessError):
            conv_a.sudo().with_user(user_b).action_rename('Hijacked Title')
