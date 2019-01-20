from codex.baseerror import *
from codex.baseview import *
from .models import *


class PersonBind(APIView):
	def post(self):
		self.check_input('open_id')
		person = Person.selectByOpenId(self.input['open_id'])
		if person is not None:
			raise LogicError('Already Bind')
		t = Person.insertPerson(self.input['open_id'])
		if not t:
			raise LogicError('Failed to bind')


class PersonInfo(APIView):
	def get(self):
		self.check_input('open_id')
		person = Person.selectByOpenId(open_id=self.input['open_id'])
		if person is None:
			raise LogicError('Not Bind Yet!')
		output_info = {
			'id': person.id,
			'open_id': person.open_id,
			'phone': person.phone,
			'email': person.email,
			'qq': person.qq,
			'description': person.description,
			'place': person.place
		}
		return output_info
	
	def post(self):
		self.check_input('open_id', 'name', 'phone', 'email', 'place', 'qq', 'description')
		person = Person.selectByOpenId(open_id=self.input['open_id'])
		if person is None:
			raise LogicError('Not Bind Yet!')
		t = Person.updataPerson(open_id=self.input['open_id'], name=self.input['name'], phone=self.input['phone'],
		                        email=self.input['email'], place=self.input['place'], qq=self.input['qq'],
		                        description=self.input['description'])
		if not t:
			raise LogicError("Update Infomation Failed")


class AllClassInfo(APIView):
	def get(self):
		output_list = []
		all_class = Class.objects.all()
		for i in all_class:
			output_list.append(
				{
					'id':i.id,
					'name':i.name,
				}
			)
		return  output_list
	
class MyClassInfo(APIView):
	def get(self):
		self.check_input('open_id')
		person = Person.selectByOpenId(self.input['open_id'])
		class_ = person.class_set.all()
		if len(class_) == 0:
			return
		elif len(class_) == 1:
			output_info = []
			for i in class_[0].members:
				output_info.append(
					{
						'id':i.id,
						'name':i.name,
						'phone':i.phone,
						'place':i.place,
						'email':i.email,
						'qq':i.qq
					}
				)
			return output_info
		else:
			output_info = []
			for i in class_:
				output_info.append(
					{
						'id':i.id,
						'name':i.name
					}
				)
			return output_info

class CreateClass(APIView):
	def post(self):
		self.check_input('open_id','name')
		person = Person.selectByOpenId(self.input['open_id'])
		t,id = Class.insertClass(self.input['name'])
		if not t:
			raise LogicError("Failed to insert class!")
		t = Class.insertPerson(id,person)
		if not t:
			raise LogicError("Failed to insert person to class!")

class ExitClass(APIView):
	def post(self):
		self.check_input('open_id','id')#id for class.id
		t = Class.removePerson(self.input['id'],self.input['open_id'])
		if not t:
			person = Person.selectByOpenId(self.input['open_id'])
			class_ = Class.selectById(self.input['id'])
			raise  LogicError("Failed to remove %s from %s" % (person.name,class_.name ))
		
		
# Create your views here.
