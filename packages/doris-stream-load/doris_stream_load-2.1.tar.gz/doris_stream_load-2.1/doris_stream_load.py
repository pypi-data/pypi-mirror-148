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




