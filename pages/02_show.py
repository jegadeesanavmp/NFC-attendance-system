import streamlit as st 
import pandas as pd 
from flask import Flask,request,jsonify 

app=Flask(__name__)
if st.button("Check now"):
    file=pd.read_csv("check_in_data.csv")
    st.write(file)
      
