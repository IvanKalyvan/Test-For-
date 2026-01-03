from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SpecialistJournal(models.Model):
    _name = 'specialist.journal'
    _description = 'Specialist Journal Entry'
    _order = 'date desc'

    date = fields.Datetime(string='Date', default=fields.Datetime.now, required=True)
    specialist_id = fields.Many2one('res.users', string='Specialist', default=lambda self: self.env.user, required=True)
    partner_id = fields.Many2one('res.partner', string='Client', required=True, ondelete='cascade', index=True)
    content = fields.Html(string='Content', sanitize=False)
    template_ids = fields.Many2many('specialist.template', string='Applied Templates')

    @api.onchange('template_ids')
    def _onchange_template_ids(self):
        if not self.template_ids:
            return

        texts = [t.content or '' for t in self.template_ids]
        appended = '<br/><br/>'.join(texts)
        if self.content:

            if not self.content.endswith('<br/>') and not self.content.endswith('<br/>'):
                self.content = (self.content or '') + '<br/><br/>' + appended
            else:
                self.content = (self.content or '') + appended
        else:
            self.content = appended

    def write(self, vals):
        return super().write(vals)
