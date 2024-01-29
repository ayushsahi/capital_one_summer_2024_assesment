import json
from datetime import datetime
import math

currentDate = datetime.now()
formattedDate = currentDate.strftime("%d-%m-%Y")


def loadData() -> None:
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def saveData(data) -> None:
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

def signup(username: str, password: str) -> None:
    data = loadData()

    if username in data:
        return False  # Username already exists

    data[username] = {
        "completeTransactionHistory": {},
        "pointsPerMonth": 0,
        "TotalExpenditurePerMerchant": {},
        "password": password
    }

    saveData(data)
    return True

def login(username, password) -> bool:
    data = loadData()
    return username in data and data[username]["password"] == password

    
def applyTransaction(merchantCode: str, purchaseAmount: float, username: str, date=formattedDate) -> None:
    
    data = loadData()

    count = len(data[username]["completeTransactionHistory"])
    transactionIndex = str(count + 1)  

    if merchantCode in data[username]["TotalExpenditurePerMerchant"].keys():
        data[username]["TotalExpenditurePerMerchant"][merchantCode]["dollars"] += math.floor(purchaseAmount)
        data[username]["TotalExpenditurePerMerchant"][merchantCode]["transactions"].append(transactionIndex)
    else:
        data[username]["TotalExpenditurePerMerchant"][merchantCode] = { 'dollars': math.floor(purchaseAmount),
                                                                          'transactions': [ transactionIndex ]}
    
    pointsEarned = 0
    transaction = {
        "date": date,
        "merchantCode": merchantCode,
        "purchaseAmount": math.floor(purchaseAmount),
        "pointsEarned": pointsEarned,
    }
    data[username]["completeTransactionHistory"][transactionIndex] = transaction
    saveData(data)

    if merchantCode not in ["sportcheck", "tim_hortons", "subway"]:
        data[username]["completeTransactionHistory"][transactionIndex]["pointsEarned"] += purchaseAmount // 1
        saveData(data)
    else: 
        calculateSpecialPoints(username, transactionIndex, date)


def calculateSpecialPoints(username: str, index: str, date=formattedDate) -> None:
    data = loadData()

    totalSportcheck = data[username]["TotalExpenditurePerMerchant"].get("sportcheck", {}).get("dollars", 0)
    totalTims = data[username]["TotalExpenditurePerMerchant"].get("tim_hortons", {}).get("dollars", 0)
    totalSubway = data[username]["TotalExpenditurePerMerchant"].get("subway", {}).get("dollars", 0)
    
    newMonthlyPoints = 0

    rules = {
        500: {"sportcheck": 75, "tim_hortons": 25, "subway": 25},
        150: {"sportcheck": 25, "tim_hortons": 10, "subway": 10},
        300: {"sportcheck": 75, "tim_hortons": 25},
        75: {"sportcheck": 20}
    }

    temp = [math.floor(totalSportcheck), math.floor(totalTims), math.floor(totalSubway)]

    while totalSportcheck >= 75 and totalTims >= 25 and totalSubway >= 25:
        newMonthlyPoints += 500
        totalSportcheck -= 75
        totalTims -= 25
        totalSubway -= 25

    while totalSportcheck >= 25 and totalTims >= 10 and totalSubway >= 10:
        newMonthlyPoints += 150
        totalSportcheck -= 25
        totalTims -= 10
        totalSubway -= 10

    while totalSportcheck >= 75 and totalTims >= 25:
        newMonthlyPoints += 300
        totalSportcheck -= 75
        totalTims -= 25

    while totalSportcheck >= 20:
        newMonthlyPoints += 75
        totalSportcheck -= 20

    newMonthlyPoints += totalSportcheck + totalTims + totalSubway

    for merchant, merchantData in data[username]["TotalExpenditurePerMerchant"].items():
        if merchant not in ["sportcheck", "tim_hortons", "subway"]:
            newMonthlyPoints += merchantData.get("dollars", 0)
    
    data[username]["pointsPerMonth"] = newMonthlyPoints
    saveData(data)

def clearData() -> None:
    with open('data.json', 'w') as file:
        json.dump({}, file, indent=4)

if __name__ == '__main__':
    clearData()
    signup('ayushsahi', 'password')
    login('ayushsahi', 'password')
    transactions = [
        ('tim_hortons', 4.90),
        ('tim_hortons', 2.90),
        ('sportcheck', 99),
        ('tim_hortons', 10),
        ('subway', 19),
        ('tim_hortons', 1.90),
        ('apple', 999),
        ('walmart', 67),
        ('sportcheck', 5),
        ('sportcheck', 277),
        ('tim_hortons', 9.90),
        ('tim_hortons', 1.90),
        ('tim_hortons', 10.90),
        ('tim_hortons', 2.90),
        ('subway', 21.40),
        ('dennys', 47),
        ('tim_hortons', 1.90),
        ('tim_hortons', 1.90),
        ('walmart', 82),
        ('sportcheck', 400)
    ]
    for merchant, amount in transactions:
        applyTransaction(merchant, amount, 'ayushsahi')

    
