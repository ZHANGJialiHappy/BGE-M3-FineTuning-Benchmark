import psycopg2
from dotenv import load_dotenv
import os
import csv
from urllib.parse import quote
import ast
# from invoke_claude import filter_data


# Load environment variables from .env file
load_dotenv()

driver = os.getenv("DRIVER")
host = os.getenv("HOST")
port = os.getenv("PORT")
database = os.getenv("DATABASE")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

connection_params = {
    'dbname': database,
    'user': username,
    'password': password,
    'host': host,
    'port': port,
}


def execute_query(query, single_item = False):
    response = None
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        cursor.execute(query)
    
        if single_item:
            response = cursor.fetchone()
        else:
            response = cursor.fetchall()
    
    except Exception as e:
        print(f"Error connecting to the PostgreSQL database: {e}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return response

def get_wrong_answer_statistics(wrong_answer_path):
    uuid_score=0
    alarm_score=0
    with open(wrong_answer_path, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            answers=ast.literal_eval(row["answers"])
            encoded_answers = [quote(answer) for answer in answers]

            if any(check_if_answer_in_uuid(encoded_answer) for encoded_answer in encoded_answers) :
                uuid_score+=1

            if any(check_if_answer_in_alarm(encoded_answer) for encoded_answer in encoded_answers) :
                alarm_score+=1

    print(f"UUID Score: {uuid_score}")
    print(f"Alarm Score: {alarm_score}")


def check_if_answer_in_uuid(answer:str) -> str:
    query = f"""
    SELECT source_uri
    FROM v9__chatbot_documents
    WHERE source_uri like '%58548175-ccef-4d6a-987c-f597b7d4d225%{answer}%' 
    """
    response = execute_query(query)
    return len(response) > 0

def check_if_answer_in_alarm(answer:str) -> str:
    query = f"""
    SELECT source_uri
    FROM v9__chatbot_documents
    WHERE source_uri like '%me_c_mk2%{answer}%' 
    """
    response = execute_query(query)
    return len(response) > 0

if __name__ == "__main__":
    wrong_answer_path="1st_finetune/finetune_top_5_dense_incorrect_questions.csv"
    get_wrong_answer_statistics(wrong_answer_path)