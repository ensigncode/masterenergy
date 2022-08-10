# -*- coding: utf-8 -*-

from odoo import models, fields


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    account_asset_id = fields.Many2one("account.asset", "Equipment Name")

    equipment_checklist_ids = fields.Many2many(
        "equipment.checklist",
        string="Equipment Checklist",
    )
    material_ids = fields.One2many(
        "maintenance.planned.material",
        "equipment_id",
        string="Maintenance Planned Material",
    )


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
