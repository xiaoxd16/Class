from django.utils import timezone
from codex.baseview import *
from codex.baseerror import *
import json
from utils.utils import *

# 获取openid, 支付提现均需要
 
 
class LoginView(APIView):
	def get(self):
		self.check_input('code')
		CODE = self.input['code']
		openid_util = OpenidUtils(CODE)
		openid = openid_util.get_openid()
		if openid is None:
			raise LogicError("Get Open Id Failed")
		return openid