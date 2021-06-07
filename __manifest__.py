# -*- coding: utf-8 -*-

{
    'name': 'Order purcharse',
    'version': '0.1',
    'author': 'congnguyen',
    'category': 'Order purcharse',
    'sequence': 1,
    'summary': 'Izi',
    'description': "",
    'images': [],
    'depends': ['base', 'mail', 'product', 'report_xlsx', 'purchase', 'hr'],
    'data': [
        'security/order_purchase_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'wizard/purchase_request_reject_view.xml',
        'wizard/purchase_request_import_line_view.xml',
        'views/purchase_request.xml',
        'views/purchase_request_line.xml',
        'views/reject_reason.xml',
        'reports/report.xml',
        'reports/purchase_request_card.xml',

    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'OEEL-1',
    'qweb': [],
}
