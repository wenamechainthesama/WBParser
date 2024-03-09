from pandas import read_sql
from sqlite3 import connect
from os.path import dirname


def create_xlsx_from_db():
    connection = connect(f"{dirname(__file__)}/products.db")
    query = "SELECT * FROM products"
    df = read_sql(query, connection)
    df.to_excel("products.xlsx")
