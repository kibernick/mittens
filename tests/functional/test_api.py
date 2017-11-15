from flask import url_for, json
import pytest

from mittens.api.models import ErrorLog


class TestLogList:

    @pytest.mark.parametrize('logs', [
        ({'id': 1, 'content': "bla"},),
        ({'id': 1, 'content': "bla"},
         {'id': 2, 'content': "bla", 'meta': {'7': 9}}),
    ])
    def test_get_all_logs(self, app, session, logs, client):
        created_ids = []
        for log_dict in logs:
            _log = ErrorLog(**log_dict)
            session.add(_log)
            session.commit()
            created_ids.append(_log.id)

        res = client.get(url_for('api.log-list'))
        assert res.status_code == 200
        assert [l['id'] for l in res.json] == created_ids

    @pytest.mark.parametrize('logdict', [
        {'content': "something"},
        {'content': "something", 'meta': None},
        {'content': "something", 'meta': {'c': 4}},
    ])
    def test_create_log(self, app, session, logdict, client):
        res = client.post(url_for('api.log-list'),
                          data=json.dumps(logdict),
                          content_type='application/json')

        assert res.status_code == 201
        for k, v in logdict.items():
            assert res.json[k] == v

    @pytest.mark.parametrize('req_data,req_ct', [
        ({'nonsense': False}, 'application/json'),
        ({'content': None}, 'application/json'),
        ({'content': ""}, 'application/json'),
        ({'content': "notjson"}, None),
    ])
    def test_wrong_arguments(self, app, session, client, req_data, req_ct):
        res = client.post(url_for('api.log-list'),
                          data=json.dumps(req_data),
                          content_type=req_ct)

        assert res.status_code == 400


class TestLogDetails:

    @pytest.mark.parametrize('existing', [
        {'content': "something"},
        {'content': "something", 'meta': None},
        {'content': "something", 'meta': {'c': 4}},
    ])
    def test_get_log_details(self, app, session, existing, client):
        _log = ErrorLog(**existing)
        session.add(_log)
        session.commit()

        res = client.get(url_for('api.log-details', log_id=_log.id))
        assert res.status_code == 200
        assert res.json['id'] == _log.id
        assert res.json['content'] == _log.content
        assert res.json['meta'] == _log.meta

    def test_get_nonexistent(self, app, session, client):
        assert ErrorLog.query.count() == 0

        res = client.get(url_for('api.log-details', log_id=1))
        assert res.status_code == 404
