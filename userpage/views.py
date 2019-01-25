from codex.baseerror import *
from codex.baseview import *
from .models import *


class PersonBind(APIView):
	def post(self):
		self.check_input('open_id')
		person = Person.selectByOpenId(self.input['open_id'])
		if person is not None:
			return
		t = Person.insertPerson(self.input['open_id'])
		if t is None:
			raise LogicError('Failed to bind')


class PersonInfo(APIView):
	def get(self):
		self.check_input('open_id')
		person = Person.selectByOpenId(open_id=self.input['open_id'])
		if person is None:
			raise LogicError('Not Bind Yet!')
		phones_data = Phone.selectPhoneByPerson(person)
		places_data = Place.selectPlaceByPerson(person)
		emails_data = Email.selectEmailByPerson(person)
		
		phones = {}
		places = {}
		emails = {}
		for i in phones_data:
			phones[i.id] = i.phone
		for i in places_data:
			places[i.id] = i.place
		for i in emails_data:
			emails[i.id] = i.email
		
		output_info = {
			'id': person.id,
			'name': person.name,
			'phones': phones,
			'emails': emails,
			'places': places,
			'qq': person.qq,
			'description': person.description,
		}
		return output_info
	
	def post(self):
		self.check_input('open_id', 'name', 'qq', 'description')
		person = Person.selectByOpenId(open_id=self.input['open_id'])
		if person is None:
			raise LogicError('Not Bind Yet!')
		t = Person.updataPerson(open_id=self.input['open_id'], name=self.input['name'], qq=self.input['qq'],
		                        description=self.input['description'])
		if not t:
			raise LogicError("Update Infomation Failed")


class AllClass(APIView):
	def get(self):
		output_list = []
		all_class = Class.objects.all()
		for i in all_class:
			output_list.append(
				{
					'id': i.id,
					'name': i.name,
				}
			)
		return output_list


class MyClass(APIView):
	def get(self):
		self.check_input('open_id')
		person = Person.selectByOpenId(self.input['open_id'])
		class_ = person.class_set.all()
		output_info = []
		for i in class_:
			output_info.append(
				{
					'id': i.id,
					'name': i.name
				}
			)
		return output_info


class ClassInfo(APIView):
	def get(self):
		self.check_input('id')
		class_ = Class.selectById(self.input['id'])
		output_info = []
		for i in class_.members:
			output_info.append(
				{
					'id': i.id,
					'qq': i.qq,
					'description': i.description,
					'name': i.name
				}
			)
		return output_info


class CreateClass(APIView):
	def post(self):
		self.check_input('open_id', 'name', 'token')
		person = Person.selectByOpenId(self.input['open_id'])
		class_ = Class.insertClass(self.input['name'], self.input['token'])
		if class_ is None:
			raise LogicError("Failed to insert class!")
		class_ = class_.insertPerson(person)
		if class_ is None:
			raise LogicError("Failed to insert person to class!")
		return {
			'id': class_.id,
			'name': class_.name,
			'token': class_.token
		}


class ExitClass(APIView):
	def get(self):
		self.check_input('open_id', 'id')  # id for class.id
		class_ = Class.selectById(self.input['id'])
		if class_ is None:
			raise LogicError("No Such Class")
		person = Person.selectByOpenId(self.input['open_id'])
		if person is None:
			raise LogicError("No Such Person")
		class_ = class_.removePerson(person)
		if class_ is None:
			raise LogicError("Remove Failed")
		return


class InsertClass(APIView):
	def get(self):
		self.check_input('open_id', 'id')
		class_ = Class.selectById(self.input['id'])
		if class_ is None:
			raise LogicError("No Such Class!")
		person = Person.selectByOpenId(self.input['open_id'])
		if person is None:
			raise LogicError("No Such Person")
		class_ = class_.insertPerson(person)
		if class_ is None:
			raise LogicError('Add To Class Failed!')

# Create your views here.
