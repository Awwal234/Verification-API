from flask_restx import Namespace, Resource, fields
import requests
from flask import request
from http import HTTPStatus

bank_namespace = Namespace('bank', description="Bank schema space")
verify_model = bank_namespace.model('Bank', {
    'accountNumber': fields.String(required=True, description='User unique account number'),
    'bankCode': fields.String(required=True, description='User unique bank code')
})


@bank_namespace.route('/get_banks')
class getBanks(Resource):
    def post(self):
        '''
            Get Verified Banks
        '''

        url = "https://api.youverify.co/v2/api/identity/ng/bank-account-number/bank-list"
        headers = {
            "token": ""
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        return data, HTTPStatus.OK

# route for bank verification


@bank_namespace.route('/verify-banks')
class verifyBanks(Resource):
    @bank_namespace.expect(verify_model)
    def post(self):
        '''
            Verify incoming banks from user
        '''

        data_field = request.get_json()
        account_number = data_field['accountNumber']
        bank_code = data_field['bankCode']

        url = "https://api.youverify.co/v2/api/identity/ng/bank-account-number/resolve"
        headers = {
            "token": ""
        }
        body = {
            "accountNumber": account_number,
            "bankCode": bank_code,
            "isSubjectConsent": True
        }

        response = requests.post(url, headers=headers, json=body)
        data = response.json()

        return data, HTTPStatus.OK
