import streamlit as st
import datetime
import sqlite3
import pandas as pd

#데이터베이스 연결
con=sqlite3.connect('users.db')
cur=con.cursor()

st.subheader("회원가입 폼")

with st.form("my_form",clear_on_submit=True):
    st.info("다음 양식을 모두 작성한 다음 제출합니다.")
    uid=st.text_input("아이디", max_chars=12)
    uname=st.text_input("성명", max_chars=10)
    upw=st.text_input("비밀번호", type='password')
    upw_chk=st.text_input("비밀번호확인", type='password')
    ubd=st.date_input("생년월일", min_value=datetime.date(1930,1,1))
    ugender=st.radio("성별", options=['남','여'],horizontal=True)
    submitted=st.form_submit_button("제출")
    if submitted:
        if len(uid)<6:
            st.warning("아이디는 6글자 이상")
            st.stop()
        if upw!=upw_chk:
            st.warning("비밀번호확인바람")
            st.stop()

        cur.execute(f"INSERT INTO users (uid,uname,upw,ubd,ugender) " VALUES ({uid},{uname},{upw},{ubd},{ugender})")
        con.commit()


        st.success(f"{uid},  {uname},  {upw},  {ubd},  {ugender}")

st.subheader("회원목록")
df=pd.read_sql('SELECT*FROM users',con)
st.dataframe(df)