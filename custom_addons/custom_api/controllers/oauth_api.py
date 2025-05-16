# import json
# import jwt
# import datetime
# from odoo import http
# from werkzeug.wrappers import Response
# import requests
# import base64

# SECRET_KEY = "7942f642-4e94-4a8a-afc6-2815bac9fa78"
# ODOO_URL = "http://dev.digitalcenter.com/jsonrpc"
# ODOO_DB = "odoo_dev"

# OAUTH2_CLIENTS = {
#     "7815241d-c3a6-41e6-85fd-5ab59b13e805": "83c9f977-ccaf-4dfd-944b-3c91d17ed4a0"
# }

# class AuthController(http.Controller):

#     @http.route('/api/auth/login', type='http', auth='public', methods=['POST'], csrf=False)
#     def odoo_login(self, **kwargs):
#         try:
#             data = http.request.jsonrequest
#             client_id = data.get('client_id')
#             client_secret = data.get('client_secret')
#             grant_type = data.get('grant_type')

#             if grant_type != "password":
#                 return Response(
#                     json.dumps({"statusCode": 400, "message": "Unsupported grant_type", "data": None}),
#                     content_type='application/json',
#                     status=400
#                 )

#             if client_id not in OAUTH2_CLIENTS or OAUTH2_CLIENTS[client_id] != client_secret:
#                 return Response(
#                     json.dumps({"statusCode": 401, "message": "Invalid client credentials", "data": None}),
#                     content_type='application/json',
#                     status=401
#                 )

#             if 'username' not in data or 'password' not in data:
#                 return Response(
#                     json.dumps({"statusCode": 400, "message": "Missing username or password", "data": None}),
#                     content_type='application/json',
#                     status=400
#                 )

#             headers = {"Content-Type": "application/json"}
#             login_payload = {
#                 "jsonrpc": "2.0",
#                 "method": "call",
#                 "params": {
#                     "service": "common",
#                     "method": "login",
#                     "args": [ODOO_DB, data['username'], data['password']]
#                 },
#                 "id": 1
#             }

#             login_response = requests.post(ODOO_URL, headers=headers, data=json.dumps(login_payload))
#             login_data = login_response.json()

#             if 'error' in login_data:
#                 return Response(
#                     json.dumps({"statusCode": 401, "message": "Invalid credentials", "data": None}),
#                     content_type='application/json',
#                     status=401
#                 )

#             user_id = login_data['result']

#             user_details_payload = {
#                 "jsonrpc": "2.0",
#                 "method": "call",
#                 "params": {
#                     "service": "object",
#                     "method": "execute_kw",
#                     "args": [
#                         ODOO_DB,
#                         user_id,
#                         data['password'],
#                         "res.users",
#                         "read",
#                         [[user_id]],
#                         {"fields": ["id", "name", "email"]}
#                     ]
#                 },
#                 "id": 2
#             }

#             user_details_response = requests.post(ODOO_URL, headers=headers, data=json.dumps(user_details_payload))
#             user_details_data = user_details_response.json()

#             if 'error' in user_details_data:
#                 return Response(
#                     json.dumps({"statusCode": 500, "message": "Failed to fetch user details", "data": None}),
#                     content_type='application/json',
#                     status=500
#                 )

#             user_details = user_details_data.get('result', [{}])[0]
#             encoded_password = base64.b64encode(data['password'].encode()).decode()
#             http.request.session['password'] = data['password']

#             payload = {
#                 "sub": data['username'],
#                 "userId": user_id,
#                 "raw": encoded_password,
#                 "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
#             }
#             access_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

#             return Response(
#                 json.dumps({
#                     "statusCode": 200,
#                     "message": "Login successful",
#                     "data": {
#                         "access_token": access_token,
#                         "token_type": "Bearer",
#                         "expires_in": 7200,
#                         "userId": user_id,
#                         "name": user_details.get("name"),
#                         "email": user_details.get("email")
#                     }
#                 }),
#                 content_type='application/json',
#                 status=200
#             )

#         except Exception as e:
#             return Response(
#                 json.dumps({"statusCode": 500, "message": "Internal server error", "data": str(e)}),
#                 content_type='application/json',
#                 status=500
#             )
