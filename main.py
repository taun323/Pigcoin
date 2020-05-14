import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore


from flask import jsonify

cred = credentials.Certificate("json_key.json")
firebase_admin.initialize_app(cred)


db = firestore.client()





def checkBalance(email):
    doc_ref = db.collection("users").document(email)
    doc = doc_ref.get()
    
    if doc.exists:
        data = doc.to_dict()
        balance = data.get("Balance")
        
        return jsonify(result=str(balance))
    else:
        print(u'No such document!')



def spend(email, cost):
    doc_ref = db.collection("users").document(email)
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()
        balance = data.get("Balance")
        cost = float(cost)
        if balance >= cost:
            message = "You can afford it, you would have €" + str(balance-cost) +" left."
            return jsonify(result=message)
        else:
            message = "You can´t afford it, you would need €" + str(cost-balance) + " more."
            return jsonify(result=message)
    else:
        print('No such document!')


def login(email, password):
    doc_ref = db.collection("users").document(email)
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()
        realPassword = data.get("password")

        if password == realPassword:
            passMessage = "Credentials are valid"
            return True
            return jsonify(result = passMessage)

        else:
            return False
            passMessage = "Check your username or password"
            return jsonify(result = passMessage)
    else:
        return False
        print('Check your username or password')




def createAccount(email, password, name, age, accountNumber):
    doc_ref = db.collection("users").document(email)
    doc = doc_ref.get()

    if doc.exists:
        message = "Email is already in use"
        return jsonify(result=message)

    else:
        doc_ref = db.collection('users').document(email)
        doc_ref.set({
            "email": email,
            "password": password,
            "name" : name,
            "age": age,
            "accountNumber" : accountNumber,
            "Balance": 1345
             })
        message = "Account successfully created"
        return jsonify(result=message)
       

def main(request):
    dict = request.get_json()
    print(dict)
    #OPERATIONS WITHOUT LOGIN
    if dict.get("intent") == "createAccount":    
        return createAccount(dict.get("email"), dict.get("password"), dict.get("name"), dict.get("age"), dict.get("accountNumber"))
    #OPERATIONS WITH LOGIN
    if(login(dict.get("email"), dict.get("password"))):
        print("login successful")
        if dict.get("intent") == "checkBalance":
            return checkBalance(dict.get("email"))
        if dict.get("intent") == "spend":
            return spend(dict.get("email"), dict.get("cost"))
        return jsonify(result = "valid credentials")
    else:
        passMessage = "TEEST Check your username or password"
        return jsonify(error = passMessage)






