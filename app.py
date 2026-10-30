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

    population_df = pd.DataFrame(country_to_view[0]["populationCounts"])

    latest_year = population_df.iloc[-1]["year"]
    latest_population = population_df.iloc[-1]["value"]
    earliest_year = population_df.iloc[0]["year"]
    earliest_population = population_df.iloc[0]["value"]

    left, right = st.columns(2)
    left.metric(f"Population in {latest_year}", f"{latest_population:,.0f}")
    right.metric(f"Population in {earliest_year}", f"{earliest_population:,.0f}")

    fig = px.bar(population_df, x="year", y="value", title="Population Growth Over Time", labels={"year" : "Year", "value" : "Population"}, color="value", color_continuous_scale="Plasma")
    st.plotly_chart(fig, use_container_width=True)

def render_home_page():
    st.title(body="Country Population Viewer")
    
    st.write("""
    Welcome to the Country Population Viewer. 

    This page provides interactive visualizations to help you understand how populations have evolved over time across the globe.""")


    st.markdown("""
    * **World Population:** View aggregated global growth trajectories over time.
    * **Country Insights:** Select specific nations to examine historical population trends and milestones.
    """)

    st.info("Select a page from the sidebar on the left to begin exploring.")
    
    st.image(image="https://geology.com/world/world-map-360.gif", caption="Global Map Overview", use_container_width=True)

def render_world_population(countries_data):
    world_data = [item for item in countries_data if item["country"] == "World"]

    if not world_data:
        st.error("World population data cannot be found.")
        return

    st.header("Global Population Overview")

    population_df = pd.DataFrame(world_data[0]["populationCounts"])

    latest_year = population_df.iloc[-1]["year"]
    latest_population = population_df.iloc[-1]["value"]
    earliest_year = population_df.iloc[0]["year"]
    earliest_population = population_df.iloc[0]["value"]

    left, right = st.columns(2)
    left.metric(f"Population in {latest_year}", f"{latest_population:,.0f}")
    right.metric(f"Population in {earliest_year}", f"{earliest_population:,.0f}")

    fig = px.bar(population_df, x="year", y="value", title="Global Population Growth Over Time", labels={"year" : "Year", "value" : "Population"}, color="value", color_continuous_scale="Plasma")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 10 Most Populated Countries")

    country_populations = []
    for item in countries_data[46:]:
        country_name = item["country"]
        country_population = item["populationCounts"]

        if country_population and country_name != "World":
            latest = country_population[-1]
            country_populations.append({
                "country": country_name,
                "population": latest["value"],
                "year": latest["year"]
            })

    if country_populations:
        countries_df = pd.DataFrame(country_populations)
        countries_df = countries_df.sort_values(by="population", ascending=False)

        top_df = countries_df.head(10).copy()

        sum = countries_df.iloc[10:]["population"].sum()
        row = pd.DataFrame([{"country": "Other Countries", "population": sum, "year": top_df["year"].iloc[0]}])

        pie_df = pd.concat([top_df, row], ignore_index=True)

        pie = px.pie(
            pie_df,
            names="country",
            values="population",
            title="Global Population Distribution",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Electric
        )
        
        pie.update_traces(textposition="inside", textinfo="percent")
        st.plotly_chart(pie)

def main():
    response = requests.get(url=URL).json()
    countries_data = response.get("data", [])

    current_page = st.sidebar.radio("Pages", options=SITE_PAGES, index=0)

    if current_page == "Home":
        render_home_page()

    elif current_page == "World Population":
        render_world_population(countries_data)

    elif current_page == "Country Insights":
        countries = get_countries(countries_data) 
        current_country = st.selectbox(label="Select a Country", options=countries)
        render_country(current_country, countries_data)

if __name__ == "__main__":
    main()