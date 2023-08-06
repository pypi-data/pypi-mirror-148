"""
Wrapper for just-mining.com API. 

Official documentation: https://docs.just-mining.com/
"""

import requests

class JustMining:
    api_key = None
    base_url = None

    def __init__(self, api_key, api_version='v1'):
        self.api_key = api_key
        self.base_url = f"https://api.just-mining.com/{api_version}/"

    def get(self, endpoint="status", id=None):
        url = self.base_url + endpoint
        if id:
            url += f"/{id}"
        headers = {'API-KEY': self.api_key}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code} {response.reason}")
            return None
        
        res = response.json()
        if res and res['success']:
            return res['data']
        return None



    # Masternodes
    def masternodes(self, id=None):
        return self.get("masternodes", id)

    # Hardwares
    def hardwares(self, type):
        return self.get("hardwares", type)

    def bobs(self, serial):
        return self.get("hardwares/bobs", serial)

    def asics(self, id):
        return self.get("hardwares/asics", id)

    # Clouds
    def clouds(self, id=None):
        return self.get("clouds", id)

    # Stakings
    def stakings(self, currency=None):
        return self.get(f"stakings", currency)

    # Lendings
    def lendings(self, currency=None):
        return self.get("lendings", currency)

    # Wallets
    def wallets(self, currency=None):
        return self.get("wallets", currency)

    # Wallet adresses
    def wallet_addresses(self, currency=None, id=None):
        params = currency
        if currency and id:
            params = f"{currency}/{id}"
        return self.get("walletAddresses", params)

    # Operations
    def operations(self, id=None):
        return self.get("operations", id)