const routes = {
  ABOUT: '/about',
  DASHBOARD: '/',
  SIGNUP: '/signup',
  PHONE_LOGIN: '/signup?auth_mode=otp',
  LOGIN: '/login',
  OTP: '/login?auth_mode=otp',
  FORGOT_PASSWORD: '/forgot-password',
  RESET_PASSWORD: '/accounts/:accountId/reset_password',
  PROFILE: '/profile',
  PROFILE_SETTINGS: '/profile/settings',
  TASKS: '/tasks',
};

export default routes;
