import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


AIRFLOW_HOME = "/home/mythili/becode/Immo_airflow/airflow"
data = pd.read_csv(AIRFLOW_HOME + '/dags/data/cleaned.csv')

# Streamlit app title
st.title("Real Estate Property Explorer")

# Add a sidebar for user interaction
st.sidebar.subheader("Agenda")

# Create a radio button to select agenda items
selected_agenda_item = st.sidebar.radio("Select one to view", ["Introduction", "Exploring the dataset",
                                                                "Visualisation", "Interactive Visualisation",
                                                                "Final notes"])

# Based on the selected agenda item, display the corresponding content
if selected_agenda_item == "Introduction":
    st.write("Welcome to exploring list of houses and apartments with scraped data. ")
    st.write("In this page you can see some visualisation and entire dataset which you can filter to see the availability of desired house or apartment. ")
elif selected_agenda_item == "Visualisation":

    # Create a countplot
    countplot_fig, countplot_ax = plt.subplots(figsize=(8, 6))
    sns.countplot(data=data, x="type_of_property", ax=countplot_ax)
    countplot_ax.set_xlabel("Property Type")
    countplot_ax.set_ylabel("Count")
    countplot_ax.set_title("Count of Houses and Apartments")
    st.pyplot(countplot_fig)

    # Create a box plot
    boxplot_fig, boxplot_ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(data=data, x="type_of_property", y="price", ax=boxplot_ax)
    boxplot_ax.set_xlabel("Property Type")
    boxplot_ax.set_ylabel("Price")
    boxplot_ax.set_title("Price Distribution for Houses and Apartments")
    st.pyplot(boxplot_fig)

    # Visualization 1: Histogram of Prices
    st.subheader("Price Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data['price'], kde=True, ax=ax)
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    st.pyplot(fig)

    # Visualization 2: Scatter Plot (Example: Bedrooms vs. Price)
    st.subheader("Scatter Plot: Bedrooms vs. Price")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=data, x='bedrooms', y='price', ax=ax)
    plt.xlabel("Number of Bedrooms")
    plt.ylabel("Price")
    st.pyplot(fig)

elif selected_agenda_item == "Interactive Visualisation":
    # interactive line chart using Plotly to visualize trends over time, such as price changes.
    st.subheader("Interactive Line Chart")
    fig = px.line(data, x="bedrooms", y="price", color="type_of_property", title="Price Trends")
    st.plotly_chart(fig)    

    # interactive scatter plots, which can be useful for exploring relationships between variables.
    st.subheader("Interactive Scatter Plot")
    fig = px.scatter(data, x="bedrooms", y="price", color="type_of_property", title="Bedrooms vs. Price")
    st.plotly_chart(fig)
    # Interactive 3D scatter plot
    st.subheader("Interactive 3D Scatter Plot")
    fig = px.scatter_3d(data, x="bedrooms", y="price", z="bathrooms", color="type_of_property", title="3D Plot")
    st.plotly_chart(fig)

    # Interactive bar chart
    st.subheader("Interactive Bar Chart")
    fig = px.bar(data, x="type_of_property", y="price", color="type_of_property", title="Average Price by Property Type")
    st.plotly_chart(fig)

elif selected_agenda_item == "Exploring the dataset":
    # Filtering options
    st.sidebar.subheader("Filters")

    property_type = st.sidebar.selectbox("1) Select Property Type", ['All', 'apartment', 'house'])
    min_price = float(0)
    max_price = float(data['price'].max())
    price = st.sidebar.slider('2) Select range of price', min_value=min_price, max_value=max_price)
    bedrooms = st.sidebar.slider("3) Number of Bedrooms", min_value=0, max_value=data['bedrooms'].max(), step=1)
    energy_class = st.sidebar.selectbox("4) Select Energy Class", ['All', 'A', 'B', 'C', 'D', 'F', 'G', 'NS'])
    kitchen_type = st.sidebar.selectbox("5) Select Kitchen Type", ['All', 'Installed', 'USA installed', 'Hyper equipped', 'Semi equipped'])
    heating_type = st.sidebar.selectbox("6) Select Heating Type", ['All', 'Fuel oil', 'Gas', 'Electric'])
    building_condition_type = st.sidebar.selectbox("7) Select Building Condition", ['All', 'Good', 'As new', 'To be done up', 'Just renovated'])

    # Copy the data to filtered_data
    filtered_data = data.copy()

    # Apply filters based on user selections
    if property_type != 'All':
        filtered_data = filtered_data[filtered_data['type_of_property'] == property_type]
    if kitchen_type != 'All':
        filtered_data = filtered_data[filtered_data['kitchen_type'] == kitchen_type]
    if heating_type != 'All':
        filtered_data = filtered_data[filtered_data['heating_type'] == heating_type]
    if building_condition_type != 'All':
        filtered_data = filtered_data[filtered_data['building_condition'] == building_condition_type]
    if price > 0:
        filtered_data = filtered_data[filtered_data['price'] > price]
    if bedrooms > 0:
        filtered_data = filtered_data[filtered_data['bedrooms'] == bedrooms]
    if energy_class != 'All':
        filtered_data = filtered_data[filtered_data['energy_class'] == energy_class]

    # Display filtered data
    st.write("Displaying Results")
    st.write(filtered_data)

elif selected_agenda_item == "Final notes":
    st.write("Thank you for exploring the dataset and visualisation.")
