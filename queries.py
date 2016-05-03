import getpass
import pg8000
import numpy as np

from decimal import *

login = input('login: ')
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
            print (('{:^' + temp + '}').format(a), "|")
        print ("")
        print ("-"*len(types)*int(temp))
        for row in results:
            for r in row:
                r = str(r)
                print (('{:^'+ temp +'}').format(r), "|")
            print("")
    except pg8000.Error as e:
        print('Database error: ', e.args[2])

def retrievePrices(cursor, query):
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        resultsNP=np.transpose(np.array(results))#'turns' the matrix 45 deg
        deltaStock=resultsNP[0]
        deltaComposite=resultsNP[1]
        dates=resultsNP[2]
        
        s=[]
        c=[]
        for d in deltaStock:
            s.append(float(Decimal(d)))
        for d in deltaComposite:
            c.append(float(Decimal(d)))
        return [s,c,dates]
    except pg8000.Error as e:
        print('Database error: ', e.args[2])
    
        
def computeCorrelation(prices):

    [stock, composite,date]=prices
    m = np.corrcoef(stock, composite)
    return (m[1,0]) 

def findMinMaxCorr(cursor, query, weekLength):
    [stock, composite,date]=retrievePrices(cursor,query)
    #8 days has to be used because there is not enough variance in
    #smaller 'sample' sizes for the covariance to be computed
    
    stocksByWeek=chunks(stock,weekLength)
    compositesByWeek=chunks(composite, weekLength)
    weekNum=0
    maxCorr=[-2,0] 
    minCorr=[2,0]
    noCorr=[2,0]
    for s, c in zip(stocksByWeek, compositesByWeek):
        maxCorr= [computeCorrelation([s,c,date]), weekNum] if computeCorrelation([s,c,date])> maxCorr[0] else maxCorr
        minCorr= [computeCorrelation([s,c,date]), weekNum] if computeCorrelation([s,c,date])< minCorr[0] else minCorr
        noCorr= [abs(computeCorrelation([s,c,date])), weekNum] if abs(computeCorrelation([s,c,date]))< noCorr[0] else noCorr
        weekNum=weekNum+1
    print ("Maximum positive correlation: " +str((maxCorr[0])))
    print ("Week of: " + str(date[maxCorr[1]*weekLength]))
    print ("Maximum negative correlation: " +str((minCorr[0])))
    print ("Week of: " + str(date[minCorr[1]*weekLength]))
    print ("Minimum absolute correlation: " +str((noCorr[0])))
    print ("Week of: " + str(date[noCorr[1]*weekLength]))
    print ("------------------------------------")
   
def overallCorrelation(cursor, query):
    print ("------------------------------------")
    print ("Overall correlation: "+ str(computeCorrelation(retrievePrices(cursor, query))))
    
    
#evenly breaks array 'l' into 'n' chunks
def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]   
def racecorrelate(cursor):
    query = """SELECT sd.open_price, cd.open_price, sd.date
               FROM stock_data sd, composite_data cd
               WHERE sd.stock_ticker_id = 1 AND sd.date = cd.date"""
    overallCorrelation(cursor, query)
    findMinMaxCorr(cursor, query, 8)
    #printStatement(cursor, query, 20, "Stock ticker id", "open price", "close price", "composite ticker id", "open price", "close price", "date")

def bhpcorrelate(curosr):
    query = """SELECT sd.open_price, cd.open_price, sd.date
               FROM stock_data sd, composite_data cd
               WHERE sd.stock_ticker_id = 2 AND sd.date = cd.date and sd.date >='2015-10-21'"""
    overallCorrelation(cursor, query)
    findMinMaxCorr(cursor, query, 8)
    #printStatement(cursor, query, 20, "Stock ticker id", "open price", "close price", "composite ticker id", "open price", "close price", "date")

def bblcorrelate(cursor):
    query = """SELECT sd.open_price, cd.open_price, sd.date
               FROM stock_data sd, composite_data cd
               WHERE sd.stock_ticker_id = 3 AND sd.date = cd.date and sd.date >='2015-10-21'"""
    overallCorrelation(cursor, query)
    findMinMaxCorr(cursor, query, 8)
    #printStatement(cursor, query, 20, "Stock ticker id", "open price", "close price", "composite ticker id", "open price", "close price", "date")

def runProgram(cursor):
    print("Please enter what information you would like to view?")
    print("RACE correlation with SSE - 1")
    print("BHP correlation with SSE - 2")
    print("BBL correlation with SSE - 3")
    i = int(input(""))
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
