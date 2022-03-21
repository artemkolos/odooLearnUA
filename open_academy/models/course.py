# -*- coding: utf-8 -*-
from odoo import models, fields, _

class course(models.Model):
     _name = 'open_academy.course'
     _description = 'open_academy.course'

     name = fields.Char()
     description = fields.Text()
     sessions = fields.One2many('open_academy.sessions',_('course'))
     responsible = fields.Many2one('res.users',string=_("Responsible"))

     _sql_constraints = [
          ('check_nameAnddescription',
           'CHECK(name != description)',
           _("The name should not equal the description")),

          ('check_uniqName',
           'UNIQUE(name)',
           _("Course title must be unique")),]


