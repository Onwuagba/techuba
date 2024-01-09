from rest_framework.views import APIView
from ..Models.User import User
from ..Models.Account import Account
from ..Models.Piggybox import Piggybox
from ..Models.SavingsGroup import SavingsGroup
from rest_framework.response import Response


class ProfileOverview(APIView):
    def get_piggybox_info(self, user):
        piggybox_info = Piggybox.objects.filter(username=user)
        return piggybox_info

    def get_savingsgroup_info(self, user):
        sg = SavingsGroup.objects.filter(group_members__email=user)
        return sg

    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(email=request.user)
            account = Account.objects.filter(username=request.user).first()

            piggybox_info = self.get_piggybox_info(request.user)
            savingsgroup_info = self.get_savingsgroup_info(request.user)

            response_data = f"{user} : Full Name: {user.firstname} {user.lastname} --- Address: {user.address}  -- Account(s): {account}"

            if piggybox_info.exists():
                response_data += f" -- Piggybox(es): {len(piggybox_info)}"
            else:
                response_data += f" -- Piggybox(es): None"

            if savingsgroup_info.exists():
                group_info = [sa.group_name for sa in savingsgroup_info]
                response_data += f" -- Savings Group(s): {group_info}"
            else:
                response_data += f" -- Not a member of a saving group"      
                
            return Response(response_data)
        else:
            return Response("Please sign in to continue")
