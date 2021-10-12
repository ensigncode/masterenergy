{
    "name": "Petty Cash",
    "version": "1.0",
    "depends": ["base", "account_accountant", "product", "sale", "purchase", "account", "account_budget"],
    "author": "Matt O'Bell Ltd",
    "website": "http://www.mattobell.com",
    "description": """
     Petty Cash
    """,
    "category": "Hidden",
    "data": [
        "security/ir.model.access.csv",
        "security/petty_cash_security.xml",
        "views/request_petty_cash_view.xml",
    ],
    "installable": True,
}
