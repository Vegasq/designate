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

from designate.i18n import _LI
from designate.backend.impl_infoblox.records import a
from designate.backend.impl_infoblox.records import aaaa
from designate.backend.impl_infoblox.records import cname
from designate.backend.impl_infoblox.records import ptr
from designate.backend.impl_infoblox.records import soa
from designate.backend.impl_infoblox.records import ns
LOG = logging.getLogger(__name__)


class RecordFactory(object):
    @staticmethod
    def factory(recordset, infoblox, tenant_name):
        if recordset.type == "A":
            return a.ARecord(infoblox, tenant_name)
        if recordset.type == "CNAME":
            return cname.CNameRecord(infoblox, tenant_name)
        if recordset.type == "NS":
            return ns.NSRecord(infoblox, tenant_name)
        if recordset.type == "SOA":
            return soa.SOARecord(infoblox, tenant_name)
        if recordset.type == "PTR":
            return ptr.PTRRecord(infoblox, tenant_name)
        if recordset.type == "AAAA":
            return aaaa.AAAARecord(infoblox, tenant_name)
        LOG.error(_LI("Unknown type %s"), recordset.type)
