from dataclasses import asdict

from modules.account.types import PhoneNumber
from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.access_token.access_token_service import AccessTokenService
from modules.access_token.types import (
    CreateAccessTokenParams,
    EmailBasedAuthAccessTokenRequestParams,
    OTPBasedAuthAccessTokenRequestParams,
)


class AccessTokenView(MethodView):
    def post(self) -> ResponseReturnValue:
        request_data = request.get_json()
        access_token_params: CreateAccessTokenParams
        if "phone_number" in request_data and "otp_code" in request_data:
            access_token_params = OTPBasedAuthAccessTokenRequestParams(
                phone_number=PhoneNumber(**request_data["phone_number"]), otp_code=request_data["otp_code"]
            )
            access_token = AccessTokenService.create_access_token_by_phone_number(params=access_token_params)
        elif "username" in request_data and "password" in request_data:
            access_token_params = EmailBasedAuthAccessTokenRequestParams(**request_data)
            access_token = AccessTokenService.create_access_token_by_username_and_password(params=access_token_params)
        access_token_dict = asdict(access_token)
        return jsonify(access_token_dict), 201
