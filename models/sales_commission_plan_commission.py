# -*- coding: utf-8 -*-

from odoo import models, fields

class SalesCommissionPlanCommission(models.Model):
	_name='sales_commission.plan_commission'
	_name='Calculate a plan commission'

	name = fields.Char(string="Commission", required=True)


	