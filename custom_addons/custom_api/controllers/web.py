from odoo import http
from odoo.http import request

class CustomApiWeb(http.Controller):

    @http.route('/custom_api/hello', type='http', auth='public', website=True)
    def hello_world(self, **kwargs):
        return request.render('custom_api.hello_template', {})
    
    @http.route('/custom_api/comments', type='http', auth='public', website=True)
    def comments_page(self, **kwargs):
        return request.render('custom_api.comments_template')
