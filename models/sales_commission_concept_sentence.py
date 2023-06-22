# -*- coding: utf-8 -*-

from odoo import models, fields

class SalesCommissionConceptSentence(models.Model):
	_name = 'sales_commission.concept_sentence'
	_description = 'Sentence for the concept'

	name = fields.Char(string="Sentencia", required=True)