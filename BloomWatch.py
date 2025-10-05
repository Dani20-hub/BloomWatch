import streamlit as st
from PIL import Image
import pandas as pd
import folium 
from streamlit_folium import st_folium

st.set_page_config(page_title="BloomWatch", page_icon="🌸", layout="centered")
st.title("🌸 BloomWatch: Flowering Plant Phenology Monitoring 🌸")
st.markdown("a community app for recording and viewing blooms 🌍")

st.subheader("Submit a Bloom Observation")
uploaded_file = st.file_uploader("Upload a photo of the bloom", type=["jpg", "jpeg", "png"])
if uploaded_file:
	image = Image.open(uploaded_file)
	st.image(image, caption='Uploaded Bloom Photo', use_column_width=True)

st.subheader("Location data")
date = st.date_input("Observation Date")
lat = st.number_input("Latitude", min_value=-90.0, max_value=90.0, format="%.6f")
lon = st.number_input("Longitude", min_value=-180.0, max_value=180.0, format="%.6f")

if st.button("Submit Observation"):
	new_data = pd.DataFrame({
		'date': [date],
		'latitude': [lat],
		'longitude': [lon]
	})
	columns = ['date', 'latitude', 'longitude']
	new_data.to_csv('bloom_data.csv', mode='a', header=False, index=False, columns=columns)
	st.success("Observation submitted!")
	
st.subheader("Observations map")
try:
    data = pd.read_csv('bloom_data.csv', names=['date', 'latitude', 'longitude'])
    if not data.empty:
        m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=2)
        for _, row in data.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"Date: {row['date']}",
                icon=folium.Icon(color='pink', icon='info-sign')
            ).add_to(m)
        st_folium(m, width=700, height=500)
    else:
        st.info("No observations yet. Be the first to submit!")
except FileNotFoundError:
    st.info("No observations yet. Be the first to submit!")
except Exception as e:
    st.error(f"An error occurred: {e}")