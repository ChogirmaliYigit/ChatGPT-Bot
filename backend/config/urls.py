"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main.views import ChatList, ChatDetail, add_new_chat, delete_chat
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/<int:user_id>/', ChatList.as_view(), name="chat_list"),
    path('message/<int:chat_id>/', ChatDetail.as_view(), name="message_list"),
    path('add/<int:user_id>/', add_new_chat, name="add_new_chat"),
    path('delete/<int:chat_id>/', delete_chat, name="delete_chat")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
