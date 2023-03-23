from odoo import api, fields, models, _
from odoo.tools import float_compare
from odoo.exceptions import ValidationError, UserError


class SaleOrderExt(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(
        [
            ("draft", "Quotation"),
            ("sent", "Quotation Sent"),
            ("sm", "Sales Manager"),
            ("ccm", "Credit Control Manager"),
            ("approved", "Approved"),
            ("done", "Locked"),
            ("reject", "Rejected"),
            ("cancel", "Cancelled"),
            ("hod", "H.O.D"),
            ("audit", "Audit"),
            ("to approve", "Plant Manager"),
            ("sale", "Sales Order"),
        ],
        string="Status",
        readonly=True,
        copy=False,
        index=True,
        tracking=3,
        default="draft",
    )
    date_approve = fields.Datetime('Confirmation Date', readonly=1, index=True, copy=False)

    def send_to_sm(self):
        user = self.env["res.users"].search([])
        email = ""
        for s in user:
            if s.has_group("sale_approvals.sm_app"):
                email = s.partner_id.email
                break
        if email:
            print("<<<<<<<<email>>>>>>>>")
            print(email)
            self.hi_sending_email(email)
        self.write({"state": "sm"})

    def validate_sm(self):
        user = self.env["res.users"].search([])
        email = ""
        for s in user:
            if s.has_group("sale_approvals.ccm_app"):
                email = s.partner_id.email
                break
        if email:
            print("<<<<<<<<email>>>>>>>>")
            print(email)
            self.hi_sending_email(email)
        self.write({"state": "ccm"})

    def validate_ccm(self):
        self.action_confirm()

    def button_reject_sm(self):
        self.write({"state": "reject"})

    def button_reject_ccm(self):
        self.write({"state": "reject"})

    def action_draft(self):
        orders = self.filtered(lambda s: s.state in ["cancel", "sent", "reject"])
        return orders.write(
            {
                "state": "draft",
                "signature": False,
                "signed_by": False,
                "signed_on": False,
            }
        )

    def action_quotation_send(self):
        """Opens a wizard to compose an email, with relevant mail template loaded by default"""
        self.write({"state": "draft"})
        self.ensure_one()
        template_id = self._find_mail_template()
        lang = self.env.context.get("lang")
        template = self.env["mail.template"].browse(template_id)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            "default_model": "sale.order",
            "default_res_id": self.ids[0],
            "default_use_template": bool(template_id),
            "default_template_id": template_id,
            "default_composition_mode": "comment",
            "mark_so_as_sent": True,
            "custom_layout": "mail.mail_notification_paynow",
            "proforma": self.env.context.get("proforma", False),
            "force_email": True,
            "model_description": self.with_context(lang=lang).type_name,
        }
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(False, "form")],
            "view_id": False,
            "target": "new",
            "context": ctx,
        }

    def action_confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped("state")):
            raise UserError(
                _("It is not allowed to confirm an order in the following states: %s")
                % (", ".join(self._get_forbidden_state_confirm()))
            )

        for order in self.filtered(
            lambda order: order.partner_id not in order.message_partner_ids
        ):
            order.message_subscribe([order.partner_id.id])
        self.write(self._prepare_confirmation_values())

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop("default_name", None)

        self.with_context(context)._action_confirm()
        if self.env.user.has_group("sale.group_auto_done_setting"):
            self.action_done()
        return True

    def action_submit_to_hod(self):
        for rec in self:
            rec.write({"state": "hod", "date_approve": fields.Datetime.now()})

    def action_hod_approve(self):
        for rec in self:
            rec.write({"state": "audit", "date_approve": fields.Datetime.now()})

    def action_audit_approve(self):
        for rec in self:
            rec.write({"state": "to approve", "date_approve": fields.Datetime.now()})

    def button_approve(self):
        self = self.filtered(lambda order: order._approval_allowed())
        self.write({"state": "sale", "date_approve": fields.Datetime.now()})
        self.filtered(lambda s: s.company_id.so_lock == "lock").write({"state": "done"})
        self.action_confirm()
        return {}

    def _approval_allowed(self):
        """Returns whether the order qualifies to be approved by the current user"""
        self.ensure_one()
        return (
            self.company_id.so_double_validation == "one_step"
            or (
                self.company_id.so_double_validation == "two_step"
                and self.amount_total
                <= self.env.company.currency_id._convert(
                    self.company_id.so_double_validation_amount,
                    self.currency_id,
                    self.company_id,
                    self.date_order or fields.Date.today(),
                )
            )
        )


    def hi_sending_email(self, email):
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
