from rest_framework import serializers
from .models import *

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




class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'role'] 

class StudentsSerializer(serializers.ModelSerializer):
    s_u_id = CustomUserSerializer() #many=False because CustomUser object is not iterable
    class Meta:
        model = StudentsNew
        fields = ['id', 'username', 'email', 'fullName', 's_u_id']

class TeachersSerializer(serializers.ModelSerializer):
    t_u_id = CustomUserSerializer(many=False, read_only=True) #many=False because CustomUser object is not iterable
    class Meta:
        model = TeachersNew
        fields = ['id', 'username', 'email', 'fullName', 't_u_id']

class GradeLevelsSerializer(serializers.ModelSerializer):

    total_students_in_grade = serializers.SerializerMethodField()
    class Meta:
        model = GradeLevel
        fields = ['id', 'gradelevel_name', 'fee', "total_students_in_grade"]

    def get_total_students_in_grade(self, obj):
        total_students = 0
        sections = Section.objects.filter(gradelevel_id=obj)
        for section in sections:
            total_students += StudentsNew.objects.filter(section=section).count()
        return total_students
    
    # if we add a new field to the serializer that is not in the model, we need to create it as a field of serializer. for eg: total_students_in_grade = serializers.SerializerMethodField() or hello = serializers.CharField(default="hi")
    # and if the field is total_students_in_grade = serializers.SerializerMethodField(), the convention for creating the function that returns total_students_in_grade is get_total_students_in_grade
    
    

class SectionsSerializer(serializers.ModelSerializer):
    
    total_students_section = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ['id', 'sectionname', 'total_students_section']
    
    def get_total_students_section(self, obj):
        return StudentsNew.objects.filter(section=obj).count()

 
        
