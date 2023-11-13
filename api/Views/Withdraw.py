from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import User, Account
from ..serializers import AccountSerializer
from ..Hashing import check_password
import pdb

class Withdraw(APIView):

    def post(self, request):
        if request.user.is_authenticated:
            amount = request.data.get('amount')
            pin = request.data.get('pin')

            accounts = request.user.accounts.all()
            if accounts:
                w_account = accounts.first() 
            try:
                amount = float(amount)

                if amount:
                    if check_password(pin.encode('utf-8'), w_account.pin.encode('utf-8')):
                        if w_account.account_balance > amount:
                            w_account.account_balance -= amount
                            w_account.save()
                            return Response(f'You have successfully withdrawn N{amount}' )
                        else:
                            return Response(f'Withdrawal failed due to insufficient funds in account with account number {w_account.account_number}')
                    else:
                        return Response("The pin provided is incorrect. Please try again")
                else:
                    return Response("Please enter a valid amount to complete your transaction")
            except Account.DoesNotExist:
                return Response('This account does not exist' )
        else:
            return Response("User is not authenticated")