# Copyright 2014 Mirantis
#
# This work is licensed under a Creative Commons Attribution 3.0
# Unported License.
# http://creativecommons.org/licenses/by/3.0/legalcode

import logging

from designate.backend.impl_infoblox.records import base

LOG = logging.getLogger(__name__)


class PTRRecord(base.DNSRecord):
    """
    https://answers.launchpad.net/designate/+question/248330
    """
    def _create_reverse_mapping_name(self, ip):
        octets = ip.split('.')
        octets.reverse()
        return ".".join(octets) + '.in-addr.arpa'

    def create(self, recordset, record):
        ip = record.to_primitive()

        attrs = {}
        attrs.update(self._create_ttl_attr(recordset))

        payload = {
            'view': self._get_dns_view(),
            'name': recordset.name[0:-1],
            'ptrdname': self._create_reverse_mapping_name(
                ip['designate_object.data']['data']),
            'comment': self._get_id(recordset, record)
        }

        self._create_infoblox_object('record:ptr', payload, attrs,
                                     check_if_exists=True)

    def _update_infoblox_record(self, recordset, record):
        ip = record.to_primitive()
        update = {
            'ptrdname': self._create_reverse_mapping_name(
                ip['designate_object.data']['data']),
        }

        request = {
            'view': self._get_dns_view(),
            'comment': self._get_id(recordset, record)
        }

        self.infoblox._update_infoblox_object('record:ptr', request, update)

    def _update_infoblox_recordset(self, recordset):
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
                'record:ptr', request, update)

    def delete(self, recordset, record=None):
        request = {
            'view': self._get_dns_view(),
            'comment': self._get_id(recordset, record),
        }
        self.infoblox._delete_infoblox_object('record:ptr', request)
