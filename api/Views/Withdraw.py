from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import User, Account, TransactionHistory
from ..serializers import AccountSerializer
from rest_framework import generics
from ..Hashing import check_password
from datetime import datetime
from rest_framework import permissions, status
import pdb

class Withdraw(APIView):

    def post(self, request):
        if request.user.is_authenticated:
            account = request.data.get('account')
            amount = request.data.get('amount')
            pin = request.data.get('pin')

            w_account = request.user.accounts.get(account_number = account)

            try:
                amount = float(amount)
                if amount:
                    if check_password(pin.encode('utf-8'), w_account.pin.encode('utf-8')):
                        if w_account.account_balance > amount:
                            w_account.account_balance -= amount
                            w_account.save()

                            TransactionHistory.objects.create(
                                account=w_account,
                                transaction_type='Withdrawal',
                                amount = amount,
                                timestamp = datetime.now(),
                                account_balance = w_account.account_balance
                            )

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
        
class GetAccount(APIView):
    def delete(self, request):
        if request.user.is_authenticated:
            acc_no = request.data.get('acc_no')
            pin = request.data.get('pin')
            try:
                account = Account.objects.get(username = request.user, account_number = acc_no)

                if request.user == account.username:
                    if check_password(pin.encode('utf-8'), account.pin.encode('utf-8')):
                        account.delete()
                        return Response("This account has been deleted",  status=200)
                    else:
                        return Response('Invalid pin')
                else:
                    return Response("User is not permitted to delete",  status=403)
            except Account.DoesNotExist:
                return Response(f"No such account", status=404)

            # Delete all the transactions in this account
        else:
            return Response("User is not permitted to delete", status=401)