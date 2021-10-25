from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    over_credit = fields.Boolean(string="Allow Over Credit")
