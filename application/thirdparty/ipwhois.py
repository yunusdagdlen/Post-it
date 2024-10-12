#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Post-it
import json

import requests


class IPWhois:
    def __init__(self, config):
        self.ipwhois_path = 'https://api.findip.net/{}/?token={}'
        self.config = config



    def get_iphois_info(self, ip_address):
        ipwhois = {}
        try:
            response = requests.get(self.ipwhois_path.format(ip_address, self.config['FINDAPI_TOKEN']), timeout=5)
            ipwhois = json.loads(response.text)
        except requests.exceptions.Timeout:
            pass

        return ipwhois
