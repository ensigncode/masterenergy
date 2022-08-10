from odoo import models, fields, api


class MasterEnergyApproval(models.AbstractModel):

    _name = "master.energy.approval"
    _description = "Master Energy Approval"

    state = fields.Selection(selection=[])
