from django.urls import path
from .views import SignupView, SigninView, GetAllUserTokensView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('get-all-tokens/', GetAllUserTokensView.as_view(), name='get_all_tokens'),  # New route for all users' tokens

]
