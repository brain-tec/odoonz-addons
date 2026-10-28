# Copyright 2026 Graeme Gellatly
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    awaiting_review = fields.Boolean(
        string="Awaiting Review",
        default=False,
        help="Set from barcode Inventory Count when the count is held for review.",
    )

    def _get_fields_stock_barcode(self):
        return [*super()._get_fields_stock_barcode(), "awaiting_review"]

    @api.model
    def _get_inventory_fields_write(self):
        return [*super()._get_inventory_fields_write(), "awaiting_review"]

    def action_validate(self):
        self.filtered("awaiting_review").write({"awaiting_review": False})
        return super().action_validate()
