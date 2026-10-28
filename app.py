import streamlit as st
import requests
import plotly.express as px
import pandas as pd

URL = "https://countriesnow.space/api/v0.1/countries/population"

SITE_PAGES = [
    "Home",
    "World Population",
    "Country Insights"
]

###########################################################################

def get_countries(countries_data):
    countries = [item["country"] for item in countries_data]

    # This is necessary because the first 47 elements pertain to income, continent, and region population data instead of specific countries    
    return countries[46:]

def render_country(country, countries_data):
    country_to_view = [item for item in countries_data if item["country"] == country]

    if not country_to_view:
        return

    st.header(f"Population Timeline of {country}")

    
    population = pd.DataFrame(country_to_view[0]["populationCounts"])

    fig = px.bar(population, x="year", y="value", title="Population Growth Over Time", labels={"year" : "Year", "value" : "Population"})
    st.plotly_chart(fig, use_container_width=True)

def render_home_page():
    st.title(body="Country Population Viewer")
    
    st.write("""
    Welcome to the Country Population Viewer.
    The purpose of this app is to view and analyze population metrics around the world.

    To view insights, navigate the pages using the sidebar on the left.""")

    st.image(image="https://geology.com/world/world-map-360.gif")

def main():
    response = requests.get(url=URL).json()
    countries_data = response.get("data", [])

    current_page = st.sidebar.radio("Pages", options=SITE_PAGES, index=0)

    if current_page == "Home":
        render_home_page()

    elif current_page == "World Population":
        render_country("World", countries_data)

    elif current_page == "Country Insights":
        countries = get_countries(countries_data) 
        current_country = st.selectbox(label="Select a Country", options=countries)
        render_country(current_country, countries_data)


if __name__ == "__main__":
    main()