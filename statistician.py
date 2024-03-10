from pandas import read_excel
from os.path import dirname
from statistics import median, mean
from loguru import logger


def calculate_statistics():
    df = read_excel(rf"{dirname(__file__)}/products.xlsx")
    price_without_discount = df["price"].mean()
    discounted_price = df["discounted_price"].mean()
    images_quantity = median([len(images.split(", ")) for images in df["images"]])
    description_lenth = mean(
        [len(str(description)) for description in df["description"]]
    )
    with open("products_stats.txt", "a") as file:
        file.writelines(
            [
                f"Average price without discount: {price_without_discount}\n",
                f"Average price with dicount: {discounted_price}\n",
                f"Average images' amount: {images_quantity}\n",
                f"Average description length: {description_lenth}\n",
            ]
        )
    logger.success("Statistics is done")