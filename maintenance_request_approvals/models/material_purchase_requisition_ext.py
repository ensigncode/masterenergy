# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError


class MaterialPurchaseReqExt(models.Model):
    _inherit = "material.purchase.requisition"
