'''
	Django REST Framework provides a "Serializer" class which gives you a powerful, generic way to control the output of your responses, as well as a "ModelSerializer class" which provides a useful shortcut for creating serializers that deal with model instances and querysets.

'''
from rest_framework import serializers
from .models import MyUser

class MyUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = MyUser
		fields = ('email', 'name', 'date_of_birth', 'password', 'sex', 'icon')

	# This overriding is a must. 	
	def create(self, validated_data):
		password = validated_data.pop('password', None)
		user = self.Meta.model(**validated_data)
		if password is not None:
			user.set_password(password)
		user.save()
		return user

	# This overriding is a must. 	
	def update(self, user, validated_data):
		for attr, value in validated_data.items():
			if attr == 'password':
				user.set_password(value)
			else:
				setattr(user, attr, value)
		user.save()
		return user

class SignInSerializer(serializers.Serializer):
	email = serializers.EmailField()

class ChangeProfileSerializer(serializers.Serializer):
	email = serializers.EmailField()
	name = serializers.CharField()
	icon = serializers.IntegerField()



'''
	serializer = CommentSerializer(comment)
	serializer.data
	# {'email': 'leila@example.com', 'content': 'foo bar',}
	--> At this point we've translated the model instance into Python native datatypes. To finalize the serialization process we render the data into json.

	---> Response object arbitrarily chooses the data type.

'''

'''
	[ Saving instances ]
	If we want to be able to return complete object instances based on the validated data we need to implement one or both of the ".create()" and "update()" methods. For example:

'''

'''
	[ Validation ]
	When deserializing data, you always need to call is_valie() before attempting to access the validated data, or save an object instance. 

'''

'''
	Often you'll want serializer classes that map closely to Django model definitions. 

	The "ModelSerializer" class provides a shortcut that lets you automatically create a "Serializer" class with fields that correspond to the Model fields.

	The ModelSerializer class is the same as a regular "Serializer" class, except that

'''
