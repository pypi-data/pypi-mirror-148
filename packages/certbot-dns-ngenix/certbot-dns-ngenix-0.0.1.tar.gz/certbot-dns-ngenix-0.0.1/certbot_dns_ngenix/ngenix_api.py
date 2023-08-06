"""NGENIX API wrapper"""
import logging

import json
from typing import Dict
import requests

logger = logging.getLogger(__name__)

class NgenixApi:
    email = None
    api_token = None
    base_url = 'https://api.ngenix.net/api/v3'

    me = None

    def __init__(self, email, api_token):
        self.http_auth = (str(email + '/token'), str(api_token))
        
    def _query(self, uri, method, kwargs=None):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        data = json.dumps(kwargs)

        if method == "GET":
            request = requests.get(self.base_url + uri, headers=headers,
                                   auth=self.http_auth, verify=True)
        # elif method == "POST":
        #     request = requests.post(self.base_url + uri, headers=headers, data=data,
        #                             auth=self.http_auth, verify=True)
        # elif method == "PUT":
        #     request = requests.put(self.base_url + uri, headers=headers, data=data,
        #                            auth=self.http_auth, verify=True)
        elif method == "PATCH":
            request = requests.patch(self.base_url + uri, headers=headers, data=data,
                                     auth=self.http_auth, verify=True)
        # elif method == "DELETE":
        #     request = requests.delete(self.base_url + uri, headers=headers,
        #                               auth=self.http_auth, verify=True)
        else:
            raise ValueError("Invalid method '%s'" % method)

        return None if request.status_code == 204 else request.json()

    def whoami(self) -> Dict:
        if self.me is None:
            me = self._query("/whoami", "GET")
            self.me = self._query("/user/%s" % me['userRef']['id'], "GET")
            logger.debug(self.me)
        return self.me

    def list_zones(self, customer_id) -> Dict:
        zones = self._query("/dns-zone?customerId=%s" % customer_id, "GET")
        logger.debug(zones)
        return zones

    def get_zone(self, zone_id) -> Dict:
        zone_data = self._query("/dns-zone/%s" % zone_id, "GET")
        logger.debug('Zone {}: {}'.format(zone_id, zone_data))
        return zone_data

    def update_zone(self, zone_id, zone_data) -> None:
        logger.debug('Zone {}: {}'.format(zone_id, zone_data))
        return self._query("/dns-zone/%s" % zone_id, "PATCH", zone_data)