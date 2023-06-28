# -*- coding: utf-8 -*-

from odoo import api, models, fields

class SalesCommissionAccountMove(models.Model):
    _inherit="account.move"

    commission_total = fields.Float(
		string="Commissions",
		compute="_compute_commission_total",
		store=True,
	)

    partner_commissioner_ids = fields.Many2many(
        string="Commissioners",
        comodel_name="res.partner",
        compute="_compute_commissioners",
        search="_search_commissioners",
    )

    def recompute_lines_commissioners(self):
        self.mapped("order_line").recompute_commissioners()


    @api.depends("partner_commissioner_ids", "invoice_line_ids.commissioner_ids.commissioner_id")
    def _compute_commissioners(self):
        for move in self:
            move.partner_commissioner_ids = [
            (6, 0, move.mapped("invoice_line_ids.commissioner_ids.commissioner_id").ids)
            ]

    @api.model
    def _search_commissioners(self, operator, value):
        ail_commissioners = self.env["account.invoice.line.commissioner"].search(
            [("commissioner_id", operator, value)]
            )
        return [("id", "in", ail_commissioners.mapped("object_id.move_id").ids)]

    def recompute_lines_commissioners(self):
        self.mapped("order_line").recompute_commissioners()

    @api.depends("line_ids.commissioner_ids.amount")
    def _compute_commission_total(self):
        for record in self:
            record.commission_total = 0.0
            for line in record.line_ids:
                record.commission_total += sum(x.amount for x in line.agent_ids)


class SalesCommissionAccountMoveLine(models.Model):
    _inherit = [
    "account.move.line",
    "sales_commission.plan.mixin",
    ]
    _name = "account.move.line"

    commissioner_ids = fields.One2many(comodel_name="account.invoice.line.commissioner")


class SalesCommissionAccountInvoiceLineCommissioner(models.Model):
    _inherit = "sales_commission.plan.line.mixin"
    _name = "account.invoice.line.commissioner"
    _description = "Commissioner detail of commission line in invoice lines"

    object_id = fields.Many2one(comodel_name="account.move.line")
    invoice_id = fields.Many2one(
        string="Invoice",
        comodel_name="account.move",
        related="object_id.move_id",
        store=True,
        )
    invoice_date = fields.Date(
        string="Invoice date",
        related="invoice_id.invoice_date",
        store=True,
        readonly=True,
        )
    company_id = fields.Many2one(
        comodel_name="res.company",
        compute="_compute_company",
        store=True,
        )
    currency_id = fields.Many2one(
        related="object_id.currency_id",
        readonly=True,
        )

    @api.depends("object_id", "object_id.company_id")
    def _compute_company(self):
        for line in self:
            line.company_id = line.object_id.company_id



