from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.AccountLoginView.as_view(), name='auth_login'),
    path('logout/', views.logout_view, name='auth_logout'),
    path('passwordreset/', views.AccountPasswordResetView.as_view(), name='auth_passwordreset'),
    path('passwordresetdone/', views.AccountPasswordResetDoneView.as_view(), name='auth_passwordresetdone'),
    path('passwordresetconfirm/<str:token>/', 
        views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('register/', views.register_view, name='auth_register'),
    path('password-change/', views.AccountPasswordChangeView.as_view(), name='auth_passwordchange'),
    path('password-change-done/', views.AccountPasswordChangeDoneView.as_view(), name='auth_passwordchangedone'),
    path('accounts/', views.account_index_view, name='auth_accounts'),
    path('setpassword/', views.AccountSetPasswordView.as_view(), name='auth_setpassword'),
    path('accounts/create/', views.create_account_view, name='auth_accounts_create'),
    path('accounts/profile/', views.profile_account_view, name='auth_accounts_profile'),
    path('accounts/<str:account_id>/get/', views.get_account_view, name='auth_accounts_query'),
    path('accounts/<str:account_id>/activate/', views.activate_account_view, name='auth_accounts_activate'),
    path('accounts/<str:account_id>/edit/', views.edit_account_view, name='auth_accounts_edit'),
    path('accounts/<str:account_id>/delete/', views.delete_account_view, name='auth_accounts_delete'),
    path('accounts/<str:token>/confirm/', views.AccountConfirmDoneView.as_view(), name='auth_accounts_confirm'),
    path('accounts/<str:account_id>/generateregister/', views.AccountGenerateConfirmView.as_view(), name='auth_accounts_generate_confirm'),
]
