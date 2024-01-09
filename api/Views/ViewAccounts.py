from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..Serializers.AccountSerializer import  AccountSerializer
from ..Serializers.TransactionHistorySerializer import TransactionHistorySerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAdminUser
from ..Models.Account import Account
from ..Models.Transaction import TransactionHistory
# Create your views here.

class ViewAccounts(generics.ListAPIView):
    permission_classes = [IsAdminUser]

    serializer_class = AccountSerializer
    queryset = Account.objects.select_related('username')

class AccountTransactionHistory(APIView):
    def get(self, request, account_number):
        if request.user.is_authenticated:
            try:
                account = Account.objects.get(account_number = account_number)
                query_acct = TransactionHistory.objects.filter(account = account)

                print(f"Received account_number: {account_number}")


                if query_acct.exists():
                    serializer = TransactionHistorySerializer(query_acct, many=True)

                    if request.user == account.username: 

                        # Format the serialized data
                        formatted_data = [
                            {
                                'Transaction_type': transaction['transaction_type'],
                                'Amount': transaction['amount'],
                                'Account_balance': transaction['account_balance'],
                                'Time': transaction['timestamp'],
                                # Add more fields as needed
                            }
                            for transaction in serializer.data
                        ]

                        # Return transaction history for the specified account
                        return Response({
                            'Account': account.account_number,
                            'Transactions': formatted_data
                        }, status=status.HTTP_200_OK)
                    else:
                        # Return an entry for the account with no transactions
                        return Response({
                            'Account': account.account_number,
                            'Transactions': 'No transactions for this account'
                        }, status=status.HTTP_200_OK)

            except Account.DoesNotExist:
                print("Lol")
                return Response("This account does not exist", status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response(f'An error occurred: {str(e)}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response("User is not authenticated", status=status.HTTP_401_UNAUTHORIZED)



class MyAccounts(generics.ListAPIView):
    serializer_class = AccountSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Account.objects.filter(username=self.request.user)
        else:
            raise AuthenticationFailed('Please log in')
            