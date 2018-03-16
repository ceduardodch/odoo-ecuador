# -*- coding: utf-8 -*-
{
    'name': "Seguridad Ocupacional",

    'summary': """
        Módulo de Seguridad Ocupacional para las empresas e instiuciones de Ecuador """,

    'description': """
        Módulo de Seguridad Ocupacional para las empresas e instiuciones de Ecuador, especificamente desarrollado 
        para la Universidad Andina Simón Bolívar
    """,

    'author': "Carlos Díaz",
    'website': "http://www.uasb.edu.ec",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Salud',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'report'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/ficha_medica.xml',
        'views/hoja_evolucion.xml',
        'views/report_ficha.xml',
        'views/report_certificado.xml',
        'views/report_hoja_evolucion.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
       # 'demo/demo.xml',
    ],
}