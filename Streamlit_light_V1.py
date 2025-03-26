# Energy Project, Light version
# Author Ivanne Poussier, from common work with Kilian Simon

# GET STARTED

import streamlit as st
import pandas as pd 
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from plotly.subplots import make_subplots
import plotly.express as px
import io
import pickle
import json
from PIL import Image

# LAYOUT AND SIDEBAR

# Adjusted padding and margins  
st.set_page_config(layout="wide")  # Remove default padding constraints

st.markdown(
    """
    <style>
        /* Apply to the entire page */
        .block-container {
            padding: 2rem !important;  /* Adjust padding */
            margin: 4rem !important;   /* Adjust margin */
        }"
    """,
    unsafe_allow_html=True, 
) 

# Sidebar and navigation
st.sidebar.title("Energy project")

pages=["Introduction", 
       "Data Exploration and Cleaning",
       "Data Preprocessing", 
       "Data Visualization", 
       "Data Modelling", 
       "Prediction", 
       "Conclusion"]

page=st.sidebar.radio("Go to", pages)

st.sidebar.markdown(
    """
    <style>
        section[data-testid="stSidebar"] h1 {
            color: var(--primary-color);
        }
    </style>
    <div class="sidebar-content">
      <p> </p>
      <p><b>A Project carried out by 
      <a href="https://www.linkedin.com/in/ivannepoussier/" target="_blank">Ivanne Poussier</a> 
      and 
      <a href="https://www.linkedin.com/in/kilian-simon-68b1a41b6/" target="_blank">Kilian Simon</a>, mentored by Tarik Anouar</b></p>
      <p><i>DataScientest Data Analyst Bootcamp, March 2025.</i></p>
    </div>
    """,
    unsafe_allow_html=True
)

# LOADING LIGHTER DATASETS
# Naming convention: p3g1 means page 3 graph 1

p1d1nans = pd.read_csv('p1d1nans.csv', sep = ',')
p3g1 = pd.read_csv('p3g1.csv', sep = ',')
p3g2 = pd.read_csv('p3g2.csv', sep = ',')
p3g3 = pd.read_csv('p3g3.csv', sep = ',')
p3g4 = pd.read_csv('p3g4.csv', sep = ',')
p3g5 = pd.read_csv('p3g5.csv', sep = ',')


# PAGE 0 # INTRODUCTION
if page == pages[0] :
    st.title("Introduction")
    st.subheader("Context")
    st.markdown("""  
                **Electricity is at the heart of the energy transition**, that is based on shifting the energy mix towards more low-carbon energy. 
                - Electricity is **produced with its own mix of primary sources** that are more or less flexible, environmental-friendly and carbon-free.
                - Electricity **cannot be stored** (at least at a big scale) contrary to other kinds of energies. 
                - As a result, the **phasing of production with consumption in real-time** is key for the reliability of the electric system.
                """)
    st.subheader("Objective")
    st.write(""" 
             The French electricity market is driven by demand. **Predicting the consumption is key** to inform the
             producers and trigger market mechanisms such as offsetting, additional production or importation of
             electricity from Europe.
             """)
    st.success(
    "This project leveraged 10 years of electricity consumption and production data, "
    "shared by the transmission system operator RTE, at both national and regional scale. ",
    icon=":material/bolt:"
    )

# PAGE 1 # Exploration and clearning
if page == pages[1] :
    st.title("Data exploration and cleaning")

    # EXPLORATION
    st.header("Presentation of the datasets")

    # Eco2mix dataset
    st.subheader("Regional éCO2mix data (RTE)")
    st.markdown(""" 
                For each administrative region and at half-hourly intervals, the dataset provides:
                - **Actual consumption** in MW  
                - **Production** in MW according to the different energy sources making up the energy mix (**Nuclear, Hydro, Wind, Solar, Bioenergy, Thermal**)  
                - **Consumption** in MW by pumps in Pumped Storage Stations (**STEP** in French) that produce Hydro electricity 
                - **The balance of exchanges** with neighbouring regions  
                - **TCO and TCH indicators**  
                    - The Coverage Rate (in French TCO) of a sector of production within a region represents the share of this sector in the consumption of this region.
                    - The CHarge Rate (in French TCH) or load factor (FC) of a sector represents its production volume in relation to the sector's installed and operational production capacity.
                """)
    st.markdown(""" The raw dataset has **2.121.408** rows, **32** columns and **67.885.056** elements.""")

    # Instantiate the DataFrame summary as a string
    dfraw_info = """
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 2121408 entries, 0 to 2121407
    Data columns (total 32 columns):
     #   Column               Dtype
    ---  ------               -----
     0   Code INSEE région    int64
     1   Région               object
     2   Nature               object
     3   Date                 object
     4   Heure                object
     5   Date - Heure         object
     6   Consommation (MW)    float64
     7   Thermique (MW)       float64
     8   Nucléaire (MW)       float64
     9   Eolien (MW)          object
    10   Solaire (MW)         float64
    11   Hydraulique (MW)     float64
    12   Pompage (MW)         float64
    13   Bioénergies (MW)     float64
    14   Ech. physiques (MW)  float64
    15   Stockage batterie    float64
    16   Déstockage batterie  float64
    17   Eolien terrestre     float64
    18   Eolien offshore      float64
    19   TCO Thermique (%)    float64
    20   TCH Thermique (%)    float64
    21   TCO Nucléaire (%)    float64
    22   TCH Nucléaire (%)    float64
    23   TCO Eolien (%)       float64
    24   TCH Eolien (%)       float64
    25   TCO Solaire (%)      float64
    26   TCH Solaire (%)      float64
    27   TCO Hydraulique (%)  float64
    28   TCH Hydraulique (%)  float64
    29   TCO Bioénergies (%)  float64
    30   TCH Bioénergies (%)  float64
    31   Column 30            float64
    dtypes: float64(25), int64(1), object(6)
    memory usage: 517.9+ MB
    """
    # Display the summary in an expander using st.code()
    with st.expander("**Original list of Variables in French**"):
        st.code(dfraw_info)

    # FOCUS ON MISSING VALUES
    st.markdown("**Focus on missing values**")
    with st.expander("**Number of Missing Values by Variable**"):
        st.dataframe(p1d1nans)

    with st.expander("**Visualizing Missing Values with a heatmap**"):
        st.write("As seen in the optional modules dedicated to data quality and to plotly, we leveraged the heatmap representation to better understand the distribution of missing values. ")
        
        tab1, tab2, tab3 = st.tabs(["2013-2019", "2020", "2021-2022"])
        
        with tab1:
            st.subheader("Every years from 2013 to 2019 share a comparable profile")
            st.warning("Missing values are displayed in light pink. We note the absence of TCO and TCH indicators that enable comparisons of energy production sectors among region. They were introduced from 2020 only.", 
                       icon=":material/percent:")
            #st.image(r"C:\Users\IvannePoussier\Documents\Streamlit_energy\Heatmap_nans_1.png")
            st.image(r"Heatmap_nans_1.png")

        with tab2:
            st.subheader("2020 has less missing values")
            st.warning("We found why Nuclear production had missing values in 33% of the rows. They correspond to regions without any nuclear facility.", 
                       icon=":material/map_search:")
            st.image(r"C:\Users\IvannePoussier\Documents\Streamlit_energy\Heatmap_nans_2.png")

        with tab3:
            st.subheader("From 2021 nuclear production is set to zero in the 5 nuclear-free regions")
            st.warning("The remaining missing values reflect the impossibility to compute the Charge Rate (TCH) of nuclear production in nuclear-free regions.", 
                       icon=":material/percent:")
            st.image(r"C:\Users\IvannePoussier\Documents\Streamlit_energy\Heatmap_nans_3.png")

    # Temperature dataset 
    st.subheader("Regional daily temperature (Weathernews France)")
    st.markdown(""" 
                For each administrative region, the dataset provides a record, in degrees Celsius, of:
                - Daily **minimum temperature**
                - Daily **maximum temperature**
                - Daily **average temperature** 
                """)

    st.markdown("""The raw dataset has **42.510** rows, **7** columns and **297.570** elements.""")

    # Instantiate the DataFrame summary as a string
    temp_info = """" 
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 42510 entries, 0 to 42509
    Data columns (total 7 columns):
     #   Column             Non-Null Count  Dtype  
    ---  ------             --------------  -----  
     0   ID                 42510 non-null  object 
     1   Date               42510 non-null  object 
     2   Code INSEE région  42510 non-null  int64  
     3   Région             42510 non-null  object 
     4   TMin (°C)          42510 non-null  float64
     5   TMax (°C)          42510 non-null  float64
     6   TMoy (°C)          42510 non-null  float64
    dtypes: float64(3), int64(1), object(3)
    memory usage: 2.3+ MB
    """
    # Display the summary in an expander using st.code()
    with st.expander("**Original list of Variables in French**"):
        st.code(temp_info)

    # FOCUS ON MISSING VALUES
    st.markdown("**Focus on missing values**")
    with st.expander("**Number of Missing Values by Variable**"):
        st.write("There are 0 missing values at first sight!")
        st.caption("Note: Only after the first merging of the datasets, we discovered that 3 dates were in fact missing between the year 2016 to the year 2022 (the equivalent of 39 rows).")  


    # CLEANING
    st.header("Data merging and cleaning")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Start", "Structure", "Variable classes", "Missing values", "Quality check"])
    with tab1:
        st.image(r"C:\Users\IvannePoussier\Documents\Streamlit_energy\Image1.png", width=800) 
    with tab2:
        st.image(r"C:\Users\IvannePoussier\Documents\Streamlit_energy\Image2.png", width=800)         
    with tab3:
        st.image(r"C:\Users\IvannePoussier\Documents\Streamlit_energy\Image3.png", width=800)         
    with tab4:
        st.image(r"C:\Users\IvannePoussier\Documents\Streamlit_energy\Image4.png", width=800)          
    with tab5:
        st.image(r"C:\Users\IvannePoussier\Documents\Streamlit_energy\Image5.png", width=800) 

    st.warning("Only the main dataset needs cleaning at this stage.", 
            icon=":material/info:")


# PAGE 2 # PREPROCESSING
if page == pages[2] :

    st.title("Data preprocessing")

    # FEATURE ENGINEERING #
    st.subheader("Feature engineering")    

    tab1, tab2, tab3, tab4 = st.tabs(["Feature creation", "Transformation", "Encoding and feature selection", "Normalisation"])
    with tab1:
        st.image(r"C:\Users\IvannePoussier\Documents\Streamlit_energy\feature_1.png", width=800) 
    with tab2:
        st.image(r"C:\Users\IvannePoussier\Documents\Streamlit_energy\feature_2.png", width=800)         
    with tab3:
        st.image(r"C:\Users\IvannePoussier\Documents\Streamlit_energy\feature_3.png", width=800)         
    with tab4:
        st.image(r"C:\Users\IvannePoussier\Documents\Streamlit_energy\feature_4.png", width=800)          

    # STATISTICAL TESTS ON FEATURES
    st.subheader("Statistical tests on features") 

    tab5, tab6, tab7, tab8 = st.tabs(["Correlation matrix I", "Correlation matrix II", "Correlation matrix III", "Histograms and QQ-plots"])
    with tab5:
        st.warning("This heatmap has label encoded regions. It does not include the seasons and the encoded months, in order to ensure legibility.",
                   icon=":material/apps:")
        st.image(r"C:\Users\IvannePoussier\Documents\Streamlit_energy\Tests_1.png", width=800) 
    with tab6:
        st.warning("Now we focus on the encoded seasons and the encoded months.",
                   icon=":material/apps:")
        st.image(r"C:\Users\IvannePoussier\Documents\Streamlit_energy\Tests_2.png", width=800)         
    with tab7:
        st.warning("This heatmap has one hot encoded regions.",
                   icon=":material/apps:")
        st.image(r"C:\Users\IvannePoussier\Documents\Streamlit_energy\Tests_3.png", width=800)         
    with tab8:
        st.success("Following the Shapiro-Willcox test, the numerical temperature-related values are not normally distributed.",
                   icon=":material/search_insights:")
        st.image(r"C:\Users\IvannePoussier\Documents\Streamlit_energy\Tests_4.png", width=800)


# PAGE 3 # DATAVISUZALIZATION
if page == pages[3] :
    st.title("Visualization")

    # GRAPH 1 #
    st.subheader("Seasonality is key to balance production and consumption")
    
    # gbraw= dfraw2.groupby('Month', as_index = False)[['Consumption_MWh', 'Production_MWh']].mean().round()
    # we replace gbraw by p3g1
    fig = px.line(p3g1, 
                  x = "Month", 
                  y = ["Production_MWh", "Consumption_MWh"], 
                  title = "Average Energy Consumption and Production by Month",
                  labels={"value": "Electricity in MWh", "variable": "Legend"})
    fig.for_each_trace(lambda t: t.update(line=dict(dash='dash')) if t.name == 'Production_MWh' else ())

    fig.update_layout( 
        width = 900, height = 500,
        plot_bgcolor="rgba(240, 242, 246, 0.8)",
        xaxis= dict( 
            showgrid=True, gridcolor="gray", gridwidth=1, griddash="dot",
            tickmode="array", tickvals=list(range(1, 13)),
            ticktext=['January', 'February', 'March', 'April', 'May', 'June', 'July', 
                      'August', 'September', 'October', 'November', 'December'],
            tickangle=315),
        yaxis=dict(showgrid=True, gridcolor="gray", gridwidth=1, griddash="dot", fixedrange=True),
        yaxis_range=[0, 5000],
        yaxis_title="Electricity in MWh"
        )
    
    st.plotly_chart(fig)

    # GRAPH 2 #  
    st.subheader("Demand also varies over the day")
    
    # gb2raw= dfraw2.groupby(['Heure', 'Season'], as_index = False)[['Consumption_MWh']].mean().round()
    # we replace gbraw by p3g2
    fig = px.line(p3g2, 
                  x = "Heure", 
                  y = "Consumption_MWh", 
                  color = "Season",
                  title = "Average Energy Consumption by Hour of the Day",
                  labels={"Consumption_MWh": "Consumption in MWh", "Heure": "Hour of the Day"},
                  category_orders={"Season": ["Winter", "Spring", "Summer", "Autumn"]}, 
                  color_discrete_sequence = ["#4C72B0", "#55A868", "#E69F00", "#9C755F"]) 

    fig.update_layout( 
        width = 900, height = 500,
        plot_bgcolor="rgba(240, 242, 246, 0.8)",
        xaxis= dict( 
            showgrid=True, gridcolor="gray", gridwidth=1, griddash="dot",
            tickmode="array", tickvals=list(range(0, 48, 4)), tickangle = 315,
        ),
        yaxis=dict(showgrid=True, gridcolor="gray", gridwidth=1, griddash="dot", 
                   fixedrange=True, range=[0, 3500]),
        yaxis_title="Electricity in MWh"
    )

    st.plotly_chart(fig)

    # GRAPH 3 # Monthly production broken down by sector in 2022
    st.subheader("The French electric mix relies on nuclear power")

    # Create gbs (groupby "small") With groupby (by Month) and melt it by month/sector
    # dfl_2022 = dfl[dfl['Year'] == 2022]
    # gbs = dfl_2022.groupby('Month')[['Nuclear', 'Hydro', 'Wind', 'Solar', 'Bioenergy', 'Thermal']].sum().mul(0.5).div(1000000).round(1)
    # we replace gbs by p3g3
    gbsmelt = p3g3.melt(id_vars='Month', var_name='Sector', value_name='Production')

    color_map = { 
        'Nuclear': '#5603AD',
        'Hydro': '#1E96FC',
        'Wind': '#5DD39E',
        'Solar': '#FFD333',
        'Bioenergy': '#FE938C',
        'Thermal': '#27313F'
         }
    
    month_labels = ['Jan.', 'Feb.', 'March', 'April', 'May', 'June', 
                    'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']

    gbsmelt['Month'] = gbsmelt['Month'].map(lambda x: month_labels[x-1]) # Use map on the 'Month' column of gbsmelt and substract 1 to match the index in the month_labels

    fig = px.bar(gbsmelt, x = 'Month', y = 'Production', barmode='stack', 
                 color='Sector', color_discrete_map=color_map, 
                 title="Monthly production of electricity in 2022, broken down by sector")
    fig.update_traces(marker=dict(line=dict(width=0.7)), width=0.6)  # Adjust bar width
    fig.update_layout( 
        width=900, height=500,
        plot_bgcolor="rgba(240, 242, 246, 0.8)",
        xaxis=dict(showgrid=True, gridcolor="gray", gridwidth=1, griddash="dot"),
        yaxis=dict(showgrid=True, gridcolor="gray", gridwidth=1, griddash="dot", fixedrange=True),
        yaxis_range=[0, 55],
        xaxis_title="Month",
        yaxis_title="Production in TWh",
        legend_title="Energy sources"
        )
    st.plotly_chart(fig)

    # GRAPH 4 # Yearly production of electricity from 2013 to 2022, broken down by sector
    st.subheader ("2013-2022: Variations among years are multifactorial")
    
    # Create gbt (groupby "tall") With groupby (by Year) and melt it by year/sector
    # gbt = dfl.groupby('Year')[ 
    #    ['Nuclear', 'Hydro', 'Wind', 'Solar', 'Bioenergy', 'Thermal'] 
    #    ].sum().mul(0.5).div(1000000).round() # replacing * 0.5 / 1000000
    # we replace gbt by p3g4
    gbtmelt = p3g4.melt(id_vars='Year', var_name='Sector', value_name='Production')

    # Ensure Year is categorical and ordered for correct display
    gbtmelt['Year'] = gbtmelt['Year'].astype(str)

    # Create bar plot
    fig = px.bar(gbtmelt, x = 'Year', y = 'Production', barmode='stack', 
                 color='Sector', color_discrete_map=color_map, 
                 title="Yearly production of electricity from 2013 to 2022, broken down by sector")
    fig.update_traces(marker=dict(line=dict(width=0.7)), width=0.6)  # Adjust bar width
    fig.update_layout( 
        width=900, height=500,
        plot_bgcolor="rgba(240, 242, 246, 0.8)",
        xaxis=dict(showgrid=True, gridcolor="gray", gridwidth=1, griddash="dot"),
        yaxis=dict(showgrid=True, gridcolor="gray", gridwidth=1, griddash="dot", fixedrange=True),
        yaxis_range=[0, 550],
        xaxis_title="Year",
        yaxis_title="Production in TWh",
        legend_title="Energy sources"
        )
    st.plotly_chart(fig)    

    # GRAPH 5 # Electricity consumption and production by region (distribution)
    st.subheader("French regions are structurally interdependent")
    st.text("Electricity generation facilities are not evenly distributed across the regions.")
    st.info("To make the data easier to read, the whisker boxes extend to the extreme values.", 
            icon=":material/info:")
    
    # we replace dfl_melted by p3g5 
    #    dfl_melted = pd.melt(dfl, id_vars="Region",
    #                     value_vars=['ConsumptionMWh', "ProductionMWh"],
    #                     var_name="Type", value_name="Value")    
    fig = px.box(p3g5,
                 x="Region",
                 y="Value",
                 color="Flow",
                 title="Electricity Consumption and Production by Region",
                 category_orders={"Region": ["Auvergne-Rhone-Alpes", "Grand Est", "Centre-Val de Loire",
                                             "Normandie", "Nouvelle-Aquitaine", "Hauts-de-France", 
                                             "Occitanie", "Provence-Alpes-Cote d'Azur", "Pays de la Loire", 
                                             "Bretagne", "Bourgogne-Franche-Comte", "Ile-de-France"]
                                             },
                 points=False,  # Hide outliers to match whis=(0,100)
                 )
    fig.update_traces(marker=dict(line=dict(width=0.7)),opacity=1)
    fig.update_layout( 
        width=1000, height=600,
        plot_bgcolor="rgba(240, 242, 246, 0.8)",
        boxmode="group",  # Equivalent to Seaborn's hue differentiation
        xaxis=dict(
        showgrid=True, gridcolor="gray", gridwidth=1, griddash="dot", tickangle=315
        ),
        yaxis=dict(
            tickformat="d", showgrid=True, gridcolor="gray", gridwidth=1, griddash="dot", fixedrange=True,
            zeroline=True, zerolinecolor="black", zerolinewidth=1  # Apply zeroline to y-axis
        ),
        yaxis_range=[-500, 12000],
        xaxis_title="Region",
        yaxis_title="Electricity (MWh)",
        legend_title="Energy sources"
        )
    st.plotly_chart(fig)

    st.warning("Please note: in order to simplify the application for publication, we have generated a limited set of synthetic data based on the centrality and dispersion values for each region.", 
        icon=":material/info:")
    
# PAGE 4 # MODELLING
if page == pages[4]:
    st.title("Data Modelling")
    st.info(
        "Predicting the consumption of electricity is **a regression problem**. Indeed, ‘Consumption’ is a continuous variable measured in MW.",
        icon=":material/show_chart:"
    )
    st.write("")
    
    # Create Tabs
    tab1, tab2, tab3 = st.tabs(["Model Pre-selection", "Detailed Model Results", "Performance Indicators"])

    with tab1:
        st.subheader("Model Pre-selection")
        preselection_data = {
            "Model": ["Linear Regression", "Decision Tree Regressor (Tree)", "Random Forest Regressor (Tree)", "Lasso (linear)", "LassoCV (linear)", "Ridge (linear)"],
            "In short, why opt for it?": [
                "Simple, interpretable, and works well for linear relationships.",
                "Captures non-linear patterns, easy to interpret, but prone to overfitting.",
                "Reduces overfitting by averaging multiple trees, improving accuracy.",
                "Feature selection by shrinking coefficients to zero.",
                "Automatic tuning of alpha using cross-validation.",
                "Reduces overfitting while keeping all features."
            ],
            "Training Time": ["Fast", "Moderate", "Slow", "Fast", "Slower (cross-validation)", "Fast"],
            "Performance": ["Moderate (linear)", "Moderate (tree-based)", "High (ensemble power)", "Moderate (sparse solution)", "Moderate (optimized sparse solution)", "Moderate (less variance)"],
            "Interpretability": ["High (easy to interpret)", "Moderate (visualizable)", "Low (complex ensemble)", "Moderate (sparse solution)", "Moderate (optimized sparse solution)", "Moderate (less variance)"]
        }
        preselection_df = pd.DataFrame(preselection_data)
        st.dataframe(preselection_df)

    with tab2:
        st.subheader("Detailed Model Results")
        data = {
            "Model": [
                "Linear regression", "Linear regression", "Lasso", "Lasso", "LassoCV", "LassoCV", "LassoCV", "Ridge", "Ridge",
                "Decision tree regressor", "Decision tree regressor", "Decision tree regressor",
                "Random forest regressor", "Random forest regressor", "Random forest regressor"
            ],
            "iteration #": ["1", "2 🥉", "1", "2", "1", "2 🥉", "3", "1", "2", "1", "2", "3 🥈", "1", "2", "3 🥇"],
            "R² train": [0.4353, 0.9198, 0.0000, 0.4350, 0.4213, 0.9194, 0.9194, 0.9194, 0.4350, 1.0000, 1.0000, 0.9953, 0.9996, 0.9996, 0.9997],
            "R² test": [0.4282, 0.9142, -0.0050, 0.4278, 0.4213, 0.9141, 0.9140, 0.9139, 0.4278, 0.9537, 0.9521, 0.9542, 0.9674, 0.9674, 0.9687],
            "MAE": [1314.5934, 0.0309, 0.1143, 1315, 1329, 0.0309, 0.0310, 0.0310, 1314.7879, 317, 0.0219, 0.0212, 0.0181, 264.8739, 0.0175],
            "MSE": [19239076, 453, 1673, 2499885.9195, 2552369.427, 453, 454, 0.0018, 19241922, 202207.9051, 0.0010, 0.0009, 0.0007, 3876430, 0.006],
            "(RMSE)": [1580.525829, 0.0418, 0.1432, 1581.1027, 1597.6137, 0.0419, 0.0419, 0.0419, 1581.105, 449.6753, 0.0313, 0.0307, 0.0258, 377.9374, 0.0252]
        }
        df = pd.DataFrame(data)

        # Highlight best models
        best_models = ["Random forest regressor", "Decision tree regressor", "LassoCV", "Linear regression"]
        best_iterations = ["3 🥇", "3 🥈", "2 🥉"]

        def highlight_rows(row):
            if row['Model'] in best_models and row['iteration #'] in best_iterations:
                return ['background-color: #A7DDBA'] * len(row)
            else:
                return [''] * len(row)

        styled_df = df.style.apply(highlight_rows, axis=1)
        st.dataframe(styled_df)

        st.warning(
            "Iteration 1 replaces region names with numerical labels using LabelEncoder and creates a boolean variable for Ile-de-France, while Iteration 2 switches to OneHotEncoding for better geographical representation and removes the is_IDF variable to avoid redundancy.",
            icon=":material/compare_arrows:"
        )

    with tab3:
        st.subheader("Performance Indicators")
        image = Image.open("Performace_RandomForrest.png")
        st.image(image, caption="Performance Model Indicators", use_container_width=True)
        st.info(
            "The model performance indicators of the QQ Plot indicate deviations from normality within the tails, even after improving the hyperparameters of the Random Forest (number of trees, maximum depth, minimum samples per leaf).",
            icon=":material/info:"
        )

# PAGE 5 # PREDICTION
if page == pages[5]:

    @st.cache_resource
    def load_model():
        with open('model_rf.pkl', 'rb') as model_file:
            model = pickle.load(model_file)
        return model

    @st.cache_resource
    def load_scaler():
        with open('scaler.pkl', 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)
        return scaler

    @st.cache_resource
    def load_ohe():
        with open('onehotencoder.pkl', 'rb') as ohe_file:
            ohe = pickle.load(ohe_file)
        return ohe

    @st.cache_data
    def load_feature_ranges():
        with open('feature_min_max.json', 'r') as json_file:
            feature_ranges = json.load(json_file)
        return feature_ranges

    @st.cache_data
    def load_original_features():
        with open('feature_names.json', 'r') as json_file:
            original_features = json.load(json_file)
        return original_features

    # Load model, scaler, and one hot encoder
    model = load_model()
    scaler = load_scaler()
    ohe = load_ohe()
    feature_ranges = load_feature_ranges()
    original_features = load_original_features()

    # Streamlit UI
    st.title("Energy Consumption Prediction")
    st.subheader("Using a Random Forest Regressor to predict Energy consumption in French regions")

    # Specific user inputs
    regions = [
        'Occitanie', 'Auvergne-Rhone-Alpes', 'Bourgogne-Franche-Comte',
        'Centre-Val de Loire', 'Grand Est', 'Ile-de-France', 'Pays de la Loire',
        'Nouvelle-Aquitaine', "Provence-Alpes-Cote d'Azur",
        'Hauts-de-France', 'Normandie', 'Bretagne'
    ]
    region = st.selectbox("Region", regions)
    tavg = st.slider("Average Temperature of the Day", -15, 40, 15)
    year = st.slider("Year", 2016, 2023, 2019)
    month = st.slider("Month", 1, 12, 6)
    hour = st.slider("Time of Day", 0, 23, 12)

    # Prepare input data
    def prepare_input_data(tavg, year, region, month, hour):
        input_df = pd.DataFrame({
            "TAvg": [tavg],
            "Year": [year],
            "Month": [month],
            "Hour_numerical": [hour],
            "Region": [region],
            "Day_type": ["workday"],
            "Season": ["Summer"],
        })

        categorical_cols = ["Day_type", "Season", "Month", "Region"]
        input_encoded = pd.DataFrame(ohe.transform(input_df[categorical_cols]), columns=ohe.get_feature_names_out(categorical_cols))
        input_df = pd.concat([input_df.drop(columns=categorical_cols), input_encoded], axis=1)

        numeric_cols = list(feature_ranges.keys())
        missing_cols = [col for col in numeric_cols if col not in input_df.columns]
        for col in missing_cols:
            input_df[col] = (feature_ranges[col]['min'] + feature_ranges[col]['max']) / 2

        input_df[numeric_cols] = scaler.transform(input_df[numeric_cols])

        input_list = [input_df[feature].values[0] if feature in input_df.columns else 0 for feature in original_features]

        return np.array([input_list])

    # Predict energy consumption
    if st.button("Predict Consumption"):
        with st.spinner('Predicting Energy Consumption...'):
            input_data = prepare_input_data(tavg, year, region, month, hour)
            prediction = model.predict(input_data)[0]
        st.markdown(f"<h3>Predicted Consumption: {prediction:.4f} MW</h3>", unsafe_allow_html=True)

    # Always display feature importance graph below the prediction button
    def feature_importance_graph():
        image = Image.open("feature_importance.png")
        st.image(image, caption="Feature Importance", use_container_width=True)

    feature_importance_graph()


# PAGE 6 # CONCLUSION
if page == pages[6]:
    st.balloons()
    st.title("Electricity Consumption Prediction Summary")

    st.header("Project Overview")
    st.write("""
    We developed supervised machine learning models to predict electricity consumption using a large dataset (nearly 1.5 million rows).
    We focused on feature engineering, particularly categorical encoding, and hyperparameter tuning.
    """)

    st.header("Model Performance")
    st.write("""
    * **Linear Models (Linear Regression, LassoCV):** Performed well, with LassoCV benefiting from cross-validation.
    * **Tree-Based Models (Decision Tree, Random Forest):** Achieved the best performance, with Random Forest outperforming Decision Tree due to reduced overfitting.
    """)

    st.header("Key Findings")
    st.write("""
    * Despite impressive metrics, the models' Mean Absolute Error (around 257 MW) represents a significant amount of electricity, comparable to the consumption of a medium-sized city.
    * The models' lifespan is estimated at 3-5 years due to evolving factors like smart meters, electric vehicles, climate change, and new data centers.
    * The models' performance will likely decline over time.
    """)

    st.header("Lessons Learned")
    st.write("""
    * Extensive research was crucial to understand the data and industry.
    * Technical skills in machine learning model documentation and hyperparameter tuning were developed.
    * Future work includes enhancing the presentation with Streamlit and Plotly for interactivity.
    """)

    st.header("Acknowledgements")
    st.write("""
    We extend our gratitude to our mentor, Tarik Anouar, for his invaluable support.
    """)
