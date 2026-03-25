# Samsung Field Intelligence Dashboard

A cutting-edge, AI-powered analytics platform for Samsung's field merchandising operations, featuring One UI 8 design and real-time intelligence capabilities.

## 🚀 Features

- **📊 Real-time Analytics**: Comprehensive dashboard with KPIs, trends, and market insights
- **🤖 AI-Powered Insights**: Claude AI integration for intelligent analysis and recommendations
- **🔍 Anomaly Detection**: Advanced algorithms to identify data quality issues and fake reports
- **📱 One UI 8 Design**: Modern, professional interface inspired by Samsung's design system
- **🔒 Secure Authentication**: Password-protected access with session management
- **📈 Performance Metrics**: Market share, shelf share, sellout analysis, and competitive intelligence
- **🎯 Team Performance**: Merchandiser scorecard and performance tracking
- **📋 Data Validation**: Automated quality checks and reporting

## 🏗️ Architecture

```
app/
├── __init__.py          # Package initialization
├── main.py             # Main application entry point
├── config.py           # Configuration settings
├── auth.py             # Authentication and session management
├── data_processing.py  # Data loading, validation, and processing
├── ai_integration.py   # AI insights and analysis
└── ui_components.py    # UI components and styling
```

## 📋 Requirements

- Python 3.8+
- Streamlit 1.31+
- Anthropic API key (for AI features)

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Verification-Report-MX-CE
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run the application:**
   ```bash
   python run.py
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Authentication
APP_PASSWORD=your_secure_password_here

# AI Integration
ANTHROPIC_API_KEY=sk-ant-your-api-key-here

# Application Settings
MAX_FILE_SIZE_MB=50
LOG_LEVEL=INFO
```

### Streamlit Secrets (Alternative)

For cloud deployment, use Streamlit secrets:

```toml
# .streamlit/secrets.toml
ANTHROPIC_API_KEY = "sk-ant-your-api-key-here"
```

## 📊 Data Format

The dashboard expects Excel files with the following required columns:

- `W`: Week identifier
- `Shop Code`: Unique store identifier
- `Shop Name`: Store name
- `Brand`: Product brand
- `Model`: Product model
- `Sellout`: Units sold
- `Shelf Share`: Percentage of shelf space
- `Price`: Product price
- `Project`: Project identifier
- `Category`: Product category
- `Price segmentation`: Price tier

## 🎨 One UI 8 Design System

The dashboard implements Samsung's One UI 8 design principles:

- **Color Palette**: Professional blue primary with high contrast
- **Typography**: Inter font family with proper hierarchy
- **Components**: Rounded corners, subtle shadows, smooth animations
- **Layout**: Responsive grid system with proper spacing
- **Interactions**: Hover effects and micro-animations

## 🤖 AI Features

### Available AI Capabilities

1. **Executive Summary**: Generate comprehensive business summaries
2. **Anomaly Analysis**: Deep-dive analysis of data quality issues
3. **Store Reports**: Individual store performance insights
4. **Trend Analysis**: Identify patterns and opportunities

### API Key Setup

1. Get an Anthropic API key from [anthropic.com](https://anthropic.com)
2. Set the key in your environment variables or Streamlit secrets
3. AI features will be available throughout the dashboard

## 🔍 Data Quality Checks

The system automatically detects:

- **Shelf Share Anomalies**: Values of 100% for single models
- **Brand Total Issues**: Brand shelf shares exceeding 100%
- **Statistical Outliers**: Unusual sellout patterns
- **Data Completeness**: Missing required fields

## 📈 Key Metrics

- **Market Share**: Samsung's percentage of total sellout
- **Shelf Share**: Average shelf space allocation
- **Store Performance**: Individual store rankings
- **Trend Analysis**: Week-over-week changes
- **Team Performance**: Merchandiser effectiveness scores

## 🚀 Deployment

### Local Development

```bash
python run.py
```

### Streamlit Cloud

1. Push to GitHub
2. Connect to Streamlit Cloud
3. Set secrets in the dashboard
4. Deploy

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["python", "run.py"]
```

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

## 📚 API Reference

### Core Functions

- `load_data(file)`: Load and validate Excel data
- `detect_anomalies(df)`: Identify data quality issues
- `calculate_kpis(df)`: Compute key performance indicators
- `get_ai_insights(prompt)`: Generate AI-powered analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

Copyright © 2026 SmartSense-LTD. All rights reserved.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the Innovation Department
- Check the documentation

## 🔄 Changelog

### Version 1.0.0
- Initial release with One UI 8 design
- AI integration with Claude
- Comprehensive anomaly detection
- Modular architecture
- Production-ready authentication