from odoo import models, fields, api,_
from datetime import date, timedelta
from odoo.exceptions import ValidationError

class sessions(models.Model):
     _name = 'open_academy.sessions'
     _description = 'open_academy.sessions'

     # responsibleUser = fields.Char()
     name = fields.Char(string=_("Name"))
     responsibleUser = fields.Many2one('res.users',string=_("Responsible user"))
     instructor = fields.Many2one('res.partner',string=_("Instructor"), domain=['|',('instructor', '=', True),('category_id.name', 'ilike', 'Teacher')])
     course = fields.Many2one('open_academy.course',string=_("Course"))
     attendees = fields.Many2many('res.partner',string=_("Attendees"))
     seatsNumber = fields.Integer(string=_("Number of seats"))
     busySeatsPercent = fields.Float(compute='compute_seats', string=_("Busy seats(%)"))
     start_date = fields.Date(string=_("Start date"),default=date.today())
     active = fields.Boolean(string=_("Active"),default=True)
     duration = fields.Integer(string=_("Duration"))
     end_date = fields.Date(string=_("End Date"), compute='compute_end_date', store=True)
     color = fields.Integer()

     @api.depends('start_date', 'duration')
     def compute_end_date(self):
          if not self.duration:
               self.end_date = self.start_date
          else:
               self.end_date = self.start_date + timedelta(days=self.duration)

     @api.depends('seatsNumber', 'attendees')
     def compute_seats(self):
          for r in self:
               if not r.seatsNumber:
                    r.busySeatsPercent = 0.0
               else:
                    r.busySeatsPercent = 100.0 * len(r.attendees) / r.seatsNumber

     @api.onchange('seatsNumber', 'attendees')
     def check_seatNumber(self):
          if self.seatsNumber < 0:
               return {
                    'warning': {
                         'title': "Error",
                         'message': _("Seats number cannot be less than zero 0"),
                    },
               }
          if self.seatsNumber < len(self.attendees):
               return {
                    'warning': {
                         'title': "Error",
                         'message': _("Seats number cannot be less than attendees"),
                    },
               }

     @api.constrains('attendees','instructor')
     def check_instructor(self):
          if self.instructor in self.attendees:
               raise ValidationError(_("Instructor cannot be in attendees"))



class partnerInherit(models.Model):
     _inherit = 'res.partner'

     sessions = fields.One2many('open_academy.sessions',_('instructor'))
     instructor = fields.Boolean()
