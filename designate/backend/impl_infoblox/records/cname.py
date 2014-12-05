# Copyright 2014 Mirantis
#
# This work is licensed under a Creative Commons Attribution 3.0
# Unported License.
# http://creativecommons.org/licenses/by/3.0/legalcode

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
