import json
from datetime import datetime

currentDate = datetime.now()
formattedDate = currentDate.strftime("%d-%m-%Y")


def loadData() -> None:
    """Load the data from the JSON file."""
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def saveData(data) -> None:
    """Save the data to the JSON file."""
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

def signup(username: str, password: str) -> None:
    """Sign up a new user."""
    data = loadData()

    if username in data:
        return False  # Username already exists

    data[username] = {
        "complete_transaction_history": {},
        "points_per_month": 0,
        "total_expenditure_per_merchant": {},
        "password": password
    }

    saveData(data)
    return True

def login(username, password) -> bool:
    """Log in a user."""
    data = loadData()

    return username in data and data[username]["password"] == password

    
def applyTransaction(merchantCode: str, purchaseAmount: float, username: str, date=formattedDate) -> None:
    
    data = loadData()

    count = len(data[username]["complete_transaction_history"])
    transactionIndex = str(count + 1)  

    if merchantCode in data[username]["total_expenditure_per_merchant"].keys():
        data[username]["total_expenditure_per_merchant"][merchantCode]["dollars"] += purchaseAmount
        data[username]["total_expenditure_per_merchant"][merchantCode]["transactions"].append(transactionIndex)
    else:
        data[username]["total_expenditure_per_merchant"][merchantCode] = { 'dollars': purchaseAmount,
                                                                          'transactions': [ str(count) ]}
    
    points_earned = 0
    transaction = {
        "date": date,
        "merchantCode": merchantCode,
        "purchaseAmount": purchaseAmount,
        "points_earned": points_earned,
    }
    data[username]["complete_transaction_history"][transactionIndex] = transaction
    saveData(data)

    if merchantCode not in ["sport_check", "tim_hortons", "subway"]:
         data[username]["complete_transaction_history"][transactionIndex]["points_earned"] += purchaseAmount // 1
    else: 
        calculateSpecialPoints(username, transactionIndex, date)


def calculateSpecialPoints(username: str, index: int, date=formattedDate) -> None:

    data = loadData()

    rules = {500: {"sport_check": 75, "tim_hortons": 25, "subway": 25},
            300: {"sport_check": 75, "tim_hortons": 25},
            200: {"sport_check": 75},
            150: {"sport_check": 25, "tim_hortons": 10, "subway": 10},
            75: {"sport_check": 20}
    }

    data[username]["complete_transaction_history"][index]["points_earned"] += data[username]["complete_transaction_history"][index]["purchaseAmount"] // 1
    data[username]['points_per_month'] += 100

if __name__ == '__main__':
    signup('ayushsahi', 'password')
    print(login('ayushsahi', 'password'))
    transactions = [
        ('tim_hortons', 4.90),
        ('tim_hortons', 2.90),
        ('sport_check', 99),
        ('tim_hortons', 10),
        ('subway', 19),
        ('tim_hortons', 1.90),
        ('apple', 999),
        ('walmart', 67),
        ('sport_check', 5),
        ('sport_check', 277),
        ('tim_hortons', 9.90),
        ('tim_hortons', 1.90),
        ('tim_hortons', 10.90),
        ('tim_hortons', 2.90),
        ('subway', 21.40),
        ('dennys', 47),
        ('tim_hortons', 1.90),
        ('tim_hortons', 1.90),
        ('walmart', 82),
        ('sport_check', 400)
    ]
    for merchant, amount in transactions:
        applyTransaction(merchant, amount, 'ayushsahi')

    
