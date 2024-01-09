from django.urls import path, include
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    
    # 38 endpoints 

    path('', views.Landing.as_view()),  

    # user registration and login
    path('register/', views.UserRegisterView.as_view(), name='user-registration'),  # frontend integration done
    path('login/', views.UserLogin.as_view(), name='user-login'), # frontend integration done
    path('logout/', views.UserLogout.as_view(), name='user-logout'),  # frontend integration done
    path('logout-view/', views.LogoutView.as_view(), name='logout-view'),  # frontend integration done

    # user authentication
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # frontend integration done
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # frontend integration done
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),  # frontend integration done


    # get user information and profile details
    path('profile/overview/', views.ProfileOverview.as_view(), name='get-user-info'),  # frontend integration done
    path('profile/edit/<str:pk>', views.EditUserInformation.as_view(), name='get_individual_user'),  # frontend integration done

    # user creations
    path('create-piggybox/', views.PiggyboxCreation.as_view(), name='create-piggybox'),  # frontend integration done
    path('create-group/', views.SavingsGroupCreation.as_view(), name='create-savings-group'),  # frontend integration done
    path('create-account', views.AccountCreation.as_view(), name='create-account'),  # frontend integration done

    # path('savings-groups', views.SGTest.as_view()),
    path('groups/<str:group_name>/info', views.SavingsGroupsView.as_view(), name='savings_group_information'), # frontend integration done
    path('groups/<str:group_name>/add-member', views.SavingsGroupMemberAdd.as_view(), name='savings_group_add_member'), # frontend integration done
    path('groups/<str:group_name>/remove-member', views.SavingsGroupMemberRemove.as_view(), name='savings_group_remove_member'),  # frontend integration done
    path('groups/<str:group_name>/deposit', views.SavingsGroupDeposit.as_view(), name='savings_group_deposit_funds'), # frontend integration done
    path('groups/<str:group_name>/deposits', views.SavingsGroupUserDeposits.as_view(), name='savings_group_all_deposits'), 
    path('groups/<str:group_name>/leaderboard', views.SavingsGroupLeaderboard.as_view(), name='savings_group_leaderboard'), # frontend integration done
    path('groups/public', views.PublicSavingsGroup.as_view(), name='savings_group_leaderboard'), # frontend integration done
    path('groups/join-<str:group_name>', views.JoinPublicSavingsGroup.as_view(), name='savings_group_leaderboard'), # frontend integration done
    path('groups/leave-<str:group_name>', views.LeaveGroup.as_view(), name='savings_group_leaderboard'),  # frontend integration done

    # piggybox functions
    path('piggyboxw', views.PiggyboxWithdraw.as_view(), name='piggybox_withdraw'), # frontend integration done
    path('piggyboxd', views.PiggyboxDeposit.as_view(), name='piggybox_deposit'), # frontend integration done
    path('piggyboxa', views.PiggyboxAuto.as_view(), name='piggybox_auto_deposit'),
    path('piggyboxes/<str:piggy>/info', views.PiggyboxInfo.as_view(), name='piggybox_info'),
    path('my-piggyboxes/', views.MyPiggyboxes.as_view(), name='my_piggybox'), # frontend integration done
    path('piggyboxdel', views.PiggyboxDelete.as_view(), name='piggybox_delete'), # frontend integration done

    # basic banking functions frontend done !!!
    path('transfer', views.Transfer.as_view(), name='transfer_funds'),  # frontend integration done
    path('my-accounts', views.MyAccounts.as_view(), name='my-accounts'),  # frontend integration done
    path('withdraw', views.Withdraw.as_view(), name='withdraw_funds'),  # frontend integration done
    path('deposit', views.Deposit.as_view(), name='deposit_funds'),  # frontend integration done
    path('transfers', views.TransactionView.as_view(), name='all_transactions'),  # frontend integration done
    path('delete-account', views.GetAccount.as_view(), name='delete-account'),  # frontend integration done
    path('<str:account_number>/transactions', views.AccountTransactionHistory.as_view(), name='transaction_history'), # frontend integration done

    # admin operations
    # admin operations
    # admin operations
    path('users', views.ViewAllUsers.as_view(), name='get-all-users'),
    path('piggys', views.ViewPiggyboxes.as_view(), name='get_all_piggyboxes'),
    path('accounts', views.ViewAccounts.as_view(), name='get_all_accounts'),
    path('groups', views.ViewSavingsGroups.as_view(), name='savings_group_leaderboard'),
    # admin operations
    # admin operations
    # admin operations

]


