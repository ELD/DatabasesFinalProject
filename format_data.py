import pg8000
import getpass
from yahoo_finance import Share

class DBInsert:
    def __init__(self, username, password, indexes, tickers):
        self.username = username
        self.password = password
        self.indexes = indexes
        self.tickers = tickers
        self.conn = pg8000.connect(username=self.username,
                                    password=self.password,
                                    host="flowers.mines.edu",
                                    database="csci403")


    def insert_data(self):
        cursor = self.conn.cursor()

        # Insert index data
        for index in self.indexes:
            query = "INSERT INTO composite_tickers(name) VALUES (%s)"
            cursor.execute()

        # Insert ticker data
        for ticker in self.tickers:
            print "Populating for %s" % ticker


# Using the class to format the data
username = raw_input("Enter your database username: ")
password = getpass.getpass("Enter your DB password: ")

indexes = ['000001.SS']
tickers = ['RACE', 'BHP', 'BBL']

db_inserter = DBInsert(username, password, indexes, tickers)
db_inserter.insert_data()
