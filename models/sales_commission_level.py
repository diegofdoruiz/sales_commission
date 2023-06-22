# -*- coding: utf-8 -*-

from odoo import models, fields

class SalesCommissionLevel(models.Model):
	_name = 'sales_commission.level'
	_description = 'Level for the sales commision'

	name = fields.Char(string="Nombre del nivel", required=True)
	concepts_required_for_next_level = fields.Selection(
		selection=[
			('all', "Todos los conceptos"),
			('all_selected', "Los conceptos seleccionados"),
			('at_least_one_selected', "Al menos un seleccionado"),
		],
		string="Conceptos para promover al siguiente nivel",
		default='all_selected',
		required=True,
		help="Operador para la condición")

	concepts_ids = fields.One2many(
		comodel_name='sales_commission.concept',
		inverse_name='level_id',
		string="Conceptos de este nivel",
		)

	plan_id = fields.Many2one(
        comodel_name="sales_commission.plan",
        required=True,
		string="Plan",
		ondelete='cascade'
    )

	#=== COMPUTE METHODS ===#

	#=== ONCHANGE METHODS ===#

	#=== ACTION METHODS ===#

