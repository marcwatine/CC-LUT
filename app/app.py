import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_modal import Modal
import folium
from streamlit_folium import folium_static
import json
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from folium.plugins import FloatImage
from PIL import Image

from constants import URLS, OPCC_DATA, DATA_DIR
from querying import descargar_opccc


import streamlit as st

st.session_state['files'] = []

def home():
    st.write("Let's get started!")
    st.write("Click the button below to set-up to load the data.")
    if st.button("Load Data"):

        st.session_state["access_granted"] = True  # Grant access to subpages
        for d in OPCC_DATA.keys():
            st.session_state['files'].append(descargar_opccc(id_capa=OPCC_DATA[d]['id_capa'], save_dir=DATA_DIR+'OPCC/'))

        print(st.session_state['files'])
# Subpage 1
def OPCC():
    margins_css = """
        <style>
            .main > div {
                padding-left: -10rem;
                padding-right: 0rem;
            }
        </style>
    """

    st.markdown(margins_css, unsafe_allow_html=True)
    st.title("OPCC RPC 4.5")
    st.write("Ploting RPC 4.5 pluviometry deficits")
    with open('./data/OPCC/Anoml_P_2050_Anual_RCP85_REGRESION_Q50.geojson') as f:
        geojson_data = json.load(f)

    # Create a Folium map centered on the desired location
    m = folium.Map(location=[42.627785863336015, 1.5057655629981275], zoom_start=15)

    # Add the GeoJSON data to the map with custom styling based on 'Q50' property
    cmap = plt.cm.get_cmap('RdYlGn')
    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': mcolors.rgb2hex(cmap(feature['properties']['Q50'] / 10)),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6,
        }
    ).add_to(m)
   # Generate color scale legend image
    legend_height = 400  # Specify the desired legend height
    legend_width = 10  # Adjust the width as desired

    # Create a color scale gradient
    gradient = np.linspace(-10, 10, legend_height).reshape((-1, 1))
    gradient = np.repeat(gradient, legend_width, axis=1)

    # Apply colormap to the gradient
    color_scale = cmap((gradient + 10) / 20)

    # Convert the color scale array to an image
    legend_img = Image.fromarray((color_scale * 255).astype(np.uint8))

    # Calculate min and max values
    min_value = -10
    max_value = 10

    # Display the map and color scale legend using Streamlit
    col1, col2 = st.columns([6, 1])  # Increase the width of the map column

    # Add the map to the left column
    with col1:
        st.write("### Map")
        folium_static(m, width=600, height=500)

    # Add the color scale legend to the right column
    with col2:
        st.write("### PP mm")
        st.write(f"Max: {-max_value}mm")
        st.image(legend_img, use_column_width='auto', width=legend_width)
        st.write(f"Min: {-min_value}mm")
        


# Subpage 2
def subpage2():
    st.title("Subpage 2")
    st.write("This is Subpage 2.")
    # Add content specific to Subpage 2

# Main function
def main():
    # Initialize session state
    if "access_granted" not in st.session_state:
        st.session_state.access_granted = False

    # Display the appropriate page based on access status
    if st.session_state.access_granted:
        subpage_selection = st.sidebar.radio("Go to", ("Home", "Subpage 1", "Subpage 2"))
        if subpage_selection == "Home":
            home()
        elif subpage_selection == "Subpage 1":
            OPCC()
        elif subpage_selection == "Subpage 2":
            subpage2()
    else:
        home()

# Run the application
if __name__ == "__main__":
    st.title("WHAT'S GOOD")
    main()


#modal = Modal(title="Welcome to CC-LUT",key=1)
#open_modal = st.button("Open")
#if open_modal:
#    modal.open()

#if modal.is_open():
#    with modal.container():
#        st.write("Text goes here")
#        html_string = '''
#        <h1>HTML string in RED</h1>

#        <script language="javascript">
#          document.querySelector("h1").style.color = "red";
#        </script>
#        '''
#        components.html(html_string)
#        st.write("Some fancy text")
#        value = st.checkbox("Check me")
#        st.write(f"Checkbox checked: {value}")
#st.title('CC-LUT')

#add_selectbox = st.sidebar.selectbox(
#    "How would you like to be contacted?",
#    ("Email", "Home phone", "Mobile phone")
#)


#m = folium.Map(control_scale=True)
#st_data = st_folium(m, width=1500)