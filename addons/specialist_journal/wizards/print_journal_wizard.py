from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SpecialistJournalReportWizard(models.TransientModel):
    _name = 'specialist.journal.report.wizard'
    _description = 'Wizard to print Specialist Journal for partner'

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    all_entries = fields.Boolean(string='All entries', default=True)
    date_from = fields.Date(string='Date from')
    date_to = fields.Date(string='Date to')

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for rec in self:
            if rec.date_from and rec.date_to and rec.date_from > rec.date_to:
                raise UserError(_('Date from must be earlier than Date to.'))

    def _get_domain(self):
        self.ensure_one()
        domain = [('partner_id', '=', self.partner_id.id)]
        if not self.all_entries:
            if not (self.date_from and self.date_to):
                raise UserError(_('Please set both Date from and Date to, or select All entries.'))

            domain += [('date', '>=', self.date_from), ('date', '<=', self.date_to + ' 23:59:59')]
        return domain

    def action_print_journal(self):
        self.ensure_one()

        if self.all_entries:
            domain = [('partner_id', '=', self.partner_id.id)]
        else:
            if not (self.date_from and self.date_to):
                raise UserError(_('Для печати по периоду укажите оба значения — с и по.'))
            domain = [
                ('partner_id', '=', self.partner_id.id),
                ('date', '>=', fields.Datetime.to_string(fields.Datetime.from_string(str(self.date_from)))),
                ('date', '<=', fields.Datetime.to_string(fields.Datetime.from_string(str(self.date_to)) + fields.Datetime.timedelta(days=1) - fields.Datetime.timedelta(seconds=1))) if False else ('date', '>=', self.date_from)
            ]

        if self.all_entries:
            entries = self.env['specialist.journal'].search([('partner_id', '=', self.partner_id.id)], order='date desc')
        else:

            dt_from = '%s 00:00:00' % self.date_from
            dt_to = '%s 23:59:59' % self.date_to
            entries = self.env['specialist.journal'].search([('partner_id', '=', self.partner_id.id),
                                                             ('date', '>=', dt_from),
                                                             ('date', '<=', dt_to)],
                                                            order='date desc')
        if not entries:
            raise UserError(_('No journal entries found for the selected partner and period.'))

        return self.env.ref('specialist_journal.action_report_journal').report_action(self)
