import json
import requests


class OpenidUtils(object):
	
	def __init__(self, jscode):
		self.url = "https://api.weixin.qq.com/sns/jscode2session"
		self.appid = APPID
		self.secret = SECRET
		self.jscode = jscode  # 前端传回的动态jscode
	
	def get_openid(self):
		# url一定要拼接，不可用传参方式
		url = self.url + "?appid=" + self.appid + "&secret=" + self.secret + "&js_code=" + self.jscode + "&grant_type=authorization_code"
		r = requests.get(url)
		print(r.json())
		if 'openid' in r:
			openid = r.json()['openid']
		else:
			openid = None
		return openid
