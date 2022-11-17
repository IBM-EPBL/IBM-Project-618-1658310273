import csv

def index_to_information (index_of_pred_class : int,files_name_list: list) -> list:
    '''
    This function takes the value of predicted class index from CNN model file
    And returns information about that file in files_name_list (csv)'s as Dictionary '''
    
    #initialize empty dictonary
    info_dict = {}
    
    # index to food name
    food_name_of_pred_class = csv_extractor (files_name_list[0], str(index_of_pred_class), row_number=1)["COMMON TERM"]
    print(food_name_of_pred_class)
    
    # food name to extract information in list of other files
    for file_name in files_name_list[1:]:
        info_dict.update(csv_extractor (file_name, food_name_of_pred_class))
    return info_dict



def csv_extractor (csv_file_name : str, food_name : int, row_number :int = 0):
    '''
    This function takes in a csv file name, a food name, and a row number.
    The row number is optional and defaults to 0.
    The function returns a dictionary with the food name as the key and the
    corresponding row as the value.
    '''

    with open(csv_file_name, 'r') as file:
        reader = csv.reader(file)
        head = next(reader)
        for row in reader:
            if row[row_number].lower() == food_name.lower():
                return dict(zip(head,row))
        else:
            return {}

