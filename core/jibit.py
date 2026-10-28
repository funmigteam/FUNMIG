from django.conf import settings

from django.core.cache import cache


import requests


class JibitError(Exception):

    pass


class JibitClient:

    BASE_URL = 'https://napi.jibit.ir/ppg/v3'

    ACCESS_TOKEN_CACHE_KEY = 'jibit_access_token'

    REFRESH_TOKEN_CACHE_KEY = 'jibit_refresh_token'


    def __init__(self):

        self.api_key = settings.JIBIT_API_KEY

        self.secret_key = settings.JIBIT_SECRET_KEY

        if not self.api_key or not self.secret_key:

            raise JibitError('تنظیمات درگاه جیبیت کامل نیست.')


    def _request(self, method, path, data=None, access_token=None):

        headers = {'Content-Type': 'application/json'}

        if access_token:

            headers['Authorization'] = f'Bearer {access_token}'


        try:

            response = requests.request(
                method,
                f'{self.BASE_URL}{path}',
                json=data or {},
                headers=headers,
                timeout=20,
            )

        except requests.RequestException as exc:

            raise JibitError('ارتباط با درگاه جیبیت برقرار نشد.') from exc


        try:

            payload = response.json()

        except ValueError as exc:

            raise JibitError('پاسخ نامعتبر از جیبیت دریافت شد.') from exc


        if response.status_code >= 400 or payload.get('errors'):

            errors = payload.get('errors') or []

            message = errors[0].get('message') if errors else None

            raise JibitError(message or 'درخواست جیبیت ناموفق بود.')


        return payload


    def _new_token(self):

        payload = self._request('POST', '/tokens', {
            'apiKey': self.api_key,
            'secretKey': self.secret_key,
        })

        access_token = payload.get('accessToken')

        refresh_token = payload.get('refreshToken')

        if not access_token:

            raise JibitError('توکن دسترسی جیبیت دریافت نشد.')


        cache.set(self.ACCESS_TOKEN_CACHE_KEY, access_token, 24 * 60 * 60 - 60)

        if refresh_token:

            cache.set(self.REFRESH_TOKEN_CACHE_KEY, refresh_token, 48 * 60 * 60 - 60)

        return access_token


    def _refresh_token(self):

        access_token = cache.get(self.ACCESS_TOKEN_CACHE_KEY)

        refresh_token = cache.get(self.REFRESH_TOKEN_CACHE_KEY)

        if not access_token or not refresh_token:

            return self._new_token()


        try:

            payload = self._request('POST', '/tokens/refresh', {
                'accessToken': access_token,
                'refreshToken': refresh_token,
            })

        except JibitError:

            return self._new_token()


        new_access_token = payload.get('accessToken')

        new_refresh_token = payload.get('refreshToken')

        if not new_access_token:

            return self._new_token()


        cache.set(self.ACCESS_TOKEN_CACHE_KEY, new_access_token, 24 * 60 * 60 - 60)

        if new_refresh_token:

            cache.set(self.REFRESH_TOKEN_CACHE_KEY, new_refresh_token, 48 * 60 * 60 - 60)

        return new_access_token


    def _access_token(self):

        return cache.get(self.ACCESS_TOKEN_CACHE_KEY) or self._refresh_token()


    def _authenticated_request(self, method, path, data=None, retry=True):

        access_token = self._access_token()

        try:

            return self._request(method, path, data, access_token)

        except JibitError as exc:

            if retry:

                cache.delete(self.ACCESS_TOKEN_CACHE_KEY)

                return self._authenticated_request(method, path, data, retry=False)

            raise exc


    def create_purchase(self, amount_rial, reference_number, user_identifier, callback_url, description=''):

        return self._authenticated_request('POST', '/purchases', {
            'amount': amount_rial,
            'callbackUrl': callback_url,
            'clientReferenceNumber': reference_number,
            'currency': 'IRR',
            'userIdentifier': user_identifier,
            'description': description,
            'additionalData': None,
        })


    def verify_purchase(self, purchase_id):

        return self._authenticated_request('GET', f'/purchases/{purchase_id}/verify')

