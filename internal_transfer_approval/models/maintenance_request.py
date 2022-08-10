# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    @api.model
    def _search(
        self,
        args,
        offset=0,
        limit=None,
        order=None,
        count=False,
        access_rights_uid=None,
    ):
        """Override search() to always show inactive children when searching via ``child_of`` operator. The ORM will
        always call search() with a simple domain of the form [('parent_id', 'in', [ids])]."""
        # a special ``domain`` is set on the ``child_ids`` o2m to bypass this logic, as it uses similar domain expressions
        if self.env.user.has_group("maintenance_request_approvals.user_app"):
            args += [("stage_id.name", "in", ["New Request", "Repaired"])]
        if self.env.user.has_group("maintenance_request_approvals.hod_app"):
            args += [("stage_id.name", "=", "HOD")]
        if self.env.user.has_group("maintenance_request_approvals.audit_app"):
            args += [("stage_id.name", "=", "Audit")]
        if self.env.user.has_group("maintenance_request_approvals.pm_app"):
            args += [("stage_id.name", "=", "Plant Manager")]
        if self.env.user.has_group("maintenance_request_approvals.man_app"):
            args += [
                (
                    "stage_id.name",
                    "in",
                    ["Maintenance Officer", "In Progress", "Repaired"],
                )
            ]
        if self.env.user.has_group("maintenance_request_approvals.store_app"):
            args += [("stage_id.name", "=", "Store Officer")]
        return super(MaintenanceRequest, self)._search(
            args,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
            access_rights_uid=access_rights_uid,
        )

    @api.depends("stage_id")
    def _compute_current_stage(self):
        print("_compute_current_stage called XXXXXXXXXXXX")
        for rec in self:
            if rec.stage_id:
                name = rec.stage_id.name
                if name == "New Request":
                    rec.current_stage = "new"
                if name == "HOD":
                    rec.current_stage = "hod"
                if name == "Audit":
                    rec.current_stage = "audit"
                if name == "Plant Manager":
                    rec.current_stage = "pm"
                if name == "Maintenance Officer":
                    rec.current_stage = "mo"
                if name == "In Progress":
                    rec.current_stage = "ip"
                if name == "Store Officer":
                    rec.current_stage = "so"
                if name == "Repaired":
                    rec.current_stage = "repaired"
                if name == "Scrap":
                    rec.current_stage = "scrap"
                if name == "Completed":
                    rec.current_stage = "done"
                if name == "Rejected":
                    rec.current_stage = "rejected"
                print("<<<<<< COMPUTED self.current_stage>>>>>>")
                print(rec.current_stage)

    current_stage = fields.Selection(
        selection=[
            ("new", "New Request"),
            ("hod", "HOD"),
            ("audit", "Audit"),
            ("pm", "Plant Manager"),
            ("mo", "Maintenance Officer"),
            ("ip", "In Progress"),
            ("so", "Store Officer"),
            ("repaired", "Repaired"),
            ("scrap", "Scrap"),
            ("done", "Completed"),
            ("rejected", "Rejected"),
        ],
        compute="_compute_current_stage",
        store=True,
    )

    @api.onchange("stage_id")
    def _onchange_stage_id(self):
        print("_onchange_stage_id Called XXXXXXXXXXXXXX")
        if self.stage_id:
            name = self.stage_id.name
            if name == "New Request":
                self.current_stage = "new"
            if name == "HOD":
                self.current_stage = "hod"
            if name == "Audit":
                self.current_stage = "audit"
            if name == "Plant Manager":
                self.current_stage = "pm"
            if name == "Maintenance Officer":
                self.current_stage = "mo"
            if name == "In Progress":
                self.current_stage = "ip"
            if name == "Store Officer":
                self.current_stage = "so"
            if name == "Repaired":
                self.current_stage = "repaired"
            if name == "Scrap":
                self.current_stage = "scrap"
            if name == "Completed":
                self.current_stage = "done"
            if name == "Rejected":
                self.current_stage = "rejected"
            print("<<<<<<self.current_stage>>>>>>")
            print(self.current_stage)

    def write(self, values):
        if "stage_id" not in values:
            print("<<<<<<<<<<<<<<<<<<<((values))>>>>>>>>>>>>>>>>>>>")
            print(values)
            if (
                self.current_stage != "new"
                and "close_date" not in values
                and "current_stage" not in values
                and "archive" not in values
            ):
                raise UserError("Maintenance Request can not be edited at this stage!")
        return super(MaintenanceRequest, self).write(values)

    def send_to_hod(self):
        print("send to HOD called XXXXXXXXXXXXX")

        user = self.env["res.users"].search([])
        email = ""
        for s in user:
            if s.has_group("maintenance_request_approvals.hod_app"):
                email = s.partner_id.email
                break
        if email:
            self.sending_email(email)

        stage = self.get_stage_id("HOD")
        if stage:
            self.stage_id = stage.id
            self._onchange_stage_id()
            print("Moved to HOD stage! XXXXXXXXXXX")
        else:
            print("name or stage not found!!!!!!!")

    def send_to_audit(self):
        print("send_to_audit called XXXXXXXXXXXXX")

        user = self.env["res.users"].search([])
        email = ""
        for s in user:
            if s.has_group("maintenance_request_approvals.audit_app"):
                email = s.partner_id.email
                break
        if email:
            self.sending_email(email)

        stage = self.get_stage_id("Audit")
        if stage:
            self.stage_id = stage.id
            self._onchange_stage_id()
            print("Moved to Audit stage! XXXXXXXXXXX")
        else:
            print("name or stage not found!!!!!!!")

    def send_to_pm(self):
        print("send_to_pm called XXXXXXXXXXXXX")

        user = self.env["res.users"].search([])
        email = ""
        for s in user:
            if s.has_group("maintenance_request_approvals.pm_app"):
                email = s.partner_id.email
                break
        if email:
            self.sending_email(email)

        stage = self.get_stage_id("Plant Manager")
        if stage:
            self.stage_id = stage.id
            self._onchange_stage_id()
            print("Moved to Plant Manager stage! XXXXXXXXXXX")
        else:
            print("name or stage not found!!!!!!!")

    def reject_hod(self):
        rs = self.env["maintenance.stage"].search([("name", "=", "Rejected")])
        self.stage_id = rs

    def reject_audit(self):
        rs = self.env["maintenance.stage"].search([("name", "=", "Rejected")])
        self.stage_id = rs

    def reject_pm(self):
        rs = self.env["maintenance.stage"].search([("name", "=", "Rejected")])
        self.stage_id = rs

    def send_to_mo(self):
        print("send_to_mo called XXXXXXXXXXXXX")

        user = self.equipment_id.technician_user_id
        email = ""
        if user.has_group("maintenance_request_approvals.man_app"):
            email = user.partner_id.email
        if email:
            self.sending_email(email)

        stage = self.get_stage_id("Maintenance Officer")
        if stage:
            self.stage_id = stage.id
            self._onchange_stage_id()
            print("Moved to Maintenance Officer stage! XXXXXXXXXXX")
        else:
            print("name or stage not found!!!!!!!")

    def start_work(self):
        print("start_work called XXXXXXXXXXXXX")
        stage = self.get_stage_id("In Progress")
        if stage:
            self.stage_id = stage.id
            self._onchange_stage_id()
            print("Moved to In Progress stage! XXXXXXXXXXX")
        else:
            print("name or stage not found!!!!!!!")

    def done_work(self):
        print("done_work called XXXXXXXXXXXXX")
        stage = self.get_stage_id("Repaired")
        if stage:
            self.stage_id = stage.id
            self._onchange_stage_id()
            print("Moved to Repaired stage! XXXXXXXXXXX")
        else:
            print("name or stage not found!!!!!!!")

    def send_to_scrap(self):
        print("send_to_scrap called XXXXXXXXXXXXX")
        stage = self.get_stage_id("Scrap")
        if stage:
            self.stage_id = stage.id
            self._onchange_stage_id()
            print("Moved to send_to_scrap stage! XXXXXXXXXXX")
        else:
            print("name or stage not found!!!!!!!")

    def send_to_done(self):
        print("send_to_done called XXXXXXXXXXXXX")

        user = self.env["res.users"].search([])
        email = ""
        for s in user:
            if s.has_group("maintenance_request_approvals.user_app"):
                email = s.partner_id.email
                break
        if email:
            self.sending_email(email)

        stage = self.get_stage_id("Completed")
        if stage:
            self.stage_id = stage.id
            self._onchange_stage_id()
            print("Moved to Completed stage! XXXXXXXXXXX")
        else:
            print("name or stage not found!!!!!!!")

    def get_stage_id(self, name):
        if name:
            stage = self.env["maintenance.stage"].search([("name", "=", name)])
            if stage:
                return stage

    def sending_email(self, email):
        if self.env.user.company_id.maintenance_email_send:
            if self.env.user.company_id.maintenance_email_id_custom:
                template = self.env.user.company_id.maintenance_email_id_custom
                template.email_to = email
                self.env["mail.template"].browse(template.id).send_mail(
                    self.id, force_send=True
                )
                print("Email Sent")
