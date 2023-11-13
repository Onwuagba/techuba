from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse        
from ..models import User, Piggybox
from ..Models.Account import Account
from ..serializers import PiggyboxSerializer
import pdb
from datetime import datetime
from decimal import Decimal
from ..Hashing import check_password


# from celery import Celery
# from celery.schedules import crontab



class PiggyboxInfo(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            
            try:
                piggybox = Piggybox.objects.get(username = request.user)

                if piggybox:
                    return Response(f"Creator: {piggybox.username} --- Box: {piggybox.name_of_box} --- Date created: {piggybox.date_created} --- Target amount: {piggybox.target_amount} --- Current Amount: {piggybox.current_amount}")
                else:
                    return Response("User has no existing piggybox", status=404)
            except Piggybox.DoesNotExist:
                return Response("No such box")
        else:
            return Response("User is not authenticated")

class PiggyboxDelete(APIView):
    def delete(self, request):
        if request.user.is_authenticated:
            
            try:
                piggybox = Piggybox.objects.get(username = request.user)

                if request.user == piggybox.username:
                    piggybox.delete()
                    return Response("This piggybox has been deleted",  status=200)
                else:
                    return Response("User is not permitted to delete",  status=403)
            except Piggybox.DoesNotExist:
                return Response("No such box", status=404)

            # Delete all the transactions in this account
        else:
            return Response("User is not permitted to delete", status=401)

class PiggyboxWithdraw(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            amount = request.data.get('amount')
            try:
                user_piggybox = Piggybox.objects.get(username = request.user)
                piggybox = user_piggybox

                current_amount = Decimal(piggybox.current_amount)
                target_amount = Decimal(piggybox.target_amount)
                amount = Decimal(amount)

                user_account = Account.objects.get(username = request.user)
                account = user_account

                if amount:
                    if amount > current_amount:
                        return Response("Your withdrawal request exceeds your current piggybox balance.")
                    elif amount <= current_amount:
                        if current_amount < target_amount:
                            # Update current_amount on the instance
                            piggybox.current_amount -= amount
                            penalty = amount * Decimal('0.25')
                            account.account_balance += amount
                            # Save the instance to persist the changes
                            account.save()
                            piggybox.save()

                            return Response(f"You have withdrawn N{amount} and we keep N{penalty:.2f} as a penalty for early withdrawal!")
                        elif current_amount >= target_amount:
                            piggybox.current_amount -= amount
                            account.account_balance += amount

                            piggybox.save()
                            account.save()

                            return Response(f"You reached your target and have withdrawn N{amount}")

                else:
                    return Response("Please enter a valid amount to withdraw")

            except Piggybox.DoesNotExist:
                return Response('No such box')
            except Exception as e:
                print(f"Exception: {e}")
                return Response("An error occurred during withdrawal.")
        else:
            return Response("User is not authenticated")

class PiggyboxDeposit(APIView):
# ...
    def post(self, request):
        if request.user.is_authenticated:
            # box_name = request.data.get('box')
            amount = request.data.get('amount')
            pin = request.data.get('pin')


            user = request.user.piggyboxes.all()
            piggybox = user.first()
            
            # return Response(f"{piggybox}")
            
            user_account = request.user.accounts.all()
            account = user_account.first()

            try:
                amount = Decimal(amount)
                
                if account:
                    if piggybox:
                        if amount:
                            if check_password(pin.encode(), account.pin.encode()):
                                if account.account_balance > 0 and amount < account.account_balance:
                                    piggybox.current_amount += amount
                                    account.account_balance -= amount

                                    piggybox.save()
                                    account.save()

                                    return Response(f"You have successfully funded your {piggybox.name_of_box} piggybox")
                                else:
                                    return Response(f"This transaction could not be completed due to insufficient funds in your account with account number {account.account_number}")
                            else:
                                return Response("Incorrect pin provided. Please try again")
                        else:
                            return Response("Please enter a valid amount to complete your deposit")           
                    else:
                        return Response('This piggybox does not exist')
                else:
                    return Response("This user does not exist")       

            except Piggybox.DoesNotExist:
                return Response('No such box')
            except Exception as e:
                # Log the exception for further investigation
                print(f"Exception: {e}")
                return Response("An error occurred during withdrawal.")
        else:
            return Response("User is not authenticated")

class PiggyboxAuto(APIView): 


    def post(self, request):
        user = request.data.get('user')
        amount = request.data.get('amount')

        try:
            piggybox_instance = Piggybox.objects.get(username = user)
            account_instance = Account.objects.get(username = user)

            if piggybox_instance.username == account_instance.username:
                if piggybox_instance.current_amount == piggybox_instance.target_amount:
                    return Response(f'This piggybox has reached its target. Make another piggybox or increase the target for {piggybox_instance.name_of_box}.')
                else:
                    if amount:
                        if account_instance.account_balance > 0:
                            if account_instance.account_balance > amount:
                                account_instance.account_balance -= amount
                                account_instance.save()

                                piggybox_instance.current_amount += amount
                                piggybox_instance.save()
                                return Response(f'Successful deposit of N{amount} into the piggybox {piggybox_instance.name_of_box}')
                            else:
                                return Response(f'Transaction failed due to insufficient balance in your account with account number {account_instance.account_number}')
                        else:
                            return Response(f'Transaction failed due to insufficient balance in your account with account number {account_instance.account_number}')
                    else:
                        return Response('Please enter a valid amount for automatic deduction!')
        except (Piggybox.DoesNotExist, Account.DoesNotExist):
            return Response('No such box or account')

        except Exception as e:
            # Handle other exceptions
            return Response(f'An error occurred: {str(e)}')