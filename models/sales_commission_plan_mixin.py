# -*- coding: utf-8 -*-
from odoo import _, api, fields, models

class SalesCommissionPlanMixin(models.AbstractModel):
	_name = "sales_commission.plan.mixin"
	_description = (
		"Mixin model for applying to any object that wants to handle commissions"
		)
	commissioner_ids = fields.One2many(
		comodel_name="sales_commission.plan.line.mixin",
		inverse_name="object_id",
		string="Commissioners & commissions",
		help="Commissioners/Commissions related to the invoice line.",
		compute="_compute_commissioner_ids",
		readonly=False,
		store=True,
		copy=True,
		)
	product_id = fields.Many2one(comodel_name="product.product", string="Product")
	plan_free = fields.Boolean(
		string="Plan. free",
		compute="_compute_plan_free",
		store=True,
		readonly=True,
		)
	plan_status = fields.Char(
		compute="_compute_plan_status",
		string="Plan",
		)

	def _prepare_commissioner_vals(self, commissioner):
		return {"commissioner_id": commissioner.id, "plan_id": commissioner.plan_id.id}

	def _prepare_commissioners_vals_partner(self, partner):
		"""Utility method for getting agents creation dictionary of a partner."""
		commissioners = partner.agent_ids
		return [(0, 0, self._prepare_commissioner_vals(commissioner)) for commissioner in commissioners]

	@api.depends("plan_free")
	def _compute_commissioner_ids(self):
		"""Empty method that needs to be implemented in children models."""
		raise NotImplementedError()

	@api.depends("product_id")
	def _compute_plan_free(self):
		"""Compute instead of a simple related to have a proper initialized value."""
		for line in self:
			line.plan_free = line.product_id.plan_free

	@api.depends("plan_free", "commissioner_ids")
	def _compute_plan_status(self):
		for line in self:
			if line.plan_free:
				line.plan_status = _("Plan free")
			elif len(line.commissioner_ids) == 0:
				line.plan_status = _("No commission commissioners")
			elif len(line.commissioner_ids) == 1:
				line.plan_status = _("1 commission commissioner")
			else:
				line.plan_status = _("%s commission commissioners") % (
					len(line.commissioner_ids),
				)

	def recompute_commissioners(self):
		self._compute_commissioner_ids()

	def button_edit_commissoners(self):
		self.ensure_one()
		view = self.env.ref("sales_commission.view_sales_commission_mixin_commissioner_only")
		return {
            "name": _("Commissioners"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": self._name,
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
            "res_id": self.id,
            "context": self.env.context,
        }

class SalesCommissionPlanLineMixin(models.AbstractModel):
	_name = "sales_commission.plan.line.mixin"
	_description = (
		"Mixin model for having commission agent lines in "
		"any object inheriting from this one"
		)
	_rec_name = "commissioner_id"
	_sql_constraints = [
	(
		"unique_commissioner",
		"UNIQUE(object_id, commissioner_id)",
		"You can only add one time each commissioner.",
		)
	]
	object_id = fields.Many2one(
		comodel_name="sales_commission.plan.mixin",
		ondelete="cascade",
		required=True,
		copy=False,
		string="Parent",
		)
	commissioner_id = fields.Many2one(
		comodel_name="res.partner",
		domain="[('commissioner', '=', True)]",
		ondelete="restrict",
		required=True,
		)
	plan_id = fields.Many2one(
		comodel_name="sales_commission.plan",
		ondelete="restrict",
		required=True,
		compute="_compute_plan_id",
		store=True,
		readonly=False,
		copy=True,
		)
	amount = fields.Monetary(
		string="Commission Amount",
		compute="_compute_amount",
		store=True,
		)
	# Fields to be overriden with proper source (via related or computed field)
	currency_id = fields.Many2one(comodel_name="res.currency")

	def _compute_amount(self):
		"""Compute method to be implemented by inherited models."""
		raise NotImplementedError()

	def _get_commission_amount(self, plan, subtotal, product, quantity):
		"""Get the commission amount for the data given. It's called by compute methods of children models.

    	This means the inheritable method for modifying the amount of the commission.
        """
		self.ensure_one()
		print(plan.amount_base_type)
		if product.plan_free or not plan:
			return 0.0
		if plan.amount_base_type == "net_amount":
        	# If subtotal (sale_price * quantity) is less than
        	# standard_price * quantity, it means that we are selling at
        	# lower price than we bought, so set amount_base to 0
			subtotal = max([0, subtotal - product.standard_price * quantity])
		print(subtotal)

	@api.depends("commissioner_id")
	def _compute_plan_id(self):
		for record in self:
			record.plan_id = record.commissioner_id.plan_id