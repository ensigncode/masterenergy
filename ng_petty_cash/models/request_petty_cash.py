from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class RequestPettyCash(models.Model):
    _name = "request.petty.cash"

    @api.model
    def create(self, vals):
        sequence = self.env["ir.sequence"].get("name")
        vals["name"] = sequence
        return super(RequestPettyCash, self).create(vals)

    name = fields.Char(string="Request Id", readonly=True)
    request_label = fields.Char(string="Request Label")
    bank_statement = fields.Many2one("account.bank.statement", string="Bank Statement")
    location = fields.Many2one("request.location", string="Location")

    petty_cashier = fields.Many2one(
        "res.users", string="Petty Cashier", required=True, default=lambda self: self.env.user
    )
    petty_cash_amount = fields.Float(string="Petty Cash Amount")
    requested_date = fields.Date(string="Requested Date")
    approved_date = fields.Date(string="Approved Date")
    approval_manager = fields.Many2one("res.users", string="Approval Manager")

    state = fields.Selection([("draft", "New"), ("submitted", "Submitted"), ("done", "Done")], default="draft")


    def submit(self):
        return self.write({"state": "submitted"})


    def done(self):
        self.approval_manager = self.env.uid
        self.approved_date = datetime.now()

        if not self.bank_statement:
            raise ValidationError(_("Kindly Select a Bank Statement for this Request"))
        else:
            get_statement = self.env["account.bank.statement"].search([("name", "=", self.bank_statement.name)])
            get_statement.line_ids.create(
                {
                    "name": self.request_label,
                    "partner_id": self.petty_cashier.id,
                    "amount": self.petty_cash_amount,
                    "statement_id": get_statement.id,
                    "journal_id": get_statement.journal_id.id,
                }
            )
            return self.write({"state": "done"})


    def return_submit(self):
        return self.write({"state": "draft"})
