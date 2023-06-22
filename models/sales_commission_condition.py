# -*- encoding: utf-8 -*-

from odoo import models, fields

class SalesCommissionCondition(models.Model):
	_name = 'sales_commission.condition'
	_description = 'Condition for the concept'

	object_id = fields.Many2one(
		comodel_name='sales_commission.object',
		string='Objeto condición',
		required=True,
		ondelete='cascade'
	)

	operator = fields.Selection(
		selection=[
			('=', "="),
			('<', "<"),
			('<=', "<="),
			('>', ">"),
			('>=', ">="),
		],
		string="Operador condición",
		default='>=',
		required=True,
		help="Operador para la condición")

	value_type = fields.Selection(
		selection=[
			('quantity', "Cantidad"),
			('monetary', "$"),
		],
		string="Tipo de valor de la condición",
		default='none',
		required=True,
		help="Tipo de valor para la recompensa.")

	value = fields.Float(digits=(12, 2), string="Valor de condición")

	concept_id=fields.Many2one(
		comodel_name='sales_commission.concept',
		string="Concepto",
		ondelete='cascade'
	)