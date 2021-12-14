from odoo import _, api, fields, models


class ModuleCat(models.Model):
    _name = 'drive.cat'
    _description = 'New Description'

    name = fields.Char(string='name')
