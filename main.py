from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

URL = "https://www.wildberries.ru/"

# Open wildberries website
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)
driver.get(URL)

sleep(1)

navigation_button = driver.find_element(By.CLASS_NAME, "nav-element__burger")
ActionChains(driver).click(navigation_button).perform()

sleep(1)

categories_location = driver.find_element(By.CLASS_NAME, "menu-burger__main-list")
categories = categories_location.find_elements(
    By.CLASS_NAME, "menu-burger__main-list-item--subcategory"
)

categories_links = []

# Loop for each category and find link to its page
for category in categories:
    category_link = category.find_element(By.TAG_NAME, "a").get_attribute("href")
    if not category_link.startswith("https://www.wildberries.ru/catalog"):
        continue
    categories_links.append(category_link)

print("telephon")
print(" See remote debugger for selenium")

data = []

for link in categories_links:
    # Go to current category page
    driver.get(link)
    sleep(0.25)
    subcategories_location = driver.find_element(By.CLASS_NAME, "menu-catalog__list-2")
    subcategories_links = list(
        map(
            lambda element: element.get_attribute("href"),
            list(
                filter(
                    lambda subcategory: not subcategory.text.startswith("Подарки"),
                    subcategories_location.find_elements(By.TAG_NAME, "a"),
                )
            ),
        )
    )
    # Go to every subcategory
    for sublink in subcategories_links:
        driver.get(sublink)
        sleep(0.5)
        if not driver.find_elements(By.CLASS_NAME, "product-card-list"):
            continue
        products = driver.find_element(
            By.CLASS_NAME, "product-card-list"
        ).find_elements(By.CLASS_NAME, "product-card")

        products_links = []

        # Loop for each product and get link to its page
        for product in products:
            product_link = product.find_element(By.TAG_NAME, "a").get_attribute("href")
            products_links.append(product_link)

        for product_link in products_links:
            # Go to product page
            driver.get(product_link)

            # Get all necessary product date such as name, price, path, ...
            name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "product-page__title"))).text
            price = None
            if len(driver.find_elements(By.CLASS_NAME, "price-block__old-price")) != 0:
                price = driver.find_element(
                    By.CLASS_NAME, "price-block__old-price"
                ).text
            price_with_discount = None
            if (
                len(driver.find_elements(By.CLASS_NAME, "price-block__wallet-price"))
                != 0
            ):
                price_with_discount = driver.find_element(
                    By.CLASS_NAME, "price-block__wallet-price"
                ).text
            else:
                price_with_discount = driver.find_element(
                    By.CLASS_NAME, "price-block__final-price"
                ).text
            if price_with_discount is None:
                price_with_discount = price
            elif price is None:
                price = price_with_discount
            path_location = driver.find_element(By.CLASS_NAME, "breadcrumbs__list")
            path_parts = path_location.find_elements(By.TAG_NAME, "span")
            path = " / ".join([part.text for part in path_parts])
            images_location = driver.find_element(By.CLASS_NAME, "custom-slider__list")
            images = [
                img.get_attribute("href")
                for img in images_location.find_elements(By.TAG_NAME, "a")
            ]
            description_button = driver.find_element(
                By.CLASS_NAME, "product-page__btn-detail"
            )
            ActionChains(driver).click(description_button).perform()
            sleep(0.25)
            description = driver.find_element(By.CLASS_NAME, "option__text").text
            params_keys = [key.text for key in driver.find_elements(By.TAG_NAME, "th")]
            params_values = [
                value.text for value in driver.find_elements(By.TAG_NAME, "td")
            ]
            params = dict(zip(params_keys, params_values))
            data.append(
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

driver.close()
