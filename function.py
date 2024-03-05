import pandas as pd
from transformers import pipeline
from google.cloud import bigquery


def get_food (image):
    model = pipeline("image-classification", model="nateraw/food")
    predict = model.predict(image)
    food_result = predict[0]['label'].upper()
    return food_result

def get_carbs (food_result):

    query = f"""
        SELECT Data_Carbohydrate, Data_Household_Weights_1st_Household_Weight,Data_Household_Weights_1st_Household_Weight_Description
        FROM `{GCP_PROJECT}.nutrition_table.main`
        WHERE Category = '{food_result}'
    """
    client = bigquery.Client(project=GCP_PROJECT)
    query_job = client.query(query)
    query_result = query_job.result()
    print(query_result)
    df = query_result.to_dataframe()
    carbs_result = df['Data_Carbohydrate'].mean()
    return carbs_result

def get_insuline (carbs_result):
    insuline_result = round(carbs_result/15)
    return insuline_result

def get_full_result (image):
    food_result = get_food(image)
    carbs_result = get_carbs(food_result)
    insuline_result = get_insuline(carbs_result)
    return food_result,carbs_result,insuline_result