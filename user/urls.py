from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.CustomUserAPIView.as_view(), name="registration_form"),
    path("login/", views.CustomLoginAPIView.as_view(), name="login_form"),
    path("list/", views.UserListAPIView.as_view(), name="user_list"),
    path("search/", views.SearchUserAPIView.as_view(), name="search_user"),
    path("request/", views.FriendRequestAPIView.as_view(), name="friend_request"),
    path(
        "request/action/<int:id>/",
        views.FriendRequestAcceptRejectAPIView.as_view(),
        name="friend_request_action",
    ),
    path(
    	'friend/accept/',
    	views.FriendRequestAcceptedAPIView.as_view(),
    	name='friend_request_accepted_list'
    )
]
