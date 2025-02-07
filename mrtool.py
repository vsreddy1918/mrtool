import streamlit as st
from tavily import TavilyClient
import pandas as pd
import plotly.express as px
from datetime import datetime
import json

# Initialize Tavily client
client = TavilyClient(api_key="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")

# Page configuration
st.set_page_config(
    page_title="Marketing Research Assistant",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        color: #1F2937;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .insight-card {
        background-color: #F3F4F6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #2563EB;
    }
    .metric-card {
        background-color: #EFF6FF;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    .source-link {
        color: #2563EB;
        text-decoration: none;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

def analyze_market_data(query, analysis_type):
    """Perform market research analysis"""
    try:
        # Enhance query based on analysis type
        enhanced_query = f"{query} {analysis_type} analysis market research data trends statistics"
        
        # Perform search
        response = client.search(
            query=enhanced_query,
            search_depth="advanced",
            max_results=15
        )
        
        return response
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        return None

def extract_metrics(content):
    """Extract numerical metrics from content"""
    import re
    
    # Look for percentage patterns
    percentages = re.findall(r'(\d+(?:\.\d+)?%)', content)
    # Look for currency patterns
    currencies = re.findall(r'[\$₹€£](\d+(?:,\d{3})*(?:\.\d+)?)', content)
    # Look for year patterns
    years = re.findall(r'\b(20\d{2})\b', content)
    
    return {
        'percentages': percentages,
        'currencies': currencies,
        'years': years
    }

# Sidebar
st.sidebar.title("Research Parameters")

# Analysis type selection
analysis_type = st.sidebar.selectbox(
    "Analysis Type",
    [
        "Market Size",
        "Competitor Analysis",
        "Consumer Behavior",
        "Industry Trends",
        "SWOT Analysis",
        "Growth Forecast",
        "Market Share",
        "ROI Analysis"
    ]
)

# Industry selection
industry = st.sidebar.selectbox(
    "Industry",
    [
        "Technology",
        "Healthcare",
        "Finance",
        "Retail",
        "Manufacturing",
        "Energy",
        "E-commerce",
        "Education"
    ]
)

# Region selection
region = st.sidebar.selectbox(
    "Region",
    [
        "Global",
        "North America",
        "Europe",
        "Asia Pacific",
        "India",
        "China",
        "Middle East"
    ]
)

# Main content
st.title("📊 Marketing Research Assistant")
st.markdown("Powered by AI-driven market analysis")

# Query builder
base_query = st.text_area(
    "Research Query",
    value=f"{analysis_type} for {industry} industry in {region}",
    height=100
)

# Example queries
st.markdown("### Quick Research Templates")
col1, col2, col3 = st.columns(3)

example_queries = [
    "Market share analysis of top e-commerce players in India",
    "Consumer behavior trends in digital payments 2024",
    "Sustainable business practices ROI analysis"
]

for col, query in zip([col1, col2, col3], example_queries):
    if col.button(query):
        base_query = query

# Analysis button
if st.button("🔍 Analyze", type="primary"):
    if base_query:
        with st.spinner("Analyzing market data..."):
            results = analyze_market_data(base_query, analysis_type)
            
            if results and results.get('results'):
                # Create tabs for different views
                tab1, tab2, tab3 = st.tabs(["Key Insights", "Market Metrics", "Detailed Analysis"])
                
                with tab1:
                    st.markdown("### 🎯 Key Insights")
                    for idx, result in enumerate(results['results'][:5], 1):
                        st.markdown(f"""
                        <div class="insight-card">
                            <h4>Insight {idx}</h4>
                            <p>{result.get('content', '')[:300]}...</p>
                            <a href="{result.get('url', '#')}" class="source-link" target="_blank">Source 🔗</a>
                        </div>
                        """, unsafe_allow_html=True)
                
                with tab2:
                    st.markdown("### 📈 Market Metrics")
                    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                    
                    # Extract and display metrics
                    all_metrics = []
                    for result in results['results']:
                        metrics = extract_metrics(result.get('content', ''))
                        all_metrics.append(metrics)
                    
                    # Display metrics in cards
                    if all_metrics:
                        with metrics_col1:
                            st.markdown("""
                            <div class="metric-card">
                                <h4>Growth Rates</h4>
                                <p>{}</p>
                            </div>
                            """.format(', '.join(all_metrics[0].get('percentages', ['N/A'])[:3])),
                            unsafe_allow_html=True)
                            
                        with metrics_col2:
                            st.markdown("""
                            <div class="metric-card">
                                <h4>Market Values</h4>
                                <p>{}</p>
                            </div>
                            """.format(', '.join(all_metrics[0].get('currencies', ['N/A'])[:3])),
                            unsafe_allow_html=True)
                            
                        with metrics_col3:
                            st.markdown("""
                            <div class="metric-card">
                                <h4>Forecast Years</h4>
                                <p>{}</p>
                            </div>
                            """.format(', '.join(all_metrics[0].get('years', ['N/A'])[:3])),
                            unsafe_allow_html=True)
                
                with tab3:
                    st.markdown("### 📑 Detailed Analysis")
                    for result in results['results']:
                        st.markdown("---")
                        st.markdown(f"#### {result.get('title', 'Analysis Point')}")
                        st.markdown(result.get('content', ''))
                        st.markdown(f"*Source: [{result.get('url', 'Link')}]({result.get('url', '#')})*")
                
                # Save results
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"market_research_{timestamp}.json"
                with open(filename, 'w') as f:
                    json.dump(results, f)
                st.sidebar.success(f"Research saved to {filename}")
                
    else:
        st.warning("Please enter a research query")

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤ By Srinivasa Reddy | "
    "© 2025 Marketing Research Assistant"
) 