from db_exporter import create_xlsx_from_db
from statistician import calculate_statistics
from web_parser import Parser
from db import session
from loguru import logger


def main():
    logger.add("debug.log", format="{time} {level} {message}", level="INFO")
    parser = Parser(3, 4, session)
    parser.open_website("https://www.wildberries.ru/")
    parser.parse_categories()
    create_xlsx_from_db()
    calculate_statistics()


if __name__ == "__main__":
    main()
