from odoo import fields, models, api, _, exceptions


class PaymentRequisition(models.Model):
    _inherit = "payment.requisition"

    @api.multi
    def action_pay(self):
        request = super(PaymentRequisition, self).action_pay()
        print("Request Received: " + str(request))
        # request = True
        payment = self.env["account.payment"]
        if request:
            for record in self:
                for line in record.request_line:
                    created_payment_id = payment.create(
                        {
                            "name": str(record.name + "  " + line.name),
                            "payment_type": "outbound" if line.partner_id.supplier is True else "inbound",
                            "partner_type": "supplier" if line.partner_id.supplier is True else "customer",
                            "journal_id": record.journal_id.id,
                            "partner_id": line.partner_id.id,
                            "amount": record.currency_id.compute(line.approved_amount, record.company_id.currency_id),
                            "payment_method_id": self.payment_method(
                                "outbound" if line.partner_id.supplier is True else "inbound"
                            )[0].id,
                        }
                    )
                    created_payment_id.post()
                    line.write({"payment_id": created_payment_id.id})

        return request

    def payment_method(self, payment_type):
        return self.env["account.payment.method"].search([("code", "=", "manual"), ("payment_type", "=", payment_type)])


class PaymentRequisitionLine(models.Model):
    _inherit = "payment.requisition.line"

    payment_id = fields.Many2one("account.payment", string="Payment Ref")
