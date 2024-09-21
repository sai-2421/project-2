import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import pandas as pd 
import mysql.connector as db
import plotly.express as px
import json
import requests
import numpy as np
import matplotlib.pyplot as plt



mydb = db.connect(  
 host="localhost",
 user="root",
 password="",
 database="phonepe"
)

mycursor = mydb.cursor(buffered=True)

# --------------------------------------------------Logo & details 

# Set page configuration
st.set_page_config(
    page_title="PHONEPE PULSE DATA VISUALIZATION | By Sai Gayathri A",
    page_icon="pulse1.png",  
    layout="wide",
    initial_sidebar_state="expanded"
)


st.title("Welcome to PhonePe Pulse Data Visualization")
        #------------------------------------------------------------------HEADER common to all menu

col,coll = st.columns([3,2],gap="small")
with col:
      st.image("pe.png",width=500)
with coll:
     st.write(" ")
     st.write(" ")
     st.write(" ")
     st.write(" ")
     st.write(" ")
     st.write(" ")
     
     st.markdown("## :violet[*Data*] *Visualization* :violet[*And*] *Exploration*")
     
     st.markdown("""
                    <style>
                    .centered-text {
                        text-align: center;
                        font-style: italic;

                    }
                    </style>
                    <div class="centered-text">
                        A User-Friendly Tool Using Streamlit and Plotly
                    </div>
                    """, unsafe_allow_html=True)
     


selected = option_menu("Phonepe Pulse | The Beat Of Progress", ["Home","Explore Data","Insights"],
                icons=["house","bar-chart-line","graph-up-arrow", "exclamation-circle"],
                menu_icon="pe.png",
                default_index=0,
                orientation='horizontal',
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})

# ----------------------------------------------------------------------------------- HOME

def home():
 if selected == "Home":
    st.image("phn.png",width=550)

    st.markdown("""
                    <div style="font-size:40px; font-weight:bold; color:#f75f85; display:inline;"> PHONEPE DATA VISUALIZATION AND EXPLORATION </div>
                    <div style="font-size:20px; font-weight:bold;display:inline;">| A User-Friendly Tool Using Streamlit and Plotly |</div>
                    """, unsafe_allow_html=True)


    col1, col2 = st.columns([3,2], gap="medium")

        
    with col1:
            st.write(" ")
            st.markdown("### :violet[DOMAIN :] FINTECH")
            st.markdown("""
                ### :violet[TECHNOLOGIES USED :]
                
                - GITHUB CLONING
                - PYTHON
                - PANDAS
                - MYSQL
                - STREAMLIT
                - PLOTLY
            """)
            st.markdown("### :violet[OVERVIEW :] This Phonepe pulse Github repository contains a large amount of data related to various metrics and statistics. The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.")

            with col2:
                   st.image("ppp.png",width=550)
       
home()


               #------------------- ANALYSIS OVER Map          
# -------------------------------------------------- EXPLORE DATA   - TRANSACTIONS

def explore_data():
    if selected == "Explore Data":
        tabm, tabc = st.tabs(["**Analysis over Map**", "**Analysis over Chart**"])

        with tabm:
            tab1, tab2 = st.tabs(["**TRANSACTION**", "**USER**"])

            # TRANSACTION TAB
            with tab1:
                col1, col2, col3 = st.columns(3)
                with col1:
                    year = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023'), key='year')
                with col2:
                    quarter = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='quarter')
                with col3:
                    type = st.selectbox('**Select Transaction type**',
                                        ('Recharge & bill payments', 'Peer-to-peer payments',
                                         'Merchant payments', 'Financial Services', 'Others'), key='type')

                mycursor.execute(
                    f"""SELECT State, Transaction_Amount 
                        FROM aggregate_transaction 
                        WHERE Year = '{year}' 
                        AND Quarter = '{quarter}' 
                        AND Transaction_Type = '{type}';""")  # Use triple quotes for the f-string
                
                df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transaction_Amount'])
                
                fig = px.bar(df,
                             x='State',
                             y='Transaction_Amount',
                             title='Transaction Amount by State',
                             labels={'Transaction_Amount': 'Transaction Amount'},
                             color='Transaction_Amount',
                             color_continuous_scale=px.colors.sequential.Agsunset)

                # Display the Plotly chart in Streamlit
                st.plotly_chart(fig, use_container_width=True)



                mycursor.execute(
                    f"""SELECT State, Transaction_Count, Transaction_Amount 
                        FROM aggregate_transaction 
                        WHERE Year = '{year}' 
                        AND Quarter = '{quarter}' 
                        AND Transaction_Type = '{type}';""")
                df0 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transaction_Count', 'Transaction_Amount'])
                df_anly = df0.set_index(pd.Index(range(1, len(df0) + 1)))

                # GEO VISUALIZATION
                df.drop(columns=['State'], inplace=True)
                # Cloning data

                url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response = requests.get(url)
                data1 = json.loads(response.content)
                state_name = [feature['properties']['ST_NM'] for feature in data1['features']]
                state_name.sort()
                df_state_name = pd.DataFrame({'State': state_name})
                df_state_name['Transaction_Amount'] = df
                df_state_name.to_csv('aggtrans_state.csv', index=False)
                df_tra = pd.read_csv('aggtrans_state.csv')

                # Geo plot
                fig_tra = px.choropleth(
                    df_tra,
                    geojson=url,
                    featureidkey='properties.ST_NM', locations='State', color='Transaction_Amount',
                    color_continuous_scale='Agsunset', title='Transaction Analysis')
                fig_tra.update_geos(fitbounds="locations", visible=False)
                fig_tra.update_layout(title_font=dict(size=33), title_font_color='#AD71EF', height=800)
                st.plotly_chart(fig_tra, use_container_width=True)

                df_anly['State'] = df_anly['State'].astype(str)
                df_anly['Transaction_Count'] = df_anly['Transaction_Count'].astype(int)

                # Create the pie chart
                df_anly_fig = px.pie(df_anly,
                                     values='Transaction_Count',
                                     names='State',
                                     color='Transaction_Count',
                                     title='Transaction Analysis Chart',
                                     height=700)

                df_anly_fig.update_layout(title_font=dict(size=33), title_font_color='#FF033E')
                st.plotly_chart(df_anly_fig, use_container_width=True)
                st.subheader(':violet[Transaction Analysis of Total calculation]')
                st.dataframe(df_anly)

            # USER TAB
            with tab2:
                col1, col2, col3 = st.columns(3)
                with col1:
                    yr = st.selectbox('***Select Year***', ('2018', '2019', '2020', '2021', '2022', '2023'), key='yr')
                with col2:
                    qtr = st.selectbox('***Select Quarter***', ('1', '2', '3', '4'), key='qtr')
                with col3:
                    brand = st.selectbox('***Select Brand_Name***', ('Xiaomi', 'Samsung', 'Vivo', 'Oppo', 'OnePlus',
                                                                     'Realme', 'Apple', 'Motorola', 'Lenovo', 'Huawei',
                                                                     'Others', 'Tecno'), key='brand')

                mycursor.execute(
                    f"""SELECT State,SUM(Count), Brand_Name
                         FROM aggregate_user 
                         WHERE Year = '{yr}' 
                         AND Quarter = '{qtr}' 
                         AND Brand_Name= '{brand}' 
                         GROUP BY State , Brand_Name;""")
                df03 = mycursor.fetchall()

                if df03:
                    df3 = pd.DataFrame(np.array(df03), columns=['State', 'User Count', 'Brand_Name'])
                    df_userbar = df3.set_index(pd.Index(range(1, len(df3) + 1)))

                    # GEO VISUALIZATION FOR USER
                    df3.drop(columns=['State', 'Brand_Name'], inplace=True)
                    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                    response = requests.get(url)
                    data2 = json.loads(response.content)
                    state_names = [feature['properties']['ST_NM'] for feature in data2['features']]
                    state_names.sort()
                    df_state_names = pd.DataFrame({'State': state_names})
                    df_state_names['User Count'] = df3
                    df_state_names.to_csv('user_state.csv', index=False)
                    df_use = pd.read_csv('user_state.csv')

                    # Geo plot
                    fig_use = px.choropleth(
                        df_use,
                        geojson=url,
                        featureidkey='properties.ST_NM', locations='State', color='User Count',
                        color_continuous_scale='ylgn', title='User Analysis')
                    fig_use.update_geos(fitbounds="locations", visible=False)
                    fig_use.update_layout(title_font=dict(size=33), title_font_color='#FF033E', height=800)
                    st.plotly_chart(fig_use, use_container_width=True)

                    df_userbar['State'] = df_userbar['State'].astype(str)
                    df_userbar['User Count'] = df_userbar['User Count'].astype(int)
                    df_userbar_fig = px.bar(df_userbar, x='State', y='User Count', color='User Count',
                                            color_continuous_scale='ylgn', title='User Analysis Chart',
                                            height=700)
                    df_userbar_fig.update_layout(title_font=dict(size=33), title_font_color='#FF033E')
                    st.plotly_chart(df_userbar_fig, use_container_width=True)

                    st.subheader(':violet[User Analysis of Total calculation]')
                    st.dataframe(df_userbar)
                else:
                    st.write(" OOPS ! No data found ")

        # Analysis over Chart
        with tabc:
            st.markdown("## :violet[Top Charts]")

            types = st.selectbox('***Select Type***', ('Transactions', 'Users'))
            if types == 'Transactions':
                Years = st.slider("**Year**", min_value=2018, max_value=2023)
                Quarter = st.slider("Quarter", min_value=1, max_value=4)

                tab1, tab2, tab3 = st.tabs(["State", "District", "Pincode"])
                with tab1:
                    st.markdown("### :violet[State]")
                    mycursor.execute(f"""select State, 
                                        sum(Transaction_Count) as Total_Transactions_Count, sum(Transaction_Amount) as Total_Transaction_Amount 
                                     FROM aggregate_transaction
                                     WHERE Year = {Years} 
                                     AND Quarter = {Quarter} 
                                     GROUP BY State 
                                     ORDER BY Total_Transaction_Amount DESC 
                                     limit 10""")
                    df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transactions_Count','Total_Transaction_Amount'])
                    fig = px.pie(df, values='Total_Transaction_Amount',
                                 names='State',
                                 title='Top 10 State based on Total number of transaction and Total amount spent on phonepe.', width=1000, height=600,
                                 color_discrete_sequence=px.colors.sequential.Viridis,
                                 hover_data=['Total_Transactions_Count'],
                                 labels={'Total_Transactions_Count':'Total_Transactions_Count'})

                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)

                with tab2:
                    st.markdown("### :violet[District]")
                    mycursor.execute(f"""select District, 
                                        sum(Count) as Total_Count, sum(Amount) as Total_Amount 
                                     FROM map_transaction 
                                     WHERE Year = {Years} 
                                     AND Quarter = {Quarter} 
                                     GROUP BY District 
                                     ORDER BY Total_Amount DESC
                                     limit 10""")
                    df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

                    fig = px.pie(df, values='Total_Amount',
                                 names='District', width=1000, height=600,
                                 title='Top 10 District based on Total number of transaction and Total amount spent on phonepe.',
                                 color_discrete_sequence=px.colors.sequential.Agsunset,
                                 hover_data=['Transactions_Count'],
                                 labels={'Transactions_Count':'Transactions_Count'})

                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)

                with tab3:
                    st.markdown("### :violet[Pincode]")
                    mycursor.execute(f"""select Pincode, 
                                        sum(Transaction_Count) as Total_Transactions_Count, sum(Transaction_Amount) as Total_Transaction_Amount 
                                     FROM top_transaction 
                                     WHERE Year = {Years} 
                                     AND Quarter = {Quarter} 
                                     GROUP BY Pincode 
                                     ORDER BY Total_Transaction_Amount DESC 
                                     limit 10""")
                    df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Transactions_Count','Total_Transaction_Amount'])
                    fig = px.pie(df, values='Total_Transaction_Amount',
                                 names='Pincode', width=1000, height=600,
                                 title='Top 10 Pincode based on Total number of transaction and Total amount spent on phonepe.',
                                 color_discrete_sequence=px.colors.sequential.Blugrn,
                                 hover_data=['Total_Transactions_Count'],
                                 labels={'Total_Transactions_Count':'Total_Transactions_Count'})

                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)

            elif types == 'Users':
                Years = st.slider("**Year**", min_value=2018, max_value=2023)
                Quarter = st.slider("Quarter", min_value=1, max_value=4)

                tab1, tab2, tab3, tab4 = st.tabs(["Brands", "District", "Pincode", "State"])
                with tab1:
                    st.markdown("### :violet[Brands]")
                    mycursor.execute(f"""select Brand_Name, 
                                        sum(Count) as Total_Users, avg(Percentage)*100 as Avg_Percentage 
                                     FROM aggregate_user
                                     WHERE Year = {Years} 
                                     ANDQuarter = {Quarter} 
                                     GROUP BY Brand_Name 
                                     ORDER BY Total_Users DESC 
                                     limit 10""")
                    df = pd.DataFrame(mycursor.fetchall(), columns=['Brand_Name', 'Total_Users','Avg_Percentage'])
                    fig = px.bar(df,
                                 title='Top 10 mobile brands and its percentage based on the how many people use phonepe.',
                                 y="Total_Users",
                                 x="Brand_Name",
                                 color='Avg_Percentage',
                                 color_continuous_scale=px.colors.sequential.Agsunset)
                    st.plotly_chart(fig, use_container_width=True)

                with tab2:
                    st.markdown("### :violet[District]")
                    mycursor.execute(f"""select District, 
                                        sum(Registered_Users) as Total_Users, sum(App_Opens) as Total_AppOpens 
                                     FROM map_users 
                                     WHERE Year = {Years} 
                                     AND Quarter = {Quarter} 
                                     GROUP BY District 
                                     ORDER BY Total_Users DESC 
                                     limit 10""")
                    df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_AppOpens'])
                    fig = px.bar(df,
                                 title='Top 10 District based on Total phonepe users and their app opening frequency',
                                 y="Total_Users",
                                 x="District",
                                 color='Total_Users',
                                 color_continuous_scale=px.colors.sequential.Tealgrn)
                    st.plotly_chart(fig, use_container_width=True)

                with tab3:
                    st.markdown("### :violet[Pincode]")
                    mycursor.execute(f"""select Pincode, 
                                        sum(Registered_Users) as Total_Users 
                                     FROM top_users 
                                     WHERE Year = {Years} 
                                     AND Quarter = {Quarter} 
                                     GROUP BY Pincode 
                                     order by Total_Users DESC 
                                     limit 10""")
                    df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
                    fig = px.bar(df,
                                 title='Top 10 Pincode based on Total phonepe users and their app opening frequency',
                                 x='Total_Users',
                                 y='Pincode',
                                 color='Total_Users',
                                 color_continuous_scale=px.colors.sequential.Aggrnyl)
                    st.plotly_chart(fig, use_container_width=True)

                with tab4:
                    st.markdown("### :violet[State]")
                    mycursor.execute(f"""select State, 
                                        sum(Registered_Users) as Total_Users, sum(App_Opens) as Total_AppOpens 
                                     FROM map_users 
                                     WHERE Year = {Years} 
                                     AND Quarter = {Quarter} 
                                     GROUP BY State 
                                     ORDER BY Total_Users DESCC 
                                     limit 10""")
                    df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_AppOpens'])
                    fig = px.bar(df,
                                 y='Total_Users',
                                 x='State',
                                 title='Top 10 State based on Total phonepe users and their app opening frequency',
                                 color='Total_Users',
                                 color_discrete_sequence=px.colors.sequential.Agsunset)

                    st.plotly_chart(fig, use_container_width=True)

explore_data()
 ################################################################################################# Insights 
def insights():
  if selected == "Insights":
    questions=st.selectbox("Shoot Your Question",
                                    ["Choose your Questions...",
                                     '1.Which district within a state has the lowest number of users over years and quartes?',
                                     '2. What are all the top 10 pincode in india with the highest number of transactions and users?',
                                     '3. How do transaction amounts or counts vary across different states over Year?',
                                     '4.Which states have the highest percentage of device users among all and what are their brand names ?',
                                     '5.Which district within a state has the highest number of phonepe users?',
                                     '6.Top Brands Of Mobiles Used by phonepe users across the states of india',
                                     "7.India's Top 15 States With Phonepe App Opens",
                                     "8.Which brands are most frequently involved in transactions",
                                     "9.How many users registered on the platform each year? ",
                                     " 10.Which1 15 state had the lowest total transaction amount in 2023 " ],
                                      index=0)
   
    if questions == '1.Which district within a state has the lowest number of users over years and quartes?':
                    Year = st.slider("**Year**", min_value=2018, max_value=2023)
                    Quarter = st.slider("Quarter", min_value=1, max_value=4)
                    mycursor.execute(f"""SELECT u.State, u.Year, u.Quarter, u.District, u.Registered_Users 
                                      FROM map_users u
                                      JOIN (
                                            SELECT State, Year, Quarter, MIN(Registered_Users) AS min_Users  
                                            FROM map_users
                                            WHERE Year = {Year} AND Quarter = {Quarter}
                                            GROUP BY State, Year, Quarter 
                                        )min_users 
                                        ON u.State = min_users.State
                                        AND u.Year = min_users.Year 
                                        AND u.Quarter = min_users.Quarter 
                                        AND u.Registered_Users = min_users.min_Users; """)
                    df = pd.DataFrame(mycursor.fetchall(), columns=['State','Year','Quarter','District','Registered_Users'])
                    st.write(df)
                    bar_chart = px.bar(df, x='District', y='Registered_Users', color='State',width=1300,height=700,
                    title='District with lowest Number of Users by State',
                    labels={'District': 'District', 'Registered_Users': 'Number of Users'})
                    st.plotly_chart(bar_chart) 

    elif questions =='2. What are all the top 10 pincode in india with the highest number of transactions and users?':
                      mycursor.execute("""SELECT State,Pincode,
                                             MAX(Max_Registered_Users) AS Max_Registered_Users, 
                                            MAX(Max_Transaction_Count) AS Max_Transaction_Count
                                            FROM(
                                                SELECT State,Pincode,
                                                     MAX(Registered_Users) AS Max_Registered_Users,
                                                     NULL AS Max_Transaction_Count
                                            FROM phonepe.top_users
                                            GROUP BY State,Pincode
                                            UNION ALL
                                            SELECT State,Pincode,
                                                 NULL AS Max_Registered_Users, 
                                                MAX(Transaction_Count) AS Max_Transaction_Count
                                            FROM phonepe.top_transaction 
                                            GROUP BY State,Pincode)
                                        AS combined
                                        GROUP BY State,Pincode 
                                        ORDER BY MAX(Max_Registered_Users) DESC, MAX(Max_Transaction_Count) DESC
                                        LIMIT 10;""")
                      df=pd.DataFrame(mycursor.fetchall(), columns=['State','Pincode','Max_Registered_Users','Max_Transaction_Count'])
                      st.write(df)
                      fig = px.scatter_3d(df, x='Max_Registered_Users', y='Max_Transaction_Count', z='Pincode',
                        color='State',  size_max=20,  opacity=0.7, 
                        labels={'Max_Registered_Users': 'reg-users', 'Max_Transaction_Count': 'trans-count', 'Pincode': 'Pincode'},
                        title='THE TOP 10 BUSIEST PINCODE OF INDIA ')
                      fig.update_layout(template='plotly_white',width=1500, height=700)
                      st.plotly_chart(fig)
                      
    elif questions =='3. How do transaction amounts or counts vary across different states over Year?':
                        year = st.slider("**Year**", min_value=2018, max_value=2023)
                        query = """SELECT State,
                                         SUM(Transaction_Count) AS Total_Transaction_Count,  
                                         SUM(Transaction_Amount) AS Total_Transaction_Amount
                                  FROM aggregate_transaction
                                  WHERE Year = %s 
                                  GROUP BY State
                                  ORDER BY State ASC;"""
                        mycursor.execute(query, (year,))
                        df=pd.DataFrame(mycursor.fetchall(),columns=['State','Total_Transaction_Count','Total_Transaction_Amount'])
                        st.write(df)
                        df_long = pd.melt(df, id_vars=['State'], value_vars=['Total_Transaction_Count', 'Total_Transaction_Amount'], var_name='Metric', value_name='Total')
                        fig = px.area(df_long, x='State', y='Total', color='Metric',
                                    labels={'State': 'State', 'Total': 'Total', 'Metric': 'Metric'},title='Total Transaction Count and Amount by State',
                                            width=1500, height=700)
                        st.plotly_chart(fig)

    elif questions =='4.Which states have the highest percentage of device users among all and what are their brand names ?':
                mycursor.execute("""SELECT State,Brand_Name,
                                             MAX(Percentage) AS High_Percentage 
                                    FROM aggregate_user
                                    GROUP BY State,Brand_Name
                                    ORDER BY  High_Percentage DESC
                                    LIMIT 10;""" )
                df=pd.DataFrame(mycursor.fetchall(),columns=['State','Brand_Name','High_Percentage'])
                st.write(df)
                fig = px.bar(df, x='State', y='High_Percentage', color='Brand_Name', title='Highest Percentage of Users by State and theirs Brand', width=1300, height=700)
                fig.update_layout(xaxis_title='State', yaxis_title='Highest Percentage')
                st.plotly_chart(fig)

    elif questions =='5.Which district within a state has the highest number of phonepe users?':
              mycursor.execute("""SELECT State, District, Registered_Users 
                                  FROM ( 
                                        SELECT  State, District, Registered_Users,
                                        ROW_NUMBER() OVER (PARTITION BY State ORDER BY Registered_Users DESC) AS row_num
                                        FROM phonepe.map_users
                                    ) AS ranked_users  
                                    WHERE  row_num = 1;""")                              
              df=pd.DataFrame(mycursor.fetchall(),columns=['State','District','Registered_Users'])
              st.write(df)
              fig = px.pie(df, values='Registered_Users', names='District', title='Districts with Highest Number of Users by State', hole=0.3 , width=1400,height=800)
              st.plotly_chart(fig)

    elif questions =='6.Top Brands Of Mobiles Used by phonepe users across the states of india':
             mycursor.execute("""SELECT Brand_Name,
                                    SUM(Count) AS Total_Users 
                              FROM aggregate_user 
                              GROUP BY Brand_Name 
                              ORDER BY Total_Users DESC 
                              LIMIT 10;""")
             df=pd.DataFrame(mycursor.fetchall(),columns=['Brand_Name','Total_Users'])
             st.write(df)
             fig = px.bar(df, x='Brand_Name', y='Total_Users',  color='Total_Users',width=1200,height=700,
             title='Top Mobile Brands',
             labels={'Total_Users': 'Total Users', 'Brand_Name': 'Brand Name'})
             st.plotly_chart(fig)

    elif questions =="7.India's Top 15 States With Phonepe App Opens":
                           mycursor.execute("""SELECT State,
                                                         SUM(App_Opens) AS Total_App_Opens 
                                                FROM map_users 
                                                GROUP BY State ORDER BY Total_App_Opens DESC
                                                LIMIT 15;""")
                           df=pd.DataFrame(mycursor.fetchall(),columns=['State','Total_App_Opens'])
                           st.write(df)
                           fig = px.line(df, x='State', y='Total_App_Opens', title='Top App Opens by State',width=1300,height=600)
                           fig.update_traces(texttemplate='%{text}', textposition='top center', mode='markers+lines')
                           fig.update_layout(xaxis_title='State', yaxis_title='Total_App_Opens')  
                           st.plotly_chart(fig)

    elif questions =="8.Which brands are most frequently involved in transactions":
                            mycursor.execute("""SELECT au.State, au.Brand_Name, 
                                                    SUM(au.Count) AS Total_Transactions 
                                                FROM aggregate_user au
                                                JOIN aggregate_transaction at
                                                        ON au.State = at.State  
                                                GROUP BY au.State, au.Brand_Name
                                                ORDER BY
                                                Total_Transactions DESC
                                                limit 10;""")
                            df=pd.DataFrame(mycursor.fetchall(),columns=['State','Brand_Name','Total_Transactions'])
                            st.write(df)
                            fig = px.area(df, color='State', y='Total_Transactions', x='Brand_Name', width=1300,height=600,title='Top 10 Brands Involved in Transactions by State')
                            fig.update_layout(xaxis_title='Brand_Name', yaxis_title='Total Transactions', legend_title='Brands')
                            st.plotly_chart(fig)  

    elif questions =="9.How many users registered on the platform each year? ":    
            mycursor.execute("""SELECT  Year, 
                                    SUM(Count) AS Total_Registered_Users 
                                FROM aggregate_user 
                                GROUP BY Year
                                ORDER BY Year;""")
            df=pd.DataFrame(mycursor.fetchall(),columns=['Year','Total_Registered_Users'])
            st.write(df)
            fig = px.pie(df, names='Year', values='Total_Registered_Users', title='Registered users year wise', hole=0.3 , width=1400,height=800)
            st.plotly_chart(fig)

    elif questions ==" 10.Which1 15 state had the lowest total transaction amount in 2023 ": 
             mycursor.execute("""SELECT State, 
                                        SUM(Transaction_Amount) AS Total_Transaction_Amount
                                 FROM aggregate_transaction 
                                 WHERE Year = 2023 
                                 GROUP BY State
                                 ORDER BY Total_Transaction_Amount ASC 
                                 LIMIT 15;""")
             df=pd.DataFrame(mycursor.fetchall(),columns=['State','Total_Transaction_Amount'])
             st.write(df)
             fig = px.bar(df, x='State', y='Total_Transaction_Amount',  color='Total_Transaction_Amount',width=1200,height=700,
             title='Lowest Transactions States in the Latest Year:2023',
             labels={'Total_Transaction_Amount': 'Total Total_Transaction_Amount', 'State': 'Brand State'})
             st.plotly_chart(fig, use_container_width=True)    

    st.cache_data()
insights()


