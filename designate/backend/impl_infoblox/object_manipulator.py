# Copyright 2014 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import logging
import gettext

from designate.backend.impl_infoblox.config import cfg
from designate.backend.impl_infoblox import exceptions as exc
from designate.i18n import _LI

_ = gettext.gettext

LOG = logging.getLogger(__name__)


class InfobloxObjectManipulator(object):
    FIELDS = ['ttl', 'use_ttl']

    def __init__(self, connector):
        self.connector = connector

    def get_member(self, member_name):
        obj = {'host_name': member_name[0:-1]}
        return self.connector.get_object('member', obj)

    def create_dns_view(self, net_view_name, dns_view_name):
        dns_view_data = {'name': dns_view_name,
                         'network_view': net_view_name}
        return self._create_infoblox_object('view', dns_view_data)

    def delete_dns_view(self, net_view_name):
        net_view_data = {'name': net_view_name}
        self._delete_infoblox_object('view', net_view_data)

    def create_network_view(self, net_view_name):
        net_view_data = {'name': net_view_name}
        return self._create_infoblox_object('networkview', net_view_data)

    def delete_network_view(self, net_view_name):
        if net_view_name == 'default':
            # never delete default network view
            return

        net_view_data = {'name': net_view_name}
        self._delete_infoblox_object('networkview', net_view_data)

    def create_tsig(self, name, algorithm, secret):
        tsig = {
            'name': name,
            'key': secret
        }
        self._create_infoblox_object(
            'tsig', tsig,
            check_if_exists=True)

    def delete_tsig(self, name, algorithm, secret):
        tsig = {
            'name': name,
            'key': secret
        }
        self._delete_infoblox_object(
            'tsig', tsig,
            check_if_exists=True)

    def get_dns_view(self, tenant):
        if cfg.CONF['backend:infoblox'].multi_tenant:
            try:
                self.create_network_view(
                    net_view_name=tenant)

                self.create_dns_view(
                    net_view_name=tenant,
                    dns_view_name=tenant)
            except Exception as e:
                LOG.warning(_LI("Issue happens during views creating: %s" % e))

            return tenant
        else:
            return cfg.CONF['backend:infoblox'].dns_view

    def create_zone_auth(self, fqdn, dns_view):
        try:
            self._create_infoblox_object(
                'zone_auth', {'fqdn': fqdn,
                              'view': dns_view},
                check_if_exists=True)
        except exc.InfobloxCannotCreateObject as e:
            LOG.warning(e)

    def delete_zone_auth(self, fqdn):
        self._delete_infoblox_object(
            'zone_auth', {'fqdn': fqdn})

    def update_zone_auth(self, fqdn):
        # TODO(nyakovlev) list of var for update
        self._update_infoblox_object(
            'zone_auth', {'fqdn': fqdn}, {})

    def _create_infoblox_object(self, obj_type, payload,
                                additional_create_kwargs=None,
                                check_if_exists=True,
                                return_fields=None):
        if additional_create_kwargs is None:
            additional_create_kwargs = {}

        ib_object = None
        if check_if_exists:
            ib_object = self._get_infoblox_object_or_none(obj_type, payload)
            if ib_object:
                LOG.info(_(
                    "Infoblox %(obj_type)s already exists: %(ib_object)s"),
                    {'obj_type': obj_type, 'ib_object': ib_object})

        if not ib_object:
            payload.update(additional_create_kwargs)
            ib_object = self.connector.create_object(obj_type, payload,
                                                     return_fields)
            LOG.info(_("Infoblox %(obj_type)s was created: %(ib_object)s"),
                     {'obj_type': obj_type, 'ib_object': ib_object})

        return ib_object

    def _get_infoblox_object_or_none(self, obj_type, payload,
                                     return_fields=None):
        ib_object = self.connector.get_object(obj_type, payload, return_fields)
        if ib_object:
            if return_fields:
                return ib_object[0]
            else:
                return ib_object[0]['_ref']

        return None

    def _update_infoblox_object(self, obj_type, payload, update_kwargs):
        ib_object_ref = None
        warn_msg = _('Infoblox %(obj_type)s will not be updated because'
                     ' it cannot be found: %(payload)s')
        try:
            ib_object_ref = self._get_infoblox_object_or_none(obj_type,
                                                              payload)
            if not ib_object_ref:
                LOG.warning(warn_msg % {'obj_type': obj_type,
                                        'payload': payload})
        except exc.InfobloxSearchError as e:
            LOG.warning(warn_msg, {'obj_type': obj_type, 'payload': payload})
            LOG.info(e)

        if ib_object_ref:
            self._update_infoblox_object_by_ref(ib_object_ref, update_kwargs)

    def _update_infoblox_object_by_ref(self, ref, update_kwargs):
        self.connector.update_object(ref, update_kwargs)
        LOG.info(_('Infoblox object was updated: %s'), ref)

    def _delete_infoblox_object(self, obj_type, payload):
        ib_object_ref = None
        warn_msg = _('Infoblox %(obj_type)s will not be deleted because'
                     ' it cannot be found: %(payload)s')
        try:
            ib_object_ref = self._get_infoblox_object_or_none(obj_type,
                                                              payload)
            if not ib_object_ref:
                LOG.warning(warn_msg, obj_type, payload)
        except exc.InfobloxSearchError as e:
            LOG.warning(warn_msg, {'obj_type': obj_type, 'payload': payload})
            LOG.info(e)

        if ib_object_ref:
            self.connector.delete_object(ib_object_ref)
            LOG.info(_('Infoblox object was deleted: %s'), ib_object_ref)
