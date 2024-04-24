"""
This module contains code for your Flask application.

It interacts with a MySQL database and serves data in both HTML and JSON formats.
"""
import json
from decimal import Decimal
from datetime import date
import pandas as pd
import mysql.connector
from flask import Flask, render_template

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for special object serialization."""

    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

class DatabaseConfig:
    """Database configuration object."""
    def __init__(self, host, port, database, user, password, auth_plugin):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.auth_plugin = auth_plugin

# Database connection details
db_config = DatabaseConfig(
    host='db',
    port=3306,
    database='db',
    user='root',
    password='root',
    auth_plugin='mysql_native_password'
)

# Установяване на връзка с базата данни
def establish_database_connection() -> mysql.connector.connection.MySQLConnection:
    """Establishes a connection to the MySQL database.

    Returns:
        MySQLConnection: A connection object representing the database connection.
    """
    try:
        connection = mysql.connector.connect(
            host=db_config.host,
            port=db_config.port,
            database=db_config.database,
            user=db_config.user,
            password=db_config.password,
            auth_plugin=db_config.auth_plugin
        )
        return connection
    except mysql.connector.Error as e:
        return e

# обработка на грешки при fail
class DatabaseConnectionError(Exception):
    """Custom exception for database connection errors."""

@app.errorhandler(DatabaseConnectionError)
def handle_database_connection_error():
    """Handle database connection error.

    Returns:
        str: Error message indicating failure to connect to the database.
    """
    return "Failed to connect to the database."

@app.route("/")
def index() -> any:
    """Render the index.html template.

    Returns:
        any: The response returned by the render_template function.
    """
    return render_template("index.html")

@app.route("/table/<table_name>", methods=["GET"])
def get_table_data(table_name: str) -> str:
    """
    Retrieve data from the specified table in the database and return it as an 
    HTML table and JSON data.

    Args:
        table_name (str): The name of the table to retrieve data from.

    Returns:
        str: An HTML representation of the data in the table and JSON data.
    """
    connection = None
    cursor = None
    try:
        connection = establish_database_connection()
        cursor = connection.cursor()
        query = f"SELECT * FROM {table_name.capitalize()}"
        cursor.execute(query)
        data = cursor.fetchall()

        if not data:
            return f"No data found in the {table_name} table."

        df = pd.DataFrame(data, columns=[col[0] for col in cursor.description])

        # Convert Decimal objects to float
        df = df.applymap(lambda x: float(x) if isinstance(x, Decimal) else x)

        # Print column names
        print("Column names:", df.columns)

        # Generate HTML table
        html_table = df.to_html()

        # Generate JSON data with new lines and spacing
        json_data = df.to_json(orient='records', date_format='iso', indent=4)

        # Combine HTML table and JSON data in response
        response = f"<h2>HTML Table:</h2>{html_table}<br><br>"
        response += f"<h2>JSON Data:</h2><pre>{json_data}</pre>"

        return response
    except mysql.connector.Error as e:
        return f"Failed to execute query.\nError: {e}"
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

@app.route("/join_tables", methods=["GET"])
def join_tables() -> str:
    """Join the Hotels and Rooms tables, fetch the joined data,
    and return HTML and JSON representations.

    Returns:
        str: HTML and JSON representations of the joined data.
    """
    try:
        connection = establish_database_connection()
        hotels_df = pd.read_sql(
            "SELECT Hotels.*, Rooms.RoomNumber, Rooms.Type, Rooms.Price "
            "FROM Hotels "
            "JOIN Rooms ON Hotels.HotelID = Rooms.HotelID",
            connection
        )

        if hotels_df.empty:
            return "No data found after joining tables."

        # Generate HTML table
        html_table = hotels_df.to_html()

        # Generate JSON data with new lines and spacing
        json_data = json.dumps(hotels_df.to_dict(orient='records'), indent=4)

        # Combine HTML table and JSON data in response
        response = f"<h2>HTML Table:</h2>{html_table}<br><br>"
        response += f"<h2>JSON Data:</h2><pre>{json_data}</pre>"

        return response
    except mysql.connector.Error as e:
        return f"Failed to execute query.\nError: {e}"
    finally:
        connection.close()

@app.route("/rate/", methods=["GET"])
def rate_hotels() -> str:
    """Retrieve hotels sorted by rating and return HTML and JSON representations.

    Returns:
        str: HTML and JSON representations of hotels sorted by rating.
    """
    connection = None
    cursor = None
    try:
        connection = establish_database_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM Hotels ORDER BY Rating DESC"
        cursor.execute(query)
        data = cursor.fetchall()

        if not data:
            return "No hotels found in the database."

        df = pd.DataFrame(data, columns=[col[0] for col in cursor.description])

        # Convert Decimal objects to float
        df = df.applymap(lambda x: float(x) if isinstance(x, Decimal) else x)

        # Generate HTML table
        html_table = df.to_html()

        # Generate JSON data with new lines and spacing
        json_data = df.to_json(orient='records', date_format='iso', indent=4)

        # Combine HTML table and JSON data in response
        response = f"<h2>Hotels Sorted by Rating (Best to Worst):</h2>{html_table}<br><br>"
        response += f"<h2>JSON Data:</h2><pre>{json_data}</pre>"

        return response
    except mysql.connector.Error as e:
        return f"Failed to execute query.\nError: {e}"
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

@app.route("/filter/hotels_by_city/<city>", methods=["GET"])
def filter_hotels_by_city(city: str) -> str:
    """Filter hotels by city and return HTML and JSON representations.

    Args:
        city (str): The city name to filter hotels by.

    Returns:
        str: HTML and JSON representations of hotels filtered by city.
    """
    try:
        connection = establish_database_connection()
        hotels_df = pd.read_sql(f"SELECT * FROM Hotels WHERE City = '{city}'", connection)

        if hotels_df.empty:
            return f"No hotels found in the city '{city.capitalize()}'."

        # Generate HTML table
        html_table = hotels_df.to_html()

        # Generate JSON data with new lines and spacing
        json_data = json.dumps(hotels_df.to_dict(orient='records'), indent=4)

        # Combine HTML table and JSON data in response
        response = f"<h2>HTML Table:</h2>{html_table}<br><br>"
        response += f"<h2>JSON Data:</h2><pre>{json_data}</pre>"

        return response
    except mysql.connector.Error as e:
        return f"Failed to execute query.\nError: {e}"
    finally:
        connection.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
    print("Flask application running at http://127.0.0.1:5000/")
