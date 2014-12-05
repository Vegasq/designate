# Copyright 2014 Mirantis
#
# This work is licensed under a Creative Commons Attribution 3.0
# Unported License.
# http://creativecommons.org/licenses/by/3.0/legalcode

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
    def get_record(recordset, infoblox, tenant_name):
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
