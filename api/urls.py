from django.urls import path, include
from . import views

urlpatterns = [
    
    path('', views.ViewAllUsers.as_view()),
    path('<int:pk>', views.SeeUser.as_view()),
    path('accounts', views.ViewAccounts.as_view()),
    path('piggys', views.ViewPiggyboxes.as_view()),
    path('user-information', views.UserInformationView.as_view()),

    path('savings-groups', views.SGTest.as_view()),
    path('savings-groups/group-info', views.SavingsGroupsView.as_view()),
    path('savings-groups/add-member', views.SavingsGroupMemberAdd.as_view()),
    path('savings-groups/remove-member', views.SavingsGroupMemberRemove.as_view()),
    path('savings-groups/deposit-funds', views.SavingsGroupDeposit.as_view()),

    path('transfer', views.Transfer.as_view()),
    path('withdraw', views.Withdraw.as_view()),
    path('deposit', views.Deposit.as_view()),
    path('alltransactions', views.TransactionView.as_view()),

    path('signup/', views.SignUpView.as_view()),
    path('piggyboxw', views.PiggyboxWithdraw.as_view()),
    path('piggyboxd', views.PiggyboxDeposit.as_view()),
    path('piggyboxa', views.PiggyboxAuto.as_view()),
    path('piggyboxi', views.PiggyboxInfo.as_view()),
    path('piggyboxdel', views.PiggyboxDelete.as_view()),
    # path('test-auto', views.Command.as_view()),

]
