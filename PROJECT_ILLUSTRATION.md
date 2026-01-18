# 📚 Daily arXiv AI-Enhanced Project Illustration

## 🎯 Project Overview

**daily-arXiv-ai-enhanced** is an innovative automated system that crawls daily arXiv papers, enhances them with AI-generated summaries, and presents them through a beautiful web interface. The project runs entirely on GitHub infrastructure (Actions + Pages) with zero server costs.

### Key Highlights
- 🤖 **AI-Powered Summarization**: Uses LLMs (DeepSeek/GPT) to generate structured summaries in Chinese/English
- 📊 **Smart Filtering**: User-customizable keyword and author filtering
- 🔄 **Automated Daily Updates**: Runs via GitHub Actions on a schedule
- 💰 **Cost-Effective**: ~0.2 CNY per day for AI processing
- 🔒 **Optional Password Protection**: Secure access control
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     GitHub Actions Workflow                      │
│                  (Runs Daily @ 1:30 AM UTC)                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: Web Scraping (Scrapy)                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Crawl arXiv.org                                       │  │
│  │  • Extract paper metadata (title, authors, abstract)     │  │
│  │  • Filter by categories (cs.CV, cs.CL, cs.AI, etc.)     │  │
│  │  • Output: data/YYYY-MM-DD.jsonl                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 2: Intelligent Deduplication                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Check for duplicate papers                            │  │
│  │  • Exit early if no new content                          │  │
│  │  • Script: daily_arxiv/check_stats.py                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 3: AI Enhancement (LangChain + OpenAI API)                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Parallel processing with ThreadPoolExecutor           │  │
│  │  • Generate structured summaries:                        │  │
│  │    - TLDR (brief summary)                                │  │
│  │    - Motivation                                          │  │
│  │    - Method                                              │  │
│  │    - Result                                              │  │
│  │    - Conclusion                                          │  │
│  │  • Sensitive content filtering                           │  │
│  │  • GitHub code link detection                            │  │
│  │  • Output: data/YYYY-MM-DD_AI_enhanced_LANGUAGE.jsonl   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 4: Markdown Conversion                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Convert JSONL to organized Markdown                   │  │
│  │  • Group by categories                                   │  │
│  │  • Generate table of contents                            │  │
│  │  • Output: data/YYYY-MM-DD.md                           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 5: Data Storage                                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Commit data files to 'data' branch                    │  │
│  │  • Update assets/file-list.txt                           │  │
│  │  • Keep code in 'main' branch                            │  │
│  │  • Deploy to GitHub Pages                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend (GitHub Pages)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  index.html                                              │  │
│  │  ├─ Dynamic paper loading                                │  │
│  │  ├─ Category filtering                                   │  │
│  │  ├─ Keyword/Author filtering                             │  │
│  │  ├─ Date range selection                                 │  │
│  │  ├─ Text search                                          │  │
│  │  └─ Paper detail modal                                   │  │
│  │                                                           │  │
│  │  settings.html                                           │  │
│  │  ├─ Custom keywords management                           │  │
│  │  └─ Custom authors management                            │  │
│  │                                                           │  │
│  │  statistic.html                                          │  │
│  │  └─ Paper statistics visualization                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Project Structure

```
daily-arXiv-ai-enhanced/
│
├── 📁 .github/workflows/
│   └── run.yml                    # Main GitHub Actions workflow
│
├── 📁 ai/                         # AI Enhancement Module
│   ├── enhance.py                 # Main AI processing script
│   ├── structure.py               # Structured output schema
│   ├── template.txt               # LLM prompt template
│   └── system.txt                 # System prompt for LLM
│
├── 📁 daily_arxiv/                # Scrapy Spider Module
│   ├── daily_arxiv/
│   │   ├── spiders/
│   │   │   └── arxiv.py          # arXiv crawler spider
│   │   ├── check_stats.py        # Deduplication logic
│   │   ├── items.py              # Scrapy item definitions
│   │   └── settings.py           # Scrapy configuration
│   └── scrapy.cfg
│
├── 📁 to_md/                      # Markdown Conversion Module
│   ├── convert.py                 # JSONL to Markdown converter
│   └── paper_template.md          # Paper markdown template
│
├── 📁 js/                         # Frontend JavaScript
│   ├── app.js                     # Main application logic
│   ├── auth.js                    # Authentication handling
│   ├── auth-config.js             # Auth configuration
│   ├── data-config.js             # Data source configuration
│   ├── settings.js                # Settings page logic
│   └── statistic.js               # Statistics page logic
│
├── 📁 css/                        # Styling
│   ├── styles.css                 # Main stylesheet
│   ├── settings.css               # Settings page styles
│   └── statistic.css              # Statistics page styles
│
├── 📁 data/                       # Generated Data (Git LFS)
│   └── *.jsonl                    # Daily paper data files
│
├── 📁 assets/                     # Static Assets
│   └── file-list.txt              # List of available data files
│
├── 📄 index.html                  # Main web interface
├── 📄 settings.html               # Settings page
├── 📄 statistic.html              # Statistics page
├── 📄 login.html                  # Login page
│
├── 📄 run.sh                      # Local testing script
├── 📄 pyproject.toml              # Python dependencies
└── 📄 README.md                   # Project documentation
```

---

## 🔄 Data Flow

### 1. **Crawling Phase**
```
arXiv.org → Scrapy Spider → Raw JSONL
                                   │
                     ┌─────────────┘
                     │
        ┌────────────▼────────────┐
        │  Extract:               │
        │  - Paper ID             │
        │  - Title                │
        │  - Authors              │
        │  - Abstract             │
        │  - Categories           │
        │  - Publication Date     │
        └─────────────────────────┘
                     │
                     ▼
        data/YYYY-MM-DD.jsonl
```

### 2. **AI Enhancement Phase**
```
Raw JSONL → LangChain Pipeline → Enhanced JSONL
                    │
        ┌───────────┴───────────┐
        │                       │
   Parallel Workers    Structured Output
   (ThreadPool)        (5 fields per paper)
        │                       │
        │              ┌────────▼────────┐
        │              │  AI Fields:     │
        │              │  - tldr         │
        │              │  - motivation   │
        │              │  - method       │
        │              │  - result       │
        │              │  - conclusion   │
        │              └─────────────────┘
        │
        └──────────► Sensitive Content Filter
                    GitHub Link Detection
                              │
                              ▼
        data/YYYY-MM-DD_AI_enhanced_LANGUAGE.jsonl
```

### 3. **Frontend Consumption**
```
Enhanced JSONL → Frontend Loader → In-Memory Data
                                            │
                           ┌────────────────┴────────────────┐
                           │                                  │
                    User Filters                      Paper Display
                    (Category, Keywords,              (Cards/Modal)
                     Authors, Date Range,
                     Text Search)
                           │                                  │
                           └──────────┬───────────────────────┘
                                      ▼
                            Filtered Paper List
                                      │
                                      ▼
                            Interactive UI
```

---

## 🛠️ Technology Stack

### Backend / Automation
- **Python 3.12+**: Main programming language
- **Scrapy 2.12+**: Web scraping framework
- **LangChain 0.3+**: LLM orchestration
- **LangChain-OpenAI**: OpenAI API integration (supports any OpenAI-compatible API)
- **UV**: Fast Python package manager

### AI/ML
- **OpenAI-compatible APIs**: DeepSeek, GPT-4, etc.
- **Function Calling**: Structured output generation
- **Parallel Processing**: ThreadPoolExecutor for efficiency

### Frontend
- **Vanilla JavaScript**: No framework dependencies
- **HTML5/CSS3**: Modern web standards
- **LocalStorage**: Client-side preference storage
- **Flatpickr**: Date picker library

### Infrastructure
- **GitHub Actions**: CI/CD automation
- **GitHub Pages**: Static site hosting
- **Git Branches**: Code/data separation (`main` + `data`)

---

## 🔧 Key Components Deep Dive

### 1. Scrapy Spider (`daily_arxiv/spiders/arxiv.py`)
```python
Purpose: Crawl arXiv.org for new papers
Key Features:
  - Multi-category support (configurable via CATEGORIES env var)
  - Filters papers by target categories
  - Extracts: ID, categories, basic metadata
  - Outputs: JSONL format for downstream processing
```

### 2. AI Enhancer (`ai/enhance.py`)
```python
Purpose: Generate structured AI summaries
Key Features:
  - Parallel processing with configurable workers
  - Structured output: tldr, motivation, method, result, conclusion
  - Sensitive content filtering via external API
  - GitHub code link detection and metadata extraction
  - Error handling with fallback defaults
  - Deduplication of processed papers
```

### 3. Markdown Converter (`to_md/convert.py`)
```python
Purpose: Convert enhanced JSONL to organized Markdown
Key Features:
  - Category-based organization
  - Table of contents generation
  - Respects category preference order
  - Validates AI fields before conversion
```

### 4. Frontend Application (`js/app.js`)
```javascript
Purpose: Interactive paper browsing interface
Key Features:
  - Dynamic data loading from JSONL files
  - Real-time filtering (category, keywords, authors)
  - Date range selection
  - Text search across all fields
  - Paper detail modal with navigation
  - Keyboard shortcuts (←→ arrows, space)
  - Responsive design
```

### 5. Authentication System (`js/auth.js`)
```javascript
Purpose: Optional password protection
Key Features:
  - SHA-256 hash-based authentication
  - Configurable via GitHub Secrets
  - Session-based login persistence
  - Graceful fallback if disabled
```

---

## 🤖 LLM Integration Deep Dive

The project leverages Large Language Models (LLMs) to transform raw arXiv paper abstracts into structured, multilingual summaries. Here's how LLMs are integrated and utilized:

### LLM Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LLM Processing Pipeline                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌──────────────────────────────────────┐
        │  1. Input: Raw Paper Abstract        │
        │     (from arXiv scraping)            │
        └──────────────────────────────────────┘
                              │
                              ▼
        ┌──────────────────────────────────────┐
        │  2. LangChain Orchestration          │
        │     ┌────────────────────────────┐  │
        │     │ ChatPromptTemplate         │  │
        │     │ ├─ System Prompt           │  │
        │     │ └─ Human Message Template  │  │
        │     └────────────────────────────┘  │
        │              │                       │
        │              ▼                       │
        │     ┌────────────────────────────┐  │
        │     │ ChatOpenAI (configurable)  │  │
        │     │ ├─ Base URL (env)          │  │
        │     │ ├─ Model Name (env)        │  │
        │     │ └─ API Key (secret)        │  │
        │     └────────────────────────────┘  │
        │              │                       │
        │              ▼                       │
        │     ┌────────────────────────────┐  │
        │     │ Structured Output          │  │
        │     │ (Function Calling)         │  │
        │     └────────────────────────────┘  │
        └──────────────────────────────────────┘
                              │
                              ▼
        ┌──────────────────────────────────────┐
        │  3. Output: Structured JSON          │
        │     {                                 │
        │       "tldr": "...",                 │
        │       "motivation": "...",           │
        │       "method": "...",               │
        │       "result": "...",               │
        │       "conclusion": "..."            │
        │     }                                 │
        └──────────────────────────────────────┘
```

### Core LLM Components

#### 1. **LangChain Integration** (`ai/enhance.py`)

The project uses **LangChain** as the orchestration framework for LLM interactions:

```python
# LLM initialization with structured output
llm = ChatOpenAI(model=model_name).with_structured_output(
    Structure, 
    method="function_calling"
)

# Prompt template construction
prompt_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system),
    HumanMessagePromptTemplate.from_template(template=template)
])

# Chain composition
chain = prompt_template | llm
```

**Key Features:**
- **OpenAI-Compatible API**: Works with any OpenAI-compatible endpoint (DeepSeek, GPT-4, Claude, etc.)
- **Structured Output**: Uses function calling to guarantee consistent JSON schema
- **Configurable Model**: Model name and base URL configured via environment variables

#### 2. **Structured Output Schema** (`ai/structure.py`)

Uses **Pydantic** models to define the exact structure LLM must return:

```python
class Structure(BaseModel):
    tldr: str = Field(description="generate a too long; didn't read summary")
    motivation: str = Field(description="describe the motivation in this paper")
    method: str = Field(description="method of this paper")
    result: str = Field(description="result of this paper")
    conclusion: str = Field(description="conclusion of this paper")
```

**Benefits:**
- **Type Safety**: Guaranteed structure in Python code
- **Validation**: Automatic validation of LLM output
- **Consistency**: Every paper gets the same 5-field structure
- **Error Handling**: Clear errors when LLM output doesn't match schema

#### 3. **Prompt Engineering**

**System Prompt** (`ai/system.txt`):
```
You are a professional paper analyst.
You should avoid unnecessarily long replies and instead provide concise, 
detailed, and precise answers using correct terminology.
It is prohibited to output any sensitive content such as politics, 
ethnicity, religion, violence, pornography, terrorism, gambling, 
regional discrimination, leaders and their relatives; once it is 
detected that the question or original text contains the above elements, 
the unified reply will be: "This content has not passed the compliance 
test and has been hidden."
Your output should in {language}.
```

**Human Template** (`ai/template.txt`):
```
Please analyze the following abstract of papers. 

Content:
{content}
```

**Design Principles:**
- **Role Definition**: Clearly defines LLM's role as "professional paper analyst"
- **Style Guidance**: Instructs concise, detailed, precise answers
- **Content Safety**: Explicit prohibition of sensitive content
- **Multilingual Support**: Language specified dynamically via `{language}` variable
- **Abstract-Focused**: Only abstracts are analyzed (not full papers)

### LLM Processing Flow

#### Step-by-Step Execution

```python
# 1. Single Paper Processing
def process_single_item(chain, item: Dict, language: str):
    # Pre-processing: Check for sensitive content
    if is_sensitive(item.get("summary", "")):
        return None
    
    # Extract GitHub links from abstract
    code_info = check_github_code(item.get("summary", ""))
    
    # 2. LLM Invocation
    response: Structure = chain.invoke({
        "language": language,      # Dynamic language setting
        "content": item['summary']  # Paper abstract
    })
    
    # 3. Post-processing
    item['AI'] = response.model_dump()  # Convert Pydantic to dict
    
    # 4. Validation & Safety Check
    for v in item.get("AI", {}).values():
        if is_sensitive(str(v)):
            return None  # Filter out if AI output is sensitive
    
    return item
```

### Parallel Processing Architecture

The project processes multiple papers **in parallel** for efficiency:

```python
# ThreadPoolExecutor for concurrent LLM calls
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    future_to_idx = {
        executor.submit(process_single_item, chain, item, language): idx
        for idx, item in enumerate(data)
    }
    
    # Process completed futures with progress tracking
    for future in tqdm(as_completed(future_to_idx), ...):
        result = future.result()
```

**Performance Benefits:**
- **Speed**: Process multiple papers simultaneously
- **Resource Utilization**: Efficient API usage
- **Scalability**: Configurable worker count (`--max_workers`)
- **Cost Optimization**: Parallel processing reduces total execution time

### Error Handling & Resilience

The system implements multiple layers of error handling:

#### 1. **Structured Output Parsing Errors**
```python
try:
    response: Structure = chain.invoke(...)
    item['AI'] = response.model_dump()
except langchain_core.exceptions.OutputParserException as e:
    # Attempt to extract partial JSON from error message
    # Merge with defaults to ensure all fields exist
    item['AI'] = {**default_ai_fields, **partial_data}
```

#### 2. **General Exception Handling**
```python
except Exception as e:
    # Provide default fallback values
    item['AI'] = {
        "tldr": "Processing failed",
        "motivation": "Processing failed",
        # ... other fields
    }
```

#### 3. **Validation Layer**
```python
# Ensure all required fields exist
for field in default_ai_fields.keys():
    if field not in item['AI']:
        item['AI'][field] = default_ai_fields[field]
```

**Resilience Features:**
- **Graceful Degradation**: Papers with failed processing still appear with fallback text
- **Partial Recovery**: Attempts to salvage partial JSON from parsing errors
- **Default Values**: Always provides complete structure even on failure
- **Continuing Processing**: One paper failure doesn't stop batch processing

### Content Safety & Post-Processing

#### 1. **Sensitive Content Filtering**

Before and after LLM processing, content is checked via external API:

```python
def is_sensitive(content: str) -> bool:
    resp = requests.post(
        "https://spam.dw-dengwei.workers.dev",
        json={"text": content},
        timeout=5
    )
    return result.get("sensitive", True)
```

- **Pre-filtering**: Filters abstracts before sending to LLM (saves API costs)
- **Post-filtering**: Filters LLM-generated content before storage
- **Double Protection**: Ensures no sensitive content in final output

#### 2. **GitHub Code Detection**

Extracts and enriches GitHub repository information:

```python
def check_github_code(content: str) -> Dict:
    # Regex pattern matching for GitHub URLs
    github_pattern = r"https?://github\.com/([a-zA-Z0-9-_]+)/([a-zA-Z0-9-_\.]+)"
    
    # API call to get repository metadata
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    # Returns: code_url, code_stars, code_last_update
```

**Enhancement Features:**
- **Link Extraction**: Finds GitHub links in abstracts
- **Metadata Enrichment**: Fetches star count and last update date
- **User Experience**: Enables frontend to show code availability indicators

### LLM Provider Flexibility

The architecture supports multiple LLM providers:

#### Supported Providers (via OpenAI-compatible APIs)

1. **DeepSeek** (Default/Recommended)
   - Cost-effective (~0.2 CNY/day)
   - Good quality for academic content
   - `OPENAI_BASE_URL=https://api.deepseek.com/v1`
   - `MODEL_NAME=deepseek-chat`

2. **OpenAI GPT Models**
   - `OPENAI_BASE_URL=https://api.openai.com/v1`
   - `MODEL_NAME=gpt-4o-mini` or `gpt-4o`

3. **Any OpenAI-Compatible Provider**
   - Anthropic Claude
   - Local LLM servers (Ollama, vLLM, etc.)
   - Other compatible APIs

**Configuration:**
```yaml
# GitHub Secrets
OPENAI_API_KEY: "your-api-key"
OPENAI_BASE_URL: "https://api.deepseek.com/v1"  # Any compatible endpoint

# GitHub Variables
MODEL_NAME: "deepseek-chat"  # Model identifier
LANGUAGE: "Chinese"          # Output language
```

### Cost Optimization Strategies

1. **Parallel Processing**: Reduces total execution time
2. **Early Filtering**: Sensitive content filtered before LLM call
3. **Efficient Models**: Default to cost-effective models (DeepSeek)
4. **Structured Output**: Function calling reduces retries/parsing overhead
5. **Deduplication**: Prevents processing same paper twice

### LLM Output Schema

Each paper's LLM-enhanced data includes:

```json
{
  "AI": {
    "tldr": "Brief, concise summary in target language",
    "motivation": "Research problem and motivation explanation",
    "method": "Approach, methodology, and technical details",
    "result": "Key findings, experimental results, and metrics",
    "conclusion": "Conclusions, contributions, and future work"
  }
}
```

**Use Cases:**
- **TLDR**: Quick overview for busy researchers
- **Motivation**: Understanding research problem and context
- **Method**: Technical approach and implementation details
- **Result**: Experimental outcomes and performance metrics
- **Conclusion**: Key takeaways and future directions

### Integration with Frontend

The LLM-generated structured data powers the frontend features:

- **Search**: Full-text search across all AI fields
- **Filtering**: Keyword matching in AI summaries
- **Display**: Organized paper cards with AI summaries
- **Detail View**: Modal showing complete AI analysis
- **Localization**: Language-specific summaries based on `LANGUAGE` config

---

## ⚙️ Configuration

### Required GitHub Secrets
```yaml
OPENAI_API_KEY:        # API key for LLM service
OPENAI_BASE_URL:       # Base URL (e.g., https://api.deepseek.com/v1)
TOKEN_GITHUB:          # Optional: GitHub token for repo metadata
ACCESS_PASSWORD:       # Optional: Password for site protection
```

### Required GitHub Variables
```yaml
CATEGORIES:            # Comma-separated (e.g., "cs.CV, cs.CL, cs.AI")
LANGUAGE:              # Output language (e.g., "Chinese", "English")
MODEL_NAME:            # LLM model name (e.g., "deepseek-chat", "gpt-4o-mini")
EMAIL:                 # Git commit email
NAME:                  # Git commit name
```

---

## 🚀 Workflow Execution Flow

### Daily Automated Run (GitHub Actions)

```
1. Trigger (Cron: 1:30 AM UTC daily)
   │
   ├─► Install dependencies (UV)
   │
   ├─► Crawl arXiv papers
   │   └─► Output: data/YYYY-MM-DD.jsonl
   │
   ├─► Check for duplicates
   │   ├─► Exit if no new content (skip remaining steps)
   │   └─► Continue if new content found
   │
   ├─► AI Enhancement
   │   └─► Output: data/YYYY-MM-DD_AI_enhanced_LANGUAGE.jsonl
   │
   ├─► Convert to Markdown
   │   └─► Output: data/YYYY-MM-DD.md
   │
   ├─► Update file list
   │   └─► Update: assets/file-list.txt
   │
   ├─► Inject configuration
   │   ├─► Password hash into auth-config.js
   │   └─► Repository info into data-config.js
   │
   ├─► Commit to branches
   │   ├─► Code changes → main branch
   │   └─► Data files → data branch
   │
   └─► Deploy to GitHub Pages (automatic)
```

---

## 💡 Features & Capabilities

### For End Users
- 📅 **Date Navigation**: Browse papers by specific date or date range
- 🏷️ **Category Filtering**: Filter by arXiv categories (cs.CV, cs.CL, etc.)
- 🔍 **Smart Search**: Full-text search across titles, abstracts, AI summaries
- ⭐ **Keyword Highlighting**: Custom keywords for personalized paper discovery
- 👤 **Author Tracking**: Follow papers from specific authors
- 📊 **Statistics**: Visualize paper trends over time
- 🔒 **Privacy**: All preferences stored locally (LocalStorage)

### For Developers
- 🧪 **Local Testing**: `run.sh` script for local development
- 🔄 **Modular Design**: Easy to extend or modify components
- 📝 **Structured Output**: Consistent JSON schema for AI summaries
- 🚀 **Scalable**: Parallel processing support
- 🛡️ **Error Resilient**: Comprehensive error handling and fallbacks

---

## 📊 Data Schema

### Input JSONL (from Scrapy)
```json
{
  "id": "2401.12345",
  "categories": ["cs.CV", "cs.AI"],
  "title": "Paper Title",
  "authors": ["Author 1", "Author 2"],
  "summary": "Abstract text...",
  "abs": "https://arxiv.org/abs/2401.12345"
}
```

### Enhanced JSONL (after AI processing)
```json
{
  "id": "2401.12345",
  "categories": ["cs.CV", "cs.AI"],
  "title": "Paper Title",
  "authors": ["Author 1", "Author 2"],
  "summary": "Abstract text...",
  "abs": "https://arxiv.org/abs/2401.12345",
  "AI": {
    "tldr": "Brief summary in target language",
    "motivation": "Research motivation explanation",
    "method": "Methodology description",
    "result": "Key results and findings",
    "conclusion": "Conclusion and future work"
  },
  "code_url": "https://github.com/owner/repo",  // Optional
  "code_stars": 123,                             // Optional
  "code_last_update": "2024-01-15"              // Optional
}
```

---

## 🔐 Security Considerations

1. **Sensitive Content Filtering**: AI-generated content is checked via external API
2. **Optional Authentication**: Password protection via SHA-256 hashing
3. **Secrets Management**: All API keys stored in GitHub Secrets
4. **Data Isolation**: Code and data stored in separate branches
5. **Client-Side Privacy**: User preferences never sent to server

---

## 🎨 UI/UX Features

- **Modern Design**: Clean, minimalist interface with smooth animations
- **Responsive Layout**: Works on desktop, tablet, and mobile devices
- **Keyboard Navigation**: Arrow keys for paper navigation, space for random
- **Loading States**: Visual feedback during data loading
- **Error Handling**: User-friendly error messages
- **Accessibility**: Semantic HTML and ARIA labels

---

## 📈 Performance Optimizations

- **Parallel AI Processing**: Multiple workers for faster summarization
- **Lazy Loading**: Papers loaded on-demand
- **Client-Side Filtering**: No server round-trips for filtering
- **Efficient Data Structures**: Optimized filtering and search algorithms
- **Git LFS**: Large data files stored efficiently

---

## 🐛 Error Handling

- **Scrapy Failures**: Logged and reported in workflow
- **AI API Errors**: Fallback to default structured output
- **Missing Data**: Graceful degradation with placeholder text
- **Network Issues**: Retry logic in GitHub Actions workflow
- **Frontend Errors**: Error boundaries and user notifications

---

## 📝 License

Apache 2.0 License - See LICENSE file for details

---

## 🤝 Contributing

The project welcomes contributions! Key areas:
- Additional LLM providers
- New filtering options
- UI/UX improvements
- Performance optimizations
- Documentation enhancements

---

## 🔗 Links

- **Live Demo**: https://dw-dengwei.github.io/daily-arXiv-ai-enhanced/
- **GitHub Repository**: https://github.com/dw-dengwei/daily-arXiv-ai-enhanced
- **Documentation**: See README.md for setup instructions

---

*This illustration was generated to provide a comprehensive overview of the daily-arXiv-ai-enhanced project architecture, data flow, and key components.*

