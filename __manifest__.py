# -*- coding: utf-8 -*-
{
    'name': 'Sales Commission',

    'summary': """
        Module for calculate the the additional income a 
        salesperson earns based on the number of sales they've made.
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': 'RudeCode',
    'website': 'https://www.yourcompany.com',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/Sales',
    'version': '0.67',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sales_commission_menu.xml',
        'views/res_partner_view.xml',
        'views/sales_commission_plan_view.xml',
        'views/sales_commission_level_view.xml',
        'views/sales_commission_concept_view.xml',
        'views/sales_commission_concept_sentence_view.xml',
        'views/sales_commission_object_view.xml',
        'views/sales_commission_condition_view.xml',
        'views/sales_commission_reward_view.xml'
        # 'views/views.xml'
        # 'views/templates.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
