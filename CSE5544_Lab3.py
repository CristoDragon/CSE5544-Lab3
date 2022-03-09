import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt
import random


st.title("CSE5544 Lab3: Ethics in Data Visualization")
st.subheader("Author: Dragon Xu")
st.header("Step 1: Choose Your Dataset")

# Read in the data from csv file
climate_data = pd.read_csv("https://raw.githubusercontent.com/CSE5544/data/main/ClimateData.csv")
# Replace the values ".." with Nan
df = climate_data.replace("..", np.nan)
# Convert columns of string type to float
df[df.columns[2:33]] = df[df.columns[2:33]].astype('float')

# Transform the orginal df into its "long form" df2, convenient for altair plot
df2 = df.drop(columns=['Non-OECD Economies'])
df2 = pd.melt(df2, id_vars=['Country\year'], var_name='year')
df2.rename(columns={"Country\year": "country", "value":"emission"}, inplace = True)
df2["ln(emission)"] = np.log(df2["emission"])
st.write(df2)
st.caption("Transform the orginal df into its long form, convenient for altair plot")

# Create a new df "country_stats" that contains the mean and std of each country
countries = climate_data['Country\\year']
df_data_country = climate_data.iloc[:,2:]
df_data_country = df_data_country.apply(pd.to_numeric, errors='coerce')
country_stats = pd.DataFrame({'country': countries, 'mean': df_data_country.mean(axis=1),'std': df_data_country.std(axis=1)})
country_stats["ln(mean)"] = np.log(country_stats["mean"])
country_stats["ln(std)"] = np.log(country_stats["std"])
st.write(country_stats)
st.caption("Create a new dataframe that contains summary statistics about the emission of each country")
# df4 = df2[df2["country"] != "OECD - Total"]




st.header("Step 2: Deploy Visualizations by Streamlit")
st.subheader("Part 1: Honest/Ethical/Truthful Visualization")

# Heatmap - df2
df3 = df2.copy()
df3.sort_values(by=["ln(emission)"],ascending=True,inplace=True)
heatmap2 = alt.Chart(df3).mark_rect().encode(
    x = alt.X('country:N', title = 'Country'),
    y = alt.Y('year:O', title = 'Year', bin=alt.BinParams(maxbins=30)),
    color = 'ln(emission):Q',
    tooltip = ['country', 'year', 'emission']
).properties(
    title = 'ln(emission) Level of Each Country from 1990 to 2019'
)
st.altair_chart(heatmap2, use_container_width = True)
st.write("The heatmap above is more truthful and intuitive than the heatmap in Part 2, because we have a clear titel \
    and labels on both X and Y axis. We take the natural log of all emission levels, which makes the whole plot easier \
        to find patterns and trend across years or between different countries. I also add tooltip so that users could \
            know the exact emission level value instead of its log value by hanging their mouses over a particular point.")


# Scatterplot - country_stats
country_stats1 = country_stats.copy()
country_stats1.sort_values(by=["ln(mean)"], ascending=False, inplace=True)
scatterplot1 = alt.Chart(country_stats1.iloc[0:15,:]).mark_circle().encode(
    alt.X('country:N'),
    alt.Y('mean:Q'),
    alt.Size('std:Q'),
    tooltip = ['country', 'mean', 'std']
).properties(
    title = 'Scatterplot of the Mean of Emission for Top 15 Average Emission Countries'
)
st.altair_chart(scatterplot1, use_container_width = True)
st.write("The scatterplot above is honest. We have made circle size as channel to encode the std of emission, and we \
    also add tooltip to show relevant information. In this plot, it seems that there's no linear relationship between \
        the mean and std of emission for the top 15 countries.")


# Heatmap - country_stats
heatmap3 = alt.Chart(country_stats1).mark_bar().encode(
    alt.X('ln(mean):Q'),
    alt.Y('ln(std):Q'),
    alt.Color('country:N'),
    tooltip = ['country', 'ln(mean)', 'ln(std)']
).properties(
    title = 'ln(Mean) of Emission vs ln(Std) of Emission for All Countries'
)
st.altair_chart(heatmap3, use_container_width = True)
st.write("The heatmap above is honest. To reveal any potential relationship between the ln(mean) and ln(std), we use \
    color(hue) as channel to encode different countries. As we can see, it seems like there's a positive linear \
        association between ln(mean) and ln(std), which is a very interesting insight. It implies that countries \
            with larger average emission level tend to change their emission levels more dramatically.")


# Line chart - country_stats
line1 = alt.Chart(country_stats1).mark_line().encode(
    alt.X('country:N'),
    alt.Y('mean:Q')
).properties(
    title = 'Mean of Emission for All Countries During the Last 30 Years'
)
line2 = alt.Chart(country_stats1).mark_line().encode(
    alt.X('country:N'),
    alt.Y('std:Q')
).properties(
    title = 'Std of Emission for All Countries During the Last 30 Years'
)
st.altair_chart((line1 + line1.mark_circle()).interactive(), use_container_width = True)
st.altair_chart((line2 + line2.mark_circle()).interactive(), use_container_width = True)


# Radial Chart - country_stats3
country_stats3 = country_stats.copy()
country_stats3 = country_stats3[country_stats3["country"] != "OECD - Total"]
country_stats3.sort_values(by=["mean"], ascending=False, inplace=True)
country_stats3 = country_stats3.iloc[0:10, :]
radial1 = alt.Chart(country_stats3).encode(
    theta = alt.Theta("ln(mean):Q", stack = True),
    radius = alt.Radius("ln(mean):Q", scale = alt.Scale(type="linear", zero=True, rangeMin=20)),
    color="country:N",
).properties(
    title = 'Radial Chart with ln(mean) as angel theta & radius for the top 10 countries'
)
c1 = radial1.mark_arc(innerRadius=20, stroke="#fff")
c2 = radial1.mark_text(radiusOffset=10).encode(text="country:N")
st.altair_chart(c1 + c2, use_container_width = True)
st.write("The radial chart above is honest. Though angel theta and radius are used as channels to encode \
    ln(mean), the difference between ln(mean) is a lot less than that between mean. Thus, this chart basically \
        reveals the truth, no visual deception here.")






st.header("Step 2: Deploy Visualizations by Streamlit")
st.subheader("Part 2: Dishonest/Unethical/Deceiving Visualization")

# Heatmap - df2
heatmap1 = alt.Chart(df2).mark_rect().encode(
    x = alt.X('country:N', title = 'Country'),
    y = alt.Y('year:O', title = 'Year'),
    color = 'emission:Q',
    tooltip = ['country', 'year', 'emission']
)
st.altair_chart(heatmap1, use_container_width = True)
st.write("The heatmap above is somehow deceiving. The first reason is that we didn't remove OECD-Total in the climate \
    data, and it's emission level is much larger than the rest of the countries, so it's hard to interpret any change \
        or trend either across countries or across years(they have pretty much the same color). The second reason is \
            lack of appropriate lables and title, and the country names on the x-axis are hard to read when in 90 degrees \
                 position.")


# Scatterplot - country_stats
scatterplot2 = alt.Chart(country_stats1.iloc[0:15,:]).mark_circle().encode(
    alt.X('ln(mean):Q', bin=alt.BinParams(maxbins=30)),
    alt.Y('ln(std):Q', bin=alt.BinParams(maxbins=30)),
    alt.Size('country:N')
).properties(
    title = 'Top 15 Average Emission Countries'
)
st.altair_chart(scatterplot2, use_container_width = True)
st.write("The scatterplot above is deceiving, given that we want to show the relationship of mean emission and its std \
    for the top 15 mean emission countries. However, we use circle size as channel to encode nominal variable 'country' \
        , which gives users a wrong sense that there's some kind of order between different countries. Besides, the title \
            is also misleading and implies order.")


# Heatmap - country_stats
heatmap4 = alt.Chart(country_stats1).mark_bar().encode(
    alt.X('ln(mean):Q'),
    alt.Y('ln(std):Q'),
    alt.Color('country:O'),
    tooltip = ['country', 'ln(mean)', 'ln(std)']
).properties(
    title = 'ln(Mean) of Emission vs ln(Std) of Emission for All Countries'
)
st.altair_chart(heatmap4, use_container_width = True)
st.write("The heatmap above is deceiving because color(brightness) is used as channel to encode country, which gives \
    users a useless order information: alphabetical order by countries' names. This happens because we treat 'country' \
        as ordinal when construct the plot.")



# Radial Chart - country_stats3
radial1 = alt.Chart(country_stats3).encode(
    theta = alt.Theta("mean:Q", stack = True),
    radius = alt.Radius("mean:Q", scale = alt.Scale(type="linear", zero=True, rangeMin=20)),
    color="country:N"
).properties(
    title = 'Radial Chart with mean as angel theta & radius for the top 10 countries'
)
c1 = radial1.mark_arc(innerRadius=20, stroke="#fff")
c2 = radial1.mark_text(radiusOffset=10).encode(text="country:N")
st.altair_chart(c1 + c2, use_container_width = True)
st.write("The readial chart above is somehow deceiving. Since we use the values of mena as radius and angels theta, \
    instead of only use angle as channel to encode the mean of top countries, this radial chart exaggerates the \
        actual mean different between countries, gives users a sense of huge mean different between countries.")
