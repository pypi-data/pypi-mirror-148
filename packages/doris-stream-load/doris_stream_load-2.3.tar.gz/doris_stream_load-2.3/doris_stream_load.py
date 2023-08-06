from http import client
import base64
import requests
client.HTTPConnection._http_vsn = 10
client.HTTPConnection._http_vsn_str = 'HTTP/1.0'


class stream_load:

    def __init__(self, doris_host,doris_user,doris_password,doris_http_port,database,table_name,column_separator):
        self.doris_host = doris_host
        self.doris_user = doris_user
        self.doris_password = doris_password
        self.doris_http_port = doris_http_port
        self.database = database
        self.table_name = table_name
        self.column_separator = column_separator
        self.requests_session = requests.session()

    def sendData(self,row_list):
        loadUrl = "http://%s:%s/api/%s/%s/_stream_load/" % (self.doris_host,self.doris_http_port, self.database, self.table_name)
        headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                   'column_separator': self.column_separator,
                   'two_phase_commit': 'true',
                   'Accept': 'application/json;charset=UTF-8',
                   'Expect': '100-continue',
                   "Authorization": "Basic " + base64.b64encode(
                       bytes(self.doris_user + ":" + self.doris_password, 'utf-8')).decode(
                       'utf-8')}
        # print(loadUrl)
        # print(json_content)
        response_put = self.requests_session.put(loadUrl, data='\n'.join(row_list), headers=headers, timeout=600)
        return response_put.json()

    def help(self):
        return "## 简介\n " \
               "Stream load 是一个同步的导入方式,用户通过发送 HTTP 协议发送请求将本地文件或数据流导入到 Doris 中。Stream load 同步执行导入并返回导入结果。用户可直接通过请求的返回体判断本次导入是否成功。\n " \
               "Stream load 主要适用于导入本地文件,或通过程序导入数据流中的数据。\n " \
               "## Install\n " \
                "``\n " \
                    "pip install doris_stream_load\n " \
                "```\n " \
                "## Usage\n " \
                "```\n " \
                    "from doris_stream_load1 import stream_load\n " \
                    "dsl = stream_load(doris_host, doris_user, doris_password, doris_http_port, database, table_name, column_separator)\n " \
                    "row_list=[] # 数据源每行数据的列表,列表元素必须是由column_separator拼接的字段字符串,建议row_list长度为10000~100000\n " \
                    "dsl.sendData(row_list)\n " \
                "```\n " \
                "## __init__\n " \
                "```\n " \
                    "def __init__(self, doris_host,doris_http_port,doris_user,doris_password,,database,table_name,column_separator):\n " \
                        "stream_load类初始化\n " \
                        ":param doris_host: doris的Be节点IP地址\n " \
                        ":param doris_http_port: doris_host对应的http端口号\n " \
                        ":param doris_user: doris账户\n " \
                        ":param doris_password: doris账户对应的密码\n " \
                        ":param database: 要导入的数据库\n " \
                        ":param table_name: 要导入的表\n " \
                        ":param column_separator: 字段分隔符\n " \
                "```\n " \
                "## sendData\n " \
                "```\n " \
                    "def sendData(self,row_list):\n " \
                        "stream_load导入数据\n " \
                        ":param row_list: 数据源每行数据的列表,列表元素必须是由column_separator拼接的字段字符串,建议row_list长度为10000~100000\n " \
                        ":return: str,stream load返回的json格式结果\n " \
                "```"




