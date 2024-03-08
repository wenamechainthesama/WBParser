from web_parser import Parser
from db import session


def main():
    parser = Parser(3, 4, session)
    parser.open_website("https://www.wildberries.ru/")
    parser.parse_categories()


if __name__ == "__main__":
    main()

print("telephon")

"""
git dev branch
"""
