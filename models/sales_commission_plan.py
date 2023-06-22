# -*- coding: utf-8 -*-

from odoo import models, fields

class SalesCommissionPlan(models.Model):
	_name = 'sales_commission.plan'
	_description = 'Plan of levels'

	name = fields.Char(string='Nombre del plan', required=True)

	company_id = fields.Many2one(
		comodel_name="res.company",
		default=lambda self: self._default_company_id(),
		required=True,
		)

	amount_base_type = fields.Selection(
        selection=[
        	("gross_amount", "Valor bruto"), 
        	("net_amount", "Valor neto")],
        string="Valor base",
        required=True,
        default="gross_amount",
    )

	level_ids = fields.One2many(
        comodel_name="sales_commission.level",
        inverse_name="plan_id",
        string="Niveles",
    )

	commissioner_ids = fields.Many2many(
		comodel_name="res.partner",
		relation="sales_commission_partner_plan_rel",
		column1="plan_id",
		column2="partner_id",
		domain=[("commissioner", "=", True)],
		readonly=False,
		string="Comisionistas"
		)

	def _default_company_id(self):
		return self.env.company.id