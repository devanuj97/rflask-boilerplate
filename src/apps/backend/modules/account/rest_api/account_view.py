from dataclasses import asdict

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.access_token.rest_api.access_auth_middleware import access_auth_middleware
from modules.account.account_service import AccountService
from modules.account.types import (
    CreateAccountByPhoneNumberParams,
    CreateAccountByUsernameAndPasswordParams,
    CreateAccountParams,
    ResetPasswordParams,
    SearchAccountByIdParams,
)
from modules.cleanup.cleanup_service import CleanupService


class AccountView(MethodView):
    def post(self) -> ResponseReturnValue:
        request_data = request.get_json()
        account_params: CreateAccountParams
        if "phone_number" in request_data:
            account_params = CreateAccountByPhoneNumberParams(**request_data)
            account = AccountService.get_or_create_account_by_phone_number(params=account_params)
        elif "username" in request_data and "password" in request_data:
            account_params = CreateAccountByUsernameAndPasswordParams(**request_data)
            account = AccountService.create_account_by_username_and_password(params=account_params)
        account_dict = asdict(account)
        return jsonify(account_dict), 201

    @access_auth_middleware
    def get(self, id: str) -> ResponseReturnValue:
        account_params = SearchAccountByIdParams(id=id)
        account = AccountService.get_account_by_id(params=account_params)
        account_dict = asdict(account)
        return jsonify(account_dict), 200

    def patch(self, id: str) -> ResponseReturnValue:
        request_data = request.get_json()
        reset_account_params = ResetPasswordParams(account_id=id, **request_data)
        account = AccountService.reset_account_password(params=reset_account_params)
        account_dict = asdict(account)
        return jsonify(account_dict), 200

    @access_auth_middleware
    def delete(self, id: str) -> ResponseReturnValue:
        account_params = SearchAccountByIdParams(id=id)
        CleanupService.execute_cleanup_hooks(params=account_params)
        return "", 200
