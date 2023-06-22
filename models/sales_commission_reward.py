# -*- coding: utf-8 -*-

from odoo import models, fields

class SalesCommissionReward(models.Model):
	_name = 'sales_commission.reward'
	_description = 'Reward for the concept'
	_rec_name = "value_type"

	value_type = fields.Selection(
		selection=[
			('percentage', "%"),
			('monetary', "$"),
		],
		string="Tipo de valor de recompensa",
		default='none',
		required=True,
		help="Tipo de valor para la recompensa.")

	value = fields.Float(digits=(12, 2), string="Valor de recompensa")

	concept_id=fields.Many2one(
		comodel_name='sales_commission.concept',
		string="Concepto",
		ondelete='cascade'
	)