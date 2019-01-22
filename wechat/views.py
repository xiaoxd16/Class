from django.utils import timezone
from codex.baseview import *
import json
from utils.utils import *

CONFIGS = json.loads(open('configs.json').read())

WECHAT_APPID = CONFIGS['WECHAT_APPID']
WECHAT_SECRET = CONFIGS['WECHAT_SECRET']

# 获取openid, 支付提现均需要
 
 
class LoginView(APIView):
	def get(self):
		self.check_input('code')
		CODE = self.input['code']
		openid_util = OpenidUtils(CODE)
		openid = openid_util.get_openid()
		return openid