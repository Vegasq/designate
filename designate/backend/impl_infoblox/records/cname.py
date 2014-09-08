# Copyright 2014 Mirantis
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

import logging

from designate.backend.impl_infoblox.records import base

LOG = logging.getLogger(__name__)


class CNameRecord(base.DNSRecord):
    def create(self, recordset, record=None):
        ip = record.to_primitive()

        attrs = {}
        attrs.update(self._create_ttl_attr(recordset))

        payload = {
            'view': self._get_dns_view(),
            'name': recordset.name[0:-1],
            'canonical': ip['designate_object.data']['data'][0:-1],
            'comment': self._get_id(recordset, record)
        }

        self.infoblox._create_infoblox_object('record:cname', payload, attrs,
                                              check_if_exists=True)

    def update(self, recordset, record=None):
        if record:
            self._update_infoblox_record(recordset, record)
        else:
            self._update_infoblox_recordset(recordset, record)

    def _update_infoblox_record(self, recordset, record):
        ip = record.to_primitive()
        update = {
            'canonical': ip['designate_object.data']['data'][0:-1]
        }

        request = {
            'view': self._get_dns_view(),
            'comment': self._get_id(recordset, record)
        }

        self.infoblox._update_infoblox_object('record:cname', request, update)

    def _update_infoblox_recordset(self, recordset, record):
        rs = recordset.to_primitive()
        for record in recordset.records:
            update = {
                'name': rs['designate_object.data']['name'][0:-1]
            }
            update.update(self._create_ttl_attr(recordset))

            request = {
                'view': self._get_dns_view(),
                'comment': self._get_id(recordset, record),
            }
            self.infoblox._update_infoblox_object(
                'record:cname', request, update)

    def delete(self, recordset, record=None):
        request = {
            'view': self._get_dns_view(),
            'comment': self._get_id(recordset, record),
        }
        self.infoblox._delete_infoblox_object('record:cname', request)
