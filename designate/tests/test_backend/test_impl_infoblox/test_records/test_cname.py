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
from mock import ANY

from designate import tests
from designate.backend.impl_infoblox.records import cname
from designate.tests.test_backend import BackendTestMixin
from designate import utils


class CNameRecordTestCase(tests.TestCase, BackendTestMixin):
    def create_record_primitive(self, ip):
        def to_primitive():
            return {
                'designate_object.data': {
                    'data': ip,
                    'name': 'some.example.com'
                }
            }
        return to_primitive

    def get_domain_fixture(self):
        return super(CNameRecordTestCase, self).get_domain_fixture(
            values={
                'name': 'test.example.com.'
            }
        )

    def get_recordset_fixture(self, domain_name, record_type):
        def obj_get_changes():
            return {
                'records': [
                    collections.namedtuple(
                        'RecordSet', {'data': 'example.com'}
                    )(data='example.com')
                ]
            }

        values = super(CNameRecordTestCase, self).get_recordset_fixture(
            domain_name=domain_name,
            values={
                'id': utils.generate_uuid(),
                'ttl': 123456,
                'obj_get_changes': obj_get_changes
            }
        )
        return collections.namedtuple('RecordSet', values)(**values)

    def get_record_fixture(self, recordset_type):

        values = super(CNameRecordTestCase, self).get_record_fixture(
            recordset_type,
            values={
                'id': utils.generate_uuid(),
                'to_primitive': self.create_record_primitive('example.com.')
            }
        )
        return collections.namedtuple('Record', values)(**values)

    def setUp(self):
        super(CNameRecordTestCase, self).setUp()
        self.infoblox = MagicMock()
        self.infoblox._create_infoblox_object = MagicMock()
        self.infoblox._delete_infoblox_object = MagicMock()
        self.infoblox._update_infoblox_object = MagicMock()

        self.cnamerecord = cname.CNameRecord(self.infoblox, 'default')

    def test_create_record(self):
        domain = self.get_domain_fixture()
        recordset = self.get_recordset_fixture(domain['name'], "A")
        record = self.get_record_fixture("A")

        self.cnamerecord.create(recordset, record)
        self.infoblox._create_infoblox_object.assert_called_once_with(
            'record:cname',
            {
                'comment': ANY,
                'canonical': 'example.com',
                'name': 'mail.test.example.com',
                'view': 'default'
            },
            {'ttl': 123456, 'use_ttl': True},
            check_if_exists=True
        )

    def test_update_record(self):
        domain = self.get_domain_fixture()
        recordset = self.get_recordset_fixture(domain['name'], "A")
        record = self.get_record_fixture("A")

        self.cnamerecord.create(recordset, record)
        self.cnamerecord.update(recordset, record)
        self.infoblox._update_infoblox_object.assert_called_once_with(
            'record:cname',
            {
                'comment': ANY,
                'view': 'default'
            },
            {
                'canonical': 'example.com',
            }
        )

    def test_delete_record(self):
        domain = self.get_domain_fixture()
        recordset = self.get_recordset_fixture(domain['name'], "A")
        record = self.get_record_fixture("A")

        self.cnamerecord.create(recordset, record)
        self.cnamerecord.delete(recordset, record)
        self.infoblox._delete_infoblox_object.assert_called_once_with(
            'record:cname',
            {
                'comment': ANY,
                'view': 'default'
            }
        )
