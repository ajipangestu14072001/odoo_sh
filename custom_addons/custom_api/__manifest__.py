{
  'name': 'API Biodata',
  'version': '1.0',
  'category': 'Tools',
  'summary': 'Expose Biodata CRUD via API',
  'depends': ['base', 'website'],
  'data': [
    'views/hello_template.xml',
    'views/comments_template.xml',
    'views/custom_base.xml',

  ],
  'assets': {
    'website.assets_frontend': [
      'custom_api/static/src/js/biodata.js',
      'custom_api/static/src/js/comments.js',
      'custom_api/static/src/css/tailwind.css',
    ],
  },
  'installable': True,
}
