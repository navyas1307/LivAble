import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

def load_visualizations():
    # Load the dataset
    file_path = 'world 2023.csv'
    df = pd.read_csv(file_path)

    # Title of the page
    st.title("Global Livability Insights")

    # Create a tabbed interface for visualizations
    tab1, tab2, tab3, tab4 = st.tabs([
        "Health vs Livability", 
        "Education Insights", 
        "Economic Correlations", 
        "Environmental Factors"
    ])

    with tab1:
        # Visualization 1: Health Index vs Livability Score
        fig1 = px.scatter(
            df, 
            x='Health Index', 
            y='Livability Score', 
            color='Country',
            hover_data=['Country', 'Health Index', 'Livability Score'],
            title='Health Index Impact on Livability Score'
        )
        st.plotly_chart(fig1, use_container_width=True, key='health_livability_scatter')
        st.markdown("""
        **Key Insights:**
        - Correlation between Health Index and Livability Score
        - Countries with higher health indices tend to have better livability scores
        - Hover over points to explore individual country details
        """)

    with tab2:
        # Visualization 2: Top Countries by Education Index
        df_top_education = df.nlargest(15, 'Education Index')
        
        fig2 = px.bar(
            df_top_education, 
            x='Education Index', 
            y='Country', 
            orientation='h',
            color='Education Index',
            title='Top 15 Countries by Education Index',
            labels={'Education Index': 'Education Performance'},
            color_continuous_scale='viridis'
        )
        
        fig2.update_layout(
            height=600,
            xaxis_title='Education Index Score',
            yaxis_title='Country'
        )
        
        st.plotly_chart(fig2, use_container_width=True, key='education_top_countries')
        st.markdown("""
        **Key Insights:**
        - Ranking of top 15 countries by education performance
        - Color intensity reflects education index magnitude
        - Quick comparative view of global education leaders
        """)

    with tab3:
        # Visualization 3: Economic Index Treemap
        df['Economic Performance'] = df['Economic Index'] * df['Livability Score'] / 100
        
        # Custom color scale with vibrant, smooth transitions
        custom_colorscale = [
            [0, 'rgb(36,104,180)'],     # Deep blue
            [0.25, 'rgb(70,167,228)'],  # Bright blue
            [0.5, 'rgb(255,193,7)'],    # Vibrant yellow
            [0.75, 'rgb(255,87,34)'],   # Warm orange
            [1, 'rgb(211,47,47)']       # Rich red
        ]
        
        fig3 = px.treemap(
            df, 
            path=['Country'], 
            values='Economic Performance',
            color='Economic Index',
            hover_data=['Country', 'Economic Index', 'Livability Score', 'Economic Performance'],
            title='Global Economic Performance Landscape',
            color_continuous_scale=custom_colorscale
        )
        
        fig3.update_layout(
            height=600,
            title_x=0.5,
            title_font_size=20
        )
        
        st.plotly_chart(fig3, use_container_width=True, key='economic_performance_treemap')
        st.markdown("""
        **Key Insights:**
        - Dynamic visualization of economic performance
        - Color gradient reflects economic complexity
        - Size indicates economic and livability potential
        """)
    with tab4:
        # Visualization 4: Environmental Factors Scatter Plot
        # Calculate composite environmental performance
        df['Environmental Performance'] = (
            df['Environment Index'] * 
            (df['Forested Area (%)'] / 100) * 
            (1 / (df['Co2-Emissions'] + 1))  # Inverse relationship with CO2
        )
        
        # Prepare data for visualization
        df_env = df.sort_values('Environmental Performance', ascending=False).head(30)
        
        fig4 = px.scatter(
            df_env, 
            x='Forested Area (%)', 
            y='Environment Index',
            size='Environmental Performance',
            color='Co2-Emissions',
            hover_name='Country',
            hover_data=['Country', 'Environment Index', 'Forested Area (%)', 'Co2-Emissions'],
            title='Environmental Performance Insights',
            color_continuous_scale='RdYlGn_r'  # Red to Green (reversed)
        )
        
        fig4.update_layout(
            height=600,
            xaxis_title='Forest Coverage (%)',
            yaxis_title='Environment Index'
        )
        
        st.plotly_chart(fig4, use_container_width=True, key='environmental_performance_scatter')
        
        st.markdown("""
        **Key Environmental Insights:**
        - Bubble size reflects comprehensive environmental performance
        - Color intensity shows CO2 emissions (darker = higher emissions)
        - Larger bubbles indicate better overall environmental health
        - Intersection of forest coverage and environmental index
        """)
        
        # Additional context
        top_5_env = df_env.head(5)[['Country', 'Environment Index', 'Forested Area (%)', 'Co2-Emissions']]
        st.dataframe(top_5_env)