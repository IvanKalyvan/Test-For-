from odoo import models, fields

class SpecialistTemplate(models.Model):
    _name = 'specialist.template'
    _description = 'Journal Template'

    name = fields.Char(string='Title', required=True)
    content = fields.Html(string='Content', sanitize=False)
    active = fields.Boolean(default=True)
