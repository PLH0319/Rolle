import sqlite3
import pandas as pd
class MusicalDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Connect to the SQLite database."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def create_activity_table(self):
        """Create musical_activity table."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS musical_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                UID VARCHAR(255) UNIQUE,
                version VARCHAR(50),
                title VARCHAR(255),
                category INTEGER,
                showUnit VARCHAR(255),
                discountInfo VARCHAR(255),
                descriptionFilterHtml TEXT,
                imageUrl VARCHAR(255),
                masterUnit VARCHAR(255),
                subUnit VARCHAR(255),
                supportUnit VARCHAR(255),
                otherUnit VARCHAR(255),
                webSales VARCHAR(255),
                sourceWebPromote VARCHAR(255),
                comment TEXT,
                editModifyDate DATETIME,
                sourceWebName VARCHAR(255),
                startDate DATETIME,
                endDate DATETIME,
                hitRate INTEGER
            )
        ''')

    def create_showinfo_table(self):
        """Create musical_showinfo table."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS musical_showinfo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                activity_id INTEGER REFERENCES musical_activity(id),
                location_id INTEGER REFERENCES musical_location(id),
                time DATETIME ,
                onSales VARCHAR(255),
                price VARCHAR(255),
                endTime DATETIME
            )
        ''')

    def create_location_table(self):
        """Create musical_location table."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS musical_location (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location VARCHAR(255),
                locationName VARCHAR(255) UNIQUE,
                latitude FLOAT,
                longitude FLOAT
            )
        ''')

    def insert_location_data(self, row):
        """Insert data into musical_location table."""
        query = """
        INSERT INTO musical_location (location, locationName, latitude, longitude)
                VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(query, row)

    def insert_activity_data(self, row):
        """Insert data into musical_activity table."""
        query = """
        INSERT INTO musical_activity 
                (UID, version, title, category, showUnit, discountInfo, descriptionFilterHtml,
                 imageUrl, masterUnit, subUnit, supportUnit, otherUnit, webSales,
                 sourceWebPromote, comment, editModifyDate, sourceWebName, startDate, endDate, hitRate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, row)

    def insert_show_data(self, row):
        """Insert data into musical_showinfo table."""
        query = """
        INSERT INTO musical_showinfo (activity_id, location_id, time, onSales, price, endTime)
                VALUES (?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, row)

    def fetch_location(self) -> pd.DataFrame: 
        _query = """
        Select *
        from musical_location
        """
        df = pd.read_sql_query(_query, self.conn)
        return df
    def fetch_activity(self) -> pd.DataFrame:
        _query = """
        Select *
        from musical_activity
        """
        df = pd.read_sql_query(_query, self.conn)
        return df

    def fetch_showinfo(self) -> pd.DataFrame:
        _query = """
        Select *
        from musical_showinfo
        """
        df = pd.read_sql_query(_query, self.conn)
        return df

    def get_dict_UID_locNames(self):
        df_locs = self.fetch_location()
        df_activ = self.fetch_activity()
        dict_UID = dict(zip(df_activ['UID'],df_activ['id']))
        dict_locNames = dict(zip(df_locs['locationName'],df_locs['id']))
        return dict_UID, dict_locNames

    def drop_table(self, tablename):
        self.cursor.execute(f"DROP TABLE IF EXISTS {tablename}")


if __name__ == "__main__":
    db = MusicalDatabase('../Web/test.db')
    db.connect()

    db.create_activity_table()
    db.create_showinfo_table()
    db.create_location_table()

    db.close()


