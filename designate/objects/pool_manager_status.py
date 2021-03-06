# Copyright 2014 eBay Inc.
#
# Author: Ron Rickard <rrickard@ebaysf.com>
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
from designate.objects import base


class PoolManagerStatus(base.DictObjectMixin, base.PersistentObjectMixin,
                        base.DesignateObject):
    FIELDS = {
        'server_id': {},
        'domain_id': {},
        'status': {},
        'serial_number': {},
        'action': {}
    }


class PoolManagerStatusList(base.ListObjectMixin, base.DesignateObject):
    LIST_ITEM_TYPE = PoolManagerStatus
