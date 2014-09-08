# Copyright (C) 2014 Mirantis
#
# Author: Nikolay Yakovlev <nyakovlev@mirantis.com>
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
from designate.backend.impl_infoblox.records import a
from designate.tests.test_backend import BackendTestMixin
from designate import utils



class ARecordTestCase(tests.TestCase, BackendTestMixin):
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
        return super(ARecordTestCase, self).get_domain_fixture(
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

        values = super(ARecordTestCase, self).get_recordset_fixture(
            domain_name=domain_name,
            values={
                'id': utils.generate_uuid(),
                'ttl': 123456,
                'to_primitive': self.create_record_primitive('172.25.1.2'),
                'obj_get_changes': obj_get_changes
            }
        )
        return collections.namedtuple('RecordSet', values)(**values)

    def get_record_fixture(self, recordset_type):

        values = super(ARecordTestCase, self).get_record_fixture(
            recordset_type,
            values={
                'id': utils.generate_uuid(),
                'to_primitive': self.create_record_primitive('172.25.1.1')
            }
        )
        return collections.namedtuple('Record', values)(**values)

    def setUp(self):
        super(ARecordTestCase, self).setUp()
        self.infonfoblox = MagicMock()
        self.infonfoblox._create_infoblox_object = MagicMock()
        self.infonfoblox._delete_infoblox_object = MagicMock()
        self.infonfoblox._update_infoblox_object = MagicMock()

        self.arecord = a.ARecord(self.infonfoblox)

    def test_create_record(self):
        domain = self.get_domain_fixture()
        recordset = self.get_recordset_fixture(domain['name'], "A")
        record = self.get_record_fixture("A")

        self.arecord.create(recordset, record)
        self.infonfoblox._create_infoblox_object.assert_called_once_with(
            'record:a',
            {
                'comment': ANY,
                'ipv4addr': '172.25.1.1',
                'name': 'mail.test.example.co',
                'view': 'default'
            },
            {'ttl': 123456, 'use_ttl': True},
            check_if_exists=True
        )

    def test_update_record(self):
        domain = self.get_domain_fixture()
        recordset = self.get_recordset_fixture(domain['name'], "A")
        record = self.get_record_fixture("A")

        self.arecord.create(recordset, record)
        self.arecord.update(recordset, record)
        self.infonfoblox._update_infoblox_object.assert_called_once_with(
            'record:a',
            {
                'comment': ANY,
                'view': 'default'
            },
            {
                'ipv4addr': '172.25.1.1',
            }
        )

    def test_delete_record(self):
        domain = self.get_domain_fixture()
        recordset = self.get_recordset_fixture(domain['name'], "A")
        record = self.get_record_fixture("A")

        self.arecord.create(recordset, record)
        self.arecord.delete(recordset, record)
        self.infonfoblox._delete_infoblox_object.assert_called_once_with(
            'record:a',
            {
                'comment': ANY,
                'view': 'default'
            }
        )
