import os
from openai import OpenAI
import streamlit as st
import pandas as pd

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
st.set_page_config(
    page_title="유아 놀이 관찰 기록 문장 생성 🎨",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="auto",
)
 
# Custom CSS for a child-friendly UI
st.markdown("""
    <style>
        .main {
            background-color: #fffbe7;
            font-family: 'Comic Sans MS', cursive, sans-serif;
        }
        h1 {
            color: #ff6347;
            text-align: center;
            font-family: 'Comic Sans MS', cursive, sans-serif;
            font-size: 2.5em;
        }
        .instructions {
            background-color: #ffebcd;
            padding: 15px;
            border-radius: 20px;
            margin-bottom: 20px;
            box-shadow: 3px 3px 5px #c1c1c1;
        }
        .section {
            background-color: #fffaf0;
            padding: 20px;
            border-radius: 20px;
            box-shadow: 3px 3px 5px #c1c1c1;
            margin-bottom: 20px;
            font-size: 1.2em;
        }
        .button {
            background-color: #ffb6c1;
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 15px;
            border-radius: 20px;
            border: none;
            cursor: pointer;
            width: 100%;
        }
        .button:hover {
            background-color: #ff69b4;
        }
    </style>
""", unsafe_allow_html=True)

# Title of the application
st.markdown("<h1>유아 놀이 관찰 기록 문장 생성 🎨</h1>", unsafe_allow_html=True)

# Instructions for users with a child-friendly card style
st.markdown("""
<div class="instructions">
    <h3>사용 설명서 🖍️</h3>
    <ul>
        <li>👶 <b>이름</b>과 <b>영역</b>을 직접 입력하고, <b>관찰 누가기록</b>은 엑셀 파일을 통해 업로드하세요.</li>
        <li>📄 엑셀 파일은 다음과 같은 컬럼을 포함해야 합니다: 관찰 누가기록 1~5.</li>
        <li>⬇️ 아래 링크에서 <b>예시 파일</b>을 다운로드 받아 양식을 확인할 수 있습니다.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Provide a download link for the example Excel template
st.markdown("""
    [엑셀 양식 다운로드](https://docs.google.com/spreadsheets/d/1JmQdZnRNGNdwAWFhG0XcYHtwEuMgp8aQ/edit?usp=drive_link&ouid=109125530609256193549&rtpof=true&sd=true)
""")

# Optionally, show a preview of the template
st.markdown("<h3>엑셀 파일 양식 미리보기 📄</h3>", unsafe_allow_html=True)

# Example DataFrame that mimics the structure of the required Excel file
example_df = pd.DataFrame({
    '관찰 누가기록 1': ['기록 예시 1'],
    '관찰 누가기록 2': ['기록 예시 2'],
    '관찰 누가기록 3': ['기록 예시 3'],
    '관찰 누가기록 4': ['기록 예시 4'],
    '관찰 누가기록 5': ['기록 예시 5']
})

# Display the example DataFrame as a table
st.dataframe(example_df)

# Inputs for name and grade
name_keyword = st.text_input("이름 🌼", placeholder="학생 이름을 입력해주세요.")
grade_options = ["신체운동건강 🌞", "의사소통 📚", "사회관계 🤝", "예술경험 🎨", "자연탐구 🌳"]
grade_keyword = st.selectbox("영역 선택 🎓", grade_options)

# File uploader for Excel file
uploaded_file = st.file_uploader("관찰 누가기록이 포함된 엑셀 파일을 업로드하세요 📂", type=["xlsx"])

# Display the 'Generate' button at all times
generate_button_clicked = st.button('생성하기', key='generate_button', help="아이의 관찰 기록을 생성합니다")

# Process after the button is clicked
if generate_button_clicked:
    if uploaded_file and name_keyword and grade_keyword:
        # Read the uploaded Excel file
        df = pd.read_excel(uploaded_file)

        # Check if the required columns exist in the uploaded file
        required_columns = ['관찰 누가기록 1', '관찰 누가기록 2', '관찰 누가기록 3', '관찰 누가기록 4', '관찰 누가기록 5']
        if all(column in df.columns for column in required_columns):
            with st.spinner('생성 중입니다...'):
                # Process each row in the Excel file
                for index, row in df.iterrows():
                    topic_keyword1 = row['관찰 누가기록 1']
                    topic_keyword2 = row['관찰 누가기록 2']
                    topic_keyword3 = row['관찰 누가기록 3']
                    topic_keyword4 = row['관찰 누가기록 4']
                    topic_keyword5 = row['관찰 누가기록 5']

                    # Combine keywords into a single input
                    keywords_combined = f"관찰 누가기록 1: {topic_keyword1}, 관찰 누가기록 2: {topic_keyword2}, 관찰 누가기록 3: {topic_keyword3}, " \
                                        f"관찰 누가기록 4: {topic_keyword4}, 관찰 누가기록 5: {topic_keyword5}, 영역: {grade_keyword}, 이름: {name_keyword}"
        
        
        # Create a chat completion request to OpenAI API"
        
        chat_completion = client.chat.completions.create(
            
            messages=[
                {
                    "role": "user",
                    "content": keywords_combined,
                },
                {
                    "role": "system",
                    "content": 
                         "당신은 유아놀이 관찰 전문가입니다. 입력된 관찰 누가기록과 영역을 바탕으로 유치원 학생의 입력된 이름을 넣어 놀이 관찰을 한 문단으로 기록해주세요 "
                        "1. 입력된 관찰 누가기록을 모두 다 반영해서 생성해주세요."                      
                        "2. 영역에 맞게 10 문장 정도 생성 해주세요. "
                        "3. 만4세 기준으로 학생의 놀이 활동이 너무 어렵지 않았으면 좋겠습니다."
                        "4. 이것은 꼭 지켜야해 놀이관찰 기록과 전문가의 평가 모든 내용 꼭 한 문단 안에 기록되어야 한다."
                        "5. 꼭 한 문단 안에 모든 내용이 들어가야 한단다. " 
                        "6. 놀이 관찰 기록 문단 안에 전문가의 평가라는 단어는 들어가면 안된다."
                        "7. 놀이 관찰 기록이 꼭 긍정적으로 나올 필요는 없단다."
                        "8. 관찰 누가기록과 영역의 관련성을 높이면 좋겠어."
                        "9. 누가기록, 첫번째 두번째와 같은 순서를 넣어서는 표현하지 말아주세요. 그리고 문장이 자연스럽게 이어지도록 표현해주세요"
    
                    
                }
            ],
            model="gpt-4o",
        )

        # Extract the generated content
        result = chat_completion.choices[0].message.content

        # Display the result in Streamlit app
        st.write(f"**{name_keyword}**의 관찰 기록:")
        st.write(result)
        st.write("---")
    else:
        st.error("엑셀 파일에 필요한 모든 관찰 누가기록이 컬럼이 포함되어 있지 않습니다.")