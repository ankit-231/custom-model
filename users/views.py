from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from .forms import *
from .models import *
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail, EmailMessage, get_connection
from mycustomuser.settings import EMAIL_HOST_USER


# Create your views here.

def home_page(request):
    return HttpResponse("<h1>This is homepage</h1>")

def register_page(request):
    if request.method == "POST":
        if request.POST['role'] == "student":
            print(request.POST)
            form = StudentForm(request.POST)
            print("before valid")
            # is_valid is a function so is_valid()
            if form.is_valid():
                print("stu form valid")
                print(form)
                # form.username=request.POST.get('username')
                print(form.cleaned_data['email'])
                form.save()
                print("saved")

                user = CustomUser.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password'], role="student")
                user.save()

                # saving user foreign key in s_u_id
                t = StudentsNew.objects.get(username=form.cleaned_data['username'])
                t.s_u_id = user
                t.save()

                print("user saved")
            # print("this stu")
        else:
            print(request.POST)
            form = TeacherForm(request.POST)
            print("before valid")
            # is_valid is a function so is_valid()
            if form.is_valid():
                print("tea form valid")
                print(form)
                # form.username=request.POST.get('username')
                print(form.cleaned_data['email'])
                form.save()
                print("saved")

                user = CustomUser.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password'], role="teacher")
                user.save()
                print(user.role)

                # saving user foreign key in s_u_id
                t = TeachersNew.objects.get(username=form.cleaned_data['username'])
                t.t_u_id = user
                t.save()

                print("user saved")
    
        return render(request, "studentform.html", {"form": form})
    else:
        form = StudentForm()
        return render(request, "studentform.html", {"form": form})

def register_page_new(request):
    if request.method == "POST":
        if request.POST['role'] == "student":
            print(request.POST)
            try:
                user = CustomUser.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'], role="student")
                form = StudentForm(request.POST)
                print(form)
                # is_valid is a function so is_valid()
                if form.is_valid():
                    print("stu form valid")
                    print(form)
                    # form.username=request.POST.get('username')
                    print(form.cleaned_data['email'])
                    s = form.save()
                    s.s_u_id = user
                    s.save()

            except Exception as e:
                print(e)
            print("before valid")

        elif request.POST["role"] == "teacher":
            print(request.POST)
            try:
                user = CustomUser.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'], role="teacher")
                form = TeacherForm(request.POST)
                print(form)
                # is_valid is a function so is_valid()
                if form.is_valid():
                    print("stu form valid")
                    print(form)
                    # form.username=request.POST.get('username')
                    print(form.cleaned_data['email'])
                    t = form.save()
                    t.t_u_id = user
                    t.save()
            except Exception as e:
                print(e)
            print("before valid")
        else:
            print("error: no role")
            
        return render(request, "studentform.html", )
    else:
        form = StudentForm()
        return render(request, "studentform.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request=request, user=user)
                print("loggedin")

                return redirect('/users/home/')
            else:
                print("not loggedin")

                messages.error(request, "Invalid username or password.")
        else:
            print("form invalid")
            messages.error(request, "Invalid username or password.")
    
    else:
        form = AuthenticationForm()

    return render(request, "loginform.html", {"form": form})

def home(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect('/users/login/')

def myprofile(request):
    return render(request, "profile.html")
     

def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/users/home/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'passwordchangeform.html', {
        'form': form
    })

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
# from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            user = CustomUser.objects.filter(Q(email=data))
            if user.exists():
                subject = "Password Reset Requested"
                email_template_name = "password/password_reset_email.txt"
                c = {
                "email":user.email,
                'domain':'127.0.0.1:8000',
                'site_name': 'Website',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

def send_mail_try(request):
    # message = f'Hi testing, thank you for registering in geeksforgeeks.'
    # email = 'try231things@gmail.com'
    # subject = 'welcome to GFG world'
    # body= "testuing"
    # recipient_list = ["twarinxteslt@gmail.com", "sslicedbreadd@gmail.com", ]
    # try:
    #     send_mail(subject, message, from_email=email, recipient_list=recipient_list, connection=get_connection(username='try231things@gmail.com',
    #     password="qljxdoiikixhprfr") , connection=get_connection(username="try231things@gmail.com", password="qljxdoiikixhprfr"), fail_silently=False )
    #     print("Sent")
    # except Exception as e:
    #      print(e, "not sent")
    
    return HttpResponse("this page is not made, go back")

def add_user(request):
    if request.method == "POST":
        try:
            print("aa")
            user = CustomUser.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'], role="admin")
            
            print("aaa")
            print(user.id)
            messages.success(request, "user saved.")
        except Exception as e:
            print(e)
            print("bbb")
            messages.error(request, "user not saved. make sure you've entered all fields and username is unique" )
    
    return render(request, "adduser.html", {})

def create_grade_level(request):
    if request.method == 'POST':
        form = CreateGradeLevelForm(request.POST)
        gradelevel = GradeLevel.objects.filter(gradelevel_name=request.POST["gradelevel_name"])
        if  gradelevel.exists():
            print("grade exists")
            return HttpResponse("grade not saved, it already exists")
        else:
            if form.is_valid():
                print("cr grade valid")
                gradelevel = GradeLevel.objects.filter(gradelevel_name=form.cleaned_data["gradelevel_name"])
                print(gradelevel)
                form.save()
                print("grade saved")
                return HttpResponse("grade saved")
        return render(request, "gradelevel.html", {'form': form})
    else:
        form = CreateGradeLevelForm()
        return render(request, "gradelevel.html", {'form': form})
    
def create_section(request):
    if request.method == 'POST':
        form = CreateSectionForm(request.POST)
        print(form)
        sectionname_ = Section.objects.filter(sectionname=request.POST["sectionname"])
        if sectionname_.exists():
            print("section exists")
            return HttpResponse("section not saved, it already exists")
        else:
            if form.is_valid():
                print("section valid")
                print(sectionname_)
                form.save()
                print("section saved")
                return HttpResponse("section saved")
        return render(request, "section.html", {'form': form, 'gradelevels': GradeLevel.objects.filter(is_deleted=0)})
    else:
        form = CreateSectionForm()
        return render(request, "section.html", {'form': form, 'gradelevels': GradeLevel.objects.filter(is_deleted=0)})




def addstdtosec(request):
    students = StudentsNew.objects.filter(is_deleted=0)
    sections = Section.objects.filter(is_deleted=0)
    if request.method == "POST":
        print("lol")
        print(request.POST)
        st = StudentsNew.objects.get(username=request.POST["sel_student"])
        print(Section.objects.get(id=request.POST["sel_section"]))
        st.section = Section.objects.get(id=request.POST["sel_section"])
        st.save()
    return render(request, "addstdtosec.html", context={"students":students, "sections":sections, })


def viewalldata(request):
    users = CustomUser.objects.values('id', 'username', 'email', 'role')
    teachers = TeachersNew.objects.filter(is_deleted=0)
    students = StudentsNew.objects.filter(is_deleted=0)
    gradelevels = GradeLevel.objects.filter(is_deleted=0)
    sections = Section.objects.filter(is_deleted=0)
    return render(request, "viewalldata.html", context={"users":users, "teachers": teachers, "students":students, "gradelevels":gradelevels, "sections":sections, })

def studentviewdata(request):
    students = StudentsNew.objects.filter(is_deleted=0)
    if request.method == "GET":
        query = request.GET.get("q")
        # print(query)
        if query is not None:
            students = students.filter(Q(fullName__icontains=query) | Q(username__icontains=query) | Q(email__icontains=query))
        return render(request, "studentviewdata.html", context={"students":students, })

def updatestudentviewdata(request, id):
    student = StudentsNew.objects.get(id=id)
    context = {'students': student,}
    if request.method == "POST":
        fullName = request.POST["fullName"]
        email = request.POST["email"]
        rollno = request.POST["rollno"]
        print(student.fullName)
        print(request.POST["fullName"])
        if not fullName == "":
            student.fullName = request.POST["fullName"]
        if not email == "":
            student.email = request.POST["email"]
        if not rollno == "":
            student.rollno = request.POST["rollno"]
        print(student.fullName)
        student.save()

    return render(request, "updatestudentviewdata.html", context)

def studentdeletedata(request, id):
    student = StudentsNew.objects.get(id=id)
    student.is_deleted = 1
    student.save()
    return redirect("/users/viewalldata/studentviewdata")

def teacherviewdata(request):
    teachers = TeachersNew.objects.filter(is_deleted=0)
    if request.method == "GET":
        query = request.GET.get("q")
        # print(query)
        if query is not None:
            teachers = teachers.filter(Q(fullName__icontains=query) | Q(username__icontains=query) | Q(email__icontains=query) | Q(subject__icontains=query))
        return render(request, "teacherviewdata.html", context={"teachers":teachers, })

def updateteacherviewdata(request, id):
    teacher = TeachersNew.objects.get(id=id)
    context = {'teachers': teacher,}
    
    if request.method == "POST":
        fullName = request.POST["fullName"]
        email = request.POST["email"]
        subject = request.POST["subjects"]
        print(teacher.fullName)
        print(request.POST["fullName"])
        if not fullName == "":
            teacher.fullName = request.POST["fullName"]
        if not email == "":
            teacher.email = request.POST["email"]
        if not subject == "":
            teacher.subject = request.POST["subjects"]
        print(teacher.fullName)
        teacher.save()

    return render(request, "updateteacherviewdata.html", context)


def gradelevelviewdata(request):
    gradelevels = GradeLevel.objects.filter(is_deleted=0)
    if request.method == "GET":
        query = request.GET.get("q")
        # print(query)
        if query is not None:
            gradelevels = gradelevels.filter(Q(gradelevel_name__icontains=query) | Q(fee__icontains=query) | Q(subjects__icontains=query))
        return render(request, "gradelevelviewdata.html", context={"gradelevels":gradelevels, })

def updategradelevelviewdata(request, id):
    gradelevel = GradeLevel.objects.get(id=id)
    context = {'gradelevels': gradelevel,}
    
    if request.method == "POST":
        gradelevel_name = request.POST["gradelevel_name"]
        fee = request.POST["fee"]
        subjects = request.POST["subjects"]
        print(gradelevel.gradelevel_name)
        print(request.POST["gradelevel_name"])
        try:
            GradeLevel.objects.exclude(gradelevel_name=gradelevel.gradelevel_name).filter(gradelevel_name=gradelevel_name).exists()
            if not gradelevel_name == "":
                gradelevel.gradelevel_name = request.POST["gradelevel_name"]
            if not fee == "":
                gradelevel.fee = request.POST["fee"]
            if not subjects == "":
                gradelevel.subjects = request.POST["subjects"]
            print(gradelevel.gradelevel_name)
            gradelevel.save()
        except Exception as e:
            print(e)
            print("grade level already exists")

    return render(request, "updategradelevelviewdata.html", context)

def gradeleveldeletedata(request, id):
    gradelevels = GradeLevel.objects.get(id=id)
    gradelevels.is_deleted = 1
    gradelevels.save()
    return redirect("/users/viewalldata/gradelevelviewdata")

def sectionviewdata(request):
    sections = Section.objects.filter(is_deleted=0)
    if request.method == "GET":
        query = request.GET.get("q")
        print(query)
        if query is not None:
            sections = sections.filter(Q(sectionname__icontains=query) | Q(gradelevel_id__gradelevel_name__icontains=query))
        return render(request, "sectionviewdata.html", context={"sections":sections, })


# django rest framework start
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import StudentsNew
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def student_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.user.role != "admin":
        return JsonResponse({"error": "you are not an admin"})
    
    students = StudentsNew.objects.filter(is_deleted=0)
    serializer = StudentsSerializer(students, many=True) # many=True allows multiple instances to be passed as parameter
    return JsonResponse(serializer.data, safe=False)
    

    
@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def studentteacher_post(request):

    if request.user.role != "admin":
        return JsonResponse({"error": "you are not an admin"})

    data = JSONParser().parse(request)

    if 'role' not in data:
        return JsonResponse({"error": "No role given"}, status=status.HTTP_400_BAD_REQUEST)

    if data['role'] not in ['student', 'teacher']:
        return JsonResponse({"error": "invalid role given"}, status=status.HTTP_400_BAD_REQUEST)
    
    print(CustomUser.objects.filter(username=data["username"]).exists())

    if CustomUser.objects.filter(username=data["username"]).exists():
        return Response({"error": "user already exist"}, status=400)

    if data['role'] == 'student':
        serializer = StudentsSerializerPost(data=data)
        if serializer.is_valid():
            user = CustomUser.objects.create_user(username=data['username'], email=data['email'], password=data['password'], role="student")
            s = serializer.save()
            s.s_u_id = user
            s.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=400)
    
    else:
        serializer = TeachersSerializerPost(data=data)
        if serializer.is_valid():
            print("whaaat")
            try:
                user = CustomUser.objects.create_user(username=data['username'], email=data['email'], password=data['password'], role="teacher")
                t = serializer.save()
                t.t_u_id = user
                t.save()
                print("saved")
                return JsonResponse(serializer.data, status=201)
            except:
                return Response("username invalid or exists")
        else:
            return Response(serializer.errors, status=400)

@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def section_post(request):

    if request.user.role != "admin":
        return JsonResponse({"error": "you are not an admin"})
    
    data = JSONParser().parse(request)

    sectionf = Section.objects.filter(sectionname=data["sectionname"], is_deleted=0)
    if sectionf:
        return Response({"error": "section with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = SectionsSerializerPost(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=400)

@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def gradelevel_post(request):

    if request.user.role != "admin":
        return JsonResponse({"error": "you are not an admin"})
    
    data = JSONParser().parse(request)

    gradelevelf = GradeLevel.objects.filter(Q(gradelevel_name=data["gradelevel_name"]) & Q(is_deleted=0))
    if gradelevelf:
        return Response({"error": "gradelevel with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
    serializer = GradeLevelSerializerPost(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=400)

    
    
@csrf_exempt
@permission_classes((permissions.AllowAny))
@api_view(["GET"])
def student_detail_get(request, pk):
    print(pk)
    try:
        student = StudentsNew.objects.get(pk=pk)
    except StudentsNew.DoesNotExist:
        return HttpResponse(status=404)
    
    print(request.user, student.s_u_id)
    if request.user.role == "admin" or request.user == student.s_u_id:
        serializer = StudentsSerializer(student)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({"error": "you are neither admin nor the user whose info you're trying to access"})

@permission_classes((IsAuthenticated,))
@api_view(["GET"])
def teacher_detail_get(request, pk):

    try:
        teacher = TeachersNew.objects.get(pk=pk)
    except TeachersNew.DoesNotExist:
        return HttpResponse(status=404)
    print(request.user)
    if request.user.role == "admin" or request.user == teacher.t_u_id:
        serializer = TeachersSerializer(teacher)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({"error": "you are neither admin nor the user whose info you're trying to access"})

@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def snippet_detail_put(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """

    if request.user.role != "admin":
        return JsonResponse({"error": "you are not an admin"})
    
    try:
        student = StudentsNew.objects.get(pk=pk)
    except StudentsNew.DoesNotExist:
        return HttpResponse(status=404)

    data = JSONParser().parse(request)
    serializer = StudentsSerializerPost(student, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)

    
@csrf_exempt
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def student_delete(request, pk):
    """
    delete student.
    """

    if request.user.role != "admin":
        return JsonResponse({"error": "you are not an admin"})
    

    try:
        student = StudentsNew.objects.get(pk=pk)
        
    except StudentsNew.DoesNotExist:
        return Response(data={"error": "this student does not exist"}, status=404)

    if student.is_deleted == 0:
        student.is_deleted = 1
        student.save()
        return Response({"success": f"student {student.s_u_id.username} is deleted"}, status=200)
    else:
        return Response({"error": f"student {student.s_u_id.username} was already deleted"}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def teacher_delete(request, pk):
    """
    delete teacher.
    """

    if request.user.role != "admin":
        return JsonResponse({"error": "you are not an admin"})
    

    try:
        teacher = TeachersNew.objects.get(pk=pk)
        
    except TeachersNew.DoesNotExist:
        return Response(data={"error": "this teacher does not exist"}, status=404)

    if teacher.is_deleted == 0:
        teacher.is_deleted = 1
        teacher.save()
        return Response({"success": f"teacher {teacher.t_u_id.username} is deleted"}, status=200)
    else:
        return Response({"error": f"teacher {teacher.t_u_id.username} was already deleted"}, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def gradelevel_delete(request, pk):
    """
    delete gradelevel.
    """

    if request.user.role != "admin":
        return JsonResponse({"error": "you are not an admin"})
    

    try:
        gradelevel = GradeLevel.objects.get(pk=pk)
        
    except GradeLevel.DoesNotExist:
        return Response(data={"error": "this gradelevel does not exist"}, status=404)

    if gradelevel.is_deleted == 0:
        gradelevel.is_deleted = 1
        gradelevel.save()
        return Response({"success": f"gradelevel {gradelevel.gradelevel_name} is deleted"}, status=200)
    else:
        return Response({"error": f"gradelevel {gradelevel.gradelevel_name} was already deleted"}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def section_delete(request, pk):
    """
    delete section.
    """

    if request.user.role != "admin":
        return JsonResponse({"error": "you are not an admin"})
    

    try:
        section = Section.objects.get(pk=pk)
        
    except Section.DoesNotExist:
        return Response(data={"error": "this section does not exist"}, status=404)

    if section.is_deleted == 0:
        section.is_deleted = 1
        section.save()
        return Response({"success": f"section {section.sectionname} is deleted"}, status=200)
    else:
        return Response({"error": f"section {section.sectionname} was already deleted"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def teacher_list(request):
    """
    List all teacher.
    """

    if request.user.role != "admin":
        return JsonResponse({"error": "you are not an admin"})
    
    teachers = TeachersNew.objects.filter(is_deleted=0)
    serializer = TeachersSerializer(teachers, many=True) # many=True allows multiple instances to be passed as parameter
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def section_list(request):
    """
    List all section.
    """

    if request.user.role != "admin":
        return JsonResponse({"error": "you are not an admin"})
    

    sections = Section.objects.filter(is_deleted=0)
    serializer = SectionsSerializer(sections, many=True) # many=True allows multiple instances to be passed as parameter
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def gradelevel_list(request):
    """
    List all gradelevel.
    """
    if request.user.role != "admin":
        return JsonResponse({"error": "you are not an admin"})
    
    gradelevels = GradeLevel.objects.filter(is_deleted=0)
    serializer = GradeLevelsSerializer(gradelevels, many=True) # many=True allows multiple instances to be passed as parameter
    return JsonResponse(serializer.data, safe=False)

# @csrf_exempt
# @api_view(['PUT'])
# @permission_classes((IsAuthenticated,))
# def gradelevel_update(request, pk):
#     """
#     update gradelevel.
#     """
#     data = JSONParser().parse(request)

#     try:
#         gradelevel = GradeLevel.objects.get(pk=pk)
#     except:
#         return Response({"error": "gradelevel doesnot exist"})
#     serializer = GradeLevelSerializerPost(gradelevel, data=data)
#     if serializer.is_valid():
#         print(serializer.data)
#         return JsonResponse(serializer.data)
#     else:
#         return JsonResponse(serializer.errors)

@csrf_exempt
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def gradelevel_update(request, pk):
    """
    update gradelevel.
    """

    if request.user.role != "admin":
        return JsonResponse({"error": "you are not an admin"})
    

    data = JSONParser().parse(request)

    try:
        gradelevel = GradeLevel.objects.get(pk=pk)
    except:
        return Response({"error": "gradelevel doesnot exist"})
    serializer = GradeLevelSerializerPost(gradelevel, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse(serializer.errors)

@csrf_exempt
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def section_update(request, pk):
    """
    update section.
    """

    if request.user.role != "admin":
        return JsonResponse({"error": "you are not an admin"})
    

    data = JSONParser().parse(request)

    try:
        section = Section.objects.get(pk=pk)
    except:
        return Response({"error": "section doesnot exist"})
    serializer = SectionsSerializerPost(section, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse(serializer.errors)

@csrf_exempt
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def teacher_update(request, pk):
    """
    update teacher.
    """


    data = JSONParser().parse(request)

    try:
        teacher = TeachersNew.objects.get(pk=pk)
    
    except:
        return Response({"error": "teacher doesnot exist"})
    
    if request.user.role != "admin" and request.user != teacher.t_u_id:
        return JsonResponse({"error": "you are neither admin nor the user whose info you're trying to access"})

    serializer = TeachersSerializerPost(teacher, data=data, partial=True)
    if serializer.is_valid():
        try:
            cust_teach = CustomUser.objects.get(username=teacher.t_u_id.username)
            cust_teach.username = data["username"]
            cust_teach.save()
            print(cust_teach)
            serializer.save()
        except:
            return Response({"error": f"user with this username already exists"})
        
        print(serializer.data)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse(serializer.errors)

@csrf_exempt
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def student_update(request, pk):
    """
    update student.
    """
    data = JSONParser().parse(request)

    try:
        student = StudentsNew.objects.get(pk=pk)
    except:
        return Response({"error": "student doesnot exist"})
    
    if request.user.role != "admin" and request.user != student.s_u_id:
        return JsonResponse({"error": "you are neither admin nor the user whose info you're trying to access"})

    serializer = StudentsSerializerPost(student, data=data, partial=True)
    if serializer.is_valid():
        try:
            cust_stud = CustomUser.objects.get(username=student.s_u_id.username)
            cust_stud.username = data["username"]
            cust_stud.save()
            print(cust_stud)
            serializer.save()
        except Exception as e:
            return Response({"error": f"user with this username already exists: {e}"})
        
        print(serializer.data)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse(serializer.errors)

@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def test_api(request):
    """
    just for testing.
    """
    data = JSONParser().parse(request)
    try:
        print(data["username"])
    except Exception as e:
        print(e)

    try:
        student = StudentsNew.objects.get(username=data["username"])
    except:
        return Response({"error": "student doesnot exist"})
    try:
        user = CustomUser.objects.create_user(username=student.s_u_id.username, email=student.email, password="12345678", role="student")
        student.s_u_id = user
        student.save()
        return Response({"success": "uuu"})
        
    except Exception as e:
        user = CustomUser.objects.get(username=data["username"])
        student.s_u_id = user
        student.save()
        return Response({"error": f"purano but done"})
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users import serializers

class HelloView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        content = {'message': 'Hello, GeeksforGeeks'}
        return Response(content)


# gives custom token to user
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated 
from django.utils.decorators import method_decorator
from .serializers import CustomTokenObtainPairSerializer

from rest_framework_simplejwt.tokens import RefreshToken


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (permissions.AllowAny,)
    
    
    def update(self, request, *args, **kwargs):

        obj = CustomUser.objects.get(username=request.data["username"])
        self.object = obj
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            print(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# token = RefreshToken(base64_encoded_token_string)
# token.blacklist()

class BlacklistRefreshView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        print(request.data.get('refresh'))
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success")
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addstdtosecapi(request):
    serializer = AddStdToSecApiSerializer(data=request.data)
    if serializer.is_valid():
        try:
            student = StudentsNew.objects.get(id=request.data["studentid"])
            section = Section.objects.get(id=request.data["sectionid"])
        except:
            return Response({"error":"student or section with this id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        

        if request.method == "POST":
            if serializer.is_valid():
                print(request.data['studentid'])
                print(student.section)
                if student.section is None:
                    student.section = section
                    student.save()
                    return Response(f"{student.s_u_id.username} is added to the section {student.section.sectionname}", status=status.HTTP_200_OK)
                else:
                    before_section = student.section.sectionname
                    student.section = section
                    student.save()
                    return Response(f"{student.s_u_id.username}'s section is updated from {before_section} to {student.section.sectionname}", status=status.HTTP_200_OK)

    return Response(serializer.errors)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getteachersectionsubject(request):

    if request.user.role != "admin":
        return JsonResponse({"error": "you are not an admin"})

    teachsecsub = TeacherSectionGradeSubject.objects.all()

    serializer = TeacherSectionSubjectSerializer(teachsecsub, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

    


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def teachersectionsubject(request):

    if request.user.role != "admin":
        return JsonResponse({"error": "you are not an admin"})

    data = JSONParser().parse(request)

    serializer = TeacherSectionSubjectSerializerPost(data=data)
    print(serializer.is_valid())

    print("before valid")
    
    if serializer.is_valid():
        t = TeachersNew.objects.get(pk=data["teacher"])
        user = t.t_u_id
        sec = Section.objects.get(pk=data["section"])
        sub = Subjects.objects.get(pk=data["subject"])
        grade = GradeLevel.objects.get(pk=data["grade"])

        teachsecsub = TeacherSectionGradeSubject.objects.filter(teacher=t, section=sec, subject=sub, grade=grade)      
        if teachsecsub.exists():
            note = f"{user.username}, {grade.gradelevel_name}, {sec.sectionname} and {sub.name} were already linked together"
            return Response({"note": note}, status=status.HTTP_200_OK)

        print("before saving")
        serializer.save()
        print("after saving")
        note = {"data": serializer.data, "teacher": user.username, "grade": grade.gradelevel_name, "section": sec.sectionname, "subject": sub.name, }
        return Response(note, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def teacherandsubjectdelete(request):

    if request.user.role != "admin":
        return JsonResponse({"error": "you are not an admin"})

    data = JSONParser().parse(request)
    note = {"error": "provide tid and sid", "note": "tid = teacher's id, subid = subject's id"}

    if 'tid' not in data or 'subid' not in data:
        return Response(note, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        print("here")
        t = TeachersNew.objects.get(pk=data["tid"])
        user = t.t_u_id
        print(user, user.username)
    except TeachersNew.DoesNotExist as e:
        return Response({"error": str(e)})
    
    try:
        sub = Subjects.objects.get(pk=data["subid"])
    except Subjects.DoesNotExist as e:
        return Response({"error": str(e)})
    
    teachsub = t.subjects.filter(id=sub.id)
    
    if teachsub.exists():
        note = f"{user.username} and {sub.name} were already linked together"
        return Response({"note": note}, status=status.HTTP_200_OK)

    t.subjects.add(sub)
    t.save()

    return Response({"success": f"{user.username} and {sub.name} are successfully linked together"}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sectionandsubject(request):

    if request.user.role != "admin":
        return JsonResponse({"error": "you are not an admin"})

    data = JSONParser().parse(request)
    print("haha")
    
    if 'secid' not in data or 'subid' not in data :
        note = {"error": "provide secid and subid", "note": "secid = section's id, subid = subject's id"}
        return Response(note, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        sec = Section.objects.get(pk=data["secid"])
    except:
        return Response({"error": str(Section.DoesNotExist)})
    
    try:
        sub = Subjects.objects.get(pk=data["subid"])
    except:
        return Response({"error": str(Subjects.DoesNotExist)})
    
    secsub = sec.subjects.filter(id=sub.id)
    if secsub.exists():
        note = f"{sec.sectionname} and {sub.name} were already linked together"
        return Response({"note": note}, status=status.HTTP_200_OK)


    sec.subjects.add(sub)
    sec.save()

    return Response({"success": f"{sec.sectionname} and {sub.name} are successfully linked together"}, status=status.HTTP_201_CREATED)

    


