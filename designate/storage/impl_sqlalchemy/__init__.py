# Copyright 2012 Managed I.T.
#
# Author: Kiall Mac Innes <kiall@managedit.ie>
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
import time
import hashlib

from oslo.config import cfg
from oslo.db import options
from sqlalchemy import select, distinct, func

from designate.openstack.common import log as logging
from designate import exceptions
from designate import objects
from designate.sqlalchemy import base as sqlalchemy_base
from designate.storage import base as storage_base
from designate.storage.impl_sqlalchemy import tables


LOG = logging.getLogger(__name__)

cfg.CONF.register_group(cfg.OptGroup(
    name='storage:sqlalchemy', title="Configuration for SQLAlchemy Storage"
))

cfg.CONF.register_opts(options.database_opts, group='storage:sqlalchemy')


class SQLAlchemyStorage(sqlalchemy_base.SQLAlchemy, storage_base.Storage):
    """SQLAlchemy connection"""
    __plugin_name__ = 'sqlalchemy'

    def __init__(self):
        super(SQLAlchemyStorage, self).__init__()

    def get_name(self):
        return self.name

    # CRUD for our resources (quota, server, tsigkey, tenant, domain & record)
    # R - get_*, find_*s
    #
    # Standard Arguments
    # self      - python object for the class
    # context   - a dictionary of details about the request (http etc),
    #             provided by flask.
    # criterion - dictionary of filters to be applied
    #

    # Quota Methods
    def _find_quotas(self, context, criterion, one=False, marker=None,
                     limit=None, sort_key=None, sort_dir=None):
        return self._find(
            context, tables.quotas, objects.Quota, objects.QuotaList,
            exceptions.QuotaNotFound, criterion, one, marker, limit,
            sort_key, sort_dir)

    def create_quota(self, context, quota):
        if not isinstance(quota, objects.Quota):
            # TODO(kiall): Quotas should always use Objects
            quota = objects.Quota(**quota)

        return self._create(
            tables.quotas, quota, exceptions.DuplicateQuota)

    def get_quota(self, context, quota_id):
        return self._find_quotas(context, {'id': quota_id}, one=True)

    def find_quotas(self, context, criterion=None, marker=None, limit=None,
                    sort_key=None, sort_dir=None):
        return self._find_quotas(context, criterion, marker=marker,
                                 limit=limit, sort_key=sort_key,
                                 sort_dir=sort_dir)

    def find_quota(self, context, criterion):
        return self._find_quotas(context, criterion, one=True)

    def update_quota(self, context, quota):
        return self._update(
            context, tables.quotas, quota, exceptions.DuplicateQuota,
            exceptions.QuotaNotFound)

    def delete_quota(self, context, quota_id):
        # Fetch the existing quota, we'll need to return it.
        quota = self._find_quotas(context, {'id': quota_id}, one=True)
        return self._delete(context, tables.quotas, quota,
                            exceptions.QuotaNotFound)

    # Server Methods
    def _find_servers(self, context, criterion, one=False, marker=None,
                     limit=None, sort_key=None, sort_dir=None):
        return self._find(
            context, tables.servers, objects.Server, objects.ServerList,
            exceptions.ServerNotFound, criterion, one, marker, limit,
            sort_key, sort_dir)

    def create_server(self, context, server):
        return self._create(
            tables.servers, server, exceptions.DuplicateServer)

    def get_server(self, context, server_id):
        return self._find_servers(context, {'id': server_id}, one=True)

    def find_servers(self, context, criterion=None, marker=None, limit=None,
                     sort_key=None, sort_dir=None):
        return self._find_servers(context, criterion, marker=marker,
                                  limit=limit, sort_key=sort_key,
                                  sort_dir=sort_dir)

    def find_server(self, context, criterion):
        return self._find_servers(context, criterion, one=True)

    def update_server(self, context, server):
        return self._update(
            context, tables.servers, server, exceptions.DuplicateServer,
            exceptions.ServerNotFound)

    def delete_server(self, context, server_id):
        # Fetch the existing server, we'll need to return it.
        server = self._find_servers(context, {'id': server_id}, one=True)
        return self._delete(context, tables.servers, server,
                            exceptions.ServerNotFound)

    # TLD Methods
    def _find_tlds(self, context, criterion, one=False, marker=None,
                   limit=None, sort_key=None, sort_dir=None):
        return self._find(
            context, tables.tlds, objects.Tld, objects.TldList,
            exceptions.TldNotFound, criterion, one, marker, limit,
            sort_key, sort_dir)

    def create_tld(self, context, tld):
        return self._create(
            tables.tlds, tld, exceptions.DuplicateTld)

    def get_tld(self, context, tld_id):
        return self._find_tlds(context, {'id': tld_id}, one=True)

    def find_tlds(self, context, criterion=None, marker=None, limit=None,
                  sort_key=None, sort_dir=None):
        return self._find_tlds(context, criterion, marker=marker, limit=limit,
                               sort_key=sort_key, sort_dir=sort_dir)

    def find_tld(self, context, criterion):
        return self._find_tlds(context, criterion, one=True)

    def update_tld(self, context, tld):
        return self._update(
            context, tables.tlds, tld, exceptions.DuplicateTld,
            exceptions.TldNotFound)

    def delete_tld(self, context, tld_id):
        # Fetch the existing tld, we'll need to return it.
        tld = self._find_tlds(context, {'id': tld_id}, one=True)
        return self._delete(context, tables.tlds, tld, exceptions.TldNotFound)

    # TSIG Key Methods
    def _find_tsigkeys(self, context, criterion, one=False, marker=None,
                       limit=None, sort_key=None, sort_dir=None):
        return self._find(
            context, tables.tsigkeys, objects.TsigKey, objects.TsigKeyList,
            exceptions.TsigKeyNotFound, criterion, one, marker, limit,
            sort_key, sort_dir)

    def create_tsigkey(self, context, tsigkey):
        return self._create(
            tables.tsigkeys, tsigkey, exceptions.DuplicateTsigKey)

    def get_tsigkey(self, context, tsigkey_id):
        return self._find_tsigkeys(context, {'id': tsigkey_id}, one=True)

    def find_tsigkeys(self, context, criterion=None, marker=None, limit=None,
                      sort_key=None, sort_dir=None):
        return self._find_tsigkeys(context, criterion, marker=marker,
                                   limit=limit, sort_key=sort_key,
                                   sort_dir=sort_dir)

    def find_tsigkey(self, context, criterion):
        return self._find_tsigkeys(context, criterion, one=True)

    def update_tsigkey(self, context, tsigkey):
        return self._update(
            context, tables.tsigkeys, tsigkey, exceptions.DuplicateTsigKey,
            exceptions.TsigKeyNotFound)

    def delete_tsigkey(self, context, tsigkey_id):
        # Fetch the existing tsigkey, we'll need to return it.
        tsigkey = self._find_tsigkeys(context, {'id': tsigkey_id}, one=True)
        return self._delete(context, tables.tsigkeys, tsigkey,
                            exceptions.TsigKeyNotFound)

    ##
    # Tenant Methods
    ##
    def find_tenants(self, context):
        # returns an array of tenant_id & count of their domains
        query = select([tables.domains.c.tenant_id,
                        func.count(tables.domains.c.id)])
        query = self._apply_tenant_criteria(context, tables.domains, query)
        query = self._apply_deleted_criteria(context, tables.domains, query)
        query = query.group_by(tables.domains.c.tenant_id)

        resultproxy = self.session.execute(query)
        results = resultproxy.fetchall()

        tenant_list = objects.TenantList(
            objects=[objects.Tenant(id=t[0], domain_count=t[1]) for t in
                     results])

        tenant_list.obj_reset_changes()

        return tenant_list

    def get_tenant(self, context, tenant_id):
        # get list list & count of all domains owned by given tenant_id
        query = select([tables.domains.c.name])
        query = self._apply_tenant_criteria(context, tables.domains, query)
        query = self._apply_deleted_criteria(context, tables.domains, query)
        query = query.where(tables.domains.c.tenant_id == tenant_id)

        resultproxy = self.session.execute(query)
        results = resultproxy.fetchall()

        return objects.Tenant(
            id=tenant_id,
            domain_count=len(results),
            domains=[r[0] for r in results])

    def count_tenants(self, context):
        # tenants are the owner of domains, count the number of unique tenants
        # select count(distinct tenant_id) from domains
        query = select([func.count(distinct(tables.domains.c.tenant_id))])
        query = self._apply_tenant_criteria(context, tables.domains, query)
        query = self._apply_deleted_criteria(context, tables.domains, query)

        resultproxy = self.session.execute(query)
        result = resultproxy.fetchone()

        if result is None:
            return 0

        return result[0]

    ##
    # Domain Methods
    ##
    def _find_domains(self, context, criterion, one=False, marker=None,
                      limit=None, sort_key=None, sort_dir=None):
        # Check to see if the criterion can use the reverse_name column
        criterion = self._rname_check(criterion)

        return self._find(
            context, tables.domains, objects.Domain, objects.DomainList,
            exceptions.DomainNotFound, criterion, one, marker, limit,
            sort_key, sort_dir)

    def create_domain(self, context, domain):
        # Patch in the reverse_name column
        extra_values = {"reverse_name": domain.name[::-1]}

        # Don't handle recordsets for now
        return self._create(
            tables.domains, domain, exceptions.DuplicateDomain, ['recordsets'],
            extra_values=extra_values)

    def get_domain(self, context, domain_id):
        return self._find_domains(context, {'id': domain_id}, one=True)

    def find_domains(self, context, criterion=None, marker=None, limit=None,
                     sort_key=None, sort_dir=None):
        return self._find_domains(context, criterion, marker=marker,
                                  limit=limit, sort_key=sort_key,
                                  sort_dir=sort_dir)

    def find_domain(self, context, criterion):
        return self._find_domains(context, criterion, one=True)

    def update_domain(self, context, domain):
        # Don't handle recordsets for now
        return self._update(
            context, tables.domains, domain, exceptions.DuplicateDomain,
            exceptions.DomainNotFound, ['recordsets'])

    def delete_domain(self, context, domain_id):
        # Fetch the existing domain, we'll need to return it.
        domain = self._find_domains(context, {'id': domain_id}, one=True)
        return self._delete(context, tables.domains, domain,
                            exceptions.DomainNotFound)

    def count_domains(self, context, criterion=None):
        query = select([func.count(tables.domains.c.id)])
        query = self._apply_criterion(tables.domains, query, criterion)
        query = self._apply_tenant_criteria(context, tables.domains, query)
        query = self._apply_deleted_criteria(context, tables.domains, query)

        resultproxy = self.session.execute(query)
        result = resultproxy.fetchone()

        if result is None:
            return 0

        return result[0]

    # RecordSet Methods
    def _find_recordsets(self, context, criterion, one=False, marker=None,
                         limit=None, sort_key=None, sort_dir=None):
        query = None

        # Check to see if the criterion can use the reverse_name column
        criterion = self._rname_check(criterion)

        if criterion is not None \
                and not criterion.get('domains_deleted', True):
            # Ensure that we return only active recordsets
            rjoin = tables.recordsets.join(
                tables.domains,
                tables.recordsets.c.domain_id == tables.domains.c.id)
            query = select([tables.recordsets]).select_from(rjoin).\
                where(tables.domains.c.deleted == '0')

            # remove 'domains_deleted' from the criterion, as _apply_criterion
            # assumes each key in criterion to be a column name.
            del criterion['domains_deleted']
        return self._find(
            context, tables.recordsets, objects.RecordSet,
            objects.RecordSetList, exceptions.RecordSetNotFound, criterion,
            one, marker, limit, sort_key, sort_dir, query)

    def create_recordset(self, context, domain_id, recordset):
        # Fetch the domain as we need the tenant_id
        domain = self._find_domains(context, {'id': domain_id}, one=True)

        recordset.tenant_id = domain.tenant_id
        recordset.domain_id = domain_id

        # Patch in the reverse_name column
        extra_values = {"reverse_name": recordset.name[::-1]}

        recordset = self._create(
            tables.recordsets, recordset, exceptions.DuplicateRecordSet,
            ['records'], extra_values=extra_values)

        if recordset.obj_attr_is_set('records'):
            for record in recordset.records:
                # NOTE: Since we're dealing with a mutable object, the return
                #       value is not needed. The original item will be mutated
                #       in place on the input "recordset.records" list.
                self.create_record(context, domain_id, recordset.id, record)
        else:
            recordset.records = objects.RecordList()

        recordset.obj_reset_changes('records')

        return recordset

    def get_recordset(self, context, recordset_id):
        recordset = self._find_recordsets(
            context, {'id': recordset_id}, one=True)

        recordset.records = self._find_records(
            context, {'recordset_id': recordset.id})

        recordset.obj_reset_changes('records')

        return recordset

    def find_recordsets(self, context, criterion=None, marker=None, limit=None,
                        sort_key=None, sort_dir=None):
        recordsets = self._find_recordsets(context, criterion, marker=marker,
                                           limit=limit, sort_key=sort_key,
                                           sort_dir=sort_dir)

        for recordset in recordsets:
            recordset.records = self._find_records(
                context, {'recordset_id': recordset.id})

            recordset.obj_reset_changes('records')

        return recordsets

    def find_recordset(self, context, criterion):
        recordset = self._find_recordsets(context, criterion, one=True)

        recordset.records = self._find_records(
            context, {'recordset_id': recordset.id})

        recordset.obj_reset_changes('records')

        return recordset

    def update_recordset(self, context, recordset):
        recordset = self._update(
            context, tables.recordsets, recordset,
            exceptions.DuplicateRecordSet, exceptions.RecordSetNotFound,
            ['records'])

        if recordset.obj_attr_is_set('records'):
            # Gather the Record ID's we have
            have_records = set([r.id for r in self._find_records(
                context, {'recordset_id': recordset.id})])

            # Prep some lists of changes
            keep_records = set([])
            create_records = []
            update_records = []

            # Determine what to change
            for record in recordset.records:
                keep_records.add(record.id)
                try:
                    record.obj_get_original_value('id')
                except KeyError:
                    create_records.append(record)
                else:
                    update_records.append(record)

            # NOTE: Since we're dealing with mutable objects, the return value
            #       of create/update/delete record is not needed. The original
            #       item will be mutated in place on the input
            #       "recordset.records" list.

            # Delete Records
            for record_id in have_records - keep_records:
                self.delete_record(context, record_id)

            # Update Records
            for record in update_records:
                self.update_record(context, record)

            # Create Records
            for record in create_records:
                self.create_record(
                    context, recordset.domain_id, recordset.id, record)

        return recordset

    def delete_recordset(self, context, recordset_id):
        # Fetch the existing recordset, we'll need to return it.
        recordset = self._find_recordsets(
            context, {'id': recordset_id}, one=True)

        return self._delete(context, tables.recordsets, recordset,
                            exceptions.RecordSetNotFound)

    def count_recordsets(self, context, criterion=None):
        query = select([func.count(tables.recordsets.c.id)])
        query = self._apply_criterion(tables.recordsets, query, criterion)
        query = self._apply_tenant_criteria(context, tables.recordsets, query)
        query = self._apply_deleted_criteria(context, tables.recordsets, query)

        resultproxy = self.session.execute(query)
        result = resultproxy.fetchone()

        if result is None:
            return 0

        return result[0]

    # Record Methods
    def _find_records(self, context, criterion, one=False, marker=None,
                      limit=None, sort_key=None, sort_dir=None):
        return self._find(
            context, tables.records, objects.Record, objects.RecordList,
            exceptions.RecordNotFound, criterion, one, marker, limit,
            sort_key, sort_dir)

    def _recalculate_record_hash(self, record):
        """
        Calculates the hash of the record, used to ensure record uniqueness.
        """
        md5 = hashlib.md5()
        md5.update("%s:%s" % (record.recordset_id, record.data))

        return md5.hexdigest()

    def create_record(self, context, domain_id, recordset_id, record):
        # Fetch the domain as we need the tenant_id
        domain = self._find_domains(context, {'id': domain_id}, one=True)

        record.tenant_id = domain.tenant_id
        record.domain_id = domain_id
        record.recordset_id = recordset_id
        record.hash = self._recalculate_record_hash(record)

        return self._create(
            tables.records, record, exceptions.DuplicateRecord)

    def get_record(self, context, record_id):
        return self._find_records(context, {'id': record_id}, one=True)

    def find_records(self, context, criterion=None, marker=None, limit=None,
                     sort_key=None, sort_dir=None):
        return self._find_records(context, criterion, marker=marker,
                                  limit=limit, sort_key=sort_key,
                                  sort_dir=sort_dir)

    def find_record(self, context, criterion):
        return self._find_records(context, criterion, one=True)

    def update_record(self, context, record):
        if record.obj_what_changed():
            record.hash = self._recalculate_record_hash(record)

        return self._update(
            context, tables.records, record, exceptions.DuplicateRecord,
            exceptions.RecordNotFound)

    def delete_record(self, context, record_id):
        # Fetch the existing record, we'll need to return it.
        record = self._find_records(context, {'id': record_id}, one=True)
        return self._delete(context, tables.records, record,
                            exceptions.RecordNotFound)

    def count_records(self, context, criterion=None):
        query = select([func.count(tables.records.c.id)])
        query = self._apply_criterion(tables.records, query, criterion)
        query = self._apply_tenant_criteria(context, tables.records, query)
        query = self._apply_deleted_criteria(context, tables.records, query)

        resultproxy = self.session.execute(query)
        result = resultproxy.fetchone()

        if result is None:
            return 0

        return result[0]

    # Blacklist Methods
    def _find_blacklists(self, context, criterion, one=False, marker=None,
                         limit=None, sort_key=None, sort_dir=None):
        return self._find(
            context, tables.blacklists, objects.Blacklist,
            objects.BlacklistList, exceptions.BlacklistNotFound, criterion,
            one, marker, limit, sort_key, sort_dir)

    def create_blacklist(self, context, blacklist):
        return self._create(
            tables.blacklists, blacklist, exceptions.DuplicateBlacklist)

    def get_blacklist(self, context, blacklist_id):
        return self._find_blacklists(context, {'id': blacklist_id}, one=True)

    def find_blacklists(self, context, criterion=None, marker=None, limit=None,
                        sort_key=None, sort_dir=None):
        return self._find_blacklists(context, criterion, marker=marker,
                                     limit=limit, sort_key=sort_key,
                                     sort_dir=sort_dir)

    def find_blacklist(self, context, criterion):
        return self._find_blacklists(context, criterion, one=True)

    def update_blacklist(self, context, blacklist):
        return self._update(
            context, tables.blacklists, blacklist,
            exceptions.DuplicateBlacklist, exceptions.BlacklistNotFound)

    def delete_blacklist(self, context, blacklist_id):
        # Fetch the existing blacklist, we'll need to return it.
        blacklist = self._find_blacklists(
            context, {'id': blacklist_id}, one=True)

        return self._delete(context, tables.blacklists, blacklist,
                            exceptions.BlacklistNotFound)

    # Pool methods
    def _find_pools(self, context, criterion, one=False, marker=None,
                    limit=None, sort_key=None, sort_dir=None):
        return self._find(context, tables.pools, objects.Pool,
                          objects.PoolList, exceptions.PoolNotFound,
                          criterion, one, marker, limit, sort_key,
                          sort_dir)

    def create_pool(self, context, pool):
        pool = self._create(
            tables.pools, pool, exceptions.DuplicatePool,
            ['attributes', 'nameservers'])

        if pool.obj_attr_is_set('attributes'):
            for pool_attribute in pool.attributes:
                self.create_pool_attribute(context, pool.id, pool_attribute)
        else:
            pool.attributes = objects.PoolAttributeList()
        pool.obj_reset_changes('attributes')

        if pool.obj_attr_is_set('nameservers'):
            for nameserver in pool.nameservers:
                self.create_pool_attribute(context, pool.id, nameserver)
        else:
            pool.nameservers = objects.NameServerList()
        pool.obj_reset_changes('nameservers')

        return pool

    def get_pool(self, context, pool_id):
        pool = self._find_pools(context, {'id': pool_id}, one=True)
        pool.attributes = self._find_pool_attributes(
            context, {'pool_id': pool_id, 'key': '!nameserver'})
        pool.nameservers = self._find_pool_attributes(
            context, {'pool_id': pool_id, 'key': 'nameserver'})
        pool.obj_reset_changes('attributes')
        pool.obj_reset_changes('nameservers')
        return pool

    def find_pools(self, context, criterion=None, marker=None,
                   limit=None, sort_key=None, sort_dir=None):
        pools = self._find_pools(context, criterion, marker=marker,
                                limit=limit, sort_key=sort_key,
                                sort_dir=sort_dir)
        for pool in pools:
            pool.attributes = self._find_pool_attributes(
                context, {'pool_id': pool.id, 'key': '!nameserver'})
            pool.nameservers = self._find_pool_attributes(
                context, {'pool_id': pool.id, 'key': 'nameserver'})
            pool.obj_reset_changes('attributes')
            pool.obj_reset_changes('nameservers')

        return pools

    def find_pool(self, context, criterion):
        pool = self._find_pools(context, criterion, one=True)
        pool.attributes = self._find_pool_attributes(
            context, {'pool_id': pool.id, 'key': '!nameserver'})
        pool.nameservers = self._find_pool_attributes(
            context, {'pool_id': pool.id, 'key': 'nameserver'})
        pool.obj_reset_changes('attributes')
        pool.obj_reset_changes('nameservers')
        return pool

    def update_pool(self, context, pool):
        pool = self._update(context, tables.pools, pool,
                            exceptions.DuplicatePool, exceptions.PoolNotFound,
                            ['attributes', 'nameservers'])
        if pool.obj_attr_is_set('attributes') or \
                pool.obj_attr_is_set('nameservers'):
            # Gather the pool ID's we have
            have_attributes = set([r.id for r in self._find_pool_attributes(
                context, {'pool_id': pool.id})])

            # Prep some lists of changes
            keep_attributes = set([])
            create_attributes = []
            update_attributes = []

            attributes = []
            if pool.obj_attr_is_set('attributes'):
                for r in pool.attributes.objects:
                    attributes.append(r)
            if pool.obj_attr_is_set('nameservers'):
                for r in pool.nameservers.objects:
                    attributes.append(r)

            # Determine what to change
            for attribute in attributes:
                keep_attributes.add(attribute.id)
                try:
                    attribute.obj_get_original_value('id')
                except KeyError:
                    create_attributes.append(attribute)
                else:
                    update_attributes.append(attribute)

            # NOTE: Since we're dealing with mutable objects, the return value
            #       of create/update/delete attribute is not needed. The
            #       original item will be mutated in place on the input
            #       "pool.attributes" or "pool.nameservers" list.

            # Delete attributes
            for attribute_id in have_attributes - keep_attributes:
                self.delete_pool_attribute(context, attribute_id)

            # Update attributes
            for attribute in update_attributes:
                self.update_pool_attribute(context, attribute)

            # Create attributes
            for attribute in create_attributes:
                self.create_pool_attribute(
                    context, pool.id, attribute)

        return pool

    def delete_pool(self, context, pool_id):
        pool = self._find_pools(context, {'id': pool_id}, one=True)

        return self._delete(context, tables.pools, pool,
                            exceptions.PoolNotFound)

    # Pool attribute methods
    def _find_pool_attributes(self, context, criterion, one=False, marker=None,
                    limit=None, sort_key=None, sort_dir=None):
        return self._find(context, tables.pool_attributes,
                          objects.PoolAttribute, objects.PoolAttributeList,
                          exceptions.PoolAttributeNotFound, criterion, one,
                          marker, limit, sort_key, sort_dir)

    def create_pool_attribute(self, context, pool_id, pool_attribute):
        pool_attribute.pool_id = pool_id
        return self._create(tables.pool_attributes, pool_attribute,
                            exceptions.DuplicatePoolAttribute)

    def get_pool_attributes(self, context, pool_attribute_id):
        return self._find_pool_attributes(
            context, {'id': pool_attribute_id}, one=True)

    def find_pool_attributes(self, context, criterion=None, marker=None,
                   limit=None, sort_key=None, sort_dir=None):
        return self._find_pool_attributes(context, criterion, marker=marker,
                                          limit=limit, sort_key=sort_key,
                                          sort_dir=sort_dir)

    def find_pool_attribute(self, context, criterion):
        return self._find_pool_attributes(context, criterion, one=True)

    def update_pool_attribute(self, context, pool_attribute):
        return self._update(context, tables.pool_attributes, pool_attribute,
                            exceptions.DuplicatePoolAttribute,
                            exceptions.PoolAttributeNotFound)

    def delete_pool_attribute(self, context, pool_attribute_id):
        pool_attribute = self._find_pool_attributes(
            context, {'id': pool_attribute_id}, one=True)
        deleted_pool_attribute = self._delete(
            context, tables.pool_attributes, pool_attribute,
            exceptions.PoolAttributeNotFound)

        return deleted_pool_attribute

    # diagnostics
    def ping(self, context):
        start_time = time.time()

        try:
            result = self.engine.execute('SELECT 1').first()
        except Exception:
            status = False
        else:
            status = True if result[0] == 1 else False

        return {
            'status': status,
            'rtt': "%f" % (time.time() - start_time)
        }

    # Reverse Name utils
    def _rname_check(self, criterion):
        # If the criterion has 'name' in it, switch it out for reverse_name
        if criterion is not None and criterion.get('name', "").startswith('*'):
                criterion['reverse_name'] = criterion.pop('name')[::-1]
        return criterion
