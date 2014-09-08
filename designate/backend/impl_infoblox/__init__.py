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

import base64

import record_factory

from designate.backend import base
from designate.backend.impl_infoblox import exceptions
from designate.backend.impl_infoblox import connector
from designate.backend.impl_infoblox import object_manipulator
from designate.openstack.common import log as logging
from designate.i18n import _LI

LOG = logging.getLogger(__name__)


class InfobloxBackend(base.Backend):
    __plugin_name__ = 'infoblox'

    def __init__(self, *args, **kwargs):
        super(InfobloxBackend, self).__init__(*args, **kwargs)

        self.infoblox = object_manipulator.InfobloxObjectManipulator(
            connector.Infoblox())

    def create_record(self, context, domain, recordset, record):
        LOG.info(_LI('Create Record %(domain)r / %(recordset)r / %(record)r') %
                 {'domain': domain, 'recordset': recordset, 'record': record})
        record_manipulator = record_factory.RecordFactory.factory(
            recordset, self.infoblox, context.tenant)
        record_manipulator.create(recordset, record)

    def update_record(self, context, domain, recordset, record):
        LOG.info(_LI('Update Record %(domain)r / %(recordset)r / %(record)r') %
                 {'domain': domain, 'recordset': recordset, 'record': record})
        record_manipulator = record_factory.RecordFactory.factory(
            recordset, self.infoblox, context.tenant)
        record_manipulator.update(recordset, record)

    def delete_record(self, context, domain, recordset, record):
        LOG.info(_LI('Delete Record %(domain)r / %(recordset)r / %(record)r') %
                 {'domain': domain, 'recordset': recordset, 'record': record})
        record_manipulator = record_factory.RecordFactory.factory(
            recordset, self.infoblox, context.tenant)
        record_manipulator.delete(recordset, record)

    def create_domain(self, context, domain):
        LOG.info(_LI('Create Domain %r') % domain)

        dns_net_view = self.infoblox.get_dns_view(context.tenant)
        self.infoblox.create_zone_auth(
            fqdn=domain['name'][0:-1],
            dns_view=dns_net_view
        )

    def update_domain(self, context, domain):
        LOG.info(_LI('Update Domain %r') % domain)

        self.infoblox.update_zone_auth(
            domain['name'][0:-1]
        )

    def delete_domain(self, context, domain):
        LOG.info(_LI('Delete Domain %r') % domain)
        self.infoblox.delete_zone_auth(domain['name'][0:-1])

    # TODO(nyakovlev) Howto call this place?
    def create_tsigkey(self, context, tsigkey):
        LOG.info(_LI('Create TSIG Key %r') % tsigkey)
        self.infoblox.create_tsig(tsigkey['name'], tsigkey['algorithm'],
                                  base64.b64encode(tsigkey['secret']))

    def update_tsigkey(self, context, tsigkey):
        LOG.info(_LI('Update TSIG Key %r') % tsigkey)
        self.infoblox.update_tsig(tsigkey['name'], tsigkey['algorithm'],
                                  base64.b64encode(tsigkey['secret']))

    def delete_tsigkey(self, context, tsigkey):
        LOG.info(_LI('Delete TSIG Key %r') % tsigkey)
        self.infoblox.delete_tsig(tsigkey['name'], tsigkey['algorithm'],
                                  base64.b64encode(tsigkey['secret']))

    def create_server(self, context, server):
        LOG.info(_LI('Create Server %r') % server)
        resp = self.infoblox.get_member(server.name)
        if not resp:
            raise exceptions.NoInfobloxMemberAvailable()

    def update_server(self, context, server):
        LOG.info(_LI('Update Server %r') % server)
        resp = self.infoblox.get_member(server.name)
        if not resp:
            raise exceptions.NoInfobloxMemberAvailable()

    def delete_server(self, context, server):
        LOG.info(_LI('Delete Server %r') % server)

    def create_recordset(self, context, domain, recordset):
        LOG.info(_LI('Create RecordSet %(domain)r / %(recordset)r') %
                 {'domain': domain, 'recordset': recordset})

    def update_recordset(self, context, domain, recordset):
        LOG.info(_LI('Update RecordSet %(domain)r / %(recordset)r') %
                 {'domain': domain, 'recordset': recordset})

        record_manipulator = record_factory.RecordFactory.factory(
            recordset, self.infoblox, context.tenant)
        record_manipulator.update(recordset)

    def delete_recordset(self, context, domain, recordset):
        LOG.info(_LI('Delete RecordSet %(domain)r / %(recordset)r') %
                 {'domain': domain, 'recordset': recordset})

    def sync_domain(self, context, domain, records):
        LOG.info(_LI('Sync Domain %(domain)r / %(records)r') %
                 {'domain': domain, 'records': records})

    def sync_record(self, context, domain, record):
        LOG.info(_LI('Sync Record %(domain)r / %(record)r') %
                 {'domain': domain, 'record': record})

    def ping(self, context):
        LOG.info(_LI('Ping'))
