from odoo import models, fields, api


class PurchaseOrder(models.Model):

    _inherit = "purchase.order"

    state = fields.Selection(
        selection_add=[
            ("hod", "H.O.D"),
            ("audit", "Audit"),
            ("to approve", "Plant Manager"),
            ("group_audit", "Group Audit"),
            ("ed", "Executive Director"),
            ("gmd", "Group Managing Director"),
            ("purchase",),
        ],
        ondelete={"hod": "set default", "audit": "set default"},
        tracking=True,
    )

    def button_group_audit(self):
        for rec in self:
            rec.write({"state": "ed"})

    def button_ed_approve(self):
        for rec in self:
            rec.write({"state": "gmd"})

    def button_approve(self, force=False):
        order = self.filtered(lambda order: order._approval_allowed())
        print(order, "!!!!!!!!!!!!!!!!!", order)
        if order:
            order.write({"state": "purchase", "date_approve": fields.Datetime.now()})
        else:
            self.write({"state": "group_audit", "date_approve": fields.Datetime.now()})

    def action_submit_to_hod(self):
        for rec in self:
            rec.write({"state": "hod", "date_approve": fields.Datetime.now()})

    def action_hod_approve(self):
        for rec in self:
            rec.write({"state": "audit", "date_approve": fields.Datetime.now()})

    def action_audit_approve(self):
        for rec in self:
            rec.write({"state": "to approve", "date_approve": fields.Datetime.now()})

    def _approval_allowed(self):
        """Returns whether the order qualifies to be approved by the current user"""
        self.ensure_one()
        return (
            self.company_id.po_double_validation == "one_step"
            or (
                self.company_id.po_double_validation == "two_step"
                and self.amount_total
                <= self.env.company.currency_id._convert(
                    self.company_id.po_double_validation_amount,
                    self.currency_id,
                    self.company_id,
                    self.date_order or fields.Date.today(),
                )
            )
            or self.user_has_groups("purchase.group_purchase_manager")
            or self.user_has_groups("masterenergy_base_approval.group_ed")
        )

    def button_confirm(self):
        for order in self:
            if order.state not in ["to approve", "gmd"]:
                continue
            order._add_supplier_to_product()
            #     # Deal with double validation process
            print("!!!!!!!!!!!!!!!!!!!", order.state)
            if order.state == "gmd":
                order.button_approve()
                return True

            if order._approval_allowed():
                # order.button_approve()
                pass
            else:
                order.write({"state": "to approve"})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True
