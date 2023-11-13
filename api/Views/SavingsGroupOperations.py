from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse        
from ..serializers import SavingsGroupSerializer
from ..Models.SavingsGroup import SavingsGroup
from rest_framework import status
from ..Models.User import User
from ..Models.Account import Account

class SavingsGroupsView(APIView): 
    def get(self, request):
        if request.user.is_authenticated:
            group_name = request.data.get("group_name")
            
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
                return Response("No such savings group exists")
        else:
            return Response("User is not authenticatd.")

class SavingsGroupMemberAdd(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            member = request.data.get('member')
            group_name = request.data.get('group_name')

            try:
                instance = SavingsGroup.objects.filter(group_name = group_name)

                if User.objects.filter(email = member).exists():
                    if request.user.is_staff or request.user == instance[0].creator:
                        if instance[0].group_members.filter(email = member).exists():
                            return Response(f"{member} is already a member of this group")
                        else:
                            add_member = User.objects.get(email = member)
                            instance[0].group_members.add(add_member.id)
                            instance[0].save
                            return Response(f"{member} is not in this group. Send an invitational email.")
                    else:
                        return Response("You are not authorized to access this info")
                else:
                    return Response("This user does not exist")
            except SavingsGroup.DoesNotExist:
                return Response("Error: No such Savings Group exists", status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response("User is not authenticated")

class SavingsGroupMemberRemove(APIView):
    def post(self, request):
        if request.user.is_authenticated:

            member = request.data.get('member')
            group_name = request.data.get('group_name')

            try:
                instance = SavingsGroup.objects.filter(group_name = group_name)

                if request.user.is_staff or request.user == instance[0].creator:
                    if instance[0].group_members.filter(email = member).exists():

                        remove_member = User.objects.get(email = member)
                        instance[0].group_members.remove(remove_member)
                        instance[0].save()
                        
                        return Response(f"You have successfully removed {member} from {instance[0].group_name} savings group")
                    else:
                        return Response(f"No member, {member}, to remove from {instance[0].group_name}")
                else:
                    return Response("You do not have access to this function")

            except SavingsGroup.DoesNotExist:
                return Response("Error: No such Savings Group exists", status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        else:
            return Response("User is not authenticated")

class SavingsGroupDeposit(APIView):
    def post(self,request):
        if request.user.is_authenticated:

            amount = request.data.get('amount')
            group_name = request.data.get('group_name')

            try:
                instance = SavingsGroup.objects.filter(group_name = group_name)
                sg = instance[0]
                user_account = Account.objects.get(username = request.user)

                if sg.group_members.filter(email = request.user).exists():
                    if sg.current_amount < sg.target_amount:
                        if amount > 0:
                            if amount <= user_account.account_balance:
                                user_account.account_balance -= amount
                                sg.current_amount += amount

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
            return Response("User is not authenticated. Please log in to continue")
        
# .exists is a far easier and efficient way to find something in a queryset or an array ///
