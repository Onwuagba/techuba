from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from ..Serializers.AccountSerializer import  AccountSerializer
from ..models import Account, TransactionHistory
from ..Serializers.TransactionHistorySerializer import TransactionHistorySerializer
from rest_framework.permissions import IsAdminUser
# Create your views here.

class ViewAccounts(generics.ListAPIView):
    permission_classes = [IsAdminUser]

    serializer_class = AccountSerializer
    queryset = Account.objects.all()

class AccountTransactionHistory(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            try:
                # Get all accounts associated with the user
                user_accounts = Account.objects.filter(username=request.user)

                # Initialize an empty list to store transaction history for all accounts
                all_transactions = []

                # Iterate over each user account
                for account in user_accounts:
                    # Query transaction history for each account
                    query_acct = TransactionHistory.objects.filter(account=account)

                    if query_acct:
                        serializer = TransactionHistorySerializer(query_acct, many=True)
                        formatted_data = [
                            {
                                'Transaction type': transaction['transaction_type'],
                                'Account number': transaction['account_number'],
                                'Amount': transaction['amount'],
                                'Account balance': transaction['account_balance'],
                                'Time': transaction['timestamp'],
                                # Add more fields as needed
                            }
                            for transaction in serializer.data
                        ]
                        # Append transaction history for the current account
                        all_transactions.append({
                            'Account': account.account_number,
                            'Transactions': formatted_data
                        })
                    else:
                        # Append an entry for the account with no transactions
                        all_transactions.append({
                            'Account': account.account_number,
                            'Transactions': 'No transactions for this account'
                        })

                return Response(all_transactions)

            except Account.DoesNotExist:
                return Response("This user does not have any accounts with us")
            except Exception as e:
                return Response(f'An error occurred: {str(e)}')
        else:
            return Response("User is not authenticated")
