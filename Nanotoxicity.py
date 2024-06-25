import streamlit as st

# Hardcoded toxicity data
toxicity_data = {
    'Element1': {0.49: 0.1, 0.98: 0.2, 1.95: 0.4, 3.91: 0.8, 7.81: 1.6, 15.63: 3.2, 31.25: 6.4, 62.5: 12.8, 125: 25.6, 250: 51.2},
    'Element2': {0.49: 0.05, 0.98: 0.1, 1.95: 0.2, 3.91: 0.4, 7.81: 0.8, 15.63: 1.6, 31.25: 3.2, 62.5: 6.4, 125: 12.8, 250: 25.6},
    'Element3': {0.49: 0.3, 0.98: 0.6, 1.95: 1.2, 3.91: 2.4, 7.81: 4.8, 15.63: 9.6, 31.25: 19.2, 62.5: 38.4, 125: 76.8, 250: 153.6}
}

# Predefined concentration values
concentration_values = [0.49, 0.98, 1.95, 3.91, 7.81, 15.63, 31.25, 62.5, 125, 250]

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
            justify-content: space-between;
            align-items: flex-start;
        }
        .input-block {
            flex: 3;
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

    # Create a container for the number of elements input
    with st.container():
        num_elements = st.number_input("Number of Particles", min_value=1, max_value=10, step=1, value=1, key="num_elements")

    # Initialize or resize session state percentages list
    if 'percentages' not in st.session_state or len(st.session_state.percentages) != num_elements:
        st.session_state.percentages = [0.0] * num_elements
        st.session_state.percentages[0] = 100.0 if num_elements > 0 else 0.0

    elements = []
    concentrations = []
    percentages = []

    rows = []
    for i in range(num_elements):
        # Create a new row for every three elements
        if i % 3 == 0:
            rows.append(st.columns([1, 1, 1, 0.1, 1]))  # Added extra column for spacing and bar

        # Get the current row and column
        row = rows[-1]
        col = i % 3

        with row[col]:
            st.markdown(f"<h3>Particle {i+1}</h3>", unsafe_allow_html=True)
            element = st.selectbox(f"Select Nanoparticle {i+1}", list(toxicity_data.keys()), key=f"element_{i}")
            concentration = st.selectbox(f"Select Concentration for {element} (%)", concentration_values, key=f"concentration_{i}")
            percentage = st.number_input(f"Enter Percentage Used for {element} (%)", min_value=0.0, max_value=100.0, step=0.1, value=st.session_state.percentages[i], key=f"percentage_{i}")
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

        # Normalize the final toxicity score to not exceed 10
        normalized_toxicity = min(final_toxicity, 10)

        # Ensure the bar is aligned with the input elements
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
