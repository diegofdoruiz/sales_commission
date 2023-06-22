# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResPartner(models.Model):
    """Add some fields related to commissions"""

    _inherit = "res.partner"

    commissioner_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="partner_commissioner_rel",
        column1="partner_id",
        column2="commissioner_id",
        domain=[("commissioner", "=", True)],
        readonly=False,
        string="Comisionistas",
    )

    commissioner = fields.Boolean(
        string="Creditor/Commissioner",
        help="Check this field if the partner is a creditor or an commissioner.",
    )

    periodicity = fields.Selection(
        selection=[
            ("biweekly", "Quincenal"),
            ("monthly", "Mensual"),
            ("quaterly", "Trimestral"),
            ("semi", "Semestral"),
            ("annual", "Anual"),
        ],
        string="Periodo",
        default="monthly",
    )

    plan_ids = fields.Many2many(
        comodel_name="sales_commission.plan",
        relation="sales_commission_partner_plan_rel",
        column1="partner_id",
        column2="plan_id",
        readonly=False,
        string="Planes"
    )

    @api.model
    def _commercial_fields(self):
        """Add commissioners to commercial fields that are synced from parent to childs."""
        res = super()._commercial_fields()
        res.append("commissioner_ids")
        return res

    
