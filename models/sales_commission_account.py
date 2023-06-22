# -*- coding: utf-8 -*-

from odoo import api, models, fields

class SalesCommissionAccount(models.Model):
	_inherit="account.move"

	commission_total = fields.Float(
		string="Commissions",
		compute="_compute_commission_total",
		store=True,
		)

	@api.depends("line_ids.agent_ids.amount")
	def _compute_commission_total(self):
		for record in self:
			record.commission_total = 0.0
			for line in record.line_ids:
				record.commission_total += sum(x.amount for x in line.agent_ids)