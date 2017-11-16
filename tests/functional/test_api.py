from flask import url_for, json
import pytest

from mittens.logs.models import ErrorLog, Tenant


class TestLogList:

    @pytest.mark.parametrize('logs', [
        ({'id': 1, 'content': "bla"},),
        ({'id': 1, 'content': "bla"},
         {'id': 2, 'content': "bla", 'meta': {'7': 9}}),
    ])
    def test_get_all_logs(self, app, session, logs, client, tenant):
        created_ids = []
        for log_dict in logs:
            _log = ErrorLog(**log_dict)
            _log.tenant = tenant
            session.add(_log)
            session.commit()
            created_ids.append(_log.id)

        res = client.get(url_for('api.log-list'), headers={'Authorization': f"Basic {tenant.api_key}"})
        assert res.status_code == 200
        assert [l['id'] for l in res.json] == created_ids

    def test_do_not_retrieve_other_logs(self, app, session, client, tenant):
        other_tenant = Tenant(api_key=f"NOT{tenant.api_key}")
        other_log = ErrorLog(content="asdf", tenant=other_tenant)
        my_log = ErrorLog(content="qwer", tenant=tenant)
        session.add(other_tenant)
        session.add(other_log)
        session.add(my_log)
        session.commit()

        res = client.get(url_for('api.log-list'),
                         headers={'Authorization': f"Basic {tenant.api_key}", 'X-Fields': 'id'})
        assert res.status_code == 200
        assert res.json == [{'id': my_log.id}]

    def test_list_with_wrong_tenant(self, app, session, client, tenant):
        res = client.get(url_for('api.log-list'), headers={'Authorization': f"Basic Z{tenant.api_key}"})
        assert res.status_code == 401

    @pytest.mark.parametrize('logdict', [
        {'content': "something"},
        {'content': "something", 'meta': None},
        {'content': "something", 'meta': {'c': 4}},
    ])
    def test_create_log(self, app, session, logdict, client, tenant):
        res = client.post(url_for('api.log-list'),
                          data=json.dumps(logdict),
                          content_type='application/json',
                          headers={'Authorization': f"Basic {tenant.api_key}"})

        assert res.status_code == 201
        for k, v in logdict.items():
            assert res.json[k] == v

    @pytest.mark.parametrize('req_data,req_ct', [
        ({'nonsense': False}, 'application/json'),
        ({'content': None}, 'application/json'),
        ({'content': ""}, 'application/json'),
        ({'content': "notjson"}, None),
    ])
    def test_wrong_arguments(self, app, session, client, req_data, req_ct, tenant):
        res = client.post(url_for('api.log-list'),
                          data=json.dumps(req_data),
                          content_type=req_ct,
                          headers={'Authorization': f"Basic {tenant.api_key}"})

        assert res.status_code == 400

    def test_create_with_wrong_tenant(self, app, session, client, tenant):
        res = client.post(url_for('api.log-list'),
                          data=json.dumps({'content': "1"}),
                          content_type='application/json',
                          headers={'Authorization': f"Basic Z{tenant.api_key}"})

        assert res.status_code == 401


class TestLogDetails:

    @pytest.mark.parametrize('existing', [
        {'content': "something"},
        {'content': "something", 'meta': None},
        {'content': "something", 'meta': {'c': 4}},
    ])
    def test_get_log_details(self, app, session, existing, client, tenant):
        _log = ErrorLog(**existing)
        _log.tenant = tenant
        session.add(_log)
        session.commit()

        res = client.get(url_for('api.log-details', log_id=_log.id),
                         headers={'Authorization': f"Basic {tenant.api_key}"})
        assert res.status_code == 200
        assert res.json['id'] == _log.id
        assert res.json['content'] == _log.content
        assert res.json['meta'] == _log.meta

    def test_get_nonexistent(self, app, session, client, tenant):
        assert ErrorLog.query.count() == 0

        res = client.get(url_for('api.log-details', log_id=1),
                         headers={'Authorization': f"Basic {tenant.api_key}"})
        assert res.status_code == 404

    def test_get_with_wrong_tenant(self, app, session, client, tenant):
        res = client.get(url_for('api.log-details', log_id=1), headers={'Authorization': f"Basic Z{tenant.api_key}"})
        assert res.status_code == 401
