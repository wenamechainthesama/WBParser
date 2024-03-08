from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class Parser:
    def __init__(
        self, subcategories_per_category_limit, products_per_subcategory_limit
    ):
        self.__driver = None
        self.__categories = []
        self.__categories_links = []
        self.__current_subcategories_links = []
        self.__current_products_links = []
        self.__data = []

        self.__subcategories_per_category_limit = subcategories_per_category_limit
        self.__products_per_subcategory_limit = products_per_subcategory_limit

    def open_website(self, url):
        options = Options()
        options.add_experimental_option("detach", True)
        self.__driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        self.__driver.get(url)
        sleep(0.5)

    def get_product_name(self):
        return (
            WebDriverWait(self.__driver, 5)
            .until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-page__title"))
            )
            .text
        )

    def get_product_prices(self):
        price = None
        price_class = "price-block__old-price"
        if len(self.__driver.find_elements(By.CLASS_NAME, price_class)) != 0:
            price = self.__driver.find_element(By.CLASS_NAME, price_class).text

        price_with_discount = None
        wallet_price_class = "price-block__wallet-price"
        if len(self.__driver.find_elements(By.CLASS_NAME, wallet_price_class)) != 0:
            price_with_discount = self.__driver.find_element(
                By.CLASS_NAME, wallet_price_class
            ).text
        else:
            another_wallet_price_class = "price-block__final-price"
            price_with_discount = self.__driver.find_element(
                By.CLASS_NAME, another_wallet_price_class
            ).text

        if price_with_discount is None:
            price_with_discount = price
        elif price is None:
            price = price_with_discount

        return (price, price_with_discount)

    def get_product_path(self):
        path_location = self.__driver.find_element(By.CLASS_NAME, "breadcrumbs__list")
        path_parts = path_location.find_elements(By.TAG_NAME, "span")
        path = " / ".join([part.text for part in path_parts])
        return path

    def get_product_images(self):
        images_location = self.__driver.find_element(
            By.CLASS_NAME, "custom-slider__list"
        )
        images = [
            img.get_attribute("href")
            for img in images_location.find_elements(By.TAG_NAME, "a")
        ]
        return images

    def get_product_description(self):
        description_button = self.__driver.find_element(
            By.CLASS_NAME, "product-page__btn-detail"
        )
        ActionChains(self.__driver).click(description_button).perform()
        sleep(0.5)
        description = self.__driver.find_element(By.CLASS_NAME, "option__text").text
        return description

    def get_product_characteristics(self):
        params_keys = [
            key.text for key in self.__driver.find_elements(By.TAG_NAME, "th")
        ]
        params_values = [
            value.text for value in self.__driver.find_elements(By.TAG_NAME, "td")
        ]
        return dict(zip(params_keys, params_values))

    def save_product_data(self):
        # Get all necessary product data
        name = self.get_product_name()
        price, price_with_discount = self.get_product_prices()
        path = self.get_product_path()
        images = self.get_product_images()
        description = self.get_product_description()
        params = self.get_product_characteristics()

        # Save data
        self.__data.append(
            {
                "name": name,
                "price": price,
                "price_with_discount": price_with_discount,
                "path": path,
                "images": images,
                "description": description,
                "params": params,
            }
        )

        print(
            {
                "name": name,
                "price": price,
                "price_with_discount": price_with_discount,
                "path": path,
                "images": images,
                "description": description,
                "params": params,
            }
        )

    def get_products_links(self):
        products = self.__driver.find_element(
            By.CLASS_NAME, "product-card-list"
        ).find_elements(By.CLASS_NAME, "product-card")[
            : self.__products_per_subcategory_limit
        ]

        products_links = []
        for product in products:
            product_link = product.find_element(By.TAG_NAME, "a").get_attribute("href")
            products_links.append(product_link)

        self.__current_products_links = products_links

    def get_subcategories_links(self):
        subcategories_location = self.__driver.find_element(
            By.CLASS_NAME, "menu-catalog__list-2"
        )
        self.__current_subcategories_links = list(
            map(
                lambda element: element.get_attribute("href"),
                list(
                    filter(
                        lambda subcategory: not subcategory.text.startswith("Подарки"),
                        subcategories_location.find_elements(By.TAG_NAME, "a")[
                            : self.__subcategories_per_category_limit
                        ],
                    )
                ),
            )
        )

    def parse_subcategories(self, category_link):
        restricted_categories_links = [
            "https://www.wildberries.ru/catalog/zdorove",
            "https://www.wildberries.ru/catalog/aksessuary/tovary-dlya-vzroslyh",
        ]
        self.get_subcategories_links()
        for subcategory_link in self.__current_subcategories_links:
            self.__driver.get(subcategory_link)
            sleep(0.25)
            if not self.__driver.find_elements(By.CLASS_NAME, "product-card-list"):
                continue
            self.get_products_links()
            for product_index, product_link in enumerate(self.__current_products_links):
                self.__driver.get(product_link)
                sleep(0.25)
                if product_index == 0 and category_link in restricted_categories_links:
                    self.confirm_age()
                self.save_product_data()

    def get_product_categories(self):
        navigation_button = self.__driver.find_element(
            By.CLASS_NAME, "nav-element__burger"
        )
        ActionChains(self.__driver).click(navigation_button).perform()
        sleep(0.5)

        categories_location = self.__driver.find_element(
            By.CLASS_NAME, "menu-burger__main-list"
        )
        self.__categories = categories_location.find_elements(
            By.CLASS_NAME, "menu-burger__main-list-item--subcategory"
        )[7:]

    def get_categories_links(self):
        categories_links = []
        for category in self.__categories:
            category_link = category.find_element(By.TAG_NAME, "a").get_attribute(
                "href"
            )
            if (
                not category_link.startswith("https://www.wildberries.ru/catalog")
                or category_link == "https://www.wildberries.ru/catalog/sport"
            ):
                continue
            categories_links.append(category_link)
        self.__categories_links = categories_links

    def confirm_age(self):
        if len(self.__driver.find_elements(By.CLASS_NAME, "popup-confirm-age")) != 0:
            popup_window = self.__driver.find_element(
                By.CLASS_NAME, "popup-confirm-age"
            )
            ActionChains(self.__driver).click(
                popup_window.find_element(By.TAG_NAME, "button")
            ).perform()
            sleep(0.25)

    def parse_categories(self):
        self.get_product_categories()
        self.get_categories_links()
        for category_link in self.__categories_links:
            self.__driver.get(category_link)
            sleep(0.25)
            self.parse_subcategories(category_link)

        self.__driver.quit()

    def get_data(self):
        return self.__data


def main():
    parser = Parser(3, 3)
    parser.open_website("https://www.wildberries.ru/")
    parser.parse_categories()
    data = parser.get_data()
    print(data)
    print(len(data))


if __name__ == "__main__":
    main()

print("telephon")
print(" See remote debugger for selenium")
