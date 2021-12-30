{
    "name": "Payment Request",
    "version": "11.0",
    "author": "Mattobell",
    "website": "http://www.mattobell.com/",
    "description": "Payment Request",
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/request_sequence.xml",
        "views/payment_requisition_view.xml",
        "views/company_view.xml",
        "payment_request_report.xml",
        "views/request_report_view.xml",
        # 'views/journal_view.xml'
    ],
    "depends": ["account", "hr", "masterenergy_base_approval"],
    "installable": True,
    "auto_install": False,
}
