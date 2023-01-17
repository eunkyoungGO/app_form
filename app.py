
import streamlit as st
import datetime
import sqlite3
import pandas as pd
import os.path
from st_aggrid import GridOptionsBuilder, \
    AgGrid, GridUpdateMode, DataReturnMode

file_path = os.path.dirname(__file__)
db_file = os.path.join(file_path, 'users.db')

# 데이터베이스 연결
con = sqlite3.connect(db_file)
cur = con.cursor()

menu=st.sidebar.selectbox('메뉴',['회원가입','회원목록','로그인'])

if menu == '회원가입':

    st.subheader('회원가입 폼')

    with st.form('my_form', clear_on_submit=True):
        st.info('다음 양식을 모두 작성한 다음 제출합니다.')
        uid = st.text_input('아이디', max_chars=12)
        uname = st.text_input('성명', max_chars=8)
        upw = st.text_input('비밀번호', type='password')
        upw_chk = st.text_input('비밀번호 확인', type='password')
        ubd = st.date_input('생년월일', min_value=datetime.date(1930,1,1))
        ugender = st.radio('성별', options=['남', '여'], horizontal=True)

        submitted = st.form_submit_button('제출')
        if submitted:
            if len(uid) < 6:
                st.warning('아이디는 6글자 이상이어야 합니다.')
                st.stop()

            if upw != upw_chk:
                st.warning('비밀번호가 일치하지 않습니다.')
                st.stop()

            cur.execute(f"INSERT INTO users ("
                        f"uid, "
                        f"uname, "
                        f"upw, "
                        f"ubd, "
                        f"ugender) VALUES ("
                        f"'{uid}', "
                        f"'{uname}',"
                        f"'{upw}',"
                        f"'{ubd}',"
                        f"'{ugender}')")
            con.commit()

            st.success(f'{uid} {uname} {upw} {ubd} {ugender}')

elif menu == '회원목록':

    st.subheader('회원목록')

    data = pd.read_sql('SELECT * FROM users', con)

    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_default_column(editable=True, groupable=True)
    # Add pagination
    gb.configure_pagination(paginationAutoPageSize=True)
    # Add a sidebar
    gb.configure_side_bar()
    # Enable multi-row selection
    gb.configure_selection(
        'single',
        use_checkbox=True
    )
    gridOptions = gb.build()

    grid_response = AgGrid(
        data,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT',
        update_mode='MODEL_CHANGED',
        fit_columns_on_grid_load=True,
        enable_enterprise_modules=True,
        height=350,
        reload_data=False,
    )

    data = grid_response['data']
    selected = grid_response['selected_rows']

    if selected:
        updateBtn = st.button('수정')

        if updateBtn:
            row = selected[0]
            cur.execute(f"UPDATE users SET uname='{row['uname']}' WHERE no={row['no']}")
            con.commit()
            st.experimental_rerun()


elif menu == '로그인':
    st.subheader('로그인')
    #로그인 전
    with st.form('login_form'):
        id=st.text_input('아이디')
        pw=st.text_input('비밀번호', type='password')
        login_btn=st.form_submit_button('로그인')



# df = pd.read_sql('SELECT * FROM users', con)
# st.dataframe(df)


