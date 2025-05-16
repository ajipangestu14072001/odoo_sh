import json
import jwt
from odoo import http
from werkzeug.wrappers import Response
import requests
import base64

SECRET_KEY = "7942f642-4e94-4a8a-afc6-2815bac9fa78"
ODOO_URL = "http://dev.digitalcenter.com/jsonrpc"
ODOO_DB = "odoo_dev"

def authenticate_request(http_request):
    auth_header = http_request.httprequest.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, {
            "statusCode": 401,
            "message": "Missing or invalid Authorization header",
            "data": None
        }

    token = auth_header.split(" ")[1]

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded, None
    except jwt.ExpiredSignatureError:
        return None, {
            "statusCode": 401,
            "message": "Token has expired",
            "data": None
        }
    except jwt.InvalidTokenError:
        return None, {
            "statusCode": 401,
            "message": "Invalid token",
            "data": None
        }


class OdooApiController(http.Controller):

    @http.route('/api/user/info', type='http', auth='public', methods=['GET'], csrf=False)
    def get_user_info(self, **kwargs):
        decoded_token, error_response = authenticate_request(http.request)
        if error_response:
            return Response(
                json.dumps(error_response),
                content_type='application/json',
                status=401
            )

        user_id = decoded_token.get("userId")
        rawpass = decoded_token.get("raw")

        try:
            http.request.session['user_id'] = user_id
            http.request.session['raw'] = rawpass
            decoded_password = base64.b64decode(rawpass.encode('utf-8')).decode('utf-8')

            headers = {
                "Authorization": f"Bearer {decoded_token['sub']}",
                "Content-Type": "application/json"
            }

            user_details_payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute_kw",
                    "args": [
                        ODOO_DB,
                        user_id,
                        decoded_password,
                        "res.users",
                        "read",
                        [[user_id]],
                        {"fields": ["id", "name", "email"]}
                    ]
                }
            }

            user_details_response = requests.post(ODOO_URL, headers=headers, data=json.dumps(user_details_payload))
            user_details_data = user_details_response.json()

            if 'error' in user_details_data:
                return Response(
                    json.dumps({"statusCode": 500, "message": "Failed to fetch user details", "data": user_details_data['error']}),
                    content_type='application/json',
                    status=500
                )

            user_info = user_details_data.get('result', [{}])[0]

            return Response(
                json.dumps({
                    "statusCode": 200,
                    "message": "User info retrieved successfully",
                    "data": user_info
                }),
                content_type='application/json',
                status=200
            )

        except Exception as e:
            return Response(
                json.dumps({"statusCode": 500, "message": "Internal server error", "data": str(e)}),
                content_type='application/json',
                status=500
            )

    @http.route('/api/contacts/list', type='http', auth='public', methods=['GET'], csrf=False)
    def get_contacts_list(self, **kwargs):
        decoded_token, error_response = authenticate_request(http.request)
        if error_response:
            return Response(
                json.dumps(error_response),
                content_type='application/json',
                status=401
            )

        user_id = decoded_token.get("userId")
        rawpass = decoded_token.get("raw")

        try:
            decoded_password = base64.b64decode(rawpass.encode('utf-8')).decode('utf-8')

            headers = {
                "Authorization": f"Bearer {decoded_token['sub']}",
                "Content-Type": "application/json"
            }

            contacts_payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute_kw",
                    "args": [
                        ODOO_DB,
                        user_id,
                        decoded_password,
                        "res.partner",
                        "search_read",
                        [[]],  # empty domain = all contacts
                        {"fields": ["id", "name", "email", "phone"], "limit": 50}
                    ]
                }
            }

            contacts_response = requests.post(ODOO_URL, headers=headers, data=json.dumps(contacts_payload))
            contacts_data = contacts_response.json()

            if 'error' in contacts_data:
                return Response(
                    json.dumps({"statusCode": 500, "message": "Failed to fetch contacts", "data": contacts_data['error']}),
                    content_type='application/json',
                    status=500
                )

            contacts = contacts_data.get('result', [])

            return Response(
                json.dumps({
                    "statusCode": 200,
                    "message": "Contacts retrieved successfully",
                    "data": contacts
                }),
                content_type='application/json',
                status=200
            )

        except Exception as e:
            return Response(
                json.dumps({"statusCode": 500, "message": "Internal server error", "data": str(e)}),
                content_type='application/json',
                status=500
            )
