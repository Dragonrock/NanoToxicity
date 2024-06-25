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
            margin-top: 20px;
        }
        .subtitle {
            font-size: 1.5em;
            text-align: center;
            margin-bottom: 50px;
        }
        .container {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }
        .input-column {
            flex: 1;
            padding: 20px;
            background-color: #f0f2f6;
            border-radius: 10px;
            margin-right: 20px;
        }
        .output-column {
            flex: 1;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 10px;
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
        .bar {
            width: 100%;
            background-color: lightgray;
            border-radius: 5px;
            padding: 5px;
            text-align: center;
            font-size: 1.2em;
        }
    </style>
""", unsafe_allow_html=True)

# Function to calculate toxicity
def calculate_toxicity(element, concentration):
    return toxicity_data[element].get(concentration, "No data available")

# Streamlit application code
def streamlit_app():
    st.markdown('<div class="title">Nanoparticle Toxicity Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Add multiple elements, their respective concentrations, and the percentage used in the device. Ensure the total percentage adds up to 100%.</div>', unsafe_allow_html=True)

    # Create layout with input elements on the left and output on the right
    input_cols = st.columns(11)
    output_col = st.columns(1)[0]

    # Number of Elements input
    with input_cols[0]:
        num_elements = st.number_input("Number of Elements", min_value=1, max_value=10, step=1, value=1, key="num_elements")

    # Initialize or resize session state percentages list
    if 'percentages' not in st.session_state or len(st.session_state.percentages) != num_elements:
        st.session_state.percentages = [0.0] * num_elements
        st.session_state.percentages[0] = 100.0 if num_elements > 0 else 0.0

    elements = []
    concentrations = []
    percentages = []

    # Dynamic columns for each element input
    for i in range(num_elements):
        with input_cols[i + 1]:
            st.markdown(f"<h3>Element {i+1}</h3>", unsafe_allow_html=True)
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

    with output_col:
        if calculate_clicked:
            final_toxicity = 0
            for element, concentration, percentage in zip(elements, concentrations, percentages):
                toxicity = calculate_toxicity(element, concentration)
                if toxicity != "No data available":
                    final_toxicity += (toxicity * (percentage / 100))
                else:
                    st.error(f"No data available for {concentration}% concentration of {element}")

            st.markdown('<div class="result">', unsafe_allow_html=True)
            st.write(f"Final Toxicity Score: {final_toxicity:.2f}")
            st.progress(final_toxicity / 10)

            color = "green"
            if final_toxicity > 2:
                color = "yellowgreen"
            if final_toxicity > 4:
                color = "yellow"
            if final_toxicity > 6:
                color = "orange"
            if final_toxicity > 8:
                color = "red"

            st.markdown(f"""
            <div class="bar" style="width: {final_toxicity*10}%; background-color: {color};">
                {final_toxicity:.2f}/10
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    streamlit_app()
