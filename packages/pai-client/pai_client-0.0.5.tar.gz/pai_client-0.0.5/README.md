## 简介
封装OpenPAI的rest-server接口，用于通过代码提交任务，为多任务调度做好基础
## 安装
> pip install pai_client --upgrade
## API说明
***ClusterCfg***  
pai集群的配置  
- user_name: 用户账号
- password: 用户密码
- host: pai的地址
- app_token: application token, 在个人profile页面可生成。若不设置，则会自动生成一个，退出时会删除  

***PaiClient***  
调用客户端，通过ClusterCfg初始化  
```create_job(self,job_config_yaml)```  
通过job配置文件(或字符串）提交一个job
- job_config_yaml: pai job的配置文件  
- return: rest-server的返回值

```get_job_status(self,job_name)```  
获取job的状态  
- job_name: 要查询的job名
- return: rest-server的返回值