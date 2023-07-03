from flask_restx import Namespace, Resource, fields
import requests
from http import HTTPStatus
from flask import request

bvn_namespace = Namespace('bvn-verify', description="Namespace for bvn verifications")
bvn_verification_model = bvn_namespace.model('BVN_VERIFY', {
    'id': fields.String(description='valid bvn id number', required=True)
})

#bvn verification with id
@bvn_namespace.route('/bvn-verification')
class BVN_VERIFICATION(Resource):
    @bvn_namespace.expect(bvn_verification_model)
    def post(self):
        '''
            Bvn Verification
        '''
        
        data_field = request.get_json()
        valid_id_number = data_field['id']
        
        if len(valid_id_number) == 11:
            response = {
                'message': 'ok'
            }
            headers = {
                #Token created by YouVerify
                'token': 'string'
            }
            
            body = {
                "id": "",
                "metadata": {
                    "requestId": ""
                },
                "isSubjectConsent": True,
                "premiumBVN": False
            }
            url = "https://api.youverify.co/v2/api/identity/ng/bvn"
            response = requests.post(url, headers=headers, json=body)
            json_result = response.json()
            
            return json_result, HTTPStatus.OK
        else:
            response = {
                "error": "Please BVN isn/t up to 11. Check and try again"
            }
            
            return response, HTTPStatus.UNAUTHORIZED
        