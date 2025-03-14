import mysql.connector
import pandas as pd 

class dbconn:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='msdhoni812',
                database='mahan'
            )
            if self.conn.is_connected():
                print("Connected successfully")
            self.mycursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print(f"Connection error: {err}")

    def ensure_connection(self):
        """Reconnects to the database if the connection is lost."""
        if not self.conn.is_connected():
            self.conn.reconnect()
            self.mycursor = self.conn.cursor()

    def fetch_all_cities(self):
        self.ensure_connection()
        city = []
        self.mycursor.execute("""
            SELECT Source FROM `flights_cleaned - flights_cleaned`
            UNION
            SELECT Destination FROM `flights_cleaned - flights_cleaned`
        """)
        data = self.mycursor.fetchall()
        for i in data:
            city.append(i[0])
        return city

    def fetch_all_flights(self, source, dest):
        self.ensure_connection()
        query=f"""
        SELECT * FROM `flights_cleaned - flights_cleaned`
        WHERE Source='{source}' AND Destination='{dest}';
        """
        self.mycursor.execute(query)
    
    # Fetch column names
        column_names = [i[0] for i in self.mycursor.description]  # Extract column names
    
    # Fetch data
        data = self.mycursor.fetchall()
    
    # Convert to Pandas DataFrame
        df = pd.DataFrame(data, columns=column_names)  
        return df  # Return DataFrame


    def fetch_flight_frequency(self):
        self.ensure_connection()
        flight, frequency = [], []
        self.mycursor.execute("""
        SELECT Airline, COUNT(*) FROM `flights_cleaned - flights_cleaned`
        GROUP BY Airline
        """)
        data = self.mycursor.fetchall()
        for i in data:
            flight.append(i[0])
            frequency.append(i[1])
        return flight, frequency

    def busiest_cities(self):
        self.ensure_connection()
        places, frequency1 = [], []
        self.mycursor.execute("""
        SELECT t.Source, COUNT(*) FROM (
            SELECT Source FROM `flights_cleaned - flights_cleaned`
            UNION ALL
            SELECT Destination FROM `flights_cleaned - flights_cleaned`
        ) t GROUP BY t.Source
        """)
        data = self.mycursor.fetchall()
        for i in data:
            places.append(i[0])
            frequency1.append(i[1])
        return places, frequency1

    def daily_frequency(self):
        self.ensure_connection()
        dates, frequency2 = [], []
        self.mycursor.execute("""
        SELECT Date_of_Journey, COUNT(*) FROM `flights_cleaned - flights_cleaned`
        GROUP BY Date_of_Journey
        """)
        data = self.mycursor.fetchall()
        for i in data:
            dates.append(i[0])
            frequency2.append(i[1])
        return dates, frequency2
