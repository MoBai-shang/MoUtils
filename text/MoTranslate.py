import json
import requests
# 翻译函数，word 需要翻译的内容
class mutiTry():
    def trans(self,text):
        pass
    def tryTrans(self,text,trys=4):
        ans=None
        for i in range(trys):
            try:
                ans=self.trans(text)
                if not ans:
                    continue
                break
            except:
                pass
        return ans
class YouDaoTranslate(mutiTry):
    def __init__(self,url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null',
                    key= {'type': "AUTO",
                       'i': None,
                        "doctype": "json",
                        "version": "2.1",
                        "keyfrom": "fanyi.web",
                        "ue": "UTF-8",
                        'Accept-Language':'zh-CN,zh;q=0.9',
                        "action": "FY_BY_CLICKBUTTON",
                        "typoResult": "true"}):
        
        self.url=url
        self.key=key
    def trans(self,text):
        self.key['i']=text
        response = requests.post(self.url, data=self.key)
        # 判断服务器是否相应成功
        if response.status_code == 200:
            # 然后相应的结果
            result = json.loads(response.text)
            return result['translateResult'][0][0]['tgt']
        else:
            print("有道词典调用失败")
            # 相应失败就返回空
            return None


"""官方Python接入百度翻译API测试Demo（有所改动，官方DEMO有些过时，Python包有些变化）"""
import httplib2
import urllib
import random
import json
from hashlib import md5
class BaiDuTranslate(mutiTry):
    def __init__(self,appid = '20151113000005349',
                 secretKey = 'osubCEzlGjzvw8qdQc41',
                 url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'):
        
        self.appid=appid
        self.secretKey=secretKey
        self.url=url
    def trans(self,text,fromLang = 'en',toLang = 'zh'):
        salt = random.randint(32768, 65536)
        # 签名
        sign = self.appid+text+str(salt)+self.secretKey
        m1 = md5()
        m1.update(sign.encode(encoding = 'utf-8'))
        sign = m1.hexdigest()
        # myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
        myurl = self.url+'?q='+urllib.parse.quote(text)+'&from='+fromLang+'&to='+toLang+'&appid='+self.appid+'&salt='+str(salt)+'&sign='+sign
        try:
            h = httplib2.Http('.cache')
            response, content = h.request(myurl)
            if response.status == 200:
                response = json.loads(content.decode('utf-8'))  # loads将json数据加载为dict格式
                return response["trans_result"][0]['dst']
        except httplib2.ServerNotFoundError:
            print("Site is Down!")

from translate import Translator
class MiscroTranslate(mutiTry):
    def __init__(self,from_lang="english",to_lang="chinese"):

        self.mt=Translator(from_lang=from_lang,to_lang=to_lang)
    def trans(self,text):
        return self.mt.translate(text)

from urllib import request, parse
import json
 
# 有道翻译：中文→英文
def fy(i):
    req_url = 'http://fanyi.youdao.com/translate'  # 创建连接接口
    # 创建要提交的数据
    Form_Date = {}
    Form_Date['i'] = i
    Form_Date['doctype'] = 'json'
    Form_Date['form'] = 'AUTO'
    Form_Date['to'] = 'AUTO'
    Form_Date['smartresult'] = 'dict'
    Form_Date['client'] = 'fanyideskweb'
    Form_Date['salt'] = '1526995097962'
    Form_Date['sign'] = '8e4c4765b52229e1f3ad2e633af89c76'
    Form_Date['version'] = '2.1'
    Form_Date['keyform'] = 'fanyi.web'
    Form_Date['action'] = 'FY_BY_REALTIME'
    Form_Date['typoResult'] = 'false'
 
    data = parse.urlencode(Form_Date).encode('utf-8')  # 数据转换
    response = request.urlopen(req_url, data)  # 提交数据并解析
    html = response.read().decode('utf-8')  # 服务器返回结果读取
    # print(html)
    # 可以看出html是一个json格式
    translate_results = json.loads(html)  # 以json格式载入
    translate_results = translate_results['translateResult'][0][0]['tgt']  # json格式调取
    # print(translate_results)  # 输出结果
    return translate_results;  # 返回结果
def tryfy(text,trys=4):
    ans=None
    for i in range(trys):
        try:
            ans=fy(text)
            if not ans:
                continue
            break
        except:
            pass
    return ans
