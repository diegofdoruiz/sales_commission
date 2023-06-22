# -*- coding: utf-8 -*-

from odoo import models, fields

class SalesCommissionObject(models.Model):
	_name = 'sales_commission.object'
	_description = 'Objects for the conditions'

	name = fields.Char(string="Name", required=True)
