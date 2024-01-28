import json

def loadData():
    """Load the data from the JSON file."""
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def saveData(data):
    """Save the data to the JSON file."""
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

def signup(username: str, password: str):
    """Sign up a new user."""
    data = loadData()

    if username in data:
        return False  # Username already exists

    data[username] = {
        "complete_transaction_history": {},
        "points_per_month": {},
        "total_expenditure_per_merchant": {},
        "password": password
    }

    saveData(data)
    return True

def login(username, password) -> bool:
    """Log in a user."""
    data = loadData()

    return username in data and data[username]["password"] == password

    
def calculatePoints(merchantCode: str, purchaseAmount: float, username: str) -> float:
    
    rules = { "sport_check": {75: [500, 300, 200],
                              25: [150, 75],
                              20: [75]},
                "tim_hortons": {25: [500, 300],
                                10: [75]},
                "subway": {25: [500], 
                            10: [150]}
            }
    


    if rules[merchantCode] is not None:
        for threshold in rules[merchantCode].keys():
            if purchaseAmount % threshold != purchaseAmount:
                print(threshold, rules[merchantCode][threshold])

if __name__ == '__main__':
    print('Starting...')
    signup('ayushsahi', 'password')
    print(login('ayushsahi', 'password'))
    calculatePoints('sport_check', 90.99, 'ayushsahi')
    
