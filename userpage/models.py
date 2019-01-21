from django.db import models


class Person(models.Model):
	id = models.AutoField(primary_key=True)
	open_id = models.CharField(max_length=50)
	
	name = models.CharField(max_length=20, default='')
	phone = models.IntegerField(default=0)
	email = models.CharField(max_length=60, default='')
	place = models.CharField(max_length=200, default='')
	qq = models.IntegerField(default=0)
	
	description = models.CharField(max_length= 1000,default = '')
	
	@classmethod
	def insertPerson(cls, open_id, name='', phone=0, email='', place='', qq=0, description=''):
		check_exist = Person.objects.filter(open_id=open_id)
		if len(check_exist):
			return False
		try:
			person = Person(open_id=open_id, name=name, phone=phone, email=email, place=place, qq=qq,
			                description=description)
			person.save()
			return True
		except Exception as e:
			print(e)
			return False
	
	@classmethod
	def updataPerson(cls, open_id, name='', phone=0, email='', place='', qq=0, description=''):
		check_exist = Person.objects.filter(open_id=open_id)
		if len(check_exist):
			person = check_exist[0]
			person.name = name
			person.phone = phone
			person.email = email
			person.place = place
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
	
	@classmethod
	def deletePerson(cls, person):
		try:
			person.delete()
			return True
		except Exception as e:
			print(e)
			return False


class Class(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	token = models.CharField(default='token',max_length=30, null=False)
	
	members = models.ManyToManyField(Person)
	
	@classmethod
	def insertClass(cls, name):
		try:
			class_ = Class(name=name)
			class_.save()
			return True,class_.id
		except Exception as e:
			print(e)
			return False,0
	
	@classmethod
	def updateClass(cls, id, name, token=''):
		class_ = Class.selectById(id)
		if class_ is None:
			return False
		class_.name = name
		if token != '':
			class_.token = token
		return True
	
	@classmethod
	def deleteClass(cls, id):
		class_ = Class.selectById(id)
		if class_ is None:
			return False
		class_.delete()
		return True
	
	@classmethod
	def selectById(cls, id):
		try:
			class_ = Class.objects.get(id=id)
			return class_
		except Exception as e:
			print(e)
			return None
	
	@classmethod
	def insertPerson(cls, id, person):
		class_ = Class.selectById(id)
		if class_ is None:
			return False
		class_.members.add(person)
		return True
	
	@classmethod
	def removePerson(cls, id, person):
		class_ = Class.selectById(id)
		if class_ is None:
			return False
		try:
			class_.members.remove(person)
			return True
		except Exception as e:
			print(e)
			return False

# Create your models here.