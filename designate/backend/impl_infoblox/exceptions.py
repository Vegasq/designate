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

import gettext

_ = gettext.gettext


class DesignateException(Exception):
    """Base Designate Exception.

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """
    message = _("An unknown exception occurred.")

    def __init__(self, **kwargs):
        try:
            super(DesignateException, self).__init__(self.message % kwargs)
            self.msg = self.message % kwargs
        except Exception:
            if self.use_fatal_exceptions():
                raise
            else:
                # at least get the core message out if something happened
                super(DesignateException, self).__init__(self.message)

    def __unicode__(self):
        return unicode(self.msg)

    def use_fatal_exceptions(self):
        return False


class ServiceUnavailable(DesignateException):
    message = _("The service is unavailable")


class ResourceExhausted(ServiceUnavailable):
    pass


class InfobloxException(DesignateException):
    """Generic Infoblox Exception."""
    def __init__(self, response, **kwargs):
        self.response = response
        super(InfobloxException, self).__init__(**kwargs)


class InfobloxIsMisconfigured(DesignateException):
    message = _("Infoblox IPAM is misconfigured: infoblox_wapi, "
                "infoblox_username and infoblox_password must be defined.")


class InfobloxSearchError(InfobloxException):
    message = _("Cannot search '%(objtype)s' object(s): "
                "%(content)s [code %(code)s]")


class InfobloxCannotCreateObject(InfobloxException):
    message = _("Cannot create '%(objtype)s' object(s): "
                "%(content)s [code %(code)s]")


class InfobloxCannotDeleteObject(InfobloxException):
    message = _("Cannot delete object with ref %(ref)s: "
                "%(content)s [code %(code)s]")


class InfobloxCannotUpdateObject(InfobloxException):
    message = _("Cannot update object with ref %(ref)s: "
                "%(content)s [code %(code)s]")


class InfobloxFuncException(InfobloxException):
    message = _("Error occured during function's '%(func_name)s' call: "
                "ref %(ref)s: %(content)s [code %(code)s]")


class NoInfobloxMemberAvailable(ResourceExhausted):
    message = _("No Infoblox Member is available.")


class InfobloxObjectParsingError(DesignateException):
    message = _("Infoblox object cannot be parsed from dict: %(data)s")
