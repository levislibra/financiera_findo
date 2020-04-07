# -*- coding: utf-8 -*-
{
    'name': "Financiera Findo",

    'summary': """
        Buro de evaluacion crediticia.""",

    'description': """
        Buro de evaluacion crediticia.
    """,

    'author': "Librasoft",
    'website': "libra-soft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'financie',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['financiera_prestamos'],

    # always loaded
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/extends_respartner.xml',
        'views/findo_configuracion.xml',
        'views/extends_res_company.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}