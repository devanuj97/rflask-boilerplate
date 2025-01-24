import { Account, AccessToken, ApiResponse } from '../types';

import APIService from './api.service';

export default class AccountService extends APIService {
  getAccountDetails = async (
    userAccessToken: AccessToken,
  ): Promise<ApiResponse<Account>> =>
    this.apiClient.get(`/accounts/${userAccessToken.accountId}`, {
      headers: {
        Authorization: `Bearer ${userAccessToken.token}`,
      },
    });

  deleteAccount = async (
    userAccessToken: AccessToken,
  ): Promise<ApiResponse<null>> =>
    this.apiClient.delete(`/accounts/${userAccessToken.accountId}`, {
      headers: {
        Authorization: `Bearer ${userAccessToken.token}`,
      },
    });
}
