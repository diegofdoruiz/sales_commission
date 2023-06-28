# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends("order_line.commissioner_ids.amount")
    def _compute_commission_total(self):
        for record in self:
            epa = sum(record.mapped("order_line.commissioner_ids.amount"))
            print(epa)
            record.commission_total = epa

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

    @api.depends("partner_commissioner_ids", "order_line.commissioner_ids.commissioner_id")
    def _compute_commissioners(self):
        for so in self:
            so.partner_commissioner_ids = [
                (6, 0, so.mapped("order_line.commissioner_ids.commissioner_id").ids)
            ]

    @api.model
    def _search_commissioners(self, operator, value):
        sol_commissioners = self.env["sale.order.line.commissioner"].search(
            [("commissioner_id", operator, value)]
        )
        return [("id", "in", sol_commissioners.mapped("object_id.order_id").ids)]

    def recompute_lines_commissioners(self):
        self.mapped("order_line").recompute_commissioners()


class SaleOrderLine(models.Model):
    _inherit = [
        "sale.order.line",
        "sales_commission.plan.mixin",
    ]
    _name = "sale.order.line"

    commissioner_ids = fields.One2many(comodel_name="sale.order.line.commissioner")

    @api.depends("order_id.partner_id")
    def _compute_commissioner_ids(self):
        self.commissioner_ids = False  # for resetting previous agents
        for record in self:
            if record.order_id.partner_id and not record.commission_free:
                record.commissioner_ids = record._prepare_commissioners_vals_partner(
                    record.order_id.partner_id
                )

    def _prepare_invoice_line(self, **optional_values):
        vals = super()._prepare_invoice_line(**optional_values)
        vals["commissioner_ids"] = [
            (0, 0, {"commissioner_id": x.commissioner_id.id, "plan_id": x.plan_id.id})
            for x in self.commissioner_ids
        ]
        return vals


class SaleOrderLineCommissioner(models.Model):
    _inherit = "sales_commission.plan.line.mixin"
    _name = "sale.order.line.commissioner"
    _description = "Commissioner detail of commission line in order lines"

    object_id = fields.Many2one(comodel_name="sale.order.line")

    @api.depends(
        "plan_id",
        "object_id.price_subtotal",
        "object_id.product_id",
        "object_id.product_uom_qty",
    )
    def _compute_amount(self):
        for line in self:
            order_line = line.object_id
            line.amount = line._get_commission_amount(
                line.plan_id,
                order_line.price_subtotal,
                order_line.product_id,
                order_line.product_uom_qty,
            )