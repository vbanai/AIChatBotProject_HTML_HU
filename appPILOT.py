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
from ChatGPTpartPILOT import get_Chat_response
import re



def flask_app(df_existing_customer_BIG, word_text):

  app=Flask(__name__)

  

  df_existing_customer=""
  context = [
  
    {'role': 'system', 'content': f"""
    You are telefonoperator in AutoDé Kft and you speak in Hungarian language and you are answering incoming questions in Hungarian. \
    If the user has a question regarding the ongoing order, ask for the client number.\
    If the user has general questions, there's no need to ask for the client number. \            
    User: Can you give me the client number? Assistant: Please provide your client number.\
    If the client number is provided, respond to the user based on the information in the table:{df_existing_customer} \
    I will provide an example to guide you on using customer numbers in your response. \
    Check if you can find the provided customer number in the 'Customer Number' column of the table.\
    
    Please note: Customer numbers usually have six digits (e.g., 975886, 367679, 659259). However, it can happen that '112112' is not in the table{df_existing_customer}, \
    even though it might be mentioned. In this case do not consider '112112' as a valid customer number from the table.\
    
    If you find the provided customer number, ask the user: "What details do you need regarding the existing order?" \
    Retrieve and provide the requested details of the corresponding order. If not, inform the user accordingly.\
    Without the client number, initiate conversation with the user using only the information from the document:{word_text}. \
    Ensure that your responses are solely based on the content of the documents mentioned (df_existing_customer and word_text). \
    Do not reference or consider information from any other external documents or sources. \
    Respond briefly, and your response should be in one installment, not multiple parts. Always ask if you can help with anything else.

    
    
  """}

  
  ]


  @app.route("/")
  @app.route('/home')
  def index():
    return render_template('index.html')


  @app.route("/messengerchat")
  def messengerchat():
    return render_template('messengerchat.html')


  @app.route("/get", methods=["GET", "POST"])
  def chat():
    global df_existing_customer
    msg=request.form["msg"]
    input=msg
    context.append({'role':'user', 'content':f"{input}"})
    client_number=extract_client_number(input)
    if client_number:
      df_existing_customer=retrieve_client_details(client_number)
      context.append(
        {'role': 'system', 'content': f"If the client number is provided, respond to the user based on the information in the table:{df_existing_customer} "}
      )
    response=get_Chat_response(context)
    context.append({'role':'assistant', 'content':f"{response}"})
    return response





  def extract_client_number(user_input):
    # Using a regular expression to extract a client number from the user input
    match = re.search(r'\b\d{6}\b', user_input)
    if match:
      return match.group()
    else:
      return None
    
  def retrieve_client_details(client_number):
    # Assuming df_existing_customer is a pandas DataFrame
    client_row = df_existing_customer_BIG[df_existing_customer_BIG['Azonosító'].astype(str) == client_number]
    return client_row.to_string(index=False)

    # if not client_row.empty:
    #   # Retrieve details from the DataFrame
    #   name = client_row['Ügyfél']
    #   car = client_row['Megrendelt autó']
    #   status = client_row['Státusz']

    #   # Construct a string with the details
    #   details_str = f"Név: {name}, Megrendelt autó márkája: {car}, A megrendelés státusza: {status}"
    #   return details_str
    # else:
    #   return "A szám nem megfelelő"


  #  # Process user's query
  # user_input = context[-1]['content']  # Extract user's input from the last turn
  # client_number = extract_client_number(user_input)

  # # Check if client number exists in the database
  # if client_number in df_existing_customer['Client Number'].values:
  #     # Retrieve details from the corresponding row
  #     client_details = retrieve_client_details(client_number)
  #     assistant_response = f"Here is the information for client number {client_number}: {client_details}"
  # else:
  #     assistant_response = f"Client number {client_number} not found in the database."

  # # Update context for future interactions
  # context.append({'role': 'assistant', 'content': assistant_response})


  return app



