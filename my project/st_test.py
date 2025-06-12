import streamlit as st
import pandas as pd


st.title('융복합 데이터셋 구축')

main_page = st.Page("main_page.py", title='AI 서치', icon='🖥️')
page_2 = st.Page('page_2.py', title= '감성표현', icon='👍')
page_3 = st.Page('page_3.py', title= '정책이슈_국정과제', icon='🚩')
page_4 = st.Page('page_4.py', title= '정책이슈_법률이슈', icon='⚖️')

pg = st.navigation ([main_page, page_2, page_3, page_4])

pg.run()