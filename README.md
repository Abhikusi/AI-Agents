## 🛠️ Setup Instructions

### Prerequisites

- Python 3.11+
- Conda or pip
- OpenAI API key (for most agents)

### Installation

#### Option 1: Using Conda (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd ai_agent_llm

# Create and activate conda environment
conda env create -f environment.yml
conda activate llms
```

#### Option 2: Using pip

```bash
# Clone the repository
git clone <repository-url>
cd ai_agent_llm

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Configuration

1. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here  # Optional
GOOGLE_API_KEY=your_google_api_key_here        # Optional
```

2. Update `config/config.yaml` with your API keys if needed.

## 🚀 Quick Start

### Basic AI Agent

```python
from agent.core import AIAgent

# Initialize the agent
agent = AIAgent()

# Run a simple task
response = agent.run("Translate this sentence to Hindi: How are you?")
print(response)
```

### Web Scraping Agent

```python
# Navigate to the webscrapper directory
cd 1-agent/1-Webscrapper/

# Run the webscrapper agent
python webscrapper_agent.py
```

### RAG Agent

```python
# Navigate to the RAG agent directory
cd 2-RAG-Agents/1-First-RAG-Agent/

# Open and run the Jupyter notebook
jupyter notebook rag-agent.ipynb
```

## 📚 Agent Types

### 1. Web Scraping Agent
- **Location**: `1-agent/1-Webscrapper/`
- **Purpose**: Extract and process content from websites
- **Features**: BeautifulSoup integration, content cleaning, OpenAI processing

### 2. Business Brochure Generator
- **Location**: `1-agent/2-Brochure/`
- **Purpose**: Generate professional business brochures
- **Features**: Website analysis, content generation, professional formatting

### 3. Conversational AI Chatbot
- **Location**: `1-agent/5-Conversational-AI-Chatbot/`
- **Purpose**: Interactive chatbot with conversation memory
- **Features**: Context awareness, conversation history, multiple response modes

### 4. RAG (Retrieval Augmented Generation) Agent
- **Location**: `2-RAG-Agents/1-First-RAG-Agent/`
- **Purpose**: Question answering with knowledge base integration
- **Features**: Document retrieval, context-aware responses, knowledge base search

### 5. Multimodal AI Agent
- **Location**: `1-agent/7-Image-Audio-LLM/`
- **Purpose**: Process images and audio with LLM capabilities
- **Features**: Image analysis, audio processing, multimodal responses

## 🔧 Configuration

### Main Configuration (`config/config.yaml`)

```yaml
llm:
  api_key: "your_api_key_here"
  model: "gpt-4"  # or "gpt-4o-mini" for cost efficiency
```

### Environment Variables

The project uses environment variables for sensitive information:

- `OPENAI_API_KEY`: Required for OpenAI-based agents
- `ANTHROPIC_API_KEY`: Optional, for Anthropic Claude models
- `GOOGLE_API_KEY`: Optional, for Google Gemini models

## 📊 Knowledge Base

The RAG system includes a comprehensive knowledge base:

- **Company Information**: About, careers, overview
- **Contracts**: Insurance contracts with various companies
- **Employees**: Employee profiles and information
- **Products**: Product documentation (Carllm, Homellm, Markellm, Rellm)

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

## 📝 Logging

Logs are stored in the `logs/` directory. The main log file is `agent.log`.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your `.env` file contains valid API keys
2. **Import Errors**: Make sure all dependencies are installed
3. **Memory Issues**: Some agents may require significant RAM for large models

### Getting Help

- Check the logs in `logs/agent.log`
- Review the troubleshooting notebooks in `1-agent/8-Google-colab-projects/`
- Ensure all dependencies are properly installed

## 🔮 Future Enhancements

- [ ] Add more agent types
- [ ] Implement agent orchestration
- [ ] Add more multimodal capabilities
- [ ] Improve RAG performance
- [ ] Add web interface for all agents

## 📞 Support

For support and questions, please open an issue in the repository.