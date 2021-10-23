# -*- coding: utf-8 -*-
# from odoo import http


# class MasterBaseAproval(http.Controller):
#     @http.route('/master_base_aproval/master_base_aproval/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/master_base_aproval/master_base_aproval/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('master_base_aproval.listing', {
#             'root': '/master_base_aproval/master_base_aproval',
#             'objects': http.request.env['master_base_aproval.master_base_aproval'].search([]),
#         })

#     @http.route('/master_base_aproval/master_base_aproval/objects/<model("master_base_aproval.master_base_aproval"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('master_base_aproval.object', {
#             'object': obj
#         })
