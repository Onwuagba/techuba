Savings platform - DRF


- User register/login -> firstname, lastname, username, phone number, email, address, password
- user can verify email
- user can update profile 
- user can delete profile -> soft delete. Permanently delete data after 10 days
-----------------------------------------------------------
- user can create account(s)
- user can transfer to other users
- user can withdraw
- user can deposit
------------------------------------------------------------
- user can create a piggybox
- user can break their piggybox at a fine
- user can auto-save -> at predefined rate, either a particular date or set occurrence
-------------------------------------------------------------
- user can create a savings group
- user can add fellow users to the savings group
- user can set rate at which their account is debited for the group. Daily/weekly/monthly
- group can be public or private
- user can invite non-users to join their group 
- user can see a leaderboard
-------------------------------------------------------------


- USER MODEL:
firstname --> alpha(30)
lastname --> alpha(30)
username (U) --> alphanumeric(30)
phone number(U) --> int()
email(U) --> email(), primary_key
address --> foreign_key(Address)
password --> hash

- ADDRESS:
id --> int, autoincrement
no --> alphanumeric
street --> alpha(30)
city --> alpha(30)
state --> alpha(30)
country --> alpha(30)

- ACCOUNT MODEL
username --> foreign_key(User)
accountnumber --> int(10), primary_key
pin --> int(4)
accountbalance --> bigfloat

- PIGGYBOX MODEL
id --> int, autoincrement ,primary_key
username --> foreign_key(User)
datecreated --> datetime(), auto
target --> bigint
datefulfilled --> datetime()
datebreak --> datetime()
interest --> float
nameofbox --> text(30)


- SAVINGS GROUP
id --> int, autoincrement
groupname --> text(30) 
creator --> foreign_key(User)
datecreated --> datetime(), auto
targetamount --> bigint
datefulfilled --> date()
datebreak --> datetime()
interest --> float
nameofbox --> text(30)
username --> foreign_key(User)

- SAVINGS GROUP MEMBERS
id --> int, autoincrement, primary_key
username --> foreign_key(User)
group --> foreign_key(Savings Group)

- GROUP TRANSACTIONS
id --> int, autoincrement
type --> choices(debit, credit)
amount --> bigfloat
description **OPTIONAL