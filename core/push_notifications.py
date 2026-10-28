import json


import time


import base64


import requests


import jwt


from cryptography.hazmat.primitives import serialization


from cryptography.hazmat.primitives.asymmetric import ec


from cryptography.hazmat.backends import default_backend


from django.conf import settings


from .models import PushSubscription


def get_vapid_public_key():


    return getattr(settings, 'VAPID_PUBLIC_KEY', '')


def send_push_notification(user, title, message, url='/'):


    subscriptions = PushSubscription.objects.filter(user=user)


    vapid_private_key = getattr(settings, 'VAPID_PRIVATE_KEY', '')


    vapid_public_key = getattr(settings, 'VAPID_PUBLIC_KEY', '')


    vapid_subject = getattr(settings, 'VAPID_SUBJECT', 'mailto:admin@funmig.com')


    if not vapid_private_key or not vapid_public_key:


        return False


    payload = json.dumps({


        'title': title,


        'body': message,


        'url': url,


        'tag': 'funmig-notification',


        'icon': '/static/logo.png'


    })


    for sub in subscriptions:


        try:


            subscription = sub.subscription_data


            endpoint = subscription.get('endpoint', '')


            if not endpoint:


                continue


            from urllib.parse import urlparse


            parsed = urlparse(endpoint)


            audience = f"{parsed.scheme}://{parsed.netloc}"


            now = int(time.time())


            try:


                private_key_bytes = base64.urlsafe_b64decode(vapid_private_key + '==')


            except:


                private_key_bytes = vapid_private_key.encode()


            private_key = serialization.load_pem_private_key(


                private_key_bytes,


                password=None,


                backend=default_backend()


            )


            public_numbers = private_key.public_key().public_numbers()


            token = jwt.encode(


                {


                    'aud': audience,


                    'exp': now + 43200,


                    'sub': vapid_subject


                },


                private_key,


                algorithm='ES256',


                headers={


                    'typ': 'JWT',


                    'alg': 'ES256'


                }


            )


            headers = {


                'Content-Type': 'application/json',


                'Authorization': f'vapid t={token}'


            }


            response = requests.post(endpoint, data=payload, headers=headers)


            if response.status_code == 410:


                sub.delete()


        except Exception as e:


            print(f"Push error: {e}")


    return True

