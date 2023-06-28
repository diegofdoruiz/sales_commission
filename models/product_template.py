# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    plan_free = fields.Boolean(string="Free of plan", default=False)
