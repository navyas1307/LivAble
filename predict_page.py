import streamlit as st
import pandas as pd
import google.generativeai as genai

genai.configure(api_key="AIzaSyBN4g03--SHgVne8N3cnuhxKF5r25qpYac")  # 🔹 Replace with your actual key

def query_gemini(question):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")  # Use Gemini-Pro model
        response = model.generate_content(question)
        return response.text  # Extract AI-generated response
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def load_data():
    file_path = "world_data_with_scores.csv"
    data = pd.read_csv(file_path)
    st.title("Livability Prediction")

    tab1, tab2 = st.tabs(["Rankings", "AI Chatbot"])

    with tab1:
        st.markdown("""
        <style>
        .predict-card {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 15px;
            padding: 15px;
            transition: transform 0.3s ease;
        }
        .predict-card:hover {
            transform: scale(1.02);
        }
        </style>
        """, unsafe_allow_html=True)
    
    
        # Calculate rankings for each index and livability score
        data['health_rank'] = data['Health Index'].rank(ascending=False).astype(int)
        data['education_rank'] = data['Education Index'].rank(ascending=False).astype(int)
        data['environment_rank'] = data['Environment Index'].rank(ascending=False).astype(int)
        data['economic_rank'] = data['Economic Index'].rank(ascending=False).astype(int)
        data['quality_of_life_rank'] = data['Quality of Life Index'].rank(ascending=False).astype(int)
        data['livability_rank'] = data['Livability Score'].rank(ascending=False).astype(int)

        country = st.selectbox("Select a country:", data['Country'])

        selected_country_data = data[data['Country'] == country].iloc[0]
        st.title(f"Rankings for {country}")

        columns = st.columns(3)

        rankings = [
            {"title": "Health Index Rank", "value": selected_country_data['health_rank']},
            {"title": "Education Index Rank", "value": selected_country_data['education_rank']},
            {"title": "Environment Index Rank", "value": selected_country_data['environment_rank']},
            {"title": "Economic Index Rank", "value": selected_country_data['economic_rank']},
            {"title": "Quality of Life Rank", "value": selected_country_data['quality_of_life_rank']},
            {"title": "Overall Livability Score Rank", "value": selected_country_data['livability_rank']},
        ]
    
        total_countries = len(data)

        for index, ranking in enumerate(rankings):
            col = columns[index % 3]
            with col:
                 st.markdown(
                f"""
                <div class="predict-card">
                    <h4 style="margin-bottom: 10px;">{ranking['title']}</h4>
                    <p style="font-size: 18px; color: #333;"><b>Rank: #{ranking['value']} of {total_countries}</b></p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    with tab2:
        st.header("Ask AI about the data or general topics!")
        user_input = st.text_area("Enter your question:")
        if st.button("Ask AI"):
            if user_input:
                response = query_gemini(user_input)
                st.write(response)
            else:
                st.warning("Please enter a question.")
