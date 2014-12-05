# Copyright 2014 Mirantis
#
# This work is licensed under a Creative Commons Attribution 3.0
# Unported License.
# http://creativecommons.org/licenses/by/3.0/legalcode

import logging

from designate.backend.impl_infoblox.records import base

LOG = logging.getLogger(__name__)


class AAAARecord(base.DNSRecord):

    def create(self, recordset, record):
        attrs = self._create_ttl_attr(recordset)

        payload = {
            'view': self._get_dns_view(),
            'name': recordset.name[0:-1],
            'comment': self._get_id(recordset, record)
        }

        if record:
            payload['ipv6addr'] = record.data

        self.infoblox._create_infoblox_object('record:aaaa', payload, attrs,
                                              check_if_exists=True)

    def _update_infoblox_record(self, recordset, record):
        update = {
            'ipv6addr': record.data
        }

        request = {
            'view': self._get_dns_view(),
            'comment': self._get_id(recordset, record)
        }

        self.infoblox._update_infoblox_object('record:aaaa', request, update)

    def _update_infoblox_recordset(self, recordset):
        for record in recordset.records:
            if not record:
                continue

            update = {
                'name': recordset.name[0:-1]
            }
            update.update(self._create_ttl_attr(recordset))

            request = {
                'view': self._get_dns_view(),
                'comment': self._get_id(recordset, record),
            }
            self.infoblox._update_infoblox_object(
                'record:aaaa', request, update)

    def delete(self, recordset, record=None):
        request = {
            'view': self._get_dns_view(),
            'comment': self._get_id(recordset, record),
        }
        self.infoblox._delete_infoblox_object('record:aaaa', request)
