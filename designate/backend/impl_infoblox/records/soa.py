# Copyright 2014 Mirantis
#
# This work is licensed under a Creative Commons Attribution 3.0
# Unported License.
# http://creativecommons.org/licenses/by/3.0/legalcode

import logging

from designate.backend.impl_infoblox.records import base
from designate.i18n import _LI

LOG = logging.getLogger(__name__)


class SOARecord(base.DNSRecord):
    def create(self, recordset):
        LOG.warning(_LI("Create SOA record not implemented"))
        pass

    def _update_infoblox_record(self, recordset):
        LOG.warning(_LI("Update SOA record not implemented"))
        pass

    def _update_infoblox_recordset(self, recordset):
        LOG.warning(_LI("Update SOA recordset not implemented"))
        pass

    def delete(self, recordset):
        LOG.warning(_LI("Delete SOA record not implemented"))
        pass
