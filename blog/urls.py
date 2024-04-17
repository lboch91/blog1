"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from posts.views import edit_post
from django.contrib.auth import views as auth_views
from posts.views import SignUpView, posts_by_category, post_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('posts.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('post/<int:post_id>/edit/', edit_post, name='edit_post'),
    path('category/<int:category_id>/', posts_by_category, name='posts_by_category'),
    path('posts/', post_list, name='post_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







