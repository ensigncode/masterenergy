# -*- coding: utf-8 -*-

from odoo import fields, models

class Company(models.Model):
    _inherit = 'res.company'

    so_lock = fields.Selection([
        ('edit', 'Allow to edit sale orders'),
        ('lock', 'Confirmed sale orders are not editable')
        ], string="Sale Order Modification", default="edit",
        help='Sale Order Modification used when you want to sale order editable after confirm')

    so_double_validation = fields.Selection([
        ('one_step', 'Confirm sale orders in one step'),
        ('two_step', 'Get 2 levels of approvals to confirm a sale order')
        ], string="Levels of Approvals", default='one_step',
        help="Provide a double validation mechanism for sales")

    so_double_validation_amount = fields.Monetary(string='Double validation amount', default=5000,
        help="Minimum amount for which a double validation is required")
