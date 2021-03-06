# Copyright 2014 eBay Inc.
#
# Author: Ron Rickard <rrickard@ebay.com>
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
import socket

from oslo.config import cfg

from designate.openstack.common import log as logging
from designate import exceptions
from designate import utils
from designate.backend import base
from designate.openstack.common import processutils


LOG = logging.getLogger(__name__)

cfg_opts = [
    cfg.ListOpt('masters', default=['127.0.0.1:5354'],
                help='Comma-separated list of master DNS servers, in '
                     ' <ip-address>:<port> format. If <port> is omitted, '
                     'the default 5354 is used.  These are mdns servers.'),
    cfg.StrOpt('rndc-host', default='127.0.0.1', help='RNDC Host'),
    cfg.IntOpt('rndc-port', default=953, help='RNDC Port'),
    cfg.StrOpt('rndc-config-file', default=None, help='RNDC Config File'),
    cfg.StrOpt('rndc-key-file', default=None, help='RNDC Key File'),
]
DEFAULT_PORT = 5354


class Bind9PoolBackend(base.PoolBackend):
    __plugin_name__ = 'bind9_pool'

    def __init__(self, backend_options):
        super(Bind9PoolBackend, self).__init__(backend_options)
        self.masters = [self._parse_master(master)
                        for master in self.get_backend_option('masters')]
        self.rndc_host = self.get_backend_option('rndc_host')
        self.rndc_port = self.get_backend_option('rndc_port')
        self.rndc_config_file = self.get_backend_option('rndc_config_file')
        self.rndc_key_file = self.get_backend_option('rndc_key_file')

    @staticmethod
    def _parse_master(master):
        try:
            (ip_address, port) = master.split(':', 1)
        except ValueError:
            ip_address = str(master)
            port = DEFAULT_PORT
        try:
            port = int(port)
        except ValueError:
            raise exceptions.ConfigurationError(
                'Invalid port "%s" in masters option.' % port)
        if port < 0 or port > 65535:
            raise exceptions.ConfigurationError(
                'Port "%s" is not between 0 and 65535 in masters option.' %
                port)
        try:
            socket.inet_pton(socket.AF_INET, ip_address)
        except socket.error:
            raise exceptions.ConfigurationError(
                'Invalid IP address "%s" in masters option.' % ip_address)
        return {'ip-address': ip_address, 'port': port}

    @classmethod
    def get_cfg_opts(cls):
        return cfg_opts

    def create_domain(self, context, domain):
        LOG.debug('Create Domain')
        masters = []
        for master in self.masters:
            ip_address = master['ip-address']
            port = master['port']
            masters.append('%s port %s' % (ip_address, port))
        rndc_op = [
            'addzone',
            '%s { type slave; masters { %s;}; file "slave.%s%s"; };' %
            (domain['name'], '; '.join(masters), domain['name'], domain['id']),
        ]
        self._execute_rndc(rndc_op)

    def delete_domain(self, context, domain):
        LOG.debug('Delete Domain')
        rndc_op = [
            'delzone',
            '%s' % domain['name'],
        ]
        self._execute_rndc(rndc_op)

    def _rndc_base(self):
        rndc_call = [
            'rndc',
            '-s', self.rndc_host,
            '-p', str(self.rndc_port),
        ]

        if self.rndc_config_file:
            rndc_call.extend(
                ['-c', self.rndc_config_file])

        if self.rndc_key_file:
            rndc_call.extend(
                ['-k', self.rndc_key_file])

        return rndc_call

    def _execute_rndc(self, rndc_op):
        try:
            rndc_call = self._rndc_base()
            rndc_call.extend(rndc_op)
            LOG.debug('Executing RNDC call: %s' % " ".join(rndc_call))
            utils.execute(*rndc_call)
        except processutils.ProcessExecutionError as e:
            raise exceptions.Backend(e)
