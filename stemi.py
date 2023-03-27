import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import cv2
#from  PIL import ImageChops
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
import io 

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode
from PIL import Image

#st.set_page_config(page_title="Sharone's Streamlit App Gallery", page_icon="", layout="wide")

# sysmenu = '''
# <style>
# #MainMenu {visibility:hidden;}
# footer {visibility:hidden;}
# '''
#st.markdown(sysmenu,unsafe_allow_html=True)

#Add a logo (optional) in the sidebar
logo = Image.open(r'/media/tuongvi/Data/stemi/stemivn.png')
profile = Image.open(r'/media/tuongvi/Data/stemi/stemivn.png')

with st.sidebar:
    choose = option_menu("App Gallery", ["About", "Thông tin chuyên gia", "Danh sách chuyên gia", "Contact"],
                         icons=['house', 'kanban', 'book','person lines fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )


logo = Image.open(r'/media/tuongvi/Data/stemi/stemivn.png')
profile = Image.open(r'/media/tuongvi/Data/stemi/stemivn.png')
if choose == "About":
#Add the cover image for the cover page. Used a little trick to center the image
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">About the STEMI Viet Nam</p>', unsafe_allow_html=True)
        
    with col2:               # To display brand logo
        
        st.image(logo, width=130 )
    st.write("Truyền cảm hứng học tập và nâng cao năng lực về giáo dục STEM cho học sinh và giáo viên trên khắp Việt Nam, góp phần xây dựng một nền giáo dục tiên tiến, hiện đại và phát triển bền vững.")    
    st.image(profile, width=700 )


elif choose == "Thông tin chuyên gia":
#Add a file uploader to allow users to upload their project plan file
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Thông tin chuyên gia</p>', unsafe_allow_html=True)

    df=pd.read_excel(r'/media/tuongvi/Data/stemi/stemi.xlsx')
    # df_head=df.head()
    # st.write(df)
    
    # select the columns you want the users to see
    gb = GridOptionsBuilder.from_dataframe(df[["Họ và tên", "Mã số chuyên gia"]])
    # configure selection
    gb.configure_selection(selection_mode="single", use_checkbox=True)
    gb.configure_side_bar()
    gridOptions = gb.build()

    data = AgGrid(df,
                  gridOptions=gridOptions,
                  enable_enterprise_modules=True,
                  allow_unsafe_jscode=True,
                  update_mode=GridUpdateMode.SELECTION_CHANGED,
                  columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)

    selected_rows = data["selected_rows"]

    if len(selected_rows) != 0:

        image = Image.open('person.png')

        st.image(image, caption='Sunrise by the mountains')
        
        col1, col2, col3, col4 = st.columns(4)
        

        with col1:
            st.markdown("##### Họ và tên")
            st.markdown(f":orange[{selected_rows[0]['Họ và tên']}]")
        with col2:
            st.markdown("##### Mã số chuyên gia")
            st.markdown(f":orange[{selected_rows[0]['Mã số chuyên gia']}]")
        with col3:
            st.markdown("##### Lĩnh vực")
            st.markdown(f":orange[{selected_rows[0]['Lĩnh vực']}]")
        with col4:
            st.markdown("##### Vị trí hiện tại")
            st.markdown(f":orange[{selected_rows[0]['Vị trí hiện tại']}]")
        

elif choose == "Danh sách chuyên gia":
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Danh sách chuyên gia</p>', unsafe_allow_html=True)

    #Allow users to check the results of the first code snippet by clicking the 'Check Results' button
    df=pd.read_excel(r'/media/tuongvi/Data/stemi/stemi.xlsx')

    def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        modify = st.checkbox("Add filters")

        if not modify:
            return df

        df = df.copy()

        # Try to convert datetimes into a standard format (datetime, no timezone)
        for col in df.columns:
            if is_object_dtype(df[col]):
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception:
                    pass

            if is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.tz_localize(None)

        modification_container = st.container()

        with modification_container:
            to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
            for column in to_filter_columns:
                left, right = st.columns((1, 20))
                left.write("↳")
                # Treat columns with < 10 unique values as categorical
                if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                    user_cat_input = right.multiselect(
                        f"Values for {column}",
                        df[column].unique(),
                        default=list(df[column].unique()),
                    )
                    df = df[df[column].isin(user_cat_input)]
                elif is_numeric_dtype(df[column]):
                    _min = float(df[column].min())
                    _max = float(df[column].max())
                    step = (_max - _min) / 100
                    user_num_input = right.slider(
                        f"Values for {column}",
                        _min,
                        _max,
                        (_min, _max),
                        step=step,
                    )
                    df = df[df[column].between(*user_num_input)]
                elif is_datetime64_any_dtype(df[column]):
                    user_date_input = right.date_input(
                        f"Values for {column}",
                        value=(
                            df[column].min(),
                            df[column].max(),
                        ),
                    )
                    if len(user_date_input) == 2:
                        user_date_input = tuple(map(pd.to_datetime, user_date_input))
                        start_date, end_date = user_date_input
                        df = df.loc[df[column].between(start_date, end_date)]
                else:
                    user_text_input = right.text_input(
                        f"Substring or regex in {column}",
                    )
                    if user_text_input:
                        df = df[df[column].str.contains(user_text_input)]

        return df
    
    st.dataframe(filter_dataframe(df))


elif choose == "Contact":
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Contact Form</p>', unsafe_allow_html=True)
    with st.form(key='columns_in_form2',clear_on_submit=True): #set clear_on_submit=True so that the form will be reset/cleared once it's submitted
        #st.write('Please help us improve!')
        Name=st.text_input(label='Please Enter Your Name') #Collect user feedback
        Email=st.text_input(label='Please Enter Your Email') #Collect user feedback
        Message=st.text_input(label='Please Enter Your Message') #Collect user feedback
        submitted = st.form_submit_button('Submit')
        if submitted:
            st.write('Thanks for your contacting us. We will respond to your questions or inquiries as soon as possible!')