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
import abc

import six

from designate.plugin import DriverPlugin


@six.add_metaclass(abc.ABCMeta)
class Storage(DriverPlugin):

    """Base class for storage plugins"""
    __plugin_ns__ = 'designate.storage'
    __plugin_type__ = 'storage'

    @abc.abstractmethod
    def create_quota(self, context, quota):
        """
        Create a Quota.

        :param context: RPC Context.
        :param quota: Quota object with the values to be created.
        """

    @abc.abstractmethod
    def get_quota(self, context, quota_id):
        """
        Get a Quota via ID.

        :param context: RPC Context.
        :param quota_id: Quota ID to get.
        """

    @abc.abstractmethod
    def find_quotas(self, context, criterion=None, marker=None,
                    limit=None, sort_key=None, sort_dir=None):
        """
        Find Quotas

        :param context: RPC Context.
        :param criterion: Criteria to filter by.
        :param marker: Resource ID from which after the requested page will
                       start after
        :param limit: Integer limit of objects of the page size after the
                      marker
        :param sort_key: Key from which to sort after.
        :param sort_dir: Direction to sort after using sort_key.
        """

    @abc.abstractmethod
    def find_quota(self, context, criterion):
        """
        Find a single Quota.

        :param context: RPC Context.
        :param criterion: Criteria to filter by.
        """

    @abc.abstractmethod
    def update_quota(self, context, quota):
        """
        Update a Quota

        :param context: RPC Context.
        :param quota: Quota to update.
        """

    @abc.abstractmethod
    def delete_quota(self, context, quota_id):
        """
        Delete a Quota via ID.

        :param context: RPC Context.
        :param quota_id: Delete a Quota via ID
        """

    @abc.abstractmethod
    def create_server(self, context, server):
        """
        Create a Server.

        :param context: RPC Context.
        :param server: Server object with the values to be created.
        """

    @abc.abstractmethod
    def find_servers(self, context, criterion=None, marker=None,
                     limit=None, sort_key=None, sort_dir=None):
        """
        Find Servers.

        :param context: RPC Context.
        :param criterion: Criteria to filter by.
        :param marker: Resource ID from which after the requested page will
                       start after
        :param limit: Integer limit of objects of the page size after the
                      marker
        :param sort_key: Key from which to sort after.
        :param sort_dir: Direction to sort after using sort_key.
        """

    @abc.abstractmethod
    def get_server(self, context, server_id):
        """
        Get a Server via ID.

        :param context: RPC Context.
        :param server_id: Server ID to get.
        """

    @abc.abstractmethod
    def update_server(self, context, server):
        """
        Update a Server

        :param context: RPC Context.
        :param server: Server object
        """

    @abc.abstractmethod
    def delete_server(self, context, server_id):
        """
        Delete a Server via ID.

        :param context: RPC Context.
        :param server_id: Delete a Server via ID
        """

    @abc.abstractmethod
    def create_tld(self, context, tld):
        """
        Create a TLD.

        :param context: RPC Context.
        :param tld: Tld object with the values to be created.
        """

    @abc.abstractmethod
    def get_tld(self, context, tld_id):
        """
        Get a TLD via ID.

        :param context: RPC Context.
        :param tld_id: TLD ID to get.
        """

    @abc.abstractmethod
    def find_tlds(self, context, criterion=None, marker=None,
                  limit=None, sort_key=None, sort_dir=None):
        """
        Find TLDs

        :param context: RPC Context.
        :param criterion: Criteria to filter by.
        :param marker: Resource ID from which after the requested page will
                       start after
        :param limit: Integer limit of objects of the page size after the
                      marker
        :param sort_key: Key from which to sort after.
        :param sort_dir: Direction to sort after using sort_key.
        """

    @abc.abstractmethod
    def find_tld(self, context, criterion):
        """
        Find a single TLD.

        :param context: RPC Context.
        :param criterion: Criteria to filter by.
        """

    @abc.abstractmethod
    def update_tld(self, context, tld):
        """
        Update a TLD

        :param context: RPC Context.
        :param tld: TLD to update.
        """

    @abc.abstractmethod
    def delete_tld(self, context, tld_id):
        """
        Delete a TLD via ID.

        :param context: RPC Context.
        :param tld_id: Delete a TLD via ID
        """

    @abc.abstractmethod
    def create_tsigkey(self, context, tsigkey):
        """
        Create a TSIG Key.

        :param context: RPC Context.
        :param tsigkey: TsigKey object with the values to be created.
        """

    @abc.abstractmethod
    def find_tsigkeys(self, context, criterion=None,
                      marker=None, limit=None, sort_key=None, sort_dir=None):
        """
        Find TSIG Keys.

        :param context: RPC Context.
        :param criterion: Criteria to filter by.
        :param marker: Resource ID from which after the requested page will
                       start after
        :param limit: Integer limit of objects of the page size after the
                      marker
        :param sort_key: Key from which to sort after.
        :param sort_dir: Direction to sort after using sort_key.
        """

    @abc.abstractmethod
    def get_tsigkey(self, context, tsigkey_id):
        """
        Get a TSIG Key via ID.

        :param context: RPC Context.
        :param tsigkey_id: Server ID to get.
        """

    @abc.abstractmethod
    def update_tsigkey(self, context, tsigkey):
        """
        Update a TSIG Key

        :param context: RPC Context.
        :param tsigkey: TSIG Keyto update.
        """

    @abc.abstractmethod
    def delete_tsigkey(self, context, tsigkey_id):
        """
        Delete a TSIG Key via ID.

        :param context: RPC Context.
        :param tsigkey_id: Delete a TSIG Key via ID
        """

    @abc.abstractmethod
    def find_tenants(self, context):
        """
        Find all Tenants.

        :param context: RPC Context.
        """

    @abc.abstractmethod
    def get_tenant(self, context, tenant_id):
        """
        Get all Tenants.

        :param context: RPC Context.
        :param tenant_id: ID of the Tenant.
        """

    @abc.abstractmethod
    def count_tenants(self, context):
        """
        Count tenants

        :param context: RPC Context.
        """

    @abc.abstractmethod
    def create_domain(self, context, domain):
        """
        Create a new Domain.

        :param context: RPC Context.
        :param domain: Domain object with the values to be created.
        """

    @abc.abstractmethod
    def get_domain(self, context, domain_id):
        """
        Get a Domain via its ID.

        :param context: RPC Context.
        :param domain_id: ID of the Domain.
        """

    @abc.abstractmethod
    def find_domains(self, context, criterion=None, marker=None,
                     limit=None, sort_key=None, sort_dir=None):
        """
        Find Domains

        :param context: RPC Context.
        :param criterion: Criteria to filter by.
        :param marker: Resource ID from which after the requested page will
                       start after
        :param limit: Integer limit of objects of the page size after the
                      marker
        :param sort_key: Key from which to sort after.
        :param sort_dir: Direction to sort after using sort_key.
        """

    @abc.abstractmethod
    def find_domain(self, context, criterion):
        """
        Find a single Domain.

        :param context: RPC Context.
        :param criterion: Criteria to filter by.
        """

    @abc.abstractmethod
    def update_domain(self, context, domain):
        """
        Update a Domain

        :param context: RPC Context.
        :param domain: Domain object.
        """

    @abc.abstractmethod
    def delete_domain(self, context, domain_id):
        """
        Delete a Domain

        :param context: RPC Context.
        :param domain_id: Domain ID to delete.
        """

    @abc.abstractmethod
    def count_domains(self, context, criterion=None):
        """
        Count domains

        :param context: RPC Context.
        :param criterion: Criteria to filter by.
        """

    @abc.abstractmethod
    def create_recordset(self, context, domain_id, recordset):
        """
        Create a recordset on a given Domain ID

        :param context: RPC Context.
        :param domain_id: Domain ID to create the recordset in.
        :param recordset: RecordSet object with the values to be created.
        """

    @abc.abstractmethod
    def get_recordset(self, context, recordset_id):
        """
        Get a recordset via ID

        :param context: RPC Context.
        :param recordset_id: RecordSet ID to get
        """

    @abc.abstractmethod
    def find_recordsets(self, context, criterion=None,
                        marker=None, limit=None, sort_key=None, sort_dir=None):
        """
        Find RecordSets.

        :param context: RPC Context.
        :param criterion: Criteria to filter by.
        :param marker: Resource ID from which after the requested page will
                       start after
        :param limit: Integer limit of objects of the page size after the
                      marker
        :param sort_key: Key from which to sort after.
        :param sort_dir: Direction to sort after using sort_key.
        """

    @abc.abstractmethod
    def find_recordset(self, context, criterion):
        """
        Find a single RecordSet.

        :param context: RPC Context.
        :param criterion: Criteria to filter by.
        """

    @abc.abstractmethod
    def update_recordset(self, context, recordset):
        """
        Update a recordset

        :param context: RPC Context
        :param recordset: RecordSet to update
        """

    @abc.abstractmethod
    def delete_recordset(self, context, recordset_id):
        """
        Delete a recordset

        :param context: RPC Context
        :param recordset_id: RecordSet ID to delete
        """

    @abc.abstractmethod
    def count_recordsets(self, context, criterion=None):
        """
        Count recordsets

        :param context: RPC Context.
        :param criterion: Criteria to filter by.
        """

    @abc.abstractmethod
    def create_record(self, context, domain_id, recordset_id, record):
        """
        Create a record on a given Domain ID

        :param context: RPC Context.
        :param domain_id: Domain ID to create the record in.
        :param recordset_id: RecordSet ID to create the record in.
        :param record: Record object with the values to be created.
       """

    @abc.abstractmethod
    def get_record(self, context, record_id):
        """
        Get a record via ID

        :param context: RPC Context.
        :param record_id: Record ID to get
        """

    @abc.abstractmethod
    def find_records(self, context, criterion=None, marker=None,
                     limit=None, sort_key=None, sort_dir=None):
        """
        Find Records.

        :param context: RPC Context.
        :param criterion: Criteria to filter by.
        :param marker: Resource ID from which after the requested page will
                       start after
        :param limit: Integer limit of objects of the page size after the
                      marker
        :param sort_key: Key from which to sort after.
        :param sort_dir: Direction to sort after using sort_key.
        """

    @abc.abstractmethod
    def find_record(self, context, criterion):
        """
        Find a single Record.

        :param context: RPC Context.
        :param criterion: Criteria to filter by.
        """

    @abc.abstractmethod
    def update_record(self, context, record):
        """
        Update a record

        :param context: RPC Context
        :param record: Record to update
        """

    @abc.abstractmethod
    def delete_record(self, context, record_id):
        """
        Delete a record

        :param context: RPC Context
        :param record_id: Record ID to delete
        """

    @abc.abstractmethod
    def count_records(self, context, criterion=None):
        """
        Count records

        :param context: RPC Context.
        :param criterion: Criteria to filter by.
        """

    @abc.abstractmethod
    def create_blacklist(self, context, blacklist):
        """
        Create a Blacklist.

        :param context: RPC Context.
        :param blacklist: Blacklist object with the values to be created.
        """

    @abc.abstractmethod
    def get_blacklist(self, context, blacklist_id):
        """
        Get a Blacklist via ID.

        :param context: RPC Context.
        :param blacklist_id: Blacklist ID to get.
        """

    @abc.abstractmethod
    def find_blacklists(self, context, criterion=None, marker=None,
                        limit=None, sort_key=None, sort_dir=None):
        """
        Find Blacklists

        :param context: RPC Context.
        :param criterion: Criteria to filter by.
        :param marker: Resource ID from which after the requested page will
                       start after
        :param limit: Integer limit of objects of the page size after the
                      marker
        :param sort_key: Key from which to sort after.
        :param sort_dir: Direction to sort after using sort_key.
        """

    @abc.abstractmethod
    def find_blacklist(self, context, criterion):
        """
        Find a single Blacklist.

        :param context: RPC Context.
        :param criterion: Criteria to filter by.
        """

    @abc.abstractmethod
    def update_blacklist(self, context, blacklist):
        """
        Update a Blacklist

        :param context: RPC Context.
        :param blacklist: Blacklist to update.
        """

    @abc.abstractmethod
    def delete_blacklist(self, context, blacklist_id):
        """
        Delete a Blacklist via ID.

        :param context: RPC Context.
        :param blacklist_id: Delete a Blacklist via ID
        """

    @abc.abstractmethod
    def create_pool(self, context, pool):
        """
        Create a Pool.

        :param context: RPC Context.
        :param pool: Pool object with the values to be created.
        """

    @abc.abstractmethod
    def find_pools(self, context, criterion=None, marker=None,
                   limit=None, sort_key=None, sort_dir=None):
        """
        Find all Pools

        :param context: RPC Context
        :param criterion: Criteria by which to filter
        :param marker: Resource ID used by paging. The next page will start
                       at the next resource after the marker
        :param limit: Integer limit of objects on the page
        :param sort_key: Key used to sort the returned list
        :param sort_dir: Directions to sort after using sort_key
        """

    @abc.abstractmethod
    def find_pool(self, context, criterion):
        """
        Find a single Pool.

        :param context: RPC Context.
        :param criterion: Criteria to filter by.
        """

    @abc.abstractmethod
    def get_pool(self, context, pool_id):
        """
        Get a Pool via the id

        :param context: RPC Context
        :param pool_id: The ID of the pool to get
        :return: The requested pool
        """

    @abc.abstractmethod
    def update_pool(self, context, pool):
        """
        Update the specified pool

        :param context: RPC Context
        :param pool_id: The ID of the pool to be updated
        :return: The updated pool
        """

    @abc.abstractmethod
    def delete_pool(self, context, pool_id):
        """
        Delete the pool with the matching id

        :param context: RPC Context
        :param pool_id: The ID of the pool to be deleted
        """

    def ping(self, context):
        """Ping the Storage connection"""
        return {
            'status': None
        }
