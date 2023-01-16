import streamlit as st
import datetime

st.subheader("회원가입 폼")

with st.form("my_form",clear_on_submit=True):
    st.info("다음 양식을 모두 작성한 다음 제출합니다.")
    uid=st.text_input("아이디", max_chars=12)
    uname=st.text_input("성명", max_chars=10)
    upw=st.text_input("비밀번호", type='password')
    upw_chk=st.text_input("비밀번호확인", type='password')
    ubd=st.date_input("생년월일", min_value=datetime.date(1930,1,1))
    submitted=st.form_submit_button("제출")
    if submitted:
        st.success("제출됨")