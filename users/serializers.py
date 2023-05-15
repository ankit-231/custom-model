# if we add a new field to the serializer that is not in the model, we need to create it as a field of serializer. for eg: total_students_in_grade = serializers.SerializerMethodField() or hello = serializers.CharField(default="hi")
    # and if the field is total_students_in_grade = serializers.SerializerMethodField(), the convention for creating the function that returns total_students_in_grade is get_total_students_in_grade

from requests import Response
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

def get_unique_from_list(li: list):
    '''get unique elements from a list.
    list is converted to set, then list again
    '''
    return list(set(li))


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["role"] 

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = ["name"]



    


class TeachersSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = TeachersNew
        fields = ['id', 'username', 'email', 'fullName', 'subjects']



class SectionsSerializer(serializers.ModelSerializer):
    
    total_students_section = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    # subjects = SubjectSerializer(many=True)
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ['id', 'sectionname', 'total_students_section', "subjects", "student"]
        
    
    def get_total_students_section(self, obj):
        return StudentsNew.objects.filter(section=obj).count()
    
    def get_student(self, obj):
        external_li = []
        
        std = StudentsNew.objects.filter(section=obj)
        for s in std:
            # create dictionary, add name and rollno, append it to external_li
            # clear the dictionary and do the same again
            internal_dict = {}
            internal_dict["name"] = s.username
            internal_dict["rollno"] = s.rollno
            external_li.append(internal_dict)
        return external_li
    
    def get_subjects(self, obj):
        teachsecsub = TeacherSectionGradeSubject.objects.filter(section=obj)
        subject = []
        for tss in teachsecsub:
            subject.append(tss.subject.name)
        return get_unique_from_list(subject)



from django.db.models.query_utils import Q

class TeachersSerializer(serializers.ModelSerializer):
    t_u_id = CustomUserSerializer(many=False, read_only=True) #many=False because CustomUser object is not iterable
    sections = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField() 
    class Meta:
        model = TeachersNew
        fields = ['grade', 'id', 'username', 'email', 'fullName', 'sections', 'subjects', 't_u_id']
    
    def get_sections(self, obj):
        teachsecsub = TeacherSectionGradeSubject.objects.filter(teacher=obj)
        section = []
        for tss in teachsecsub:
            section.append(tss.section.sectionname)
        return section
    
    def get_subjects(self, obj):
        teachsecsub = TeacherSectionGradeSubject.objects.filter(teacher=obj)
        subject = []
        for tss in teachsecsub:
            subject.append(tss.subject.name)
        return subject
    
    def get_grade(self, obj):
        external = []
        ourteacher = obj
        grades = TeacherSectionGradeSubject.objects.filter(teacher=ourteacher)
        grade = []
        for k in grades:
            grade.append(k.grade)
        grade = get_unique_from_list(grade)
        for i in grade:
            ext_dic = {}
            ext_dic["gradelevel"] = i.gradelevel_name
            section = TeacherSectionGradeSubject.objects.filter(grade=i, teacher=ourteacher)
            sections = []
            for l in section:
                sections.append(l.section)
            sections = get_unique_from_list(sections)
            internal = []
            for j in sections:
                int_dic = {}
                int_dic["sectionname"] = j.sectionname
                subject = []
                subjects = TeacherSectionGradeSubject.objects.filter(grade=i, section=j, teacher=ourteacher)
                for m in subjects:
                    subject.append(m.subject.name)
                sections = get_unique_from_list(subjects)
                
                int_dic["subjects"] = subject
                internal.append(int_dic)

            ext_dic["section"] = internal
            external.append(ext_dic)
        print(external)
        return external
        

    
class SectionsSerializerPost(serializers.ModelSerializer):
    
    class Meta:
        model = Section
        fields = ['sectionname', 'total_students_section', 'gradelevel_id']
    
class GradeLevelsSerializer(serializers.ModelSerializer):

    total_students_in_grade = serializers.SerializerMethodField()
    section = serializers.SerializerMethodField()
    class Meta:
        model = GradeLevel
        fields = ['id', 'gradelevel_name', 'fee', "total_students_in_grade", "section"]
    
    def get_total_students_in_grade(self, obj):
        total_students = 0
        sections = Section.objects.filter(gradelevel_id=obj)
        for section in sections:
            total_students += StudentsNew.objects.filter(section=section).count()
        return total_students
    
    def get_section(self, obj):
        sectionnames = []
        sections = Section.objects.filter(gradelevel_id = obj.id)
        for i in sections:
            sectionnames.append({"sectionname": i.sectionname, "total_students": total_students_section(i)})
        return sectionnames

def total_students_section(id):
    return StudentsNew.objects.filter(section=id).count()

class GradeLevelSerializerPost(serializers.ModelSerializer):

    class Meta:
        model = GradeLevel
        fields = ['gradelevel_name', 'fee', "subjects", ]


class GradeForSecSerializer(serializers.ModelSerializer):

    class Meta:
        model = GradeLevel
        fields = ['id', 'gradelevel_name']

class SecForStdSerializer(serializers.ModelSerializer):
    gradelevel_id = GradeForSecSerializer()
    class Meta:
        model = Section
        fields = ['id', 'sectionname', 'gradelevel_id']

class StudentsSerializer(serializers.ModelSerializer):
    s_u_id = CustomUserSerializer()
    section = SecForStdSerializer()
    class Meta:
        model = StudentsNew
        fields = ['id', 'username', 'email', 'fullName', 's_u_id', "section"]
    

class StudentsSerializerPost(serializers.ModelSerializer):
    
    class Meta:
        model = StudentsNew
        fields = ['id', 'username', 'email', 'fullName', 'section']

class TeacherSectionSubjectSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    section = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    class Meta:
        model = TeacherSectionGradeSubject
        fields = ['teacher', 'subject', 'section', 'grade', ]
    
    def get_teacher(self, obj):
        return obj.teacher.t_u_id.username
    
    def get_subject(self, obj):
        return obj.subject.name
    
    def get_section(self, obj):
        return obj.section.sectionname
    
    def get_grade(self, obj):
        return obj.grade.gradelevel_name

class TeacherSectionSubjectSerializerPost(serializers.ModelSerializer):

    class Meta:
        model = TeacherSectionGradeSubject
        fields = ['teacher', 'subject', 'section', 'grade', ]
        extra_kwargs = {'teacher': {'required': True,}, 'subject': {'required': True,}, 'section': {'required': True,}, 'grade': {'required': True,} }

# DRF simple_jwt

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, update_last_login
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings


# creating a CustomTokenObtainPairSerializer and overriding the validate() function.
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['role'] = user.role
        token["lololol"] = "lalala"
        # ...

        return token
    
    # Copied the body of the method from the original TokenObtainPairSerializer.validate() and added data["role"] = str(self.user.role)
    # data["username"] = str(self.user.username)
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        print(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["role"] = str(self.user.role)
        data["username"] = str(self.user.username)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
    
from rest_framework import serializers

class ChangePasswordSerializer(serializers.Serializer):

    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    username = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class AddStdToSecApiSerializer(serializers.Serializer):


    """
    Serializer for AddStdToSecApi.
    """
    studentid = serializers.IntegerField(required=True)
    sectionid = serializers.IntegerField(required=True)

    

        
