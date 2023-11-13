from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import User, Account
from ..serializers import AccountSerializer
import pdb
from ..Hashing import check_password

class Deposit(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            # pdb.set_trace()
            amount = request.data.get('amount')
            pin = request.data.get('pin')

            accounts = request.user.accounts.all()
            d_account = accounts.first()

            if d_account:
                try:
                    # get account number from account table
                    amount = float(amount)

                    if check_password(pin.encode(), d_account.pin.encode()):
                    # check if account is valid
                        if not d_account:
                            return Response("Account does not exist")
                        
                        # get account number from account table
                        if not amount or amount <= 0:
                            return Response("Invalid amount. Please provide a positive value.")

                        d_account.account_balance += amount
                        d_account.save()

                        return Response(f"You have successfully deposited N{amount}")
                    else:
                        return Response("The pin provided is incorrect. Please try again")
                except  Account.DoesNotExist:
                    return Response('Invalid account number')
            else:
                return Response("There is no account associated with this user")
        else:
            return Response("User is not authenticated")
            