{
    'name': 'Custom Commission',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Calculate sales commissions for salespeople based on sales orders.',
    'depends': ['base', 'sale'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/x_commission_views.xml',
    ],
    'installable': True,
    'application': True,
}
