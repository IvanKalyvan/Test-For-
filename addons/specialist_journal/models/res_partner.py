from odoo import models, fields

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    specialist_journal_ids = fields.One2many('specialist.journal', 'partner_id', string='Specialist Journal')
