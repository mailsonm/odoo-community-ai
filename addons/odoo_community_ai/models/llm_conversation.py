# -*- coding: utf-8 -*-
from odoo import models, fields, _
from odoo.exceptions import UserError, AccessError


class LLMConversation(models.Model):
    _name = 'llm.conversation'
    _description = 'AI Assistant Conversation Thread'
    _order = 'is_favorite desc, write_date desc, id desc'

    name = fields.Char(string='Title', required=True, default='New Conversation')
    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user,
        required=True,
        ondelete='cascade',
        index=True
    )
    message_ids = fields.One2many('llm.message', 'conversation_id', string='Messages')
    is_favorite = fields.Boolean(string='Favorite', default=False)
    create_date = fields.Datetime(string='Created On', readonly=True)
    write_date = fields.Datetime(string='Last Activity', readonly=True)

    def action_rename(self, new_name):
        """Renames the conversation ensuring only the owner or system administrator can modify it."""
        self.ensure_one()
        if not new_name or not new_name.strip():
            raise UserError(_("The conversation title cannot be empty."))
        if self.user_id != self.env.user and not self.env.user.has_group('base.group_system'):
            raise AccessError(_("You can only rename your own conversations."))
        self.write({'name': new_name.strip()})
        return True

    def action_toggle_favorite(self):
        """Toggles the favorite status of the conversation."""
        self.ensure_one()
        if self.user_id != self.env.user and not self.env.user.has_group('base.group_system'):
            raise AccessError(_("You can only mark your own conversations as favorite."))
        self.write({'is_favorite': not self.is_favorite})\
        return self.is_favorite

    def action_delete_conversation(self):
        """Deletes the conversation and its messages after verifying ownership."""
        self.ensure_one()
        if self.user_id != self.env.user and not self.env.user.has_group('base.group_system'):
            raise AccessError(_("You can only delete your own conversations."))
        self.unlink()
        return True
