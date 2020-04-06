# -*- coding: utf-8 -*-
from openerp import http

# class FinancieraFindo(http.Controller):
#     @http.route('/financiera_findo/financiera_findo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/financiera_findo/financiera_findo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('financiera_findo.listing', {
#             'root': '/financiera_findo/financiera_findo',
#             'objects': http.request.env['financiera_findo.financiera_findo'].search([]),
#         })

#     @http.route('/financiera_findo/financiera_findo/objects/<model("financiera_findo.financiera_findo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('financiera_findo.object', {
#             'object': obj
#         })