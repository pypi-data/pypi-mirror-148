import os,time
import requests
import yaml
import logging

formatter="%(asctime)s: [{0}] %(filename)sline:%(lineno)d %(message)s".format("pai")
logging.basicConfig(level=logging.INFO,format=formatter)
logger=logging.getLogger("pai")

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
                logger.info("login failed: {0},{1}".format(response.status_code,response.text))
        except Exception as e:
            logger.error()
        return response.json()

    def __create_app_token(self):
        response=self.__login()
        if not 'token' in response or (response['token']==""):
            logger.error("create app token failed")
            return ""
        
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
        return response_app
    
    def __revoke_browser_token(self,token=""):
        if token=="":
            return
        api_url = self.rest_server + "/api/v2/tokens/{0}".format(token)
        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(token)
        }
        response_app = requests.delete(api_url,headers=header)
        return response_app
    
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
    
    def wait_for_job_complete(self,job_name):
        interval_sec = 60
        while True:
            response=self.get_job_status(job_name)
            if response.status_code != 200: #todo: only exit when job has error
                logger.error("error happened: JobName: {0} status {1}, {2}".format(job_name, response.status_code,response.text))
                return response

            response_json=response.json()
            job_state=response_json['jobStatus']['state']
            if job_state=='STOP' or job_state=='FAILED':
                response.status_code=400
                logger.error("error happened: JobName: {0} status {1}, {2}".format(job_name, job_state,response.text))
                return response
            elif job_state=='SUCCEEDED':
                logger.info("job finished: JobName: {0}".format(job_name))
                return response

            logger.info("job is {0}, JobName: {1}".format(job_state,job_name))
            time.sleep(interval_sec)