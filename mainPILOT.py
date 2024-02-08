from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import os
import pandas as pd
import os
import openai
import docx
import pandas as pd
from datetime import datetime
import inflect
from dotenv import load_dotenv, find_dotenv
from ChatGPTpartPILOT import data_preparation
from appPILOT import flask_app

load_dotenv()
openai.api_key=os.getenv("OPENAI_KEY")

existing_customers_xls_path=r"C:\Users\vbanai\Documents\Programming\Dezsi porject\ChatFrontEnd\HU_Chat_HTML\output_file_expanded3.xlsx"
potential_customers_xls_path=r"C:\Users\vbanai\Documents\Programming\Dezsi porject\ChatFrontEnd\HU_Chat_HTML\tesztexcel_general.xlsx"
general_services_file_path = r"C:\Users\vbanai\Documents\Programming\Dezsi porject\ChatFrontEnd\HU_Chat_HTML\Vásárolható_autók_BIG.docx"

df_existing_customer_original, df_existing_customer, df_potential_customer, word_text=data_preparation(
    existing_customers_xls_path, potential_customers_xls_path, general_services_file_path)

app = flask_app(df_existing_customer_original, word_text)

if __name__ == "__main__":
    app.run(debug=True)

df_existing_customer_original, df_existing_customer_segments, df_potential_customer, word_text_segments = data_preparation(
    existing_customers_xls_path="your_existing_customers_path.xls",
    potential_customers_xls_path="your_potential_customers_path.xls",
    general_services_file_path="your_general_services_file.docx",
    segment_size=40000  # You can adjust the segment size as needed
)

app = flask_app(df_existing_customer_segments, word_text_segments)

if __name__ == '__main__':
    app.run(debug=True)
