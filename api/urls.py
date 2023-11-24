from django.urls import path, include
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    # 32 ENDPOINTS
    
    path('', views.Landing.as_view()),  
    # 1

    # user registration and login
    path('register/', views.UserRegisterView.as_view(), name='user-registration'),
    path('login/', views.UserLogin.as_view(), name='user-login'),
    path('logout/', views.UserLogout.as_view(), name='user-logout'),
    # 3

    # user authentication
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 3

    # get user information
    path('profile/overview/', views.UserInformationView.as_view(), name='get-user-info'),
    path('profile/<str:pk>', views.SeeUser.as_view(), name='get_individual_user'),
    # 2

    # user creations
    path('create-piggybox/', views.PiggyboxCreation.as_view(), name='create-piggybox'),
    path('create-group/', views.SavingsGroupCreation.as_view(), name='create-savings-group'),
    path('create-account', views.AccountCreation.as_view(), name='create-account'),
    # 3

    # admin operations
    path('users', views.ViewAllUsers.as_view(), name='get-all-users'),
    path('yo', views.my_view, name='check-if-logged-in'),
    path('piggys', views.ViewPiggyboxes.as_view(), name='get_all_piggyboxes'),
    path('accounts', views.ViewAccounts.as_view(), name='get_all_accounts'),
    path('groups', views.ViewSavingsGroups.as_view(), name='savings_group_leaderboard'),
    # 5

    # path('savings-groups', views.SGTest.as_view()),
    path('groups/<str:group_name>/info', views.SavingsGroupsView.as_view(), name='savings_group_information'), 
    path('groups/<str:group_name>/add-member', views.SavingsGroupMemberAdd.as_view(), name='savings_group_add_member'),
    path('groups/<str:group_name>/remove-member', views.SavingsGroupMemberRemove.as_view(), name='savings_group_remove_member'), 
    path('groups/<str:group_name>/deposit', views.SavingsGroupDeposit.as_view(), name='savings_group_deposit_funds'),
    path('groups/<str:group_name>/deposits', views.SavingsGroupUserDeposits.as_view(), name='savings_group_all_deposits'),
    path('groups/<str:group_name>/leaderboard', views.SavingsGroupLeaderboard.as_view(), name='savings_group_leaderboard'),
    path('groups/public', views.PublicSavingsGroup.as_view(), name='savings_group_leaderboard'),
    path('groups/join-<str:group_name>', views.JoinPublicSavingsGroup.as_view(), name='savings_group_leaderboard'),
    path('groups/leave-<str:group_name>', views.LeaveGroup.as_view(), name='savings_group_leaderboard'),
    # 6


    # basic banking functions 
    path('transfer', views.Transfer.as_view(), name='transfer_funds'),
    path('withdraw', views.Withdraw.as_view(), name='withdraw_funds'),
    path('deposit', views.Deposit.as_view(), name='deposit_funds'),
    path('all-transfers', views.TransactionView.as_view(), name='all_transactions'),
    path('transaction-history', views.AccountTransactionHistory.as_view(), name='transaction_history'), 
    # 5


    # piggybox functions
    path('piggyboxw', views.PiggyboxWithdraw.as_view(), name='piggybox_withdraw'),
    path('piggyboxd', views.PiggyboxDeposit.as_view(), name='piggybox_deposit'),
    path('piggyboxa', views.PiggyboxAuto.as_view(), name='piggybox_auto_deposit'),
    path('piggyboxes/<int:id>/info', views.PiggyboxInfo.as_view(), name='piggybox_info'),
    path('my-piggyboxes/', views.MyPiggyboxes.as_view(), name='my_piggybox'),
    path('piggyboxdel', views.PiggyboxDelete.as_view(), name='piggybox_delete'),
    # 5
]


