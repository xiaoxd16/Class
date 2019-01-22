from django.utils import timezone
from codex.baseview import *
from urllib import parse,request
import json


CONFIGS = json.loads(open('configs.json').read())

WECHAT_APPID = CONFIGS['WECHAT_APPID']
WECHAT_SECRET = CONFIGS['WECHAT_SECRET']

class LoginView(APIView):
	def get(self):
		self.check_input('code')
		url = "https://api.weixin.qq.com/sns/jscode2session"
		CODE = self.input['code']
		data = {
			'appid': WECHAT_APPID,
            'secret': WECHAT_SECRET,
            'js_code': CODE,
            'grant_type': 'authorization_code'
		}
		data = parse.urlencode(data).encode('utf-8')
		req = request.Request(url=url,data = data)
		res = request.urlopen(req)
		res = res.read()
		print(res)
		return res