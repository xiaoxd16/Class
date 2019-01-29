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

class PhoneCreate(APIView):
	def post(self):
		self.check_input('open_id','phone')
		person = Person.selectByOpenId(self.input['open_id'])
		if person is None:
			raise  LogicError("No Such Person")
		check_repeat = Phone.objects.filter(phone=self.input['phone'],person=person)
		if len(check_repeat):
			raise LogicError("Already record this phone")
		Phone.insertPhone(self.input['phone'],person)

class EmailCreate(APIView):
	def post(self):
		self.check_input('open_id', 'email')
		person = Person.selectByOpenId(self.input['open_id'])
		if person is None:
			raise LogicError("No Such Person")
		check_repeat = Email.objects.filter(email=self.input['email'], person=person)
		if len(check_repeat):
			raise LogicError("Already record this email")
		Email.insertEmail(self.input['email'], person)

class PlaceCreate(APIView):
	def post(self):
		self.check_input('open_id', 'place')
		person = Person.selectByOpenId(self.input['open_id'])
		if person is None:
			raise LogicError("No Such Person")
		check_repeat = Place.objects.filter(place=self.input['place'], person=person)
		if len(check_repeat):
			raise LogicError("Already record this place")
		Place.insertPlace(self.input['place'], person)

class PhoneDelete(APIView):
	def get(self):
		self.check_input('id','open_id')
		person = Person.selectByOpenId(self.input['open_id'])
		
		to_delete = Phone.selectPhoneById(self.input['id'])
		
		if not to_delete:
			raise LogicError("No Such Phone with this id")
		if to_delete.person != person:
			raise LogicError("Not Your Phone,Error Occur!")
		to_delete.delete()
	
class PlaceDelete(APIView):
	def get(self):
		self.check_input('id','open_id')
		person = Person.selectByOpenId(self.input['open_id'])
		to_delete = Place.selectPlaceById(self.input['id'])
		if not to_delete:
			raise LogicError("No Such Place with this id")
		if to_delete.person != person:
			raise LogicError("Not Your Address,Error Occur!")
		to_delete.delete()

class EmailDelete(APIView):
	def get(self):
		self.check_input('id','open_id')
		person = Person.selectByOpenId(self.input['open_id'])
		to_delete = Email.selectEmailById(self.input['id'])
		if not to_delete:
			raise LogicError('No Such Email with this id')
		if to_delete.person != person :
			raise LogicError('Not Your Email,Error Occur!')
		to_delete.delete()


class AllClass(APIView):
	def get(self):
		self.check_input('open_id')
		output_list = []
		all_class = Class.objects.exclude(members__open_id=self.input['open_id'])
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
		members = Class.selectById(self.input['id']).members.all()
		output_info = []
		for i in members:
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
		check_repeat = Class.selectByName(self.input['name'])
		if len(check_repeat) != 0:
			raise LogicError('Name in use, try another name please!')
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
