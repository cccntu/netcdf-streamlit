import urllib.request
from datetime import datetime, timedelta

import plotly.graph_objects as go
import streamlit as st
from netCDF4 import Dataset as NetCDFFile


@st.cache
def get_data():
    url = "https://portal.geobon.org/data/upload/6/netcdf/predicts_003.nc"
    filename = url.split("/")[-1]
    urllib.request.urlretrieve(url, filename)
    return filename


filename = get_data()
nc = NetCDFFile(filename)
# from pprint import  pprint
# pprint(nc.__dict__) # prints the attributes to terminal for inspection
st.title(nc.title)
st.header("Description")
st.write(nc.description)

metric0 = nc.groups["scenario0"].groups["metric0"]
alpha = metric0.variables["alphaDiversityAndSpeciesRichness"][:]
lat = nc.variables["lat"][:]
lon = nc.variables["lon"][:]
time = nc.variables["time"][:]
# without filled array, plotly fills with unwanted colors
alpha = alpha.filled(fill_value=0)

# this is the definition of time in this dataset
def convert_time(t):
    specific_date = datetime(1860, 1, 1)
    new_date = specific_date + timedelta(int(t))
    return new_date


def id_to_time(i):
    return convert_time(time[i])


@st.cache
def plotly_plot(time_idx):
    fig = go.Figure(data=go.Heatmap(x=lon, y=lat, z=alpha[time_idx]))
    return fig


time_id = st.select_slider("Date", options=range(len(time)), format_func=id_to_time)
fig = plotly_plot(time_id)
st.write(fig)
