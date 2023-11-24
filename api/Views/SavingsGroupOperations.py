from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse        
from ..serializers import SavingsGroupSerializer, SGDepositSerializer
from ..Models.SavingsGroup import SavingsGroup, SGDeposit
from rest_framework import status
from ..Models.User import User
from ..Models.Account import Account
from rest_framework import generics
from ..serializers import UserSerializer
from django.db.models import Sum


class SavingsGroupsView(APIView): 
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            group_name = self.kwargs.get('group_name')
            
            user = request.user
                    
            try:
                s_group = SavingsGroup.objects.get(group_name = group_name)
                if user.is_staff or user == s_group.creator:

                    x = s_group.group_members.all()
                    length = len(x)

                    return Response(f"Savings Group: {s_group.group_name} -- Creator: {s_group.creator} -- Members: {length} -- Date created: {s_group.date_created} -- Target amount: {s_group.target_amount} -- Private Savings Group: {s_group.is_private}")
                else:
                    return Response("You are not authorized to view this information")
            except:
                return Response(f"No such savings group {group_name} exists")
        else:
            return Response("Please log in to continue.")

class SavingsGroupMemberAdd(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            member = request.data.get('member')
            group_name = self.kwargs.get('group_name')

            try:
                instance = SavingsGroup.objects.get(group_name = group_name)

                if User.objects.filter(email = member).exists():
                    if instance.is_private == True:
                        if request.user.is_staff or request.user == instance.creator:
                            if instance.group_members.filter(email = member).exists():
                                return Response(f"{member} is already a member of this group")
                            else:
                                add_member = User.objects.get(email = member)
                                instance.group_members.add(add_member.id)
                                instance.save()
                                return Response(f"An email has been sent to {member}. User will join upon acceptance.")
                        else:
                            return Response("You are not authorized to add a member to the group.")
                    elif instance.is_private == False:
                        if instance.group_members.filter(email = request.user).exists():
                            if instance.group_members.filter(email = member).exists():
                                return Response(f"{member} is already a member of this group")
                            else:
                                add_member = User.objects.get(email = member)
                                instance.group_members.add(add_member.id)
                                instance.save()
                                return Response(f"An email has been sent to {member}. User will join upon acceptance.")
                        else:
                            return Response("You are not a member of this group. Join to add other users")
                else:
                    return Response(f"Email has been sent to {member} to create an account and join the savings group")
            except SavingsGroup.DoesNotExist:
                return Response("Error: No such Savings Group exists", status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response("Please log in to continue")

class SavingsGroupMemberRemove(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            wa = request.data.get('account')
            member = request.data.get('member')
            group_name = self.kwargs.get('group_name')

            sgdi = SGDeposit.objects.filter(user__email = member)
            users_total_deposits = sgdi.aggregate(total_amount=Sum('amount'))['total_amount']

            user_account = Account.objects.get(account_number = wa)

            try:
                instance = SavingsGroup.objects.get(group_name = group_name)
                query_user = instance.group_members.filter(email = member)
                if request.user.is_staff or request.user == instance.creator:
                    if query_user.exists():
                        if query_user.first() == instance.creator:
                            return Response("Can not remove yourself from your savings group")
                        else:
                            remove_member = User.objects.get(email = member)
                            instance.group_members.remove(remove_member)
                            instance.current_amount -= users_total_deposits
                            instance.save()

                            user_account.account_balance += users_total_deposits
                            user_account.save()

                        return Response(f"You have successfully removed {member} from {instance.group_name} savings group")
                    else:
                        return Response(f"No member, {member}, to remove from {instance.group_name}")
                else:
                    return Response("You do not have access to this function")

            except SavingsGroup.DoesNotExist:
                return Response("Error: No such Savings Group exists", status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        else:
            return Response("Please log in to continue")

class SavingsGroupDeposit(APIView):
    def post(self,request, *args, **kwargs):
        if request.user.is_authenticated:

            amount = request.data.get('amount')
            group_name = self.kwargs.get('group_name')
            account = request.data.get('account')

            try:
                instance = SavingsGroup.objects.get(group_name = group_name)
                sg = instance
                user_account = Account.objects.get(account_number = account)

                if sg.group_members.filter(email = request.user).exists():
                    if sg.current_amount < sg.target_amount:
                        if amount > 0:
                            if amount <= user_account.account_balance:
                                user_account.account_balance -= amount
                                sg.current_amount += amount

                                SGDeposit.objects.create(
                                    user = request.user,
                                    amount = amount,
                                    sg = instance
                                )

                                user_account.save()
                                sg.save()

                                return Response(f"You have successfully deposited N{amount} to the savings group {group_name}")
                            else:
                                return Response("Insufficient funds to deposit to this Savings Group")
                        else:
                            return Response(f"Please enter a valid amount to deposit into {sg.group_name}")
                    else:
                        return Response("This savings group has reached it's target")
                else:
                    return Response("You can't deposit to this group as you are not a member.")
                    
                        
            except SavingsGroup.DoesNotExist:
                return Response("Error: No such Savings Group exists", status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        else:
            return Response("Please log in to continue")
        
class SavingsGroupUserDeposits(APIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            sg = self.kwargs.get("group_name")

            try:
                instance = SavingsGroup.objects.get(group_name=sg)

                if instance.group_members.filter(email=request.user).exists():
                    sgd = SGDeposit.objects.filter(sg__group_name=sg)

                    if sgd.exists():
                        # Serialize the data
                        serializer = SGDepositSerializer(sgd, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response("This savings group hasn't recorded any deposits")
                else:
                    return Response('You cannot view deposit history, as you are not a member of this group')

            except SavingsGroup.DoesNotExist:
                return Response("Savings group does not exist", status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response(f"Error: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response("Please log in to continue", status=status.HTTP_401_UNAUTHORIZED)
    
class PublicSavingsGroup(APIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            public_savings_groups = SavingsGroup.objects.filter(is_private=False)
            serializer = SavingsGroupSerializer(public_savings_groups, many=True)

            return Response(serializer.data)

class JoinPublicSavingsGroup(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            group_name = self.kwargs.get('group_name')

            try:
                instance = SavingsGroup.objects.get(group_name = group_name)

                if instance.group_members.filter(email = request.user).exists():
                    return Response("Wadup nigga")
                else:
                    add_member = User.objects.get(email = request.user)
                    instance.group_members.add(add_member.id)
                    instance.save()
                    return Response(f"You just joined the public savings group, {group_name}")
            
            except SavingsGroup.DoesNotExist:
                return Response("This savings does not exist")

class SavingsGroupLeaderboard(APIView):
    def get(self, request, *args, **kwargs):
        sg = self.kwargs.get('group_name')
        if request.user.is_authenticated:
            user_deposits = (
                SGDeposit.objects
                .filter(sg__group_name = sg) 
                .values('user__email')
                .annotate(Total=Sum('amount')) 
                .order_by('-Total') 
            )

            return Response(user_deposits)

        return Response("Please log in to continue")   
    
class LeaveGroup(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            wa = request.data.get('account')
            sg = self.kwargs.get('group_name')
            sgi = SavingsGroup.objects.get(group_name = sg)

            sgdi = SGDeposit.objects.filter(user__email = request.user)
            users_total_deposits = sgdi.aggregate(total_amount=Sum('amount'))['total_amount']

            user_account = request.user.accounts.get(account_number = wa)

            if sgi:
                if sgi.group_members.filter(email = request.user).exists():
                    if request.user == sgi.creator:
                        return Response("You can not remove yourself from your group")
                    else:
                        remove_member = User.objects.get(email = request.user)
                        sgi.group_members.remove(remove_member)
                        sgi.current_amount -= users_total_deposits
                        sgi.save()

                        user_account.account_balance += users_total_deposits
                        user_account.save()

                    return Response(f"You have left {sg} and your contributions have been refunded")
                return Response("You are not a member of this group")
            return Response("This group does not exist")
        return Response("Please log in to continue")
    

