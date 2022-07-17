
from typing import Dict, Any

from django.conf import settings

from mailjet_rest import Client

from .util import make_random_code

env = settings.ENV

API_KEY = env.str('MJ_APIKEY_PUBLIC')
API_SECRET = env.str('MJ_APIKEY_PRIVATE')

mailjet = Client(auth=(API_KEY, API_SECRET), version='v3.1')


def send_email(
    to: str,
    subject: str,
    plain_text: str,
    html: str,
    name: str = "",
) -> Dict[str, Any]:

    """Send an email through Mailjet"""

    name = name if name != "" else "BlankName"
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "wrecodde@gmail.com",
                    "Name": "Deji"
                },
                "To": [
                    {
                        "Email": to,
                        "Name": name
                    }
                ],
                "Subject": subject,
                "TextPart": plain_text,
                "HTMLPart": html,
                "CustomID": f"{to}_{make_random_code()}"
            }
        ]
    }

    result = mailjet.send.create(data=data)

    return result
