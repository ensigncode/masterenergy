# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today Mattobell (<http://www.mattobell.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
    'name': 'Payment Request',
    'version': '11.0',
    'author': 'Mattobell',
    'website': 'http://www.mattobell.com/',
    'description': "Payment Request",
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/request_sequence.xml',
        'views/payment_requisition_view.xml',
        'views/company_view.xml',
        'payment_request_report.xml',
        'views/request_report_view.xml',
        'views/journal_view.xml'
    ],
    'depends': ['account', 'hr'],
    'installable': True,
    'auto_install': False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: