from odoo import models, fields, api


class PurchaseRequisition(models.Model):

    _inherit = "purchase.requisition"

    state = fields.Selection(
        selection_add=[("hod", "H.O.D"), ("audit", "Audit"), ("ongoing",)],
        ondelete={"hod": "set default", "audit": "set default"},
        tracking=True,
    )
    state_blanket_order = fields.Selection(
        selection_add=[("hod", "H.O.D"), ("audit", "Audit"), ("ongoing",)],
        ondelete={"hod": "set null", "audit": "set null"},
        tracking=True,
    )

    def action_submit_to_hod(self):
        for rec in self:
            rec.write({"state": "hod"})

    def action_hod_approve(self):
        for rec in self:
            rec.write({"state": "audit"})
