# -*- coding: utf-8 -*-
from odoo import http

# class SeguridadOcupacional(http.Controller):
#     @http.route('/seguridad_ocupacional/seguridad_ocupacional/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/seguridad_ocupacional/seguridad_ocupacional/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('seguridad_ocupacional.listing', {
#             'root': '/seguridad_ocupacional/seguridad_ocupacional',
#             'objects': http.request.env['seguridad_ocupacional.seguridad_ocupacional'].search([]),
#         })

#     @http.route('/seguridad_ocupacional/seguridad_ocupacional/objects/<model("seguridad_ocupacional.seguridad_ocupacional"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('seguridad_ocupacional.object', {
#             'object': obj
#         })