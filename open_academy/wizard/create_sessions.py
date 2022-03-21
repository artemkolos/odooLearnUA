
from odoo import models, fields, _

class CreateSessionsWizard(models.TransientModel):
    _name = 'create.sessions.wizard'
    _description = _('Create sessions wizard')

    def default_session(self):
        return self.env['open_academy.sessions'].browse(self._context.get('active_id'))

    session = fields.Many2many('open_academy.sessions',
        string=_("Session"), required=True, default=default_session)
    attendee = fields.Many2many('res.partner', string=_("Attendees"))

    def subscribe(self):
        for el_session in self.session:
            el_session.attendees |= self.attendee

        # print(self.session.attendee)
        # self.session.attendees |= self.attendee
        # return {}
