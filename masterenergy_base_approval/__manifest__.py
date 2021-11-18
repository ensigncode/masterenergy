{
    "name": "Master Energy",
    "summary": """Master Energy""",
    "description": """
        Long description of module's purpose
    """,
    "author": "My Company",
    "website": "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "purchase_requisition", "purchase_stock"],
    # always loaded
    "data": [
        # 'security/ir.model.access.csv',
        "views/purchase_order.xml",
        "views/purchase_requisition.xml",
        "views/templates.xml",
        "data/res_group.xml",
    ],
}
