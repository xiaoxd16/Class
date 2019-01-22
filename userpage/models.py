from django.db import models


class Person(models.Model):
	id = models.AutoField(primary_key=True)
	open_id = models.CharField(max_length=50)
	
	name = models.CharField(max_length=20, default='')
	
	qq = models.IntegerField(default=0)
	
	description = models.CharField(max_length=1000, default='')
	
	@classmethod
	def insertPerson(cls, open_id, name='', qq=0, description=''):
		check_exist = Person.objects.filter(open_id=open_id)
		if len(check_exist):
			return False
		try:
			person = Person(open_id=open_id, name=name, qq=qq,
			                description=description)
			person.save()
			return person
		except Exception as e:
			print(e)
			return None
		return None
	
	@classmethod
	def updataPerson(cls, open_id, name='', qq=0, description=''):
		check_exist = Person.objects.filter(open_id=open_id)
		if len(check_exist):
			person = check_exist[0]
			person.name = name
			person.qq = qq
			person.description = description
			person.save()
			return True
		return False
	
	@classmethod
	def selectById(cls, id):
		try:
			person = Person.objects.get(id=id)
			return person
		except Exception as e:
			print(e)
			return None
	
	@classmethod
	def selectByOpenId(cls, open_id):
		try:
			person = Person.objects.get(open_id=open_id)
			return person
		except Exception as e:
			print(e)
			return None
		return None
	
	@classmethod
	def deletePerson(cls, person):
		try:
			person.delete()
			return True
		except Exception as e:
			print(e)
			return False
		return False

class Phone(models.Model):
	id = models.AutoField(primary_key=True)
	phone = models.IntegerField(null=False)
	create_time = models.DateTimeField(auto_now=True)
	person = models.ForeignKey(Person, on_delete=models.CASCADE)
	
	@classmethod
	def insertPhone(cls, phone, person):
		try:
			new_phone = Phone(phone=phone, person=person)
			new_phone.save()
			return new_phone
		except Exception as e:
			print(e)
			return None
		return None
	
	@classmethod
	def deletePhone(cls, phone, person):
		try:
			delete_phone = cls.objects.get(person=person, phone=phone)
			delete_phone.delete()
			return True
		except Exception as e:
			print(e)
			return False
		return False
	
	@classmethod
	def selectPhoneByPerson(cls, person):
		phones = cls.objects.filter(person=person)
		return phones

	@classmethod
	def selectPhoneById(cls,id):
		try:
			phone = cls.objects.get(id=id)
			return phone
		except Exception as e:
			print(e)
			return None
		return None

class Email(models.Model):
	id = models.AutoField(primary_key=True)
	email = models.CharField(max_length=100, null=False)
	create_time = models.DateTimeField(auto_now=True)
	person = models.ForeignKey(Person, on_delete=models.CASCADE)
	
	@classmethod
	def insertEmail(cls, email, person):
		try:
			new_email = cls(email=email, person=person)
			new_email.save()
			return new_email
		except Exception as e:
			print(e)
			return None
		return None
	
	@classmethod
	def deleteEmail(cls, email, person):
		try:
			delete_email = cls.objects.get(email=email, person=person)
			delete_email.delete()
			return True
		except Exception as e:
			print(e)
			return False
		return False
	
	@classmethod
	def selectEmailByPerson(cls, person):
		emails = cls.objects.filter(person=person)
		return emails
	
	@classmethod
	def selectEmailById(cls,id):
		try:
			email = cls.objects.get(id=id)
			return email
		except Exception as e:
			print(e)
			return None
		return None


class Place(models.Model):
	id = models.AutoField(primary_key=True)
	place = models.CharField(max_length=300, null=False)
	create_time = models.DateTimeField(auto_now=True)
	person = models.ForeignKey(Person, on_delete=models.CASCADE)
	
	@classmethod
	def insertPlace(cls, place, person):
		try:
			new_place = cls(place=place, person=person)
			new_place.save()
			return new_place
		except Exception as e:
			print(e)
			return None
		return None
	
	@classmethod
	def deletePlace(cls, place, person):
		try:
			delete_place = cls.objects.get(place=place, person=person)
			delete_place.delete()
			return True
		except Exception as e:
			print(e)
			return False
		return False
	
	@classmethod
	def selectPlaceByPerson(cls, person):
		places = cls.objects.filter(person=person)
		return places

	@classmethod
	def selectPlaceById(cls,id):
		try:
			place = cls.objects.get(id=id)
			return place
		except Exception as e:
			print(e)
			return None
		return None

class Class(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	token = models.CharField(default='token', max_length=30, null=False)
	
	members = models.ManyToManyField(Person)
	
	@classmethod
	def insertClass(cls, name):
		try:
			class_ = cls(name=name)
			class_.save()
			return class_
		except Exception as e:
			print(e)
			return None
		return None
	
	@classmethod
	def updateClass(cls, id, name, token=''):
		class_ = Class.selectById(id)
		if class_ is None:
			return None
		class_.name = name
		if token != '':
			class_.token = token
		return class_
	
	@classmethod
	def deleteClass(cls, id):
		class_ = cls.selectById(id)
		if class_ is None:
			return False
		class_.delete()
		return True
	
	@classmethod
	def selectById(cls, id):
		try:
			class_ = cls.objects.get(id=id)
			return class_
		except Exception as e:
			print(e)
			return None
		return None
	
	def insertPerson(self,person):
		'''
		:param person: can be both Object or Openid
		:return:
		'''
		if not isinstance(person,Person):
			person = Person.selectByOpenId(person)
			if person is None:
				return None
		self.members.add(person)
		return self
	
	
	def removePerson(self,person):
		'''
		
		:param person:can be both Object or Openid
		:return:
		'''
		if not isinstance(person,Person):
			person = Person.selectByOpenId(person)
			if person is None:
				return None
		try:
			self.members.remove(person)
			return self
		except Exception as e:
			print(e)
			return None
		return None
# Create your models here.
