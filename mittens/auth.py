import base64
import binascii

from flask_login import LoginManager

from mittens.logs.models import Tenant

login_manager = LoginManager()


@login_manager.request_loader
def load_tenant_from_token(request):
    """Simple token based auth. Provide a (base64-encoded or not) api_key
    in the `Authorization` header to authenticate a Tenant.

    Returns:
        Either an authenticated Tenant or None.
    """
    auth_header = request.headers.get('Authorization')
    if auth_header:
        api_key = auth_header.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except (TypeError, binascii.Error):
            pass
        tenant = Tenant.query.filter_by(api_key=api_key).first()
        if tenant:
            return tenant
    return None
