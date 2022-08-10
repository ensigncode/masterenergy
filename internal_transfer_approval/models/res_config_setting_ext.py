from odoo import api, fields, models, _


class ResConfigExt(models.TransientModel):
    _inherit = "res.config.settings"

    maintenance_email_send = fields.Boolean(
        "Send Email", related="company_id.maintenance_email_send", readonly=False
    )
    maintenance_email_id_custom = fields.Many2one(
        "mail.template",
        domain="[('model_id.model', '=', 'maintenance.request')]",
        related="company_id.maintenance_email_id_custom",
        string="Email Template",
        readonly=False,
    )


class ResCompanyExt(models.Model):
    _inherit = "res.company"

    maintenance_email_send = fields.Boolean("Send Email")
    maintenance_email_id_custom = fields.Many2one(
        "mail.template", string="Email Template"
    )
