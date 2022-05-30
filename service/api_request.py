import requests



response = requests.get(url="http://64.188.16.166:8915/user/addContacts?phone=919923144199&contacts_numbere=6282117645669", verify=False)

print(response.text)


