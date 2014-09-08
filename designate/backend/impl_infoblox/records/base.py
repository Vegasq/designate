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

from abc import abstractmethod
from abc import ABCMeta
import logging

import six

from designate.backend.impl_infoblox.config import cfg


LOG = logging.getLogger(__name__)


@six.add_metaclass(ABCMeta)
class DNSRecord():
    def __init__(self, infoblox, tenant_name):
        self.infoblox = infoblox
        self.tenant_name = tenant_name

    def _get_id(self, recordset, record):
        if record:
            return "%s:%s" % (recordset.id, record.id)
        else:
            return "%s" % recordset.id

    def _create_ttl_attr(self, recordset):
        attrs = {}
        if recordset.ttl:
            attrs['use_ttl'] = True
            attrs['ttl'] = recordset.ttl
        return attrs

    @abstractmethod
    def create(self, recordset, record=None):
        raise Exception('Non implemented')

    def update(self, recordset, record=None):
        if record:
            self._update_infoblox_record(recordset, record)
        else:
            self._update_infoblox_recordset(recordset)

    @abstractmethod
    def delete(self, recordset, record=None):
        raise Exception('Non implemented')

    @abstractmethod
    def _update_infoblox_record(self, recordset, record):
        pass

    @abstractmethod
    def _update_infoblox_recordset(self, recordset, record):
        pass

    def _get_dns_view(self):
        if cfg.CONF['backend:infoblox'].multi_tenant:
            return self.tenant_name
        else:
            return cfg.CONF['backend:infoblox'].dns_view
