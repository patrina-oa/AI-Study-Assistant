# streamlit_app.py
import streamlit as st
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv
import wikipedia
from pint import UnitRegistry

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for pink theme
st.markdown("""
    <style>
    /* Main background */
    .main {
        background-color: #fff5f7;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #ffc0cb;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #c71585;
    }
    
    /* Input boxes */
    .stTextInput > div > div > input {
        background-color: #ffe4e9;
        color: #8b0045;
        border: 2px solid #ff69b4;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #ff1493;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #c71585;
        border: none;
    }
    
    /* Chat messages */
    [data-testid="stChatMessage"] {
        background-color: #CC8899;
        border-left: 4px solid #ff69b4;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #ffb6c1;
        color: #8b0045;
        font-weight: bold;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] .element-container {
        color: #8b0045;
    }
    
    /* Markdown in sidebar */
    [data-testid="stSidebar"] .stMarkdown {
        color: #8b0045;
    }
    
    /* Info boxes */
    .stAlert {
        background-color: #ffe4e9;
        border: 2px solid #ff69b4;
        color: #8b0045;
    }
    
    /* Success boxes */
    .element-container .stSuccess {
        background-color: #ffb6c1;
    }
    
    /* Divider */
    hr {
        border-color: #ff69b4;
    }
    </style>
""", unsafe_allow_html=True)

# Define tools
@tool
def calculator(expression: str) -> str:
    """A calculator tool that evaluates mathematical expressions.
    
    Args:
        expression: A mathematical expression as a string (e.g., "2 + 2", "10 * 5 - 3")
    
    Returns:
        The result of the calculation
    """
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"The result of {expression} is: {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"

@tool
def wikipedia_search(query: str) -> str:
    """Search Wikipedia and return a summary of the topic.
    
    Args:
        query: The topic to search for on Wikipedia
    
    Returns:
        A summary of the Wikipedia article
    """
    try:
        summary = wikipedia.summary(query, sentences=3, auto_suggest=True)
        return f"Wikipedia summary for '{query}':\n{summary}"
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:5]
        return f"Multiple results found for '{query}'. Please be more specific. Options: {', '.join(options)}"
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{query}'. Please try a different search term."
    except Exception as e:
        return f"Error searching Wikipedia for '{query}': {str(e)}"

@tool
def unit_converter(value: float, from_unit: str, to_unit: str) -> str:
    """Convert between different units of measurement.
    
    Supports distance, weight, temperature, volume, speed, time, and more.
    Examples: km to miles, kg to lb, celsius to fahrenheit, liters to gallons
    
    Args:
        value: The numeric value to convert
        from_unit: The source unit (e.g., 'km', 'lb', 'celsius')
        to_unit: The target unit (e.g., 'miles', 'kg', 'fahrenheit')
    
    Returns:
        The converted value with explanation
    """
    try:
        ureg = UnitRegistry()
        
        from_unit = from_unit.strip().lower()
        to_unit = to_unit.strip().lower()
        
        unit_aliases = {
            'km': 'kilometer', 'kms': 'kilometer', 'mi': 'mile', 'miles': 'mile',
            'ft': 'foot', 'feet': 'foot', 'm': 'meter', 'meters': 'meter',
            'cm': 'centimeter', 'mm': 'millimeter', 'in': 'inch', 'inches': 'inch',
            'yd': 'yard', 'yards': 'yard', 'kg': 'kilogram', 'kgs': 'kilogram',
            'g': 'gram', 'grams': 'gram', 'mg': 'milligram', 'lb': 'pound',
            'lbs': 'pound', 'pounds': 'pound', 'oz': 'ounce', 'ounces': 'ounce',
            'c': 'degC', 'celsius': 'degC', 'f': 'degF', 'fahrenheit': 'degF',
            'k': 'kelvin', 'kelvin': 'kelvin', 'l': 'liter', 'liters': 'liter',
            'litres': 'liter', 'ml': 'milliliter', 'gal': 'gallon', 'gallons': 'gallon',
            'qt': 'quart', 'cup': 'cup', 'cups': 'cup', 'mph': 'mile/hour',
            'kph': 'kilometer/hour', 'kmh': 'kilometer/hour', 'mps': 'meter/second',
            'sec': 'second', 'seconds': 'second', 'min': 'minute', 'minutes': 'minute',
            'hr': 'hour', 'hours': 'hour', 'day': 'day', 'days': 'day',
        }
        
        from_unit = unit_aliases.get(from_unit, from_unit)
        to_unit = unit_aliases.get(to_unit, to_unit)
        
        quantity = value * ureg(from_unit)
        result = quantity.to(to_unit)
        
        return f"{value} {from_unit} = {result.magnitude:.4f} {to_unit}"
    
    except Exception as e:
        error_msg = str(e)
        if "dimensionality" in error_msg.lower():
            return f"Cannot convert '{from_unit}' to '{to_unit}' - they measure different things."
        elif "undefined" in error_msg.lower():
            return f"Unit not recognized. From: '{from_unit}', To: '{to_unit}'."
        else:
            return f"Error converting units: {error_msg}"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    llm = ChatOllama(model="llama3.2", temperature=0)
    tools = [calculator, wikipedia_search, unit_converter]
    st.session_state.agent = create_agent(llm, tools)

# Sidebar
with st.sidebar:
    st.title("AI Study Assistant")
    st.markdown("---")
    
    st.subheader("Tools Available")
    st.markdown("""
    **Calculator**
    - Perform mathematical calculations
    
    **Wikipedia Search**
    - Search for information on any topic
    
    **Unit Converter**
    - Convert between different units
    """)
    
    st.markdown("---")
    
    st.subheader("Example Queries")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Calculate", use_container_width=True):
            st.session_state.example_query = "What is 25 * 4 + 10?"
        if st.button("Wikipedia", use_container_width=True):
            st.session_state.example_query = "Tell me about quantum physics"
    
    with col2:
        if st.button("Convert Units", use_container_width=True):
            st.session_state.example_query = "Convert 5 km to miles"
        if st.button("Temperature", use_container_width=True):
            st.session_state.example_query = "Convert 100 celsius to fahrenheit"
    
    st.markdown("---")
    
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    st.subheader("About")
    st.markdown("""
    This AI Study Assistant helps you with:
    - Mathematical calculations
    - Information lookup
    - Unit conversions
    
    Simply type your question and press Enter.
    """)

# Main chat interface
st.title("Chat with ANDRINA -your AI Study Assistant")
st.markdown("Ask me anything about calculations, general knowledge, or unit conversions!")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "tool_output" in message:
            with st.expander("Tool Output"):
                st.info(message["tool_output"])

# Handle example query from sidebar
if "example_query" in st.session_state:
    prompt = st.session_state.example_query
    del st.session_state.example_query
else:
    prompt = st.chat_input("Type your question here...")

# Process user input
if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get agent response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        tool_outputs = []
        
        try:
            with st.spinner("Thinking..."):
                for chunk in st.session_state.agent.stream(
                    {'messages': [HumanMessage(content=prompt)]}
                ):
                    if "agent" in chunk:
                        for message in chunk["agent"]["messages"]:
                            full_response += message.content
                            message_placeholder.markdown(full_response + "▌")
                    elif "tools" in chunk:
                        for message in chunk["tools"]["messages"]:
                            tool_outputs.append(message.content)
            
            message_placeholder.markdown(full_response)
            
            # Display tool outputs
            if tool_outputs:
                with st.expander("Tool Output"):
                    for output in tool_outputs:
                        st.info(output)
            
            # Save to session
            message_data = {"role": "assistant", "content": full_response}
            if tool_outputs:
                message_data["tool_output"] = "\n\n".join(tool_outputs)
            st.session_state.messages.append(message_data)
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #c71585;'>ANDRINA | Powered by LangChain & Ollama</div>",
    unsafe_allow_html=True
)