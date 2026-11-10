# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class ResUsers(models.Model):
    _inherit = 'res.users'

    ai_use_personal_key = fields.Boolean(
        string='Use My Personal AI API Key',
        default=False,
        groups='base.group_user',
        help='Enable to use your own private API key instead of the shared company quota.'
    )
    ai_personal_api_key = fields.Char(
        string='My Personal AI API Key',
        groups='base.group_user',
        help='Personal API key for the AI Assistant. Your queries will use your private quota.'
    )

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ['ai_personal_api_key', 'ai_use_personal_key']

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ['ai_personal_api_key', 'ai_use_personal_key']

    def _is_ai_admin(self):
        return bool(
            self.env.su
            or self.env.is_admin()
            or self.env.user.has_group('odoo_community_ai.group_ai_admin')
        )

    def write(self, vals):
        """Ensures regular users can only modify their own personal AI API key."""
        if 'ai_personal_api_key' in vals or 'ai_use_personal_key' in vals:
            if not self._is_ai_admin():
                if any(u.id != self.env.uid for u in self):
                    raise AccessError(_("Access denied: you cannot modify another user's personal AI API key."))
        return super().write(vals)

    def read(self, fields=None, load='_classic_read'):
        """Masks other users' personal API keys for non-administrators."""
        res = super().read(fields=fields, load=load)
        if fields and 'ai_personal_api_key' in fields and not self._is_ai_admin():
            for record in res:
                if record.get('id') != self.env.uid:
                    record['ai_personal_api_key'] = False
        return res

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        """Masks other users' personal API keys in batch searches for non-administrators."""
        res = super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)
        if fields and 'ai_personal_api_key' in fields and not self._is_ai_admin():
            for record in res:
                if record.get('id') != self.env.uid:
                    record['ai_personal_api_key'] = False
        return res
