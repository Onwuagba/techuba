from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import User, Account, TransactionHistory
from ..serializers import AccountSerializer
from datetime import datetime
from ..Hashing import check_password

class Deposit(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            # pdb.set_trace()
            account = request.data.get("account")
            amount = request.data.get('amount')
            pin = request.data.get('pin')

            accounts = request.user.accounts.get(account_number = account)
            d_account = accounts

            try:
                if d_account:
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

                        TransactionHistory.objects.create(
                                account= d_account,
                                transaction_type='Deposit',
                                amount = amount,
                                timestamp = datetime.now(),
                                account_balance = d_account.account_balance
                            )

                        return Response(f"You have successfully deposited N{amount}")
                    else:
                        return Response("The pin provided is incorrect. Please try again")
                elif d_account == False:
                    return Response("There is no account associated with this user")
            except  d_account.DoesNotExist:
                return Response('Invalid account number')
        else:
            return Response("User is not authenticated")
             