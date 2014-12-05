# Copyright 2014 Mirantis
#
# This work is licensed under a Creative Commons Attribution 3.0
# Unported License.
# http://creativecommons.org/licenses/by/3.0/legalcode

import logging

from oslo.config import cfg

LOG = logging.getLogger(__name__)


cfg.CONF.register_group(cfg.OptGroup(
    name='backend:infoblox', title="Configuration for Infoblox Backend"
))

OPTS = [
    cfg.StrOpt('infoblox_wapi',
               default='https://10.39.11.123/wapi/v1.4.1/'),
    cfg.StrOpt('infoblox_username',
               default='admin'),
    cfg.StrOpt('infoblox_password',
               default='infoblox'),
    cfg.BoolOpt('infoblox_sslverify', default=False),
    cfg.BoolOpt('multi_tenant', default=False),
    cfg.IntOpt('infoblox_http_pool_connections', default=100),
    cfg.IntOpt('infoblox_http_pool_maxsize', default=100),
    cfg.StrOpt('dns_view', default='default'),
    cfg.StrOpt('net_view', default='default'),
]

cfg.CONF.register_opts(OPTS, group='backend:infoblox')
