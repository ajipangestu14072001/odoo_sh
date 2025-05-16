import requests
from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

class ExternalApiExample(models.Model):
    _name = 'external.api.example'
    _description = 'External API Example'

    title = fields.Char("Title")
    body = fields.Text("Body")
    api_id = fields.Integer("API ID")

    def fetch_api_data(self):
        url = "https://jsonplaceholder.typicode.com/posts"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            _logger.info(f"Fetched {len(data)} items from API")

            for item in data:
                if not self.env['external.api.example'].search([('api_id', '=', item.get('id'))]):
                    self.env['external.api.example'].create({
                        'title': item.get('title'),
                        'body': item.get('body'),
                        'api_id': item.get('id')
                    })
                    _logger.info(f"Created record with API ID: {item.get('id')}")

        except requests.RequestException as e:
            _logger.error("API fetch failed: %s", e)
