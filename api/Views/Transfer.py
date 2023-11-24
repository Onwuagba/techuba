from rest_framework.views import APIView
from rest_framework.response import Response
from ..Models.Account import Account
from ..Models.Transaction import Transaction
from datetime import datetime
from ..Hashing import check_password
import pdb
from django.db import transaction

class Transfer(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            account = request.data.get('account')
            receiver_number = request.data.get('receiver')
            amount = request.data.get('amount')
            pin = request.data.get('pin')

            try:
                # Ensure the authenticated user has an account
                sender_accounts = request.user.accounts.all()
                if sender_accounts:
                    sender_account = sender_accounts.get(account_number = account)

                    if not sender_account:
                        return Response("Authenticated user does not have an associated account")

                    receiver = Account.objects.get(account_number=receiver_number)
                    amount = float(amount)

                    if sender_account == receiver:
                        return Response("You cannot make a transfer to yourself")
                    else:

                        if receiver:

                            if amount == 0:
                                return Response("Please enter a valid amount to complete your transfer")

                            with transaction.atomic():
                                if check_password(pin.encode('utf-8'), sender_account.pin.encode('utf-8')):
                                    if sender_account.account_balance < amount:
                                        return Response("Transfer failed due to insufficient funds")

                                    sender_account.account_balance -= amount
                                    receiver.account_balance += amount
                                    sender_account.save()
                                    receiver.save()

                                    Transaction.objects.create(
                                        sender=sender_account,
                                        receiver=receiver,
                                        amount=amount,
                                        transaction_date = datetime.now()
                                    )

                                    return Response(f'You have successfully transferred {amount} to {receiver}')
                                else:
                                    return Response("The PIN provided is incorrect. Please try again")
                        else:
                            return Response("This account does not exist. Please enter a valid recipient account.")
                else:
                    return Response("User does not have any accounts")  

            except Account.DoesNotExist:
                    return Response('No such account')   
        else:
            return Response("User is not authenticated")

