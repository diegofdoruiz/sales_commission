# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SalesCommissionConcept(models.Model):
	_name = 'sales_commission.concept'
	_description = 'Concept for the level of sales commission'
	_rec_name = "concept_sentence_id"

	concept_sentence_id = fields.Many2one(
		comodel_name='sales_commission.concept_sentence',
		string='Sentencia',
		required=True,
		ondelete='cascade'
	)

	level_id=fields.Many2one(
		comodel_name='sales_commission.level',
		required=True,
		string="Nivel",
		ondelete='cascade'
	)

	condition_ids = fields.One2many(
		comodel_name='sales_commission.condition',
		required=True,
		inverse_name='concept_id',
		string="Condición (SI)",
	)

	reward_ids = fields.One2many(
		comodel_name='sales_commission.reward',
		required=True,
		inverse_name='concept_id',
		string="Recompensa",
	)

	required = fields.Boolean(string="Requerido", default=False)


	@api.constrains('condition_ids')
	def _check_condition_ids(self):
		for record in self:
			if len(record.condition_ids) > 1 or len(record.reward_ids) > 1:
				raise ValidationError('Una condición y una recompensa por concepto')
			elif len(record.condition_ids) == 0 or len(record.reward_ids) == 0:
				raise ValidationError('El concepto debe tener una condición y una recompensa')



