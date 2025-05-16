{
    'name': 'Consume External API Example',
    'version': '1.0',
    'summary': 'Module to consume external API in Odoo 18',
    'category': 'Tools',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/consume_api_views.xml',
    ],
    'installable': True,
    'application': True,
    'external_dependencies': {
        'python': ['requests'],
    },
}
