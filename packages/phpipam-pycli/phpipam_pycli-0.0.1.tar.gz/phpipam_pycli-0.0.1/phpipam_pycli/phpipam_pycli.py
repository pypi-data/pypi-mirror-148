import requests

class PhpIpamClient():

    def __init__(self, base_url, app_id, token, cert):
        self.base_url = base_url
        self.app_id = app_id
        self.token = token
        self.cert = cert
    
    def search_ip(self,ip):
        headers_dict = {
            "token": self.token
        }

        res = requests.get(f'{self.base_url}{self.app_id}/addresses/search/{ip}/', headers=headers_dict, verify=self.cert)
        return res.json()
    

    def search_subnet(self,range):
        headers_dict = {
            "token": self.token
        }

        res_id = requests.get(f'{self.base_url}{self.app_id}/subnets/search/{range}/', headers=headers_dict, verify=self.cert)
        res_id_json = res_id.json()
        
        if(res_id_json['success']):
            
            res = requests.get(f'{self.base_url}{self.app_id}/subnets/{res_id_json["data"][0]["id"]}/addresses/', headers=headers_dict, verify=self.cert)
            return res.json()
        else:
            return res_id.json()
    
    def search_subnet_by_id(self,id):
        headers_dict = {
            "token": self.token
        }
      
        res = requests.get(f'{self.base_url}{self.app_id}/subnets/{id}/addresses/', headers=headers_dict, verify=self.cert)
        return res.json()
 
    
    def get_public_subnet_id(self):
        headers_dict = {
            "token": self.token
        }

        res_subnet = requests.get(f'{self.base_url}{self.app_id}/subnets/all', headers=headers_dict, verify=self.cert)
        res_subnet_json = res_subnet.json()

        public_subnet_id = []

        for subnet in res_subnet_json['data']:
            if(subnet['subnet'].startswith('10') == False and subnet['subnet'].startswith('198') == False and subnet['subnet'].startswith('172') == False and subnet['subnet'].startswith('192') == False):
                public_subnet_id.append(subnet['id'])
        
        return public_subnet_id


    def get_public_subnet(self):
        headers_dict = {
            "token": self.token
        }

        res_subnet = requests.get(f'{self.base_url}{self.app_id}/subnets/all', headers=headers_dict, verify=self.cert)
        res_subnet_json = res_subnet.json()

        public_subnet = []

        for subnet in res_subnet_json['data']:
            if(subnet['subnet'].startswith('10') == False and subnet['subnet'].startswith('198') == False and subnet['subnet'].startswith('172') == False and subnet['subnet'].startswith('192') == False):
                public_subnet.append(f'{subnet["subnet"]}/{subnet["mask"]}')
        
        return public_subnet