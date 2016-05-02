import getpass
import pg8000

login = raw_input('login: ')
secret = getpass.getpass('password: ')

credentials = {'user'    : login,
               'password': secret,
               'database': 'csci403',
               'host'    : 'flowers.mines.edu'}

try:
    db = pg8000.connect(**credentials)
except pg8000.Error as e:
    print('Database error: ', e.args[2])
    exit()

cursor = db.cursor()

def printStatement(cursor, query, temp, *types):
    try:
        temp = str(temp)
        cursor.execute(query)
        results = cursor.fetchall()
        for a in types:
            print ('{:^' + temp + '}').format(a), "|",
        print ""
        print "-"*len(types)*int(temp)
        for row in results:
            for r in row:
                print ('{:^'+ temp +'}').format(r), "|",
            print ""
    except pg8000.Error as e:
        print('Database error: ', e.args[2])

def racecorrelate(cursor):
    query = """SELECT sd.stock_ticker_id, sd.open_price, sd.close_price, cd.composite_ticker_id, cd.open_price, cd.close_price, cd.date
               FROM stock_data sd, composite_data cd
               WHERE sd.stock_ticker_id = 1 AND sd.date = cd.date"""
    printStatement(cursor, query, 20, "Stock ticker id", "open price", "close price", "composite ticker id", "open price", "close price", "date")

def bhpcorrelate(curosr):
    query = """SELECT sd.stock_ticker_id, sd.open_price, sd.close_price, cd.composite_ticker_id, cd.open_price, cd.close_price, cd.date
               FROM stock_data sd, composite_data cd
               WHERE sd.stock_ticker_id = 2 AND sd.date = cd.date"""
    printStatement(cursor, query, 20, "Stock ticker id", "open price", "close price", "composite ticker id", "open price", "close price", "date")

def bblcorrelate(cursor):
    query = """SELECT sd.stock_ticker_id, sd.open_price, sd.close_price, cd.composite_ticker_id, cd.open_price, cd.close_price, cd.date
               FROM stock_data sd, composite_data cd
               WHERE sd.stock_ticker_id = 3 AND sd.date = cd.date"""
    printStatement(cursor, query, 20, "Stock ticker id", "open price", "close price", "composite ticker id", "open price", "close price", "date")

def runProgram(cursor):
    print("Please enter what information you would like to view?")
    print("RACE correlation with SSE - 1")
    print("BHP correlation with SSE - 2")
    print("BBL correlation with SSE - 3")
    i = input("")
    if i < 1 or i > 3:
        return False
    elif i == 1:
        racecorrelate(cursor)
    elif i == 2:
        bhpcorrelate(cursor)
    elif i == 3:
        bblcorrelate(cursor)
    return True;

x = True
while(x):
    x = runProgram(cursor)

cursor.close()
db.close()
