from odoo import api, fields, models, _
from odoo.tools import float_compare
from odoo.exceptions import ValidationError, UserError


class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

    is_scrap = fields.Boolean("Is Scrap")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("waiting", "Waiting Another Operation"),
            ("hod", "HOD"),
            ("audit", "AUDIT"),
            ("tm", "Terminal Manager "),
            ("store", "Store"),
            ("assigned", "Ready"),
            ("confirmed", "Waiting"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        string="Status",
        compute="_compute_state",
        copy=False,
        index=True,
        readonly=True,
        store=True,
        tracking=True,
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
        " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
        ' * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is "As soon as possible": no product could be reserved.\n(b) The shipping policy is "When all products are ready": not all the products could be reserved.\n'
        ' * Ready: The transfer is ready to be processed.\n(a) The shipping policy is "As soon as possible": at least one product has been reserved.\n(b) The shipping policy is "When all products are ready": all product have been reserved.\n'
        " * Done: The transfer has been processed.\n"
        " * Cancelled: The transfer has been cancelled.",
    )

    def button_draft(self):
        user = self.env["res.users"].search([])
        email = ""
        for s in user:
            if s.has_group("scrap_approvals.hod_app"):
                email = s.partner_id.email
                break
        if email:
            print("<<<<<<<<email>>>>>>>>")
            print(email)
            self.sending_email(email)
        self.write({"state": "hod"})

    def button_hod(self):
        user = self.env["res.users"].search([])
        email = ""
        for s in user:
            if s.has_group("scrap_approvals.audit_app"):
                email = s.partner_id.email
                break
        if email:
            print("<<<<<<<<email>>>>>>>>")
            print(email)
            self.sending_email(email)
        self.write({"state": "audit"})

    def button_audit(self):
        user = self.env["res.users"].search([])
        email = ""
        for s in user:
            if s.has_group("scrap_approvals.tm_app"):
                email = s.partner_id.email
                break
        if email:
            print("<<<<<<<<email>>>>>>>>")
            print(email)
            self.sending_email(email)
        self.write({"state": "tm"})

    def button_tm(self):
        user = self.env["res.users"].search([])
        email = ""
        for s in user:
            if s.has_group("scrap_approvals.store_app"):
                email = s.partner_id.email
                break
        if email:
            print("<<<<<<<<email>>>>>>>>")
            print(email)
            self.sending_email(email)
        self.write({"state": "store"})
        # self.action_confirm()

    def button_store(self):
        if self.state == "store":
            self.action_confirm()

    # def button_reject(self):
    #     self.write({'state': 'reject'})

    def button_reject_hod(self):
        self.write({"state": "reject"})

    def button_reject_audit(self):
        self.write({"state": "reject"})

    def button_reject_tm(self):
        self.write({"state": "reject"})

    def action_confirm(self):
        print("action_confirm Called XXXXXXXXXXXXXX")
        self._check_company()
        self.mapped("package_level_ids").filtered(
            lambda pl: pl.state == "draft" and not pl.move_ids
        )._generate_moves()
        # call `_action_confirm` on every draft move
        self.mapped("move_lines").filtered(
            lambda move: move.state == "draft"
        )._action_confirm()

        # run scheduler for moves forecasted to not have enough in stock
        self.mapped("move_lines").filtered(
            lambda move: move.state not in ("draft", "cancel", "done")
        )._trigger_scheduler()
        # if self.state == 'tm':
        #     self.write({'state': 'store'})
        return True

    def sending_email(self, email):
        if self.env.user.company_id.email_send:
            if self.env.user.company_id.email_id_custom:
                template = self.env.user.company_id.email_id_custom
                template.email_to = email
                self.env["mail.template"].browse(template.id).send_mail(
                    self.id, force_send=True
                )
                print("Email Sent")
        #     else:
        #         raise UserError("No Email Template selected for Approval Notification")
        # else:
        #     raise UserError("Send Email Not Checked in Configuration")
