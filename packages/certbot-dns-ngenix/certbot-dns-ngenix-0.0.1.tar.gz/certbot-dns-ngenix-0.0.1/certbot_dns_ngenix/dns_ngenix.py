"""DNS Authenticator for Ngenix."""
import logging
from xml import dom

import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common
from certbot_dns_ngenix.ngenix_api import NgenixApi

logger = logging.getLogger(__name__)

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for NGENIX

    This Authenticator uses the NGENIX Remote REST API to fulfill a dns-01 challenge.
    """

    description = "Obtain certificates using a DNS TXT record (if you are using Ngenix for DNS)."
    ttl = 300

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add, default_propagation_seconds: int = 300):
        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds)
        add('credentials', help='NGENIX credentials INI file.')

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return "This plugin configures a DNS TXT record to respond to a dns-01 challenge " + \
               "using the NGENIX Remote REST API."

    def _validate_credentials(self, credentials):
        email = credentials.conf('email')
        token = credentials.conf('api_token')
        if email or token:
            if not email:
                raise errors.PluginError('{}: dns_ngenix_email is required when using an API token. '
                                         '(should be email address associated with NGENIX account)'
                                         .format(credentials.confobj.filename))
            if not token:
                raise errors.PluginError('{}: dns_ngenix_api_token is required when using an '
                                         'API token.'
                                         .format(credentials.confobj.filename))
        else:
            raise errors.PluginError('{}: Both dns_ngenix_email and dns_ngenix_api_token '
                                     'are required.'.format(credentials.confobj.filename))

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'NGENIX credentials INI file',
            None,
            self._validate_credentials
        )

    def _perform(self, domain, validation_name, validation):
        self._get_ngenix_client().add_txt_record(domain, validation_name, validation, self.ttl)

    def _cleanup(self, domain, validation_name, validation):
        self._get_ngenix_client().del_txt_record(domain, validation_name, validation)

    def _get_ngenix_client(self):
        if not self.credentials:  # pragma: no cover
            raise errors.Error("Plugin has not been prepared.")
        return _NgenixClient(self.credentials.conf('email'), self.credentials.conf('api_token'))

class _NgenixClient:
    """
    Encapsulates all communication with the NGENIX API.
    """

    def __init__(self, email, api_token):
        self.api = NgenixApi(email, api_token)
        self.me = self.api.whoami()

    def add_txt_record(self, domain: str, record_name: str, record_content: str, record_ttl: int) -> None:
        """
        Add a TXT record using the supplied information.
        :param str domain: The domain to use to look up the NGENIX zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :param int record_ttl: Not used for NGENIX.
        :raises certbot.errors.PluginError: if an error occurs communicating with the NGENIX API
        """

        zone_id = self._find_zone_id(domain)
        zone_data = self._get_zone_data(zone_id)
        record_name = record_name.replace('.' + zone_data['name'], '')

        record = {"name": record_name,
                "type": "TXT",
                "data": record_content}

        records = zone_data['records']
        ok = False
        for rr in records:
            if rr['name'] == record_name:
                rr['data'] = record_content
                ok = True
        if not ok:
            records.append(record)

        self.api.update_zone(zone_id, {"records": records})

    def del_txt_record(self, domain: str, record_name: str, record_content: str) -> None:
        """
        Delete a TXT record using the supplied information.
        Note that both the record's name and content are used to ensure that similar records
        created concurrently (e.g., due to concurrent invocations of this plugin) are not deleted.
        Failures are logged, but not raised.
        :param str domain: The domain to use to look up the NGENIX zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        """

        zone_id = self._find_zone_id(domain)
        zone_data = self._get_zone_data(zone_id)
        record_name = record_name.replace('.' + zone_data['name'], '')

        record = {"name": record_name, 
                "type": "TXT",
                "data": record_content}

        records = zone_data['records']
        for rr in records:
            if rr['name'] == record_name and rr['data'] == record_content:
                del records[records.index(record)]

        self.api.update_zone(zone_id, {"records": records})

    def _find_zone_id(self, domain):
        """
        Find the zone_id for a given domain.
        :param str domain: The domain for which to find the zone_id.
        :returns: The zone_id, if found.
        :rtype: str
        :raises certbot.errors.PluginError: if no zone_id is found.
        """

        zone_name_guesses = dns_common.base_domain_name_guesses(domain)
        logger.debug(zone_name_guesses)

        try:
            zones = self.api.list_zones(self.me['customerRef']['id'])
            for zone in zones['elements']:
                logger.debug(zone)
                if zone['name'] in zone_name_guesses:
                    return zone['id']
        except Exception as e:
            raise errors.PluginError('{}'.format(e))
        
        raise errors.PluginError('Cannot find zone for domain: {}'.format(domain))
        
    def _get_zone_data(self, zone_id):
        """
        Get zone data.
        :param str zone_id: id to use to get the zone.
        :returns: The zone_data, if found.
        :rtype: object
        :raises certbot.errors.PluginError: if no zone_data is found.
        """

        try:
            zone_data = self.api.get_zone(zone_id)
        except Exception as e:
            raise errors.PluginError('Unable to get zone data: {}'.format(e))

        return zone_data