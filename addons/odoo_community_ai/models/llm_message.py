# -*- coding: utf-8 -*-
from odoo import models, fields, api


class LLMMessage(models.Model):
    _name = 'llm.message'
    _description = 'AI Assistant Message'
    _order = 'create_date asc, id asc'

    conversation_id = fields.Many2one(
        'llm.conversation',
        string='Conversation',
        required=True,
        ondelete='cascade',
        index=True
    )
    role = fields.Selection([
        ('system', 'System'),
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ], string='Role', required=True)
    content = fields.Text(string='Content', required=True)
    create_date = fields.Datetime(string='Created On', readonly=True)
    tokens_used = fields.Integer(string='Estimated Tokens', help='Approximate token count for this message.')

    @api.model_create_multi
    def create(self, vals_list):
        """Calculates approximate token usage upon message creation (~4 characters per token)."""
        for vals in vals_list:
            if 'content' in vals and vals['content']:
                vals['tokens_used'] = max(1, len(vals['content']) // 4)
        return super().create(vals_list)
