import pg8000
import getpass
from yahoo_finance import Share

class DBInsert:
    def __init__(self, username, password, indexes, tickers, date_range):
        self.username = username
        self.password = password
        self.indexes = indexes
        self.tickers = tickers
        self.date_range = date_range
        self.conn = pg8000.connect(user=self.username,
                                    password=self.password,
                                    host="flowers.mines.edu",
                                    database="csci403")


    def insert_data(self):
        cursor = self.conn.cursor()

        # Insert index data
        for index in self.indexes:
            print "inserting data for index: %s" % index
            query = "INSERT INTO composite_tickers(name) VALUES (%s) RETURNING id"
            cursor.execute(query, (index,))

            index_id = cursor.fetchone()[0]

            index = Share(index)

            query = "INSERT INTO composite_data(composite_ticker_id, open_price, close_price, date) VALUES (%s, %s, %s, %s)"

            for data in index.get_historical(self.date_range[0], self.date_range[1]):
                cursor.execute(query, (index_id, data['Open'], data['Close'], data['Date']))

            self.conn.commit()

        # Insert ticker data
        for ticker in self.tickers:
            print "Populating for %s" % ticker
            query = "INSERT INTO stock_tickers(name) VALUES (%s) RETURNING id"
            cursor.execute(query, (ticker,))

            ticker_id = cursor.fetchone()[0]

            ticker = Share(ticker)

            query = "INSERT INTO stock_data(stock_ticker_id, open_price, close_price, date) VALUES (%s, %s, %s, %s)"

            for data in ticker.get_historical(self.date_range[0], self.date_range[1]):
                cursor.execute(query, (ticker_id, data['Open'], data['Close'], data['Date']))

            self.conn.commit()

# Using the class to format the data
username = raw_input("Enter your database username: ")
password = getpass.getpass("Enter your DB password: ")

indexes = ['000001.SS']
tickers = ['RACE', 'BHP', 'BBL']

date_range = ['2014-04-28', '2016-04-28']

db_inserter = DBInsert(username, password, indexes, tickers, date_range)
db_inserter.insert_data()
