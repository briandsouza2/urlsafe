import os
import tempfile
from unittest import TestCase
import logging
import flask_unittest
import json
import pytest

from urlsafe.app import create_app, init_app
import urllib
# @pytest.fixture
# def client():
#     test_app = create_app({'TESTING': True})

#     with test_app.test_client() as client:
#         yield client


class TestURLSafe(flask_unittest.ClientTestCase):

    app = create_app({'TESTING': True, 'DATADIR': './data'})

    def test_blocked_url(self, client):
        """Start with a blank database."""
        self.app.logger.setLevel(logging.DEBUG)
        with self.app.test_client() as client:
            init_app()
            path_and_query_string="somepath?param1=val1&param2=val2"
            param = urllib.parse.quote(path_and_query_string, safe='')
            rv = client.get(f'/urlinfo/1/hostname1_port/{param}')
        expected_response = {'Blocked': True}
        self.assertEqual(json.loads(rv.data.decode('utf-8')), expected_response)

    def test_safe_url(self, client):
        """Start with a blank database."""
        self.app.logger.setLevel(logging.DEBUG)
        with self.app.test_client() as client:
            init_app()
            path_and_query_string="goodpath?param1=val1&param2=val2"
            param = urllib.parse.quote(path_and_query_string, safe='')
            rv = client.get(f'/urlinfo/1/hostname1_port/{param}')
        expected_response = {'Blocked': False}
        self.assertEqual(json.loads(rv.data.decode('utf-8')), expected_response)

    def test_blocked_url_evalparam(self, client):
        """Start with a blank database."""
        self.app.logger.setLevel(logging.DEBUG)
        with self.app.test_client() as client:
            init_app()
            path_and_query_string="someotherpath/somemorepaths/evenmorepaths;someparam?param2=val2&param1=val1&param3=val3#somefrag"
            param = urllib.parse.quote(path_and_query_string, safe='')
            #import pdb; pdb.set_trace()

            rv = client.get(f'/urlinfo/2/hostname1_port/{param}')
        expected_response = {'Blocked': True, 'Match:': 'someotherpath/somemorepaths/evenmorepaths?param1=val1&param2=val2&param3=val3'}
        self.assertEqual(json.loads(rv.data.decode('utf-8')), expected_response)