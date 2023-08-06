import os
import requests
import yaml

class ClusterCfg:
    """_summary_
    集群的配置
    app_token: profile下类型为application的token,若不设置，则会使用时生成
    """    
    def __init__(self) -> None:
        self.user_name = "user"
        self.password = "user_pwd"
        self.host = "http://localhost:80"
        self.app_token=""

class PaiClient:
    def __init__(self, cluster_cfg):
        self.cluster_cfg = cluster_cfg
        self.rest_server = self.cluster_cfg.host + "/rest-server"
        self.token_revoke=False
        if self.cluster_cfg.app_token=="":
            self.cluster_cfg.app_token=self.__create_app_token()
            self.token_revoke=True
    
    def __del__(self):
        if self.token_revoke:
            self.__revoke_app_token()

    def __login(self): 
        """_summary_
        根据账号密码获取一个token
        Returns:
            _type_: _description_
        """       
        api_url = self.rest_server + "/api/v2/authn/basic/login"
        header = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            'Connection': 'close'
        }
        try:
            response = requests.post(api_url,headers=header,data={"username":self.cluster_cfg.user_name,"password":
            self.cluster_cfg.password})
            if response.status_code!=200:
                print("login failed: {0},{1}".format(response.status_code,response.text))
        except Exception as e:
            print(e)
        return response.json()

    def __create_app_token(self):
        response=self.__login()
        if not 'token' in response or (response['token']==""):
            print("create app token failed")
            return
        
        api_url = self.rest_server + "/api/v2/tokens/application"
        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(response["token"])
        }
        response_app = requests.post(api_url,headers=header)
        #revoke himself
        self.__revoke_browser_token(token=response["token"])
        if 'token' in response_app.json():
            return response_app.json()['token']
        else:
            return ""

    def __revoke_app_token(self):
        response=self.__login()
        if not 'token' in response or (response['token']==""):
            print("create app token failed")
            return
        api_url = self.rest_server + "/api/v2/tokens/{0}".format(self.cluster_cfg.app_token)
        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(response["token"])
        }
        response_app = requests.delete(api_url,headers=header)
        #revoke himself
        self.__revoke_browser_token(response["token"])
        print(response_app.text)
    
    def __revoke_browser_token(self,token=""):
        if token=="":
            return
        api_url = self.rest_server + "/api/v2/tokens/{0}".format(token)
        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(token)
        }
        response_app = requests.delete(api_url,headers=header)
        print(response_app.text)    
    
    def create_job(self,job_config_yaml):
        api_url = self.rest_server + "/api/v2/jobs"
        header = {
            "Content-Type": "text/yaml",
            "Authorization": "Bearer {0}".format(self.cluster_cfg.app_token)
        }
        if os.path.isfile(job_config_yaml):
            with open(job_config_yaml,'r') as f:
               job_config_yaml = yaml.safe_load(f)
        return requests.post(api_url,data=yaml.safe_dump(job_config_yaml),headers=header)
    
    def get_job_status(self,job_name):
        api_url = self.rest_server + "/api/v2/jobs/{0}~{1}".format(self.cluster_cfg.user_name,job_name)
        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(self.cluster_cfg.app_token)
        }
        return requests.get(api_url,headers=header)