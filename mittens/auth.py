import base64
import binascii

from flask_login import LoginManager

from mittens.logs.models import Tenant

login_manager = LoginManager()


@login_manager.request_loader
def load_tenant_from_token(request):
    """Simple token based auth. Provide a (base64-encoded or not) api_key
    in the `Authorization` header to authenticate a Tenant.

    Since hash algorithms and HMAC don't provide hexadecimal string outputs,
    and we're being agnostic, we're checking for a base64-encoded api_key in
    the Authorization header.

    Returns:
        Either an authenticated Tenant or None.
    """
    return get_tenant_from_header(request.headers.get('Authorization'))


def get_tenant_from_header(auth_header: str):
    """Inner function, allowing for unit testing without a request context."""
    if auth_header:
        api_key = auth_header.replace('Basic ', '', 1).strip()
        try:
            api_key = base64.b64decode(api_key)
        except (TypeError, binascii.Error):
            pass
        tenant = Tenant.query.filter_by(api_key=api_key).first()
        if tenant:
            return tenant
    return None
