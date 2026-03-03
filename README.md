# AI Study Assistant

A powerful AI-powered study assistant that provides mathematical calculations, Wikipedia searches, and unit conversions through both a command-line interface and a modern web interface.

## Features

### Core Capabilities

- **Calculator Agent**: Evaluate complex mathematical expressions with instant results
- **Wikipedia Search Agent**: Access comprehensive information from Wikipedia with smart disambiguation handling
- **Unit Converter Agent**: Convert between various units including distance, weight, temperature, volume, speed, and time

### Dual Interface Options

1. **Terminal Interface** (`main.py`): Fast, lightweight command-line interaction
2. **Web Interface** (`streamlit_app.py`): Beautiful pink-themed web application with chat history and interactive features

## Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- [Ollama](https://ollama.ai) with the `llama3.2` model installed

### Installing Ollama

1. Download and install Ollama from [ollama.ai](https://ollama.ai)
2. Pull the llama3.2 model:
   ```bash
   ollama pull llama3.2
   ```
3. Verify Ollama is running:
   ```bash
   ollama list
   ```

## Installation

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd aiproject
```

### 2. Install Dependencies

Using uv (recommended):

```bash
uv add langchain langchain-ollama wikipedia pint python-dotenv streamlit
```

Or using pip:

```bash
pip install langchain langchain-ollama wikipedia pint python-dotenv streamlit
```

### 3. Set Up Environment Variables (Optional)

Create a `.env` file in the project root:

```env
# Add any environment variables if needed
```

## Usage

### Terminal Interface

Run the command-line version for quick interactions:

```bash
uv run python main.py
```

**Example interactions:**
```
You: What is 25 * 4 + 10?
Study Assistant: The result of 25 * 4 + 10 is: 110

You: Tell me about quantum physics
Study Assistant: [Wikipedia summary appears here]

You: Convert 5 km to miles
Study Assistant: 5 kilometer = 3.1069 mile
```

**Commands:**
- Type your question or calculation
- Type `exit` to quit

### Web Interface

Launch the beautiful web application:

```bash
uv run streamlit run streamlit_app.py
```

The application will automatically open in your browser at `http://localhost:8501`

**Features:**
- Interactive chat interface with message history
- Pink-themed professional design
- Quick example buttons for common queries
- Tool output visualization
- Clear chat history option

## Project Structure

```
aiproject/
├── main.py              # Terminal-based interface
├── streamlit_app.py     # Web-based interface
├── .env                 # Environment variables (optional)
├── README.md            # Project documentation
├── pyproject.toml       # Project dependencies
└── .venv/               # Virtual environment
```

## Available Tools

### Calculator

Evaluates mathematical expressions safely.

**Examples:**
- `What is 2 + 2?`
- `Calculate 100 / 5`
- `What is 25 * 4 + 10?`

### Wikipedia Search

Retrieves summarized information from Wikipedia with smart handling of ambiguous queries.

**Examples:**
- `Tell me about quantum physics`
- `Who was Albert Einstein?`
- `What is machine learning?`

**Features:**
- Auto-suggestion for similar topics
- Disambiguation handling for multiple results
- 3-sentence summaries for quick reading

### Unit Converter

Converts between various units with extensive support for common measurements.

**Supported Unit Categories:**

| Category | Units |
|----------|-------|
| **Distance** | km, miles, meters, feet, inches, yards, cm, mm |
| **Weight** | kg, pounds, grams, ounces, mg |
| **Temperature** | celsius, fahrenheit, kelvin |
| **Volume** | liters, gallons, ml, cups, quarts |
| **Speed** | mph, kph, mps |
| **Time** | seconds, minutes, hours, days |

**Examples:**
- `Convert 5 km to miles`
- `How many pounds is 70 kg?`
- `What is 100 celsius in fahrenheit?`
- `Convert 2 liters to gallons`

## Technical Details

### Technologies Used

- **LangChain**: Framework for building LLM applications
- **Ollama**: Local LLM runtime with llama3.2 model
- **Streamlit**: Web application framework
- **Wikipedia API**: For information retrieval
- **Pint**: Unit conversion library
- **Python 3.8+**: Core programming language

### Architecture

The application uses a multi-agent architecture where:

1. **LLM Agent**: Processes natural language queries and determines which tool to use
2. **Tool Agents**: Specialized agents for specific tasks (calculator, Wikipedia, unit converter)
3. **Streaming Interface**: Real-time response streaming for better user experience

### Agent Workflow

```
User Query → LLM Agent → Tool Selection → Tool Execution → Response Formatting → User
```

## Troubleshooting

### Common Issues

**Issue: "Module not found" errors**
```bash
# Reinstall dependencies
uv add langchain langchain-ollama wikipedia pint python-dotenv streamlit
```

**Issue: "Ollama connection failed"**
```bash
# Make sure Ollama is running
ollama serve

# Verify llama3.2 is installed
ollama pull llama3.2
```

**Issue: "Blank Streamlit page"**
- Check the terminal for error messages
- Ensure all dependencies are installed
- Verify Ollama is running with llama3.2 model

**Issue: "Unit conversion errors"**
- Ensure units are spelled correctly (e.g., 'km', 'celsius', 'pounds')
- Units must be compatible (can't convert distance to weight)
- Use common abbreviations from the supported units list

### Debug Mode

Run with verbose logging:

```bash
# Terminal version
python main.py

# Web version with logging
streamlit run streamlit_app.py --logger.level=debug
```

## Customization

### Changing the LLM Model

Edit the model in both `main.py` and `streamlit_app.py`:

```python
llm = ChatOllama(model="llama3.2", temperature=0)
# Change to any Ollama model you have installed
llm = ChatOllama(model="llama3.1", temperature=0)
```

### Modifying the Color Theme (Web Interface)

Edit the CSS in `streamlit_app.py` to change colors:

```python
st.markdown("""
    <style>
    .main {
        background-color: #fff5f7;  /* Change background color */
    }
    /* Modify other colors as needed */
    </style>
""", unsafe_allow_html=True)
```

### Adding More Tools

Create a new tool function:

```python
@tool
def your_new_tool(parameter: str) -> str:
    """Description of what your tool does."""
    # Your implementation here
    return result

# Add to tools list
tools = [calculator, wikipedia_search, unit_converter, your_new_tool]
```

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Suggested Improvements

- Add more specialized agents (weather, translation, code execution)
- Implement conversation memory
- Add user authentication for web interface
- Export chat history to file
- Add voice input/output capabilities
- Multi-language support


## Acknowledgments

- **LangChain** for the agent framework
- **Ollama** for local LLM capabilities
- **Streamlit** for the web interface
- **Wikipedia API** for knowledge access
- **Pint** for comprehensive unit conversion

## Support

For issues, questions, or suggestions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review existing issues in the repository
3. Create a new issue with detailed information about your problem

## Roadmap

### Planned Features

- [ ] Conversation history persistence
- [ ] Export chat to PDF/Markdown
- [ ] Voice input/output
- [ ] Multi-user support
- [ ] Custom tool creation interface
- [ ] Mobile-responsive design improvements
- [ ] Dark mode toggle
- [ ] Integration with additional LLM providers

### Version History

**v1.0.0** - Initial Release
- Terminal and web interfaces
- Calculator, Wikipedia, and Unit Converter agents
- Pink-themed web UI
- Real-time streaming responses

---

Made with care for students and learners everywhere.
