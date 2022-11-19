#libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# predefined lists
veg_list = ["Beetroot","Cauliflower","Corn","Cucumber","Brinjal","Ginger","Lemon","Mango Raw","Onion Big","Potato","Sweet Potato","Tomato"]
fruits_list = ["Apple Shimla","Banana","Cantaloupe","Guava","Orange","Papaya","Pineapple","Pomegranate Kabul","Sapota","Watermelon"]
database = []
save_address = "../csv/price_list.csv"

#functions to webscrap to list
web_scrapper("https://vegetablemarketprice.com/market/chennai/today",
       veg_list,
       database,
       food_type = "vegetable")

web_scrapper("https://vegetablemarketprice.com/fruits/tamilNadu/today",
       fruits_list,
       database,
       food_type = "fruits")

#Converting list to Pandas DataFrame and saving the file as csv
df = pd.DataFrame(data = database)
df.columns = ["NAME","WHOLESALE PRICE", "RETAIL PRICE","SHOPPING MALL PRICE","QUANTITY","TYPE"]
df.to_csv(save_address, header = True, index=False)

def web_scrapper(web_link: str, target_row_name_list : list, database_arr : list, food_type : str = "NA" ):
    """Function which is used web_scrapper required content from web_link 
       Select appropriate rows from target_row_name_list
       and appends it to database_arr list with food_type (default value = NA) """
    
    request_reply = requests.get(web_link)
    soup = BeautifulSoup(request_reply.content, 'html5lib')
    table = soup.find('table', attrs={"class":"table"})
    table_rows = table.find_all("tr")
    for tr in table_rows:
        td = tr.find_all("td")
        row = [i.text for i in td]
        if (len(row)):
            if (row[1].split("(")[0].strip() in target_row_name_list):
                database_arr.append(format_rows(row,food_type = food_type))
    return 0

def name_formatter (message : str):
    """
    This function to used to format string to remove redudant information
    """
    return message.replace(message[message.rfind("(") : message.rfind(")") + 1], "").strip()

def price_list_extractor (message : str):
    """
    Extracts the price range from a message.
    :param message: The message to extract the price range from which is in the for "₹low_price - ₹high_price".
    :return: A list of two integers, the low and high price."""

    low , high = message[1:].split(" - ")
    return [int(low), int(high)]

def format_rows (row_content : list, food_type = "NA" ): 
    """
    This function takes in a list of strings and returns a list of strings.
    The input list is a row of data from the webscrapped file.
    The output list is a row of data that is formatted for the database.
    The function does the following:
        1. Formats the name of the fruit.
        2. Formats the wholesale price.
        3. Formats the retail price.
        4. Formats the shopping mall price.
        5. Formats the quantity. """
    name_of_foodtype = name_formatter(row_content[1])
    wholesale_price = int(row_content[2][1:])
    retail_price = price_list_extractor (row_content[3])
    shopping_mall_price = price_list_extractor (row_content[4])
    quantity = row_content[5]
    
    return [name_of_foodtype,
            wholesale_price,
            retail_price,
            shopping_mall_price,
            quantity,
            food_type]