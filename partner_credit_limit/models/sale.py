from odoo import api, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def check_limit(self):
        self.ensure_one()
        partner = self.partner_id
        user_id = self.env["res.users"].search([("partner_id", "=", partner.id)], limit=1)
        if user_id and not user_id.has_group("base.group_portal") or not user_id:
            moveline_obj = self.env["account.move.line"]

            confirm_sale_order = self.search([("partner_id", "=", partner.id), ("state", "=", "sale")])

            amount_total = self.amount_total

            # partner_credit_limit = partner.credit_limit
            partner_credit_limit = (self.partner_id.total_due - partner.credit_limit) + amount_total
            available_credit_limit = partner_credit_limit

            if available_credit_limit >= 0:
                if not partner.over_credit:
                    msg = """Your available credit limit Amount = %0.2f Check %s Accounts 
                        or Credit Limits.""" % (
                        available_credit_limit,
                        self.partner_id.name,
                    )
                    raise UserError(_("You can not confirm Sale Order." + msg))

            return True

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order.check_limit()
        return res

    @api.model
    def create(self, values):
        partner = self.partner_id.id or values.get("partner_id")
        partner = self.env["res.partner"].browse([partner])
        user_id = self.env["res.users"].search([("partner_id", "=", partner.id)], limit=1)
        if user_id and not user_id.has_group("base.group_portal") or not user_id:
            moveline_obj = self.env["account.move.line"]

            confirm_sale_order = self.search([("partner_id", "=", partner.id), ("state", "=", "sale")])

            amount_total = 0
            order_line = values.get("order_line")
            if order_line:
                for line in order_line:
                    for l in line:
                        if type(l) == dict:
                            amount_total += l.get("product_uom_qty", 1) * l.get("price_unit", 0)

                partner_credit_limit = (partner.total_due - partner.credit_limit) + amount_total

                available_credit_limit = partner_credit_limit

                if available_credit_limit >= 0:
                    if not partner.over_credit:
                        msg = """Your available credit limit Amount = %0.2f Check %s Accounts 
                            or Credit Limits.""" % (
                            available_credit_limit - amount_total,
                            partner.name,
                        )
                        raise UserError(_("You can not confirm Sale Order." + msg))
            return super(SaleOrder, self).create(values)

    def write(self, values):
        partner = self.partner_id.id or values.get("partner_id")
        partner = self.env["res.partner"].browse([partner])
        user_id = self.env["res.users"].search([("partner_id", "=", partner.id)], limit=1)
        if user_id and not user_id.has_group("base.group_portal") or not user_id:
            moveline_obj = self.env["account.move.line"]

            confirm_sale_order = self.search([("partner_id", "=", partner.id), ("state", "=", "sale")])

            amount_total = 0
            order_line = self.order_line
            if order_line:
                for line in order_line:
                    for l in line:
                        amount_total += l.price_subtotal

                partner_credit_limit = (partner.total_due - partner.credit_limit) + amount_total
                print(partner_credit_limit)

                available_credit_limit = partner_credit_limit

                if available_credit_limit >= 0:
                    if not partner.over_credit:
                        msg = """Your available credit limit Amount = %0.2f Check %s Accounts 
                            or Credit Limits.""" % (
                            available_credit_limit - amount_total,
                            partner.name,
                        )
                        raise UserError(_("You can not confirm Sale Order." + msg))
            return super(SaleOrder, self).write(values)
