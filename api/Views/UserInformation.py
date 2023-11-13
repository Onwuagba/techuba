from rest_framework.views import APIView
from ..Models.User import User
from ..Models.Account import Account
from ..Models.Piggybox import Piggybox
from ..Models.SavingsGroup import SavingsGroup
from rest_framework.response import Response


class UserInformationView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            profile = User.objects.get(email = request.user)
            account = Account.objects.get(username = request.user)
            piggybox = Piggybox.objects.get(username=request.user)
            sg = SavingsGroup.objects.get(creator = request.user)
            sgs = SavingsGroup.objects.all()

            filt = sgs.filter(group_name = 'Benzo')
            return Response(f"{filt}")
            # return Response(f"{profile} {account} {piggybox} {sg} {len(sg_member)}")
        else:
            return Response("Please sign in to continue")