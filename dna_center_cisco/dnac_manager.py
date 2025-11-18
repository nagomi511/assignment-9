import requests
from requests.auth import HTTPBasicAuth
import urllib3
import sys
import os


sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cisco_dnac_assignment'))
from dnac_config import DNAC

urllib3.disable_warnings()

class DNAC_Manager:
    def __init__(self):
        self.token = None
    
    def get_auth_token(self):
        """Authenticates to DNA Center and returns token"""
        try:
            url = f"https://{DNAC['host']}:{DNAC['port']}/dna/system/api/v1/auth/token"
            response = requests.post(
                url,
                auth=HTTPBasicAuth(DNAC['username'], DNAC['password']),
                verify=False,
                timeout=10
            )
            response.raise_for_status()
            self.token = response.json()['Token']
            return {'success': True, 'token': self.token}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_network_devices(self):
        """Retrieves all network devices"""
        if not self.token:
            auth_result = self.get_auth_token()
            if not auth_result['success']:
                return {'success': False, 'error': 'Authentication failed'}
        
        try:
            url = f"https://{DNAC['host']}:{DNAC['port']}/api/v1/network-device"
            headers = {"X-Auth-Token": self.token}
            response = requests.get(url, headers=headers, verify=False, timeout=10)
            response.raise_for_status()
            devices = response.json().get('response', [])
            return {'success': True, 'devices': devices}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_device_interfaces(self, device_ip):
        """Retrieves interfaces for specific device"""
        if not self.token:
            auth_result = self.get_auth_token()
            if not auth_result['success']:
                return {'success': False, 'error': 'Authentication failed'}
        
        try:
            # Find device by IP
            devices_result = self.get_network_devices()
            if not devices_result['success']:
                return devices_result
            
            devices = devices_result['devices']
            device = next(
                (d for d in devices if d.get('managementIpAddress') == device_ip),
                None
            )
            
            if not device:
                return {'success': False, 'error': f'Device {device_ip} not found'}
            
            # Get interfaces
            url = f"https://{DNAC['host']}:{DNAC['port']}/api/v1/interface"
            headers = {"X-Auth-Token": self.token}
            params = {"deviceId": device['id']}
            response = requests.get(url, headers=headers, params=params, verify=False, timeout=10)
            response.raise_for_status()
            interfaces = response.json().get('response', [])
            return {'success': True, 'interfaces': interfaces, 'device': device}
        except Exception as e:
            return {'success': False, 'error': str(e)}