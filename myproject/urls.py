
from django.contrib import admin
from django.urls import path, include
from myapp.views import *
from django.conf import settings
from django.conf.urls.static import static


from myapp.admin_api import AllUsersinfo
from myapp.folder_set_api import FolderInfo, SetInfo


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('verify_email/', EmailVerification.as_view(), name='verify_email'),
    path('forgot_password/', ForgotPassword.as_view(), name='forgot_password'),
    path('logout/', Logout.as_view(), name='logout'),
    path('gmail_fb_verification/', SocialPlatformLogin.as_view(),
         name='gmail_fb_verification'),

    # Category API
    path('category_info/', CategoryInfo.as_view(), name='category_info'),

    # Card Content API
    path('card_content/', CardContentInfo.as_view(), name='card_content'),

    # Folder API
    path('folder_info/', FolderInfo.as_view(), name='folder_info'),

    # Set API
    path('set_info/', SetInfo.as_view(), name='set_info'),

    # Admin API
    path('all_users_info/', AllUsersinfo.as_view(), name='all_users_info'),

    # Question to text
    path('q_to_t/', QuestionToText.as_view(), name='q_to_t'),

    # Get accuracy
    path('check_accuracy/', AccuracyCalculation.as_view(),
         name='check_accuracy'),

    # Get accuracy text
    path('check_accuracy_text/',
         AccuracyCalculationText.as_view(), name='check_accuracy'),

    path('report_generation/', ReportGeneration.as_view(),
         name='report_generation'),



    path('dummy_api/', DummyAPI.as_view(), name='dummy_api'),
]


if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
