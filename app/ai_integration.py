"""
AI integration for intelligent insights and analysis
"""
import streamlit as st
import requests
import json
from typing import Optional, Tuple
from app.config import ANTHROPIC_MODEL, MAX_TOKENS, TEMPERATURE

def get_ai_insights(prompt: str, context: str = "", api_key: str = "") -> str:
    """
    Get AI-powered insights using Anthropic Claude

    Args:
        prompt: The analysis prompt
        context: Additional context data
        api_key: Anthropic API key

    Returns:
        str: AI-generated insights or error message
    """
    # Priority: st.secrets → sidebar input → empty
    if not api_key:
        try:
            api_key = st.secrets["ANTHROPIC_API_KEY"]
        except:
            api_key = st.session_state.get("api_key", "")

    if not api_key or not api_key.strip():
        return ("⚠️ **API Key Required**\n\n"
                "Please add your Anthropic API key in the sidebar under ⚙️ AI Settings "
                "Or add `ANTHROPIC_API_KEY` to your Streamlit secrets file.")

    try:
        headers = {
            "x-api-key": api_key.strip(),
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        system_prompt = """You are an expert retail intelligence analyst specializing in Samsung's field merchandising data.
        Provide actionable insights, identify trends, and suggest optimization strategies.
        Be concise, data-driven, and focus on business impact."""

        full_prompt = f"{prompt}\n\nContext: {context}" if context else prompt

        payload = {
            "model": ANTHROPIC_MODEL,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "system": system_prompt,
            "messages": [{"role": "user", "content": full_prompt}]
        }

        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return result["content"][0]["text"]
        else:
            err = response.json() if response.content else {}
            return f"❌ API Error ({err.get('type','unknown')}): {err.get('message','Check API key and quota.')}"

    except requests.Timeout:
        return "❌ Request timed out. Please try again."
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

def generate_store_report(store_data: dict, api_key: str = "") -> str:
    """
    Generate detailed store performance report

    Args:
        store_data: Dictionary containing store metrics
        api_key: Anthropic API key

    Returns:
        str: AI-generated store report
    """
    prompt = f"""
    Generate a comprehensive store performance report for:

    Store: {store_data.get('shop_name', 'Unknown')}
    Shop Code: {store_data.get('shop_code', 'Unknown')}

    Key Metrics:
    - Samsung Sellout: {store_data.get('sam_sellout', 0):,.0f} units
    - Market Share: {store_data.get('sam_share_pct', 0):.1f}%
    - Shelf Share: {store_data.get('sam_shelf', 0):.1f}%
    - Total Sellout: {store_data.get('total_sellout', 0):,.0f} units
    - Brands Stocked: {store_data.get('brands_stocked', 0)}
    - Models Stocked: {store_data.get('models_stocked', 0)}

    Provide:
    1. Performance summary
    2. Strengths and weaknesses
    3. Specific recommendations for improvement
    4. Merchandising priorities
    """

    return get_ai_insights(prompt, api_key=api_key)

def analyze_anomalies(anomalies_df, api_key: str = "") -> str:
    """
    Analyze detected anomalies and provide insights

    Args:
        anomalies_df: DataFrame with anomalies
        api_key: Anthropic API key

    Returns:
        str: AI analysis of anomalies
    """
    if anomalies_df.empty:
        return "✅ No anomalies detected in the dataset."

    high_count = len(anomalies_df[anomalies_df['Severity'] == 'HIGH'])
    med_count = len(anomalies_df[anomalies_df['Severity'] == 'MEDIUM'])

    context = f"""
    Total Anomalies: {len(anomalies_df)}
    High Severity: {high_count}
    Medium Severity: {med_count}

    Top issues:
    {anomalies_df.head(10).to_string(index=False)}
    """

    prompt = """
    Analyze these data quality issues and anomalies in Samsung merchandising data.
    Provide insights on:
    1. Most critical issues requiring immediate attention
    2. Potential root causes
    3. Recommended corrective actions
    4. Prevention strategies for future data collection
    """

    return get_ai_insights(prompt, context, api_key)

def generate_executive_summary(kpis: dict, api_key: str = "") -> str:
    """
    Generate executive summary of dashboard insights

    Args:
        kpis: Dictionary of key performance indicators
        api_key: Anthropic API key

    Returns:
        str: Executive summary
    """
    context = f"""
    Dashboard Overview:
    - Total Stores: {kpis.get('total_shops', 0)}
    - Samsung Sellout: {kpis.get('sam_sellout', 0):,.0f} units
    - Market Share: {kpis.get('sam_share_pct', 0):.1f}%
    - Average Shelf Share: {kpis.get('sam_avg_shelf', 0):.1f}%
    - Data Records: {kpis.get('total_records', 0):,}
    - Weeks Analyzed: {kpis.get('weeks_analyzed', 0)}
    - Brands Tracked: {kpis.get('brands_tracked', 0)}
    """

    prompt = """
    Create a concise executive summary highlighting:
    1. Overall business performance
    2. Key achievements and challenges
    3. Strategic recommendations
    4. Next steps for optimization
    """

    return get_ai_insights(prompt, context, api_key)