# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class ModuleName(models.Model):
    _inherit = "sale.order.line"

    fname = fields.Char(string="First name:")
    lname = fields.Char(string="Last name:")
    saddress = fields.Char(string="Street Address ")
    city = fields.Char(string="City ")
    state_province = fields.Char(string="State / Province ")
    zip_pc = fields.Char(string="ZIP / Postal Code ")
    country_id = fields.Many2one(
        string="Country", comodel_name="res.country", help="Country"
    )
    birth = fields.Date(string="Date of birth:")
    your_photo = fields.Binary(string="Your photo")
    country_birth = fields.Many2one(
        string="Country of birth:", comodel_name="res.country", help="Country of birth:"
    )
    category_a = fields.Boolean(string="")
    category_b = fields.Boolean(string="")
    category_c = fields.Boolean(string="")
    category_d = fields.Boolean(string="")
    category_be = fields.Boolean(string="")
    category_ce = fields.Boolean(string="")
    category_de = fields.Boolean(string="")
    category_a1 = fields.Boolean(string="")
    category_b1 = fields.Boolean(string="")
    category_c1 = fields.Boolean(string="")
    category_d1 = fields.Boolean(string="")
    category_c1e = fields.Boolean(string="")
    category_d1e = fields.Boolean(string="")
    license_n = fields.Char(string="Your driver's license number")
    license_d = fields.Date(string="Your driver's license first issue date")
    license_s = fields.Binary(
        string="Attach Your signature, JPEG (JPG), PNG formats only"
    )
    license_p = fields.Binary(
        string="Attach Your driver license copy, JPEG (JPG), GIF, PNG formats only"
    )
