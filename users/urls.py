from django.urls import path
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.decorators.csrf import csrf_exempt
from . import views
from .views import ChangePasswordView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('register_page_new/', views.register_page_new, name='register_page_new'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('send_mail_view/', views.send_mail_try, name='send_mail_view'),
    path('myprofile/', views.myprofile, name='myprofile'),

    path('add_user/', views.add_user, name='add_user'),
 

    path('create_grade_level/', views.create_grade_level, name='create_grade_level'),
    path('create_section/', views.create_section, name='create_section'),

    path('viewalldata/', views.viewalldata, name='viewalldata'),
    path('viewalldata/addstdtosec/', views.addstdtosec, name='addstdtosec'),

    path('viewalldata/studentviewdata', views.studentviewdata, name='studentviewdata'),
    path('viewalldata/studentviewdata/<int:id>', views.updatestudentviewdata, name='updatestudentviewdata'),
    path('viewalldata/studentviewdata/studentdeletedata/<int:id>', views.studentdeletedata, name='studentdeletedata'),
    path('viewalldata/studentviewdata/search', views.studentviewdata, name='searchstudentviewdata'),


    path('viewalldata/teacherviewdata', views.teacherviewdata, name='teacherviewdata'),
    path("viewalldata/teacherviewdata/<int:id>", views.updateteacherviewdata, name="updateteacherviewdata"),

    path('viewalldata/gradelevelviewdata', views.gradelevelviewdata, name='gradelevelviewdata'),
    path('viewalldata/gradelevelviewdata/<int:id>', views.updategradelevelviewdata, name='updategradelevelviewdata'),
    path('viewalldata/gradelevelviewdata/gradeleveldeletedata/<int:id>', views.gradeleveldeletedata, name='gradeleveldeletedata'),


    path('viewalldata/sectionviewdata', views.sectionviewdata, name='sectionviewdata'),


    path('home/', views.home, name='home'),

    path('password_change/', views.password_change, name='password_change'),

    path("password_reset", views.password_reset_request, name="password_reset"),

    # django rest framework
    # path('student_get_put/', views.student_get_put),
    # path('student_post/', views.student_post),
    path('student_list/', views.student_list),
    path('student_detail_get/<int:pk>/', views.student_detail_get),
    path('teacher_detail_get/<int:pk>/', views.teacher_detail_get),
    path('teacher_list/', views.teacher_list),

    path('teachersectionsubject/', views.teachersectionsubject),
    path('getteachersectionsubject/', views.getteachersectionsubject),
    path('sectionandsubject/', views.sectionandsubject),

    
    path('studentteacher_post/', views.studentteacher_post),

    path('student_delete/<int:pk>/', views.student_delete),
    path('section_delete/<int:pk>/', views.section_delete),
    path('teacher_delete/<int:pk>/', views.teacher_delete),
    path('gradelevel_delete/<int:pk>/', views.gradelevel_delete),
    
    path('gradelevel_update/<int:pk>/', views.gradelevel_update),
    path('section_update/<int:pk>/', views.section_update),
    path('teacher_update/<int:pk>/', views.teacher_update),
    path('student_update/<int:pk>/', views.student_update),


    path('test_api', views.test_api),


    
    path('section_post/', views.section_post),
    path('gradelevel_post/', views.gradelevel_post),

    path('section_list/', views.section_list),
    path('gradelevel_list/', views.gradelevel_list),

    path('api/token/', views.CustomTokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path('hello/', views.HelloView.as_view(), name ='hello'),

    path('api/change-password/', csrf_exempt(ChangePasswordView.as_view()), name="api_change_password"),

    path('api/logout', csrf_exempt(views.BlacklistRefreshView.as_view()), name="logout"),

    path('api/addstdtosec', csrf_exempt(views.addstdtosecapi), name="api_addstdtosec"),




]
