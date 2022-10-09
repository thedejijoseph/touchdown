
import random
import string

from django.template import loader

from rest_framework.authentication import TokenAuthentication

def make_auth_code():
    random_selection = random.choices(string.ascii_uppercase, k=5)
    code = "".join(random_selection)

    return code

make_random_code = make_auth_code

def make_default_username():
    random_selection = random.choices(string.ascii_lowercase, k=9)
    username = "u_" + "".join(random_selection)

    return username

def render_email_verification_template_text(context: dict):
    """Render email verification template, in plain text"""

    loaded_template = loader.get_template("accounts/email_verification.txt")
    content = loaded_template.render(context)

    return content

def render_email_verification_template_html(context: dict):
    """Render email verification template, in HTML"""

    loaded_template = loader.get_template("accounts/email_verification.html")
    content = loaded_template.render(context)

    return content

class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'
