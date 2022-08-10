# -*- coding: utf-8 -*-

import ast

from datetime import date, datetime, timedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class CustomModel(models.Model):
    _name = "custom.model"

    name = fields.Char("Name")

    def custom_button(self):
        print("custom_button Callled XXXXXXXXXXXXXXX")
