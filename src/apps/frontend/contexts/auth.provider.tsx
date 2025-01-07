import React, {
  createContext,
  PropsWithChildren,
  ReactNode,
  useContext,
} from 'react';

import { AuthService } from '../services';
import { AccessToken, ApiResponse, AsyncError, PhoneNumber } from '../types';

import useAsync from './async.hook';

type AuthContextType = {
  isLoginLoading: boolean;
  isSendOTPLoading: boolean;
  isSignupLoading: boolean;
  isUserAuthenticated: () => boolean;
  isVerifyOTPLoading: boolean;
  login: (
    username: string,
    password: string,
  ) => Promise<AccessToken | undefined>;
  loginError: AsyncError | undefined;
  loginResult: AccessToken | undefined;
  logout: () => void;
  sendOTP: (phoneNumber: PhoneNumber) => Promise<void>;
  sendOTPError: AsyncError | undefined;
  signup: (
    firstName: string,
    lastName: string,
    username: string,
    password: string,
  ) => Promise<void>;
  signupError: AsyncError | undefined;
  verifyOTP: (
    phoneNumber: PhoneNumber,
    otp: string,
  ) => Promise<AccessToken | undefined>;
  verifyOTPError: AsyncError | undefined;
  verifyOTPResult: AccessToken | undefined;
};

const AuthContext = createContext<AuthContextType | null>(null);

const authService = new AuthService();

export const useAuthContext = (): AuthContextType =>
  useContext(AuthContext) as AuthContextType;

const signupFn = async (
  firstName: string,
  lastName: string,
  username: string,
  password: string,
): Promise<ApiResponse<void>> =>
  authService.signup(firstName, lastName, username, password);

const loginFn = async (
  username: string,
  password: string,
): Promise<ApiResponse<AccessToken>> => {
  const result = await authService.login(username, password);
  if (result.data) {
    localStorage.setItem('access-token', JSON.stringify(result.data));
  }
  return result;
};

const logoutFn = (): void => localStorage.removeItem('access-token');

const getAccessToken = (): AccessToken =>
  JSON.parse(localStorage.getItem('access-token') || 'null') as AccessToken;

const isUserAuthenticated = () => !!getAccessToken();

const sendOTPFn = async (
  phoneNumber: PhoneNumber,
): Promise<ApiResponse<void>> => authService.sendOTP(phoneNumber);

const verifyOTPFn = async (
  phoneNumber: PhoneNumber,
  otp: string,
): Promise<ApiResponse<AccessToken>> => {
  const result = await authService.verifyOTP(phoneNumber, otp);
  if (result.data) {
    localStorage.setItem('access-token', JSON.stringify(result.data));
  }
  return result;
};

export const AuthProvider: React.FC<PropsWithChildren<ReactNode>> = ({
  children,
}) => {
  const {
    asyncCallback: signup,
    error: signupError,
    isLoading: isSignupLoading,
  } = useAsync(signupFn);

  const {
    isLoading: isLoginLoading,
    error: loginError,
    result: loginResult,
    asyncCallback: login,
  } = useAsync(loginFn);

  const {
    isLoading: isSendOTPLoading,
    error: sendOTPError,
    asyncCallback: sendOTP,
  } = useAsync(sendOTPFn);

  const {
    isLoading: isVerifyOTPLoading,
    error: verifyOTPError,
    result: verifyOTPResult,
    asyncCallback: verifyOTP,
  } = useAsync(verifyOTPFn);

  return (
    <AuthContext.Provider
      value={{
        isLoginLoading,
        isSendOTPLoading,
        isSignupLoading,
        isUserAuthenticated,
        isVerifyOTPLoading,
        login,
        loginError,
        loginResult,
        logout: logoutFn,
        sendOTP,
        sendOTPError,
        signup,
        signupError,
        verifyOTP,
        verifyOTPError,
        verifyOTPResult,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
