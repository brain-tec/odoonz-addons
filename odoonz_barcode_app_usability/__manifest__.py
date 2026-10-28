# Copyright 2026 Graeme Gellatly
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Barcode App Usability",
    "summary": """
        Mark counted lines awaiting review from Inventory Count""",
    "version": "19.0.1.0.0",
    "license": "LGPL-3",
    "author": "Graeme Gellatly",
    "website": "https://github.com/odoonz/odoonz-addons",
    "depends": ["stock_barcode"],
    "data": [
        "views/stock_quant.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "odoonz_barcode_app_usability/static/src/**/*.js",
        ],
    },
    "installable": True,
}
