from mock import call, patch, Mock
from nose.tools import eq_

import btsync
from responses import ResponseFixtures



fixtures = ResponseFixtures()


class TestClient(object):
    def _make_client(self):
        return btsync.Client(
            host='127.0.0.1',
            port='1106',
            username='admin',
            password='password',
        )

    @patch('btsync.client._current_timestamp')
    @patch('btsync.client.requests.Session')
    def test_authenticate_should_send_auth_header_and_extract_token(
            self, session_class, current_timestamp):
        current_timestamp.return_value = 100000000
        session_class.return_value = mock_session = Mock()
        TOKEN = \
            u"_0y2dsNVJ_ww1pPcfHxMpro6OLG73jHTWOob9kku9DRLhe-pz_M0a_lHVFIAAAAA"
        mock_session.post.return_value.text = (
            u"<html>"
            u"<div id='token' style='display:none;'>"
            u"{token}"
            u"</div>"
            u"</html>".format(token=TOKEN))

        client = self._make_client()
        eq_(mock_session.auth, ('admin', 'password'))
        eq_(mock_session.post.call_args_list,
            [call('http://127.0.0.1:1106/gui/token.html?t=100000000')])
        eq_(TOKEN, client._token)

    @patch('btsync.client.Client._get_token')
    @patch('btsync.client._current_timestamp')
    @patch('btsync.client.requests.Session')
    def test_get_os_type(self, session_class, current_timestamp, get_token):
        current_timestamp.return_value = 999
        session_class.return_value = mock_session = Mock()
        get_token.return_value = u'T'
        mock_session.get.return_value.text = fixtures.GETOSTYPE

        client = self._make_client()
        eq_('linux', client.os_type)
        eq_([call('http://127.0.0.1:1106/gui/?action=getostype&token=T&t=999')],
            mock_session.get.call_args_list)

    @patch('btsync.client.Client._get_token')
    @patch('btsync.client._current_timestamp')
    @patch('btsync.client.requests.Session')
    def test_get_version(self, session_class, current_timestamp, get_token):
        current_timestamp.return_value = 999
        session_class.return_value = mock_session = Mock()
        get_token.return_value = u'T'
        mock_session.get.return_value.text = fixtures.GETVERSION

        client = self._make_client()
        eq_('121', client.version)
        eq_([call('http://127.0.0.1:1106/gui/?action=getversion&token=T&t=999')],
            mock_session.get.call_args_list)

    @patch('btsync.client.Client._get_token')
    @patch('btsync.client._current_timestamp')
    @patch('btsync.client.requests.Session')
    def test_new_version(self, session_class, current_timestamp, get_token):
        current_timestamp.return_value = 999
        session_class.return_value = mock_session = Mock()
        get_token.return_value = u'T'
        mock_session.get.return_value.text = fixtures.CHECKNEWVERSION

        client = self._make_client()
        eq_({'url': '', 'version': 0}, client.new_version)
        eq_([call('http://127.0.0.1:1106/gui/?action=checknewversion&token=T&t=999')],
            mock_session.get.call_args_list)

    @patch('btsync.client.Client._get_token')
    @patch('btsync.client._current_timestamp')
    @patch('btsync.client.requests.Session')
    def test_sync_folders(self, session_class, current_timestamp, get_token):
        current_timestamp.return_value = 999
        session_class.return_value = mock_session = Mock()
        get_token.return_value = u'T'
        mock_session.get.return_value.text = fixtures.GETSYNCFOLDERS
        client = self._make_client()
        client.sync_folders
        # eq_({'url': '', 'version': 0}, client.new_version)
        eq_([call('http://127.0.0.1:1106/gui/?action=getsyncfolders&token=T&t=999')],
            mock_session.get.call_args_list)
