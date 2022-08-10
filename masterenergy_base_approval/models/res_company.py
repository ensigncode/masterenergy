from odoo import models, fields, api


class ResCompany(models.Model):

    _inherit = "res.company"

    plant_manager_purchase_approval_limit = fields.Float(
        default=100, string="Plant Manager Limit"
    )
