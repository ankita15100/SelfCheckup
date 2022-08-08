#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import pandas as pd
import numpy as np
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from tensorflow.keras.models import  model_from_json
import pickle
#import SessionState

# In[4]:


st.set_page_config(layout="wide")


# In[5]:

col_list=['Arthritis',
 'Bronchial Asthma',
 'Common Cold',
 'Covid',
 'Diabetes ',
 'Heart attack',
 'Hypertension',
 'Jaundice',
 'Migraine',
 'Osteoarthristis',
 'Pneumonia',
 'Stroke',
 'Tuberculosis',
 'Typhoid']


df=pd.read_excel("C:/Users/aashpila/Documents/Symptoms.xlsx")
df_prov=pd.read_excel("C:/Users/aashpila/Documents/provlist.xlsx")
df_diag_test=pd.read_excel("C:/Users/aashpila/Documents/diag_test.xlsx")
symp=list(set(df.columns).difference(['prognosis','DiagCode']))
dis=list(df['prognosis'].unique())
#print(symp)
#print(dis)
# In[11]:


def existing_disease():
    
    st.header('Have you been diagnosed with any other health conditions?')
    dis.append("No disease")
    hobbies = st.multiselect("Diseases: ",dis)
    return hobbies

def symptoms():
    st.header("What symptoms are you experiencing today?: ")
    hobbies_1 = st.multiselect("",symp)
 
    # write the selected options
    st.write("You selected", len(hobbies_1), 'symptoms')
    return hobbies_1

def age_func():
    age = st.text_input("How old are you?: ")
 
##    # write the selected options
##    st.write("You selected", len(hobbies), 'symptoms')
    return age

#def interactive_scatterplot():
def gender_func():
    
    gender = st.radio("Select Gender: ", ('Male', 'Female'))
    return gender

def zipcode_func():
    
    zipcode=st.text_input("Enter your Zipcode: ")
    return zipcode
    


##def func():
##    st.header("Your selected values")
##    st.write(dis,symp)
# In[12]:

def func():
    #options='Submit'
    if(len(st.session_state.keys())!=4):
        st.header("Please enter the details ")
        st.write(set(['Existing Disease','Symptoms','Age','Gender']).difference(set(st.session_state.keys())))
    else:
        st.header("Below are the most likely conditions based on the symptoms and information you entered.")
        json_file = open('C:/Users/aashpila/Documents/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights("C:/Users/aashpila/Documents/model.h5") 
        loaded_model.compile('adam', loss='categorical_crossentropy', metrics=['accuracy'])

        #score = loaded_model.evaluate(X_test_1, y_test_enc_1, verbose=0)
        with open("C:/Users/aashpila/Documents/input_cols.pickle", "rb") as file:
            loaded_dict = pickle.load(file)

        test_df=pd.DataFrame(columns=loaded_dict)
    ##    for i in st.session_state['dis']:
    ##        test_df.loc[0,i]=1


        for i in st.session_state['Symptoms']:
            test_df.loc[0,i]=1
        if st.session_state['Gender']=='Female':
            test_df.loc[0,'dmg_pat_sex_F']=1
        elif st.session_state['Gender']=='Male':
            test_df.loc[0,'dmg_pat_sex_M']=1
        if st.session_state['Age']!='':
            test_df.loc[0,'age']=int(st.session_state['age'])

        test_df.fillna(0,inplace=True)
        prediction_1= loaded_model.predict(test_df.iloc[0:1])
        prediction_1_df=pd.DataFrame(prediction_1,columns=col_list)
        prediction_1_df_out=prediction_1_df.agg(lambda s:pd.Series([*s.nlargest(3).index],['d1','d2','d3']),axis='columns')

        typ = st.radio("", ('LIKELIHOOD', 'SPECIALITY', 'SUGGESTED CLINICAL TESTS'))
        if(typ=='LIKELIHOOD'):
            st.write("Diseases",prediction_1_df_out)
        if(typ=='SPECIALITY'):
            for i in prediction_1_df_out.iloc[0:1].values[0]:
                st.write("Disease: ",i)
                st.write("Specialists : ",str(df_prov[df_prov['prognosis']==i]['Specialist'].values))
        if(typ=='SUGGESTED CLINICAL TESTS'):
            for i in prediction_1_df_out.iloc[0:1].values[0]:
                #print(df_diag_test[df_diag_test['Diseases']==i])
                st.write("Suggested Clinical Tests for: "+str(i)+" ",str([x.strip() for x in df_diag_test[df_diag_test['Diseases']==i]['Tests'].values]))

                            
##    except:
##        st.header("Please enter the complete details ")


#Sidebar navigation
st.sidebar.title('Member Details')
options = st.sidebar.radio('Please Enter Below Details:', ['Existing Disease', 'Symptoms', 'Age','Gender','Submit'])
##                                                                'Scatter Plots','Line Plot','Histogram Plot','Bar Plot', 'Pie Chart'])
#st.sidebar.button("Submit", on_click=func)


with open("C:/Users/aashpila/Documents/input_cols.pickle", "rb") as file:
        loaded_dict = pickle.load(file)

# In[13]:
dis_1=[]
symp_1=[]
test_df=pd.DataFrame(columns=loaded_dict)


    
# Navigation options
if options == 'Existing Disease':
    hobbies=existing_disease()
    dis_1.extend(hobbies)
    st.session_state['Existing Disease']=dis_1
    
elif options == 'Symptoms':
    print(dis_1)
    symptm=symptoms()
    symp_1.extend(symptm)
    st.session_state['Symptoms']=symp_1

elif options == 'Age':
    age=age_func()
    st.session_state['Age']=age
elif options == 'Gender':
    gender=gender_func()
    st.session_state['Gender']=gender
    
##elif options == 'Zipcode':
##    zipcode=zipcode_func()
##    st.session_state['Zipcode']=zipcode

elif options=='Submit':
    func()
    

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




