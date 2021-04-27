import pytest

from mittens.auth import get_tenant_from_header


class TestTenantAuth:
    @pytest.mark.parametrize(
        "auth_header",
        [
            "Basic 9779344518546cdaf4",
            "Basic OTc3OTM0NDUxODU0NmNkYWY0",
        ],
    )
    def test_retrieve_tenant(self, auth_header, tenant):
        _tenant = get_tenant_from_header(auth_header)
        assert _tenant is not None
        assert _tenant == tenant

    @pytest.mark.parametrize(
        "auth_header",
        [
            None,
            "",
            "justwrong",
            "Basic ",
            "Basic nonexistent",
            "Basic bm9uZXhpc3RlbnQ=",
        ],
    )
    def test_invalid_header(self, auth_header, tenant):
        _tenant = get_tenant_from_header(auth_header)
        assert _tenant is None
