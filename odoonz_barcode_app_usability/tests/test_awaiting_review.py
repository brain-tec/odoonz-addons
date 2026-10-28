# Copyright 2026 Graeme Gellatly
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestAwaitingReview(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {
                "name": "Awaiting Review Product",
                "is_storable": True,
            }
        )
        cls.location = cls.env.ref("stock.stock_location_stock")
        cls.quant = cls.env["stock.quant"].create(
            {
                "product_id": cls.product.id,
                "location_id": cls.location.id,
                "quantity": 4.0,
            }
        )

    def test_inventory_write_allows_awaiting_review(self):
        fields_to_write = self.env["stock.quant"]._get_inventory_fields_write()
        self.assertIn("awaiting_review", fields_to_write)
        self.quant.with_context(inventory_mode=True).write({"awaiting_review": True})
        self.assertTrue(self.quant.awaiting_review)

    def test_barcode_fields_include_awaiting_review(self):
        self.assertIn("awaiting_review", self.quant._get_fields_stock_barcode())

    def test_validate_clears_awaiting_review(self):
        self.quant.awaiting_review = True
        self.quant.action_validate()
        self.assertFalse(self.quant.awaiting_review)

    def test_to_review_filter(self):
        view = self.env.ref("odoonz_barcode_app_usability.quant_search_view")
        self.assertIn("awaiting_review", view.arch)
        self.quant.awaiting_review = True
        found = self.env["stock.quant"].search(
            [("id", "=", self.quant.id), ("awaiting_review", "=", True)]
        )
        self.assertEqual(found, self.quant)
