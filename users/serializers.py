from rest_framework import serializers
from .models import StudentsNew

# class StudentsSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     username = serializers.CharField(max_length=250)
#     email = serializers.EmailField()
#     fullName = serializers.CharField(max_length=250)

#     def create(self, validated_data):
#         """
#         Create and return a new `StudentsNew` instance, given the validated data.
#         """
#         return StudentsNew.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `StudentsNew` instance, given the validated data.
#         """
#         instance.id = validated_data.get('id', instance.id)
#         instance.username = validated_data.get('username', instance.username)
#         instance.email = validated_data.get('email', instance.email)
#         instance.fullName = validated_data.get('fullName', instance.fullName)
#         instance.save()
#         return instance

# using ModelSerializer
class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentsNew
        fields = ['id', 'username', 'email', 'fullName']
        
