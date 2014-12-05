# Copyright 2014 Infoblox
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import collections

from mock import MagicMock

from designate import tests
from designate.backend.impl_infoblox import exceptions
from designate.tests.test_backend import BackendTestMixin
from designate import utils


class InfobloxBackendTestCase(tests.TestCase, BackendTestMixin):
    def create_record_primitiv_fixture(self, ip):
        def to_primitive():
            return {
                'designate_object.data': {
                    'data': ip,
                    'name': 'some.example.com'
                }
            }
        return to_primitive

    def get_domain_fixture(self):
        return super(InfobloxBackendTestCase, self).get_domain_fixture(
            values={
                'name': 'test.example.com'
            }
        )

    def get_recordset_fixture(self, domain_name, record_type):
        def obj_get_changes():
            return {
                'records': [
                    collections.namedtuple(
                        'RecordSet', {'data': '172.25.1.1'}
                    )(data='172.25.1.1')
                ]
            }

        values = super(InfobloxBackendTestCase, self).get_recordset_fixture(
            domain_name=domain_name,
            values={
                'id': utils.generate_uuid(),
                'ttl': 123456,
                'to_primitive': self.create_record_primitiv_fixture(
                    '172.25.1.2'),
                'obj_get_changes': obj_get_changes
            }
        )
        return collections.namedtuple('RecordSet', values)(**values)

    def get_record_fixture(self, recordset_type):

        values = super(InfobloxBackendTestCase, self).get_record_fixture(
            recordset_type,
            values={
                'id': utils.generate_uuid(),
                'to_primitive': self.create_record_primitiv_fixture(
                    '172.25.1.1')
            }
        )
        return collections.namedtuple('Record', values)(**values)

    def get_server_fixture(self):
        values = super(InfobloxBackendTestCase, self).get_server_fixture()
        return collections.namedtuple('Server', values)(**values)

    def setUp(self):
        super(InfobloxBackendTestCase, self).setUp()
        self.config(backend_driver='infoblox', group='service:agent')
        self.backend = self.get_backend_driver()
        self.backend.start()
        self.backend.infoblox = MagicMock()

    def test_create_server(self):
        context = self.get_context()
        server = self.get_server_fixture()
        self.backend.create_server(context, server)

    def test_create_server_fail(self):
        self.backend.infoblox.get_member = MagicMock(
            return_value=[])

        context = self.get_context()
        server = self.get_server_fixture()
        self.assertRaises(exceptions.NoInfobloxMemberAvailable,
                          self.backend.create_server, context, server)

    def test_update_server(self):
        context = self.get_context()
        server = self.get_server_fixture()
        self.backend.create_server(context, server)
        self.backend.update_server(context, server)

    def test_update_server_fail(self):
        context = self.get_context()
        server = self.get_server_fixture()
        self.backend.create_server(context, server)

        self.backend.infoblox.get_member = MagicMock(
            return_value=[])
        self.assertRaises(exceptions.NoInfobloxMemberAvailable,
                          self.backend.update_server, context, server)

    def test_delete_server(self):
        context = self.get_context()
        server = self.get_server_fixture()
        self.backend.create_server(context, server)
        self.backend.delete_server(context, server)

    def test_create_domain(self):
        context = self.get_context()
        server = self.get_server_fixture()
        domain = self.get_domain_fixture()
        self.backend.create_server(context, server)
        self.backend.create_domain(context, domain)

    def test_update_domain(self):
        context = self.get_context()
        server = self.get_server_fixture()
        domain = self.get_domain_fixture()
        self.backend.create_server(context, server)
        self.backend.create_domain(context, domain)
        self.backend.update_domain(context, domain)

    def test_delete_domain(self):
        context = self.get_context()
        server = self.get_server_fixture()
        domain = self.get_domain_fixture()
        self.backend.create_server(context, server)
        self.backend.create_domain(context, domain)
        self.backend.delete_domain(context, domain)

    def test_create_record(self):
        context = self.get_context()
        server = self.get_server_fixture()
        domain = self.get_domain_fixture()

        recordset = self.get_recordset_fixture(domain['name'], "A")
        record = self.get_record_fixture("A")

        self.backend.create_server(context, server)
        self.backend.create_domain(context, domain)
        self.backend.create_record(context, domain, recordset, record)

    def test_delete_record(self):
        context = self.get_context()
        server = self.get_server_fixture()
        domain = self.get_domain_fixture()

        recordset = self.get_recordset_fixture(domain['name'], "A")
        record = self.get_record_fixture("A")

        self.backend.create_server(context, server)
        self.backend.create_domain(context, domain)
        self.backend.create_record(context, domain, recordset, record)

        self.backend.delete_record(context, domain, recordset, record)

    def test_update_record(self):
        context = self.get_context()
        server = self.get_server_fixture()
        domain = self.get_domain_fixture()

        recordset = self.get_recordset_fixture(domain['name'], "A")
        record = self.get_record_fixture("A")

        self.backend.create_server(context, server)
        self.backend.create_domain(context, domain)
        self.backend.create_record(context, domain, recordset, record)
        self.backend.update_record(context, domain, recordset, record)
