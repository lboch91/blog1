from django.urls import path
from . import views
from .views import edit_post, delete_post, post_detail, SignUpView, posts_by_category, post_list


urlpatterns = [
    path('', views.home, name='home'),
    path('post/add/', views.add_post, name='add_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('post/<int:post_id>/edit/', edit_post, name='edit-post'),
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('category/<str:category>/', posts_by_category, name='posts_by_category'),
    path('posts/', post_list, name='post_list'),
]

