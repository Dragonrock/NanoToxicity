import streamlit as st
import pandas as pd
from PIL import Image

# Function to load data from the Excel file
@st.cache_data
def load_toxicity_data(file_path):
    df = pd.read_excel(file_path, sheet_name='Sheet1', skiprows=1)
    df.rename(columns={df.columns[0]: 'Element'}, inplace=True)
    toxicity_data = df.set_index('Element').T.to_dict()
    data_df = df
    return toxicity_data, data_df

# Path to the Excel file
file_path = 'final.xlsx'  # Update this to the correct path if necessary

# Load toxicity data
toxicity_data, df = load_toxicity_data(file_path)

# Predefined concentration values
concentration_values = df.columns[1:].astype(float).tolist()

# Custom CSS for styling
st.markdown("""
    <style>
        .main {
            max-width: 1920px;
            margin: 0 auto;
            padding: 10px;
        }
        .title {
            font-size: 3em;
            text-align: center;
            margin-top: -90px;
            color: #333f48;
            background-image: linear-gradient(to right, #ff758c, #ff7eb3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            font-size: 1.5em;
            text-align: center;
            margin-bottom: 20px;
            color: #666;
        }
        .description {
            text-align: center;
            font-size: 1.2em;
            margin-bottom: 40px;
            color: #666;
        }
        .container {
            display: flex;
        }
        .input-block {
            flex: 2;
            padding: 20px;
            background-color: #f0f2f6;
            border-radius: 10px;
            margin-right: 20px;
        }
        .output-block {
            flex: 1;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 10px;
            text-align: center;
        }
        .calculate-button {
            display: flex;
            justify-content: center;
            margin-top: 30px;
        }
        .result {
            margin-top: 30px;
            text-align: center;
        }
        .bar-container {
            width: 100%;
            height: 30px;
            background-color: #f0f2f6;
            border-radius: 5px;
            position: relative;
            margin-top: 20px;
        }
        .bar {
            height: 100%;
            border-radius: 5px;
            text-align: center;
            font-size: 1em;
            position: absolute;
            bottom: 0;
            transition: width 0.5s ease-in-out;
        }
        .css-1d391kg.e1fqkh3o3 {
            width: 300px;  /* Adjust the width as needed */
        }
        .feedback {
            font-size: 1.2em;
            color: blue;
        }
        .bar-green {
            background-color: #00cc00;
        }
        .bar-yellowgreen {
            background-color: #99cc00;
        }
        .bar-yellow {
            background-color: #ffcc00;
        }
        .bar-orange {
            background-color: #ff6600;
        }
        .bar-red {
            background-color: #ff0000;
        }
        .stNumberInput > div > div > input {
            font-size: 1.5em;
        }
        .stButton > button {
            font-size: 1.5em;
        }
    </style>
""", unsafe_allow_html=True)

# Function to calculate toxicity
def calculate_toxicity(element, concentration):
    return toxicity_data[element].get(concentration, "No data available")

# Streamlit application code
def streamlit_app():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.markdown('<div class="title">Nano Toxicity Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Determine the toxicity of your nanoelectronic devices</div>', unsafe_allow_html=True)
    st.markdown('<div class="description">Use this tool to calculate the final toxicity score based on the nanoparticles and their concentrations. Ensure the total percentage adds up to 100%.</div>', unsafe_allow_html=True)
    
    st.sidebar.title('NanoToxicity Data Analysis')
    # Sidebar for dataset statistics
    st.sidebar.subheader('Mean Toxicity Levels Across All NanoParticles')
    mean_image = Image.open('mean.png')
    st.sidebar.image(mean_image, caption='Mean Toxicity Levels Across All NanoParticles')

    st.sidebar.subheader('Heatmap of Toxicity Levels')
    heat_image = Image.open('heat.png')
    st.sidebar.image(heat_image, caption='Heatmap of Toxicity Levels')

    # Create a container for the number of elements input
    with st.container():
        num_elements = st.number_input("Number of NanoParticles", min_value=1, max_value=10, step=1, value=1, key="num_elements")

    # Initialize or resize session state percentages list
    if 'percentages' not in st.session_state or len(st.session_state.percentages) != num_elements:
        st.session_state.percentages = [0.0] * num_elements
        st.session_state.percentages[0] = 100.0 if num_elements > 0 else 0.0

    elements = []
    concentrations = []
    percentages = []

    rows = []
    for i in range(num_elements):
        if i % 3 == 0:
            rows.append(st.columns([1, 1, 1, 0.1, 1]))  # Three columns per row
        row = rows[-1]
        col = i % 3

        with row[col]:
            st.markdown(f"<h3>Particle {i+1}</h3>", unsafe_allow_html=True)
            element = st.selectbox(f"Select Nanoparticle {i+1}", list(toxicity_data.keys()), key=f"element_{i}")
            concentration = st.selectbox(f"Select Concentration for {element} (%)", concentration_values, key=f"concentration_{i}")
            percentage = st.number_input(f"Enter Percentage Used for {element} (%)", min_value=0.0, max_value=100.0, step=5.0, value=st.session_state.percentages[i], key=f"percentage_{i}")
            elements.append(element)
            concentrations.append(concentration)
            percentages.append(percentage)

    total_percentage = sum(percentages)
    if total_percentage != 100:
        st.warning("The total percentage must add up to 100%.")
        st.stop()

    calculate_clicked = st.button("Calculate Toxicity", key='calculate', help='Click to calculate the final toxicity score')

    if calculate_clicked:
        final_toxicity = 0
        for element, concentration, percentage in zip(elements, concentrations, percentages):
            toxicity = calculate_toxicity(element, concentration)
            if toxicity != "No data available":
                final_toxicity += (toxicity * (percentage / 100))
            else:
                st.error(f"No data available for {concentration}% concentration of {element}")

        normalized_toxicity = min(final_toxicity, 10)
        with rows[0][4]:
            st.markdown('<div class="result">', unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; font-size: 1.5em;'>Final Toxicity Score: {final_toxicity:.2f}</div>", unsafe_allow_html=True)
            color = "green"
            if normalized_toxicity > 2:
                color = "yellowgreen"
            if normalized_toxicity > 4:
                color = "yellow"
            if normalized_toxicity > 6:
                color = "orange"
            if normalized_toxicity > 8:
                color = "red"

            st.markdown(f"""
                <div class="bar-container">
                    <div class="bar" style="background-color: {color}; width: {normalized_toxicity * 10}%;"></div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    streamlit_app()
