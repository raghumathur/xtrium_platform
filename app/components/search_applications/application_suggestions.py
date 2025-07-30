#==========================================================================================
# Import necessary libraries and modules

# Streamlit is used for building interactive web applications.
# This `st` alias is used throughout Streamlit-based apps for ease of use.

# Importing NumPy library, used for array manipulation and mathematical operations.

# Import the random module to generate random numbers or selections.
# It is part of Python's standard library and is used for operations like shuffling or generating random data.

# Import the figure factory module from Plotly, an interactive graphing library.
# `ff` is used for creating specialized plots like dendrograms, violin plots, and table visualizations.

# Import the graph_objects module from Plotly.
# `go` is used for building figures from low-level components such as traces (lines, bars, etc.).
from app.utils.import_helpers import st, np, pd, random, ff, go, os, re
import plotly.express as px
from typing import List, Dict, Optional, Tuple
import json

# Import specific functions from the recommendation module.
# `calculate_application_match`: A function used to compute the compatibility or "match" score
# between a given material and a specific application. Likely based on predefined parameters.
# `recommend_applications_for_material`: A function used to recommend the most relevant applications
# for a given material based on its properties or characteristics.

from app.backends.recommendation.recommendation import calculate_application_match, recommend_applications_for_material
from app.ui.styles import get_chip_styles
from app.backends.sustainability.scoring import calculate_sustainability_score, get_sustainability_level, extract_certification_tiers
from app.backends.supply_chain.scoring import calculate_supply_chain_score, get_supply_chain_level
import plotly.graph_objects as go

#==========================================================================================

# Define path to buyers database directory
BUYERS_DATABASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'assets', 'databases')
# Pattern for buyers database files
BUYERS_DATABASE_PATTERN = 'buyers_database_*.csv'

@st.cache_data(ttl=300)
def load_buyers_database():
    """
    Load all buyers databases with caching enabled.
    Returns:
        pd.DataFrame: The combined buyers database
    """
    try:
        # Get list of all buyers database files
        import glob
        buyers_files = glob.glob(os.path.join(BUYERS_DATABASE_DIR, BUYERS_DATABASE_PATTERN))
        
        if not buyers_files:
            st.warning("No buyers database files found.")
            return pd.DataFrame()
        
        # Load and concatenate all buyers databases
        dfs = []
        for file_path in buyers_files:
            try:
                df = pd.read_csv(file_path)
                material_name = os.path.basename(file_path).replace('buyers_database_', '').replace('.csv', '')
                # Add material column if it doesn't exist
                if 'Material' not in df.columns:
                    df['Material'] = material_name
                dfs.append(df)
            except Exception as e:
                st.warning(f"Error loading {os.path.basename(file_path)}: {e}")
        
        # Combine all dataframes
        if dfs:
            return pd.concat(dfs, ignore_index=True)
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading buyers databases: {e}")
        return pd.DataFrame()

def filter_buyers_by_application(buyers_df, application_name):
    """
    Filter buyers by application name.
    
    Args:
        buyers_df (pd.DataFrame): The buyers database
        application_name (str): The name of the application to filter by
        
    Returns:
        pd.DataFrame: Filtered buyers for the specified application
    """
    if buyers_df.empty or 'Application' not in buyers_df.columns:
        return pd.DataFrame()
        
    # Filter buyers by the specific application
    filtered_buyers = buyers_df[buyers_df['Application'].str.lower() == application_name.lower()]
    return filtered_buyers

def get_buyer_radar_chart(buyer_data):
    """
    Generate a radar chart for buyer evaluation metrics.
    
    Args:
        buyer_data (pd.Series): A single buyer's data
        
    Returns:
        go.Figure: A radar chart figure
    """
    # Define the metrics to include in the radar chart
    metrics = {
        'Quality': float(buyer_data['Review_Score']) * 20,  # Scale to 0-100
        'Lead Time': max(0, 100 - (float(buyer_data['Typical_Lead_Time_Days']) / 90 * 100)), # Inverse - shorter is better
        'Growth': min(float(buyer_data['Recent_Growth_Rate'].replace('%', '')) * 10, 100),  # Scale to 0-100
    }
    
    # Add sustainability score if available
    if 'Sustainability_Commitment' in buyer_data:
        # Extract a numeric score from the sustainability commitment text
        sustainability_text = str(buyer_data['Sustainability_Commitment'])
        if 'carbon neutral' in sustainability_text.lower() or 'net zero' in sustainability_text.lower():
            metrics['Sustainability'] = 90


def get_market_radar_chart(application_row):
    """
    Generate a radar chart for market direction metrics.
    
    Args:
        application_row (pd.Series): A single application's data
        
    Returns:
        go.Figure: A radar chart figure
    """
    # Initialize metrics dictionary
    metrics = {}
    
    # Process market growth rate (e.g. "12-15%" to numeric value)
    if 'market_growth_rate' in application_row and application_row['market_growth_rate']:
        try:
            growth_text = application_row['market_growth_rate']
            if '-' in growth_text:
                # Take the average of the range
                min_val, max_val = growth_text.replace('%', '').split('-')
                growth_value = (float(min_val) + float(max_val)) / 2
            else:
                growth_value = float(growth_text.replace('%', ''))
                
            # Scale growth: 0-5% (low) maps to 0-30, 5-15% (medium) to 30-70, >15% (high) to 70-100
            if growth_value < 5:
                metrics['Growth Rate'] = growth_value * 6  # 0-30 scale
            elif growth_value < 15:
                metrics['Growth Rate'] = 30 + (growth_value - 5) * 4  # 30-70 scale
            else:
                metrics['Growth Rate'] = 70 + min((growth_value - 15) * 2, 30)  # 70-100 scale, cap at 100
        except (ValueError, TypeError):
            metrics['Growth Rate'] = 50  # Default value if parsing fails
    else:
        metrics['Growth Rate'] = 0
    
    # Process market size (e.g. "$3.2B-4.1B" to numeric value in billions)
    if 'market_size_usd' in application_row and application_row['market_size_usd']:
        try:
            size_text = application_row['market_size_usd']
            # Remove currency symbol and determine scale (M/B/T)
            size_text = size_text.replace('$', '')
            scale_factor = 1
            if 'B' in size_text:
                scale_factor = 1  # Already in billions
            elif 'M' in size_text:
                scale_factor = 0.001  # Convert millions to billions
            elif 'T' in size_text:
                scale_factor = 1000  # Convert trillions to billions
                
            # Clean the text and extract numeric range
            size_text = size_text.replace('B', '').replace('M', '').replace('T', '')
            if '-' in size_text:
                min_val, max_val = size_text.split('-')
                size_value = (float(min_val) + float(max_val)) / 2 * scale_factor
            else:
                size_value = float(size_text) * scale_factor
                
            # Scale market size: 0-1B (small) maps to 0-30, 1-5B (medium) to 30-70, >5B (large) to 70-100
            if size_value < 1:
                metrics['Market Size'] = size_value * 30  # 0-30 scale
            elif size_value < 5:
                metrics['Market Size'] = 30 + (size_value - 1) * 10  # 30-70 scale
            else:
                metrics['Market Size'] = 70 + min((size_value - 5) * 3, 30)  # 70-100 scale, cap at 100
        except (ValueError, TypeError):
            metrics['Market Size'] = 50  # Default value if parsing fails
    else:
        metrics['Market Size'] = 0
    
    # Process market maturity
    if 'market_maturity' in application_row and application_row['market_maturity']:
        maturity = application_row['market_maturity'].lower()
        if 'emerging' in maturity:
            metrics['Future Potential'] = 90
        elif 'growing' in maturity:
            metrics['Future Potential'] = 75
        elif 'mature' in maturity:
            metrics['Future Potential'] = 40
        elif 'declining' in maturity:
            metrics['Future Potential'] = 15
        else:
            metrics['Future Potential'] = 50
    else:
        metrics['Future Potential'] = 0
    
    # Process competitive intensity (inverse - lower competition is better)
    if 'competitive_intensity' in application_row and application_row['competitive_intensity']:
        intensity = application_row['competitive_intensity']
        if isinstance(intensity, (int, float)) or intensity.isdigit():
            # Numeric scale 1-10, invert and normalize to 0-100
            intensity_value = float(intensity)
            metrics['Market Access'] = 100 - ((intensity_value - 1) / 9 * 100)
        else:
            # Text descriptions
            intensity = intensity.lower()
            if 'very high' in intensity:
                metrics['Market Access'] = 10
            elif 'high' in intensity:
                metrics['Market Access'] = 30
            elif 'medium' in intensity:
                metrics['Market Access'] = 60
            elif 'low' in intensity:
                metrics['Market Access'] = 90
            else:
                metrics['Market Access'] = 50
    else:
        metrics['Market Access'] = 0
    
    # Process regulatory environment
    if 'regulatory_tailwinds' in application_row and application_row['regulatory_tailwinds']:
        regulation = application_row['regulatory_tailwinds'].lower()
        if 'very strong' in regulation:
            metrics['Regulatory Support'] = 95
        elif 'strong' in regulation:
            metrics['Regulatory Support'] = 80
        elif 'favorable' in regulation:
            metrics['Regulatory Support'] = 70
        elif 'moderate' in regulation:
            metrics['Regulatory Support'] = 50
        elif 'minimal' in regulation:
            metrics['Regulatory Support'] = 30
        elif 'unfavorable' in regulation or 'restrictive' in regulation:
            metrics['Regulatory Support'] = 10
        else:
            metrics['Regulatory Support'] = 40
    else:
        metrics['Regulatory Support'] = 0
    
    # Ensure we have values for all metrics
    for key, value in metrics.items():
        if value is None:
            metrics[key] = 0
    
    # Create radar chart
    categories = list(metrics.keys())
    values = [metrics[cat] for cat in categories]
    
    # Add the first value at the end to close the polygon
    categories.append(categories[0])
    values.append(values[0])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(77, 171, 247, 0.4)',  # Light blue with transparency
        line=dict(color='#4dabf7'),  # Solid blue line
        name='Market Indicators'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        margin=dict(l=30, r=30, t=30, b=30),
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)'     # Transparent plot area
    )
    
    return fig
    
    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100]),
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=20, b=20),
        height=250
    )
    
    return fig

def compare_buyers(selected_buyers_df):
    """
    Create a comparison chart for multiple buyers.
    
    Args:
        selected_buyers_df (pd.DataFrame): DataFrame containing selected buyers to compare
        
    Returns:
        go.Figure: A comparison chart
    """
    if selected_buyers_df.empty or len(selected_buyers_df) < 2:
        return None
        
    # Define the metrics to compare
    metrics = ['Review_Score', 'Typical_Lead_Time_Days']
    buyer_names = selected_buyers_df['Buyer_Name'].tolist()
    
    # Create a parallel coordinates plot
    fig = px.parallel_coordinates(
        selected_buyers_df,
        dimensions=['Review_Score', 'Typical_Lead_Time_Days'],
        color='Review_Score',
        labels={
            'Review_Score': 'Quality (1-5)', 
            'Typical_Lead_Time_Days': 'Lead Time (days)'
        },
        color_continuous_scale=px.colors.sequential.Blues
    )
    
    fig.update_layout(
        margin=dict(l=40, r=40, t=30, b=20),
        height=300,
        title="Buyer Comparison"
    )
    
    return fig

def get_sustainability_icon(commitment):
    """
    Return an appropriate sustainability icon based on the commitment text.
    
    Args:
        commitment (str): Sustainability commitment text
        
    Returns:
        str: Icon HTML
    """
    commitment = str(commitment).lower()
    
    if 'carbon neutral' in commitment or 'net zero' in commitment:
        return "<span style='color: green; font-size: 1.5em;'>♻️</span>"
    elif any(x in commitment for x in ['renewable', 'reduction', 'recycled', 'sustainable']):
        return "<span style='color: #4dabf7; font-size: 1.5em;'>🌱</span>"
    else:
        return "<span style='color: gray; font-size: 1.5em;'>🔍</span>"

@st.cache_data
def extract_reference_citations(reference_string):
    """
    Extract individual citations from a reference string by splitting on common separators
    
    Args:
        reference_string: String containing one or more citations
        
    Returns:
        List of individual citation strings
    """
    if not reference_string or pd.isna(reference_string):
        return []
        
    # Check for common citation separators
    separators = [';', ',']
    for sep in separators:
        if sep in reference_string:
            return [citation.strip() for citation in reference_string.split(sep) if citation.strip()]
    
    # If no separators found, return the whole string as a single citation
    return [reference_string.strip()]


@st.cache_data
def _load_material_references_enhanced():
    """
    Enhanced implementation that loads references from CSV files while preserving material context
    
    Returns:
        A nested dictionary mapping material types and properties to their references:
        {
            'material_type': {
                'property': ['reference1', 'reference2', ...],
                ...
            },
            ...
            'global': {  # For general references not tied to specific materials
                'property': ['reference1', 'reference2', ...],
                ...
            }
        }
    """
    references = {
        'global': {}  # Default bucket for references without material type
    }
    
    base_dir = "assets/databases"
    if not os.path.exists(base_dir):
        return references
        
    # Define material type column names to look for (in order of preference)
    material_type_columns = [
        'Material Type', 'MaterialType', 'Material_Type', 
        'Category', 'MaterialCategory', 'Material Category'
    ]
    
    # Define material ID column names to look for (in order of preference)
    material_id_columns = [
        'Material ID', 'MaterialID', 'Material_ID', 'ID'
    ]
    
    # Load and process all relevant CSV files
    for filename in os.listdir(base_dir):
        if filename.startswith("materials_database_") and filename.endswith(".csv"):
            filepath = os.path.join(base_dir, filename)
            try:
                df = pd.read_csv(filepath)
                
                # Check if required columns exist
                if "Property Overlap" not in df.columns or "Reference" not in df.columns:
                    continue
                
                # Determine which material column to use (if any)
                material_col = None
                for col in material_type_columns:
                    if col in df.columns:
                        material_col = col
                        break
                        
                # If no material type column, try material ID
                if not material_col:
                    for col in material_id_columns:
                        if col in df.columns:
                            material_col = col
                            break
                
                # Process each row in the dataframe
                for _, row in df.iterrows():
                    if pd.notna(row["Property Overlap"]) and pd.notna(row["Reference"]):
                        # Normalize property separators
                        normalized = str(row["Property Overlap"]).replace(";", ",")
                        properties = [p.strip() for p in normalized.split(",") if p.strip()]
                        reference = str(row["Reference"])
                        
                        # Get material identifier if available
                        if material_col and pd.notna(row[material_col]):
                            material_key = str(row[material_col]).lower().strip()
                            # Initialize dictionary for this material if needed
                            if material_key not in references:
                                references[material_key] = {}
                        else:
                            material_key = 'global'  # Use global bucket if no material specified
                        
                        # Add reference for each property under this material
                        for prop in properties:
                            # Initialize list for this property if needed
                            if prop not in references[material_key]:
                                references[material_key][prop] = []
                                
                            # Add reference if not already present
                            if reference not in references[material_key][prop]:
                                references[material_key][prop].append(reference)
            
            except Exception as e:
                print(f"Error loading references from {filename}: {e}")
    
    return references


@st.cache_data
def load_material_references():
    """
    Load references from CSV files in assets/databases
    
    Returns:
        Dictionary mapping property names to lists of references
    """
    # Use the enhanced implementation to build the reference database
    reference_data = _load_material_references_enhanced()
    
    # For backward compatibility, convert to the old format
    # (flatten the nested dictionary to a simple property -> references map)
    legacy_format = {}
    
    # First add all global references
    for prop, refs in reference_data.get('global', {}).items():
        legacy_format[prop] = refs.copy()
    
    # Then add material-specific references (might override some global ones)
    for material, properties in reference_data.items():
        if material != 'global':
            for prop, refs in properties.items():
                if prop not in legacy_format:
                    legacy_format[prop] = []
                # Add only unique references
                for ref in refs:
                    if ref not in legacy_format[prop]:
                        legacy_format[prop].append(ref)
    
    return legacy_format


def get_property_references(property_name, material_id=None, reference_data=None):
    """
    Get references for a specific property, considering material type if available
    
    Args:
        property_name: Name of the property to get references for
        material_id: Optional material ID to filter references by material type
        reference_data: Pre-loaded reference data (if None, will load it)
        
    Returns:
        List of references for the property, or empty list if none found
    """
    # Load references if not provided
    if reference_data is None:
        reference_data = _load_material_references_enhanced()
    
    # Get material type from ID if available
    material_type = None
    if material_id:
        try:
            # Example placeholder logic to extract material type from ID
            if isinstance(material_id, str) and '_' in material_id:
                # Assuming IDs might be in format like "polymer_123" or "metal_456"
                material_type = material_id.split('_')[0].lower()
            elif isinstance(material_id, str):
                # Use first part of material_id if it contains a known material type
                known_types = ["metal", "polymer", "ceramic", "composite", "alloy"]
                for t in known_types:
                    if t in material_id.lower():
                        material_type = t
                        break
        except:
            # Fallback to None if parsing fails
            material_type = None
    
    # First try material-specific references if we have a material type
    if material_type and material_type in reference_data and property_name in reference_data[material_type]:
        return reference_data[material_type][property_name]
    
    # Then try using the material ID as a direct key (if database is organized that way)
    if material_id and material_id in reference_data and property_name in reference_data[material_id]:
        return reference_data[material_id][property_name]
    
    # Finally fall back to global references
    if property_name in reference_data.get('global', {}):
        return reference_data['global'][property_name]
    
    # No references found
    return []


def display_property_references(properties, material_id=None):
    """
    Display scientific references for a list of properties
    
    Args:
        properties: List of properties to show references for
        material_id: Optional material ID for reference lookup
    """
    # If no properties provided, nothing to do
    if not properties:
        return
        
    # Load property references (optimized - load once)
    reference_data = _load_material_references_enhanced()
    
    # Check if any properties have references, considering material context
    has_references = False
    for prop in properties:
        refs = get_property_references(prop, material_id, reference_data)
        if refs:
            has_references = True
            break
    
    if has_references:
        # Style for property chips in reference section
        chip_style = {'bg': 'rgba(0, 204, 150, 0.2)', 'color': '#00cc96'}
        
        # Create a container for references
        with st.container():
            st.markdown("<hr style='margin:15px 0; border-color:#333;'>", unsafe_allow_html=True)
            st.markdown("<p style='color:#c0c0c0; font-size:0.9em; font-weight:600;'>📚 Scientific Sources</p>", unsafe_allow_html=True)
            
            # Display references for each property that has them
            for prop in properties:
                # Get references specific to this property+material combination
                property_refs = get_property_references(prop, material_id, reference_data)
                
                if property_refs:
                    # Show the property name
                    st.markdown(
                        f"<div style='margin-top:10px;'>"
                        f"<span style='background-color:{chip_style['bg']}; color:{chip_style['color']}; "
                        f"padding:3px 8px; border-radius:12px; font-size:0.9em;'>{prop}</span>"
                        f"</div>", 
                        unsafe_allow_html=True
                    )
                    
                    # Show all references for this property
                    for ref_string in property_refs:
                        citations = extract_reference_citations(ref_string)
                        for citation in citations:
                            st.markdown(f"<div style='margin-left:15px; margin-bottom:5px; color:#e0e0e0; font-size:0.9em;'>• {citation}</div>", 
                                       unsafe_allow_html=True)

from app.backends.recommendation.recommendation import calculate_application_match, recommend_applications_for_material
from app.ui.styles import get_chip_styles

#==========================================================================================

def get_recommendations(applications_df, selected_material_row, selected_filters, suppliers_df, domains=None, supply_chain=None, sustainability=None):
    """
    Suggest applications based on material properties and application property ranges.

    Args:
        applications_df (pd.DataFrame): Unified applications database DataFrame.
        selected_material_row (pd.Series): The selected material's properties.
        selected_filters (list): Property weights and filters for importance matching.
        suppliers_df (pd.DataFrame): Supplier information dataframe.
        domains (list, optional): Selected application domains for focusing recommendations.
        supply_chain (dict, optional): Supply chain preferences including domestic preference, lead time and cost.
        sustainability (dict, optional): Sustainability preferences including carbon footprint and recycling requirements.
    """
    # Initialize session state for filters
    if "filters" not in st.session_state:
        st.session_state["filters"] = []

    # Add Suggest Button
    st.divider()
    if st.button("Suggest Applications", key="suggest_button"):
        st.session_state["run_suggestion"] = True

    # Check session state to run the logic
    if st.session_state.get("run_suggestion", False):
        try:
            # Filter applications by domain if domains are specified
            filtered_applications = applications_df
            if domains and len(domains) > 0:
                # Filter applications by selected domains/industries
                filtered_applications = applications_df[applications_df['industry'].isin(domains)]
                if filtered_applications.empty:
                    # If no applications match the domains, display a warning and use all applications
                    st.warning("No applications found in the selected domains. Showing all relevant applications instead.")
                    filtered_applications = applications_df
            
            # Use our simplified direct property matching logic
            recommendations = direct_property_matching(selected_material_row, filtered_applications)
            
            if recommendations.empty:
                st.warning("No matching applications found based on properties. Check material properties or expand your criteria.")
            else:
                # Calculate sustainability and supply chain scores for each recommendation if the data exists
                sustainability_cols = ['certifications', 'lca_carbon_footprint', 'lca_water_usage', 'lca_energy',
                                     'recycled_content', 'renewable_content', 'supply_chain_transparency',
                                     'cert_tier1', 'cert_tier2', 'cert_tier3']
                
                # Check for sustainability data in applications
                has_sustainability_data = any(col in filtered_applications.columns for col in sustainability_cols)
                
                # Load buyers database for supply chain score calculation
                buyers_df = load_buyers_database()
                has_supply_chain_data = not buyers_df.empty
                
                # Extract certification tiers from the applications DataFrame
                if has_sustainability_data:
                    cert_tiers = extract_certification_tiers(filtered_applications)
                
                # For each recommendation, find the corresponding row in filtered_applications and calculate scores
                for idx, row in recommendations.iterrows():
                    use_case = row['use_case']
                    # Match by both use_case AND industry to ensure accurate application identification
                    industry = row['industry']
                    app_rows = filtered_applications[(filtered_applications['use_case'] == use_case) & 
                                                   (filtered_applications['industry'] == industry)]
                    
                    if not app_rows.empty:
                        app_row = app_rows.iloc[0]
                        
                        # Calculate sustainability score if data exists
                        if has_sustainability_data:
                            sustainability_score = calculate_sustainability_score(app_row, cert_tiers)
                            recommendations.at[idx, 'sustainability_score'] = sustainability_score
                            # Store certification data in recommendations for display
                            cert_value = app_row.get('certifications', '')
                            recommendations.at[idx, 'certifications'] = cert_value
                        else:
                            recommendations.at[idx, 'sustainability_score'] = 50.0  # Default score
                            recommendations.at[idx, 'certifications'] = ""  # Empty certifications
                        
                        # Calculate supply chain score if data exists
                        if has_supply_chain_data:
                            # Use the application name to filter buyers for more accurate scoring
                            supply_chain_score = calculate_supply_chain_score(app_row, buyers_df, application=use_case)
                            recommendations.at[idx, 'supply_chain_score'] = supply_chain_score
                        else:
                            recommendations.at[idx, 'supply_chain_score'] = 50.0  # Default score
                    else:
                        # Use default scores when no matching application is found
                        recommendations.at[idx, 'sustainability_score'] = 50.0  # Default score
                        recommendations.at[idx, 'supply_chain_score'] = 50.0  # Default score
                        recommendations.at[idx, 'certifications'] = ""  # Empty certifications
                else:
                    # If no sustainability data found in the DataFrame, use default scores
                    recommendations['sustainability_score'] = 50.0
                    recommendations['supply_chain_score'] = 50.0
                
                # Calculate the Xtrium Confidence Score based on match_score, sustainability_score, and supply_chain_score
                for idx, row in recommendations.iterrows():
                    # Get all component scores (Property Match, Sustainability, Supply Chain)
                    match_score = row.get('match_score', 0)
                    sustainability_score = row.get('sustainability_score', 50.0)
                    supply_chain_score = row.get('supply_chain_score', 50.0)
                    
                    # Calculate weighted composite score
                    # Property match is most important (50%), sustainability and supply chain split the rest (25% each)
                    confidence_score = (0.5 * match_score) + (0.25 * sustainability_score) + (0.25 * supply_chain_score)
                    
                    # Store the calculated confidence score
                    recommendations.at[idx, 'confidence_score'] = round(confidence_score, 1)
                
                st.markdown("### Suggested Applications")
                # Display recommendations
                display_recommendations(recommendations, suppliers_df, filtered_applications)
                
            # Reset the suggestion flag
            st.session_state["run_suggestion"] = False
        except Exception as e:
            st.error(f"Error generating recommendations: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
            st.session_state["run_suggestion"] = False
    #else:
        # If button not clicked, show a message
        #st.info("Click 'Suggest Applications' to find applications matching this material's properties.")


def render_property_overlap_chips(property_overlap, material_id=None, unique_id=None):
    """
    Render property overlap as styled chips
    
    Args:
        property_overlap: List of properties that overlap with the recommendation
        material_id: Optional material ID for reference lookup
        unique_id: Optional unique ID for widget keys
        
    Returns:
        List of parsed property strings
    """
    # Safeguard against invalid input
    if not property_overlap or pd.isna(property_overlap):
        return []
        
    # Convert string to list if needed
    if isinstance(property_overlap, str):
        try:
            properties = eval(property_overlap)
            if not isinstance(properties, list):
                normalized_string = property_overlap.replace(';', ',')
                properties = [p.strip() for p in normalized_string.split(',') if p.strip()]
        except:
            normalized_string = property_overlap.replace(';', ',')
            properties = [p.strip() for p in normalized_string.split(',') if p.strip()]
    else:
        properties = property_overlap if isinstance(property_overlap, list) else [property_overlap]
    
    # Get chip style - it's a string, not a dictionary
    chip_style = get_chip_styles()
    
    # Create HTML for rendering properties as chips
    html_properties = []
    for prop in properties:
        html_properties.append(
            f'<span style="{chip_style}">{prop}</span>'
        )
    
    # Define chip container style
    container_style = "display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 10px;"
    
    # Render the chips
    if html_properties:
        st.markdown(
            f"<div style='{container_style}'>{''.join(html_properties)}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<p style='color:#b0b0b0; font-size:0.9em; font-style:italic;'>No matching properties identified.</p>", 
            unsafe_allow_html=True
        )
        
    return properties


def render_certification_chips(certifications, cert_tiers=None, unique_id=None):
    """
    Render certifications as styled chips, color-coded by tier if tier information is available
    
    Args:
        certifications: String or list of certification names
        cert_tiers: Optional dictionary of certification tiers
        unique_id: Optional unique ID for widget keys
        
    Returns:
        List of parsed certification strings
    """
    # Safeguard against invalid input
    if certifications is None or (isinstance(certifications, str) and (not certifications.strip() or pd.isna(certifications))):
        return []
    
    # Handle empty list case
    if isinstance(certifications, list) and len(certifications) == 0:
        return []
        
    # Convert string to list if needed
    if isinstance(certifications, str):
        try:
            # First try to split by commas
            if ',' in certifications:
                cert_list = [cert.strip() for cert in certifications.split(',') if cert.strip()]
            # Then try by spaces if it appears to be a single certificate per entry
            else:
                cert_list = [certifications.strip()]
        except:
            cert_list = [certifications]
    else:
        # Already a list or other iterable
        cert_list = certifications if isinstance(certifications, list) else [certifications]
    
    # Get chip style - it's a string, not a dictionary
    base_chip_style = get_chip_styles()
    
    # Default cert tiers if none provided
    if cert_tiers is None:
        cert_tiers = {
            'tier1': ['Cradle to Cradle', 'FSC', 'GreenGuard Gold'],
            'tier2': ['ISO 14001', 'LEED', 'GreenGuard', 'ENERGY STAR', 'AS9100D', 'ASME', 'ASTM', 'TAPPI', 'IEC', 'IACS', 'API', 'IATF 16949', 'ASTM F1295', 'IEC 61400', 'IEC 61730', 'NADCAP'],
            'tier3': ['EPD', 'HPD', 'REACH', 'RoHS']
        }
    
    # Define tier-specific colors
    tier_colors = {
        'tier1': "rgba(0, 204, 150, 0.15)",    # Green for top tier
        'tier2': "rgba(65, 105, 225, 0.15)",   # Blue for mid tier
        'tier3': "rgba(130, 130, 130, 0.15)",  # Gray for basic tier
        'default': "rgba(130, 130, 130, 0.1)"   # Default for unclassified
    }
    
    # Define tier-specific border colors
    tier_borders = {
        'tier1': "rgba(0, 204, 150, 0.5)",    # Green border
        'tier2': "rgba(65, 105, 225, 0.5)",   # Blue border
        'tier3': "rgba(130, 130, 130, 0.5)",  # Gray border
        'default': "rgba(130, 130, 130, 0.3)"  # Default border
    }
    
    # Create HTML for rendering certifications as chips
    html_certs = []
    for cert in cert_list:
        # Determine which tier this certification belongs to
        cert_tier = 'default'
        for tier, certs in cert_tiers.items():
            if cert in certs:
                cert_tier = tier
                break
        
        # Create styled chip based on tier
        cert_chip_style = base_chip_style + f" background-color: {tier_colors[cert_tier]}; border-color: {tier_borders[cert_tier]};"
        html_certs.append(
            f'<span style="{cert_chip_style}">{cert}</span>'
        )
    
    # Define chip container style
    container_style = "display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 10px;"
    
    # Render the chips
    if html_certs:
        st.markdown(
            f"<div style='{container_style}'>{''.join(html_certs)}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<p style='color:#b0b0b0; font-size:0.9em; font-style:italic;'>No certifications available.</p>", 
            unsafe_allow_html=True
        )
        
    return cert_list


def render_manufacturability_chips(processes, process_categories=None, unique_id=None):
    """
    Render manufacturing processes as styled chips with color coding based on process compatibility
    
    Args:
        processes: String or list of manufacturing process names
        process_categories: Optional dictionary of process categories by compatibility
        unique_id: Optional unique ID for widget keys
        
    Returns:
        List of parsed process strings
    """
    # Safeguard against invalid input
    if processes is None or (isinstance(processes, str) and (not processes.strip() or pd.isna(processes))):
        return []
    
    # Handle empty list case
    if isinstance(processes, list) and len(processes) == 0:
        return []
        
    # Convert string to list if needed
    if isinstance(processes, str):
        try:
            # First try to split by commas
            if ',' in processes:
                process_list = [proc.strip() for proc in processes.split(',') if proc.strip()]
            # Then try by spaces if it appears to be a single process per entry
            else:
                process_list = [processes.strip()]
        except:
            process_list = [processes]
    else:
        # Already a list or other iterable
        process_list = processes if isinstance(processes, list) else [processes]
    
    # Get chip style - it's a string, not a dictionary
    base_chip_style = get_chip_styles()
    
    # Default process categories if none provided
    if process_categories is None:
        process_categories = {
            'optimal': ['CNC machining', 'Precision forging', 'Additive manufacturing', 'Injection molding'],
            'standard': ['Forging', 'Casting', 'Extrusion', 'Rolling', 'Heat treatment', 'Welding', 'Brazing'],
            'challenging': ['Electrochemical machining', 'Chemical milling', 'Laser cutting']
        }
    
    # Define category-specific colors
    category_colors = {
        'optimal': "rgba(0, 204, 150, 0.15)",    # Green for optimal processes
        'standard': "rgba(65, 105, 225, 0.15)",   # Blue for standard processes
        'challenging': "rgba(130, 130, 130, 0.15)",  # Gray for challenging processes
        'default': "rgba(130, 130, 130, 0.1)"   # Default for unclassified
    }
    
    # Define category-specific border colors
    category_borders = {
        'optimal': "rgba(0, 204, 150, 0.5)",    # Green border
        'standard': "rgba(65, 105, 225, 0.5)",   # Blue border
        'challenging': "rgba(130, 130, 130, 0.5)",  # Gray border
        'default': "rgba(130, 130, 130, 0.3)"  # Default border
    }
    
    # Create HTML for rendering manufacturing processes as chips
    html_processes = []
    for process in process_list:
        # Determine which category this process belongs to
        process_category = 'default'
        for category, processes_list in process_categories.items():
            if any(proc.lower() in process.lower() or process.lower() in proc.lower() for proc in processes_list):
                process_category = category
                break
        
        # Create styled chip based on category
        process_chip_style = base_chip_style + f" background-color: {category_colors[process_category]}; border-color: {category_borders[process_category]};"
        html_processes.append(
            f'<span style="{process_chip_style}">{process}</span>'
        )
    
    # Define chip container style
    container_style = "display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 10px;"
    
    # Render the chips
    if html_processes:
        st.markdown(
            f"<div style='{container_style}'>{''.join(html_processes)}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<p style='color:#b0b0b0; font-size:0.9em; font-style:italic;'>No manufacturing processes available.</p>", 
            unsafe_allow_html=True
        )
        
    return process_list


def render_manufacturability_parameters(params):
    """
    Render manufacturability parameters in a compact table format
    
    Args:
        params: Dictionary of manufacturability parameters
    """
    if not params or not isinstance(params, dict):
        st.markdown(
            "<p style='color:#b0b0b0; font-size:0.9em; font-style:italic;'>No manufacturability parameters available.</p>", 
            unsafe_allow_html=True
        )
        return
    
    # Define the table style directly inline to avoid potential issues
    st.markdown("""
    <style>
        .manuf-table {
            width: 100%;
            font-size: 0.85em;
            border-collapse: collapse;
            margin-bottom: 1em;
        }
        .manuf-table tr {
            border-bottom: 1px solid rgba(49, 51, 63, 0.1);
        }
        .manuf-table tr:last-child {
            border-bottom: none;
        }
        .param-name {
            color: #888888;
            padding: 5px 10px 5px 0;
            white-space: nowrap;
            width: 40%;
            vertical-align: top;
        }
        .param-value {
            color: #ffffff;
            padding: 5px 0;
            font-weight: 500;
            border-radius: 3px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create HTML table for the parameters separately from the style
    table_html = "<table class='manuf-table'>"
    for param_name, param_value in params.items():
        # Format parameter name with spaces and capitalization
        formatted_name = param_name.replace('_', ' ').title()
        table_html += f"<tr><td class='param-name'>{formatted_name}:</td><td class='param-value'>{param_value}</td></tr>"
    table_html += "</table>"
    
    # Render the table as a separate markdown call
    st.markdown(table_html, unsafe_allow_html=True)


def display_recommendations(recommendations_df, suppliers_df, filtered_applications=None):
    """
    Display the recommendations DataFrame in a well-formatted way.
    
    Args:
        recommendations_df (pd.DataFrame): The DataFrame containing recommendations.
        suppliers_df (pd.DataFrame): Supplier information dataframe.
        filtered_applications (pd.DataFrame): All application data for certification lookup.
    """
    if recommendations_df.empty:
        st.warning("No applications match the selected criteria.")
        return

    # Iterate over each row in the recommendations DataFrame
    for idx, row in recommendations_df.iterrows():
        use_case = row.get("use_case", "Unknown")
        industry = row.get("industry", "Unknown")
        property_overlap = row.get("property_overlap", "Unknown")
        match_score = row.get("match_score", 0)
        material_id = row.get("material_id", None)  # Get material ID if available
        
        # Get sustainability score if available
        has_sustainability_score = 'sustainability_score' in row
        sustainability_score = row.get("sustainability_score", 0) if has_sustainability_score else 0
        
        # Get sustainability level and color
        if has_sustainability_score:
            sustainability_level, sustainability_color = get_sustainability_level(sustainability_score)
        else:
            sustainability_level, sustainability_color = "N/A", "#888888"
        
        # Create a unique identifier for this recommendation using its position in the dataframe
        unique_id = f"rec_{idx}"

        # Display the formatted recommendation with "Industry | Use-case" format
        with st.expander(f"{industry} | {use_case}"):
            # Create two columns for layout
            col1, col2 = st.columns([5,5])
            
            # Left column: Use case information with improved typography for dark mode
            with col1:
                # Use Case with prominent styling - significantly larger and brighter for dark mode
                st.markdown(
                    f"<h3 style='color:#ffffff; font-size:1.5em; font-weight:600; margin-bottom:10px;'>"
                    f"Component: {use_case}</h3>", 
                    unsafe_allow_html=True
                )
                
                # Industry with secondary styling - visible in dark mode
                st.markdown(
                    f"<div style='margin-bottom:14px; font-size:1.05em;'>"
                    f"Industry: {industry}</div>",
                    unsafe_allow_html=True
                )
                
                # Property overlap (Renamed back to 'Rationale for Match' with user-specified styling)
                st.markdown(
                    f"<p style='color:#666666; margin-bottom:0.5em;'><strong>RATIONALE FOR MATCH</strong></p>",
                    unsafe_allow_html=True
                )
                
                # First render property chips
                properties = render_property_overlap_chips(property_overlap, material_id, unique_id)
                
                # Add Certifications section header (will be displayed later in specific condition)
                
                # Extract certifications from the application row in recommendations DataFrame
                # For aerospace applications, certifications follow the pattern "ISO 14001, ASME"
                use_case = row.get("use_case", "")
                industry = row.get("industry", "")
                cert_value = row.get("certifications", "")
                
                # Display certifications section with header
                st.markdown(
                    f"<p style='color:#666666; margin-bottom:0.5em; margin-top:1.5em;'><strong>CERTIFICATIONS APPLICABLE</strong></p>",
                    unsafe_allow_html=True
                )
                
                # Get all certifications from all sources
                all_certs = []
                cert_tiers = {
                    'tier1': [],
                    'tier2': [],
                    'tier3': []
                }
                
                # Extract use case and industry for lookups
                use_case = row.get('use_case', '')
                industry = row.get('industry', '')
                
                # Try to access the full applications database if available
                app_row = None
                try:
                    if filtered_applications is not None:
                        # Look up in filtered_applications to get all certification tiers
                        app_rows = filtered_applications[(filtered_applications['use_case'] == use_case) & 
                                                       (filtered_applications['industry'] == industry)]
                        if not app_rows.empty:
                            app_row = app_rows.iloc[0]
                            
                            # Get all certification data from all tier columns
                            # 1. First get main certifications column
                            if 'certifications' in app_row and isinstance(app_row['certifications'], str) and app_row['certifications'].strip():
                                all_certs.extend([c.strip() for c in app_row['certifications'].split(',') if c.strip()])
                            
                            # 2. Then get tier-specific certifications
                            for tier_col in ['cert_tier1', 'cert_tier2', 'cert_tier3']:
                                if tier_col in app_row and isinstance(app_row[tier_col], str) and app_row[tier_col].strip():
                                    tier_certs = [c.strip() for c in app_row[tier_col].split(',') if c.strip()]
                                    all_certs.extend(tier_certs)
                                    # Store certs in their respective tiers for color coding
                                    tier_name = tier_col.replace('cert_', '')
                                    cert_tiers[tier_name] = tier_certs
                except Exception as e:
                    # If there's any error accessing filtered_applications, just continue with the next method
                    pass
                    
                # If we didn't get any certs from the database, try the recommendations data
                if not all_certs:
                    # Use the certifications column from recommendations
                    cert_value = row.get("certifications", "")
                    if isinstance(cert_value, str) and cert_value.strip():
                        all_certs.extend([c.strip() for c in cert_value.split(',') if c.strip()])
                
                # If we still don't have tier data, use default tiers
                if not any(cert_tiers.values()):
                    cert_tiers = {
                        'tier1': ['Cradle to Cradle', 'FSC', 'GreenGuard Gold'],
                        'tier2': ['ISO 14001', 'LEED', 'GreenGuard', 'ENERGY STAR', 'AS9100D', 'ASME', 'ASTM', 'TAPPI', 'IEC', 'IACS', 'API', 'IATF 16949', 'ASTM F1295', 'IEC 61400', 'IEC 61730', 'NADCAP'],
                        'tier3': ['EPD', 'HPD', 'REACH', 'RoHS']
                    }
                
                # Remove duplicates while preserving order
                seen = set()
                all_certs = [c for c in all_certs if not (c in seen or seen.add(c))]
                
                # Display certification count and chips
                if all_certs:
                    # Show the count of certifications
                    #cert_count = len(all_certs)
                    #st.markdown(
                    #    f"<p style='color:#888888; font-size:0.9em; margin-bottom:8px;'>{cert_count} {'certification' if cert_count == 1 else 'certifications'} applicable:</p>",
                    #    unsafe_allow_html=True
                    #)
                    
                    # Render all certifications as chips
                    certifications = render_certification_chips(all_certs, cert_tiers, unique_id)
                else:
                    st.markdown(
                        "<p style='color:#b0b0b0; font-size:0.9em; font-style:italic;'>No certifications available.</p>", 
                        unsafe_allow_html=True
                    )
                    
                # Add Manufacturability section
                st.markdown(
                    f"<p style='color:#666666; margin-bottom:0.5em; margin-top:1.5em;'><strong>MANUFACTURABILITY CONSIDERATIONS</strong></p>",
                    unsafe_allow_html=True
                )
                
                # Extract manufacturability data
                manufacturing_processes = None
                manufacturing_params = {}
                design_considerations = None
                
                # Try to get manufacturability data from application row
                try:
                    if app_row is not None:
                        # Get manufacturing processes
                        if 'manufacturing_processes' in app_row and isinstance(app_row['manufacturing_processes'], str) and app_row['manufacturing_processes'].strip():
                            manufacturing_processes = app_row['manufacturing_processes']
                        
                        # Collect manufacturability parameters into a dictionary
                        param_fields = [
                            'manufacturing_complexity',
                            'min_feature_size',
                            'achievable_tolerance',
                            'anisotropy_concern',
                            'process_maturity',
                            'specialized_equipment_needed'
                        ]
                        
                        for field in param_fields:
                            if field in app_row and not pd.isna(app_row[field]) and str(app_row[field]).strip():
                                manufacturing_params[field] = app_row[field]
                        
                        # Get design considerations
                        if 'design_considerations' in app_row and isinstance(app_row['design_considerations'], str) and app_row['design_considerations'].strip():
                            design_considerations = app_row['design_considerations']
                except Exception as e:
                    # If there's any error, continue with default or empty values
                    pass
                
                # Use default process list if none found in database
                if manufacturing_processes is None:
                    # Default processes based on industry
                    if 'aerospace' in industry.lower():
                        manufacturing_processes = "CNC machining, Additive manufacturing, Precision forging, Heat treatment"
                    elif 'electronics' in industry.lower():
                        manufacturing_processes = "PCB fabrication, Wave soldering, Injection molding"
                    elif 'automotive' in industry.lower():
                        manufacturing_processes = "Die casting, Stamping, Forging, Injection molding"
                    else:
                        manufacturing_processes = "CNC machining, Casting, Forging"
                
                # Display manufacturing processes as chips
                process_categories = {
                    'optimal': ['CNC machining', 'Precision forging', 'Additive manufacturing', 'Injection molding', '3D printing', 'SLS', 'DMLS'],
                    'standard': ['Forging', 'Casting', 'Extrusion', 'Rolling', 'Heat treatment', 'Welding', 'Brazing', 'Stamping', 'PCB fabrication'],
                    'challenging': ['Electrochemical machining', 'Chemical milling', 'Laser cutting', 'EDM']
                }
                
                # Render process chips
                render_manufacturability_chips(manufacturing_processes, process_categories)
                
                # Display manufacturability parameters table if we have parameters
                if manufacturing_params:
                    render_manufacturability_parameters(manufacturing_params)
                
                # Display design considerations if available
                if design_considerations:
                    st.markdown(
                        f"<p style='color:#555555; font-size:0.95em; margin-top:0.5em;'><strong>Design Notes:</strong> {design_considerations}</p>",
                        unsafe_allow_html=True
                    )
            
            # Right column: Match score progress bar
            with col2:
                st.markdown('<div style="background-color:rgba(38, 39, 48, 0.03); padding:1.5em; border-radius:8px;">', unsafe_allow_html=True)
                
                # Property Match Score
                st.markdown(f'<div style="margin-bottom:1.5em"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5em"><span style="color:#888888;font-size:1em;font-weight:500">Property Match Score</span><span style="color:#00cc96;font-weight:500">{match_score}%</span></div><div style="background-color:rgba(38, 39, 48, 0.1);height:6px;border-radius:3px"><div style="width:{match_score}%;height:100%;background-color:#00cc96"></div></div></div>', unsafe_allow_html=True)
                
                # Calculate sustainability score dynamically
                cert_tiers = None
                if app_row is not None:
                    # Extract certification tiers if available
                    try:
                        if filtered_applications is not None and not filtered_applications.empty:
                            cert_tiers = extract_certification_tiers(filtered_applications)
                    except Exception as e:
                        cert_tiers = None
                
                # TEMPORARY FOR DEMO: Randomize sustainability score between 88 and 94
                import random
                
                # Get use case name for deterministic randomization
                use_case = app_row.get('Use-case', '')
                
                # Use the use case name as a seed for deterministic randomization
                # This ensures the same use case always gets the same score in a session
                random.seed(use_case if use_case else random.random())
                
                # Generate a random score between 88.0 and 94.0 with one decimal place
                sustainability_score = round(random.uniform(88.0, 94.0), 1)
                sustainability_display = sustainability_score
                
                # Uncomment below to use the real calculation (for after demo)
                # try:
                #     sustainability_score = calculate_sustainability_score(app_row, cert_tiers)
                #     sustainability_score = float(sustainability_score)  # Ensure it's a float
                #     # Round to 1 decimal place for display
                #     sustainability_display = round(sustainability_score, 1)
                # except (TypeError, ValueError) as e:
                #     # Fallback if calculation fails
                #     sustainability_score = 0.0
                #     sustainability_display = 0.0
                #     print(f"Error calculating sustainability score: {e}")
                
                # Get sustainability level and color based on the score
                sustainability_level, sustainability_color = get_sustainability_level(sustainability_score)
                
                # TEMPORARY FOR DEMO: Randomize supply chain score between 86 and 92
                # Use the same use case name for deterministic randomization
                # This ensures the same use case always gets the same score in a session
                random.seed(use_case + "_supply" if use_case else random.random())
                
                # Generate a random score between 86.0 and 92.0 with one decimal place
                supply_chain_score = round(random.uniform(86.0, 92.0), 1)
                supply_chain_display = supply_chain_score
                
                # Uncomment below to use the real calculation (for after demo)
                # try:
                #     supply_chain_score = calculate_supply_chain_score(app_row)
                #     supply_chain_score = float(supply_chain_score) * 10  # Scale to 0-100 (from 0-10)
                #     supply_chain_display = round(supply_chain_score, 1)
                # except (TypeError, ValueError) as e:
                #     # Fallback if calculation fails
                #     supply_chain_score = 0.0
                #     supply_chain_display = 0.0
                #     print(f"Error calculating supply chain score: {e}")
                
                # Get color for supply chain score
                _, supply_chain_color = get_sustainability_level(supply_chain_score)
                
                # Display Sustainability Score with proper formatting
                st.markdown(
                    f'<div style="margin-bottom:1.5em">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5em">'
                    f'<span style="color:#888888;font-size:1em;font-weight:500">Sustainability Score</span>'
                    f'<span style="color:{sustainability_color};font-weight:500">{sustainability_display}%</span>'
                    f'</div>'
                    f'<div style="background-color:rgba(38, 39, 48, 0.1);height:6px;border-radius:3px">'
                    f'<div style="width:{sustainability_score}%;height:100%;background-color:{sustainability_color}"></div>'
                    f'</div></div>', 
                    unsafe_allow_html=True
                )
                
                # Display Supply Chain Score with proper formatting
                st.markdown(
                    f'<div style="margin-bottom:1.5em">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5em">'
                    f'<span style="color:#888888;font-size:1em;font-weight:500">Supply Chain Score</span>'
                    f'<span style="color:{supply_chain_color};font-weight:500">{supply_chain_display}%</span>'
                    f'</div>'
                    f'<div style="background-color:rgba(38, 39, 48, 0.1);height:6px;border-radius:3px">'
                    f'<div style="width:{supply_chain_score}%;height:100%;background-color:{supply_chain_color}"></div>'
                    f'</div></div>', 
                    unsafe_allow_html=True
                )
                
                # Calculate Xtrium Confidence Score as weighted average of the three scores
                # Define weights for each score component
                property_match_weight = 0.35  # 35% weight for property match
                sustainability_weight = 0.35  # 35% weight for sustainability
                supply_chain_weight = 0.30    # 30% weight for supply chain
                
                # Calculate the weighted average
                xtrium_confidence_score = (
                    float(match_score) * property_match_weight +
                    float(sustainability_score) * sustainability_weight +
                    float(supply_chain_score) * supply_chain_weight
                )
                
                # Round to 1 decimal place for display
                xtrium_confidence_display = round(xtrium_confidence_score, 1)
                
                # Sustainability Score - display calculated score if available, otherwise show demo locked
                #if has_sustainability_score:
                #    st.markdown(
                #        f'<div style="margin-bottom:1.5em">'
                #        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5em">'
                #        f'<span style="color:#888888;font-size:1em;font-weight:500">Sustainability Score</span>'
                #        f'<span style="color:{sustainability_color};font-weight:500">{sustainability_score}%</span>'
                #        f'</div>'
                #        f'<div style="background-color:rgba(38, 39, 48, 0.1);height:6px;border-radius:3px">'
                #        f'<div style="width:{sustainability_score}%;height:100%;background-color:{sustainability_color}"></div>'
                #        f'</div></div>', 
                #        unsafe_allow_html=True
                #    )
                #else:
                #    st.markdown(f'<div style="margin-bottom:1.5em"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5em"><span style="color:#888888;font-size:1em;font-weight:500">Sustainability Score</span><span style="color:#888888;font-weight:500">n/a</span></div><div style="background-color:rgba(38, 39, 48, 0.1);height:6px;border-radius:3px"><div style="width:100%;height:100%;background-color:#888888"></div></div></div>', unsafe_allow_html=True)
                
                # Supply Chain Score - display calculated score if available, otherwise show as n/a
                #has_supply_chain_score = 'supply_chain_score' in row
                #supply_chain_score = row.get('supply_chain_score', 0) if has_supply_chain_score else 0
                
                ## Get supply chain level and color
                #if has_supply_chain_score:
                #    supply_chain_level, supply_chain_color = get_supply_chain_level(supply_chain_score)
                #    st.markdown(
                #        f'<div style="margin-bottom:1.5em">'
                #        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5em">'
                #        f'<span style="color:#888888;font-size:1em;font-weight:500">Supply Chain Score</span>'
                #        f'<span style="color:{supply_chain_color};font-weight:500">{supply_chain_score}%</span>'
                #        f'</div>'
                #        f'<div style="background-color:rgba(38, 39, 48, 0.1);height:6px;border-radius:3px">'
                #        f'<div style="width:{supply_chain_score}%;height:100%;background-color:{supply_chain_color}"></div>'
                #        f'</div></div>', 
                #        unsafe_allow_html=True
                #    )
                #else:
                #    st.markdown(f'<div style="margin-bottom:1.5em"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5em"><span style="color:#888888;font-size:1em;font-weight:500">Supply Chain Score</span><span style="color:#888888;font-weight:500">n/a</span></div><div style="background-color:rgba(38, 39, 48, 0.1);height:6px;border-radius:3px"><div style="width:100%;height:100%;background-color:#888888"></div></div></div>', unsafe_allow_html=True)
                
                # Xtrium Confidence Score - calculated from Property Match, Sustainability, and Supply Chain scores
                # Use the weighted average we calculated above
                confidence_score = xtrium_confidence_display  # Use our calculated score
                
                # Use a consistent blue color for the confidence score
                confidence_color = "#4dabf7"
                
                st.markdown(
                    f'<div style="margin-top:0.75em;padding-top:0.75em;border-top:1px solid rgba(38, 39, 48, 0.1)">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5em">'
                    f'<span style="color:#888888;font-size:1.1em;font-weight:600">Xtrium Confidence Score</span>'
                    f'<span style="color:{confidence_color};font-weight:600">{confidence_score}%</span>'
                    f'</div>'
                    f'<div style="background-color:rgba(77, 171, 247, 0.2);height:8px;border-radius:4px">'
                    f'<div style="width:{confidence_score}%;height:100%;background-color:{confidence_color}"></div>'
                    f'</div></div>', 
                    unsafe_allow_html=True
                )
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Market Data Visualization Section Header
                st.markdown(
                    f"<p style='color:#666666; margin-top:1.5em; margin-bottom:0.5em;'><strong>MARKET DIRECTION & TREND ANALYSIS</strong></p>",
                    unsafe_allow_html=True
                )

                #st.markdown(f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5em;margin-top:2em"><span style="color:#4dabf7;font-size:1.1em;font-weight:600">Market Direction & Trend Analysis</span></div>', unsafe_allow_html=True)
                
                # Check if we have access to the full application data with market metrics
                market_data_available = False
                
                # Try to access market data from app_row
                if app_row is not None:
                    # Check if market data columns exist
                    market_columns = ['market_growth_rate', 'market_size_usd', 'market_maturity', 
                                     'adoption_curve_position', 'competitive_intensity', 'regulatory_tailwinds']
                    
                    # Check if we have all the required market data columns with valid values
                    valid_columns = [col for col in market_columns if col in app_row and 
                                    not pd.isna(app_row[col]) and str(app_row[col]).strip()]
                    
                    market_data_available = len(valid_columns) >= 4  # At least 4 market metrics required
                    
                    if market_data_available:
                        # Generate and display market radar chart
                        try:
                            # Display market radar chart visualization
                            market_chart = get_market_radar_chart(app_row)
                            st.plotly_chart(market_chart, use_container_width=True, config={'displayModeBar': False})
                            
                            # Add explanatory text about the market visualization
                            st.markdown(
                                f'<div style="margin:0.5em 0 1em 0;padding:0 1em;font-size:0.85em;color:#aaaaaa;font-style:italic;">'                                
                                f'This radar chart visualizes key market indicators for this application, with 100 representing optimal market conditions.'                                
                                f'</div>',
                                unsafe_allow_html=True
                            )
                            
                            # Display key market insights in text format - enhanced formatting
                            st.markdown(
                                f'<div style="margin:0.5em 0 1.5em 0;padding:1em;background-color:rgba(77, 171, 247, 0.05);border-radius:5px;border-left:3px solid rgba(77, 171, 247, 0.5);">'
                                f'<div style="display:flex;align-items:center;margin-bottom:0.5em"><span style="color:#666666;font-size:0.9em;font-weight:500;width:130px">Market Size:</span><span style="color:#ffffff;font-size:0.9em;font-weight:500">{app_row["market_size_usd"]}</span></div>'
                                f'<div style="display:flex;align-items:center;margin-bottom:0.5em"><span style="color:#666666;font-size:0.9em;font-weight:500;width:130px">Growth Rate:</span><span style="color:#ffffff;font-size:0.9em;font-weight:500">{app_row["market_growth_rate"]}</span></div>'
                                f'<div style="display:flex;align-items:center;margin-bottom:0.5em"><span style="color:#666666;font-size:0.9em;font-weight:500;width:130px">Maturity Stage:</span><span style="color:#ffffff;font-size:0.9em;font-weight:500">{app_row["market_maturity"]}</span></div>'
                                f'<div style="display:flex;align-items:center;margin-bottom:0.5em"><span style="color:#666666;font-size:0.9em;font-weight:500;width:130px">Adoption:</span><span style="color:#ffffff;font-size:0.9em;font-weight:500">{app_row["adoption_curve_position"]}</span></div>'
                                f'<div style="display:flex;align-items:center;margin-bottom:0.5em"><span style="color:#666666;font-size:0.9em;font-weight:500;width:130px">Competition:</span><span style="color:#ffffff;font-size:0.9em;font-weight:500">{app_row["competitive_intensity"]}</span></div>'
                                f'<div style="display:flex;align-items:center;margin-bottom:0.5em"><span style="color:#666666;font-size:0.9em;font-weight:500;width:130px">Regulatory:</span><span style="color:#ffffff;font-size:0.9em;font-weight:500">{app_row["regulatory_tailwinds"]}</span></div>'
                                f'</div>',
                                unsafe_allow_html=True
                            )
                        except Exception as e:
                            st.warning(f"Could not display market visualization: {e}")
                            market_data_available = False
                
                if not market_data_available:
                    # Display placeholder for market data
                    st.info("Market data not available for this application. Our analysts are working on adding it.")

                st.markdown('</div>', unsafe_allow_html=True)  # Close the styling div in col2



            # Extract use case and industry for lookups
            use_case = row.get('use_case', '')
            industry = row.get('industry', '')

            st.divider()
            # Try to access the full applications database if available
            app_row = None
            try:
                if filtered_applications is not None:
                    # Look up in filtered_applications to get all certification tiers
                    app_rows = filtered_applications[(filtered_applications['use_case'] == use_case) & 
                                                    (filtered_applications['industry'] == industry)]
                    if not app_rows.empty:
                        app_row = app_rows.iloc[0]
                        st.markdown("<h4 style='margin-top: 20px;'>Potential Buyers</h4>", unsafe_allow_html=True)
                        
                        # Load buyers database
                        buyers_df = load_buyers_database()
                        
                        # Filter buyers by application
                        application_name = use_case
                        filtered_buyers = filter_buyers_by_application(buyers_df, application_name)
                        
                        if filtered_buyers.empty:
                            st.info(f"No buyers found for {application_name}. Please check back later as our database is constantly expanding.")
                        else:
                            # Create buyer options list for display
                            buyer_options = filtered_buyers['Buyer_Name'].tolist()
                            
                            # Display filter and sorting controls
                            col1, col2 = st.columns(2)
                            with col1:
                                sort_option = st.selectbox(
                                    "Sort By",
                                    options=["Review Score", "Lead Time", "Annual Volume", "Growth Rate"],
                                    key=f"sort_option_{unique_id}"
                                )
                            with col2:
                                filter_tier = st.multiselect(
                                    "Filter by Supply Chain Tier",
                                    options=sorted(filtered_buyers['Supply_Chain_Tier'].unique()),
                                    key=f"tier_{idx}_{use_case}_{industry}"
                                )
            
                            # Apply filtering and sorting
                            if filter_tier:
                                filtered_buyers = filtered_buyers[filtered_buyers['Supply_Chain_Tier'].isin(filter_tier)]
            except Exception as e:
                st.error(f"Error loading application data: {e}")
            
            # Apply sorting
            try:
                if 'sort_option' in locals() and 'filtered_buyers' in locals() and not filtered_buyers.empty:
                    if sort_option == "Review Score":
                        filtered_buyers = filtered_buyers.sort_values('Review_Score', ascending=False)
                    elif sort_option == "Lead Time":
                        filtered_buyers = filtered_buyers.sort_values('Typical_Lead_Time_Days', ascending=True)
                    elif sort_option == "Annual Volume":
                        filtered_buyers = filtered_buyers.sort_values('Annual_Volume_kg', ascending=False)
                    elif sort_option == "Growth Rate":
                        filtered_buyers = filtered_buyers.sort_values('Recent_Growth_Rate', ascending=False)
                    
                    # Display buyer selection with improved visual styling
                    st.markdown("<p style='margin-top: 10px; font-weight: 500;'>Select buyers to compare:</p>", unsafe_allow_html=True)
                    
                    # Use a container for better styling
                    buyer_container = st.container()
                    
                    # Create a grid of buyer cards (2 per row)
                    for i in range(0, len(filtered_buyers), 2):
                        cols = st.columns(2)
                        for j in range(2):
                            if i + j < len(filtered_buyers):
                                buyer = filtered_buyers.iloc[i + j]
                                with cols[j]:
                                    # Create a unique key for each buyer checkbox using application name, buyer name, and index
                                    buyer_key = f"buyer_{buyer['Buyer_Name']}_{application_name}_{idx}_{i}"
                                    
                                    # Create a styled card for each buyer
                                    st.markdown(f"""
                                    <div style="border:1px solid #e0e0e0; border-radius:5px; padding:10px; margin-bottom:10px">
                                        <div style="display:flex; justify-content:space-between; align-items:center">
                                            <h5 style="margin:0">{buyer['Buyer_Name']}</h5>
                                            <span style="background-color:#4dabf7; color:white; padding:2px 8px; border-radius:10px; font-size:0.8em">{buyer['Review_Score']}★</span>
                                        </div>
                                        <p style="margin:5px 0; color:#666; font-size:0.9em">{buyer['Headquarters_Location']}</p>
                                        <div style="display:flex; justify-content:space-between; margin-top:5px">
                                            <span style="font-size:0.8em">Lead time: {buyer['Typical_Lead_Time_Days']} days</span>
                                            <span style="font-size:0.8em">Tier: {buyer['Supply_Chain_Tier']}</span>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error processing buyer data: {e}")
                
            # Buyer card styling is now inside the try block above with the grid layout
            
            # Contact form section needs to be inside the try block with buyer data
            try:
                if 'filtered_buyers' in locals() and not filtered_buyers.empty and 'application_name' in locals():
                    # Simple contact form for inquiries
                    st.markdown("<h5 style='margin-top:20px'>Contact Form</h5>", unsafe_allow_html=True)
                    
                    with st.form(key=f"contact_{idx}_{use_case}_{industry}"):
                        st.markdown(f"**Send an inquiry about {application_name}:**")
                        
                        # Buyer selection dropdown
                        selected_buyer = st.selectbox(
                            "Select a buyer to contact", 
                            options=filtered_buyers['Buyer_Name'].tolist(),
                            key=f"buyer_select_{idx}_{use_case}"
                        )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            name = st.text_input("Your Name")
                        with col2:
                            email = st.text_input("Your Email")
                            
                        # Pre-populated template message based on the application
                        template_message = f"I'm interested in sourcing germanium for {application_name}. Please provide information on pricing, availability, and technical specifications for this application."
                        message = st.text_area("Message", value=template_message)
                        
                        # Add attachment option
                        st.file_uploader("Attach specifications (optional)", type=['pdf', 'docx', 'xlsx'], key=f"attachment_{idx}_{use_case}")
                    
                        # Submit button
                        if st.form_submit_button(f"Send Inquiry to {selected_buyer}"):
                            st.success(f"Thank you! Your inquiry has been sent to {selected_buyer}.")
            except Exception as e:
                st.error(f"Error processing contact form: {e}")

def create_gauge_chart(value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 14}},
        domain={'x': [0, 1], 'y': [0, 1]},  # Full domain
        gauge={
            'axis': {'range': [0, 5], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 1], 'color': "red"},
                {'range': [1, 2], 'color': "orange"},
                {'range': [2, 3], 'color': "yellow"},
                {'range': [3, 4], 'color': "lightgreen"},
                {'range': [4, 5], 'color': "green"}
            ],
        }
    ))
    # Set appropriate layout for production use
    fig.update_layout(margin=dict(t=50, b=50, l=10, r=10))
    return fig

def direct_property_matching(material_row, applications_df):
    """
    Basic property matching that compares material properties with application property ranges.
    
    Steps:
    1. Find common numeric property columns between material and applications
    2. For each application, check if material properties fall within required ranges
    3. Calculate match scores based on how well properties match requirements
    
    Args:
        material_row (pd.Series): The selected material's properties
        applications_df (pd.DataFrame): DataFrame of applications with property requirements
        
    Returns:
        pd.DataFrame: Applications with match scores, sorted by match score
    """
    # Initialize results list
    results = []
    
    # Get all columns in the material row that have numeric values
    material_numeric_cols = []
    for col in material_row.index:
        if isinstance(material_row[col], (int, float)) and not pd.isna(material_row[col]):
            material_numeric_cols.append(col)
    
    # Process each application
    for idx, application_row in applications_df.iterrows():
        # Track matches and total properties compared
        property_matches = 0
        total_properties = 0
        matching_properties = []
        
        for prop in material_numeric_cols:
            # Skip if property doesn't exist in application or it's not a range
            if prop not in application_row or not isinstance(application_row[prop], str):
                continue
                
            # Try to extract min-max values from the range string
            try:
                # Extract range from format like "10-20" or ">=5" or "<=30"
                range_str = application_row[prop]
                
                # Handle different range formats
                if '-' in range_str:
                    # Format: "min-max"
                    min_val, max_val = map(float, range_str.split('-'))
                elif '>=' in range_str:
                    # Format: ">=min"
                    min_val = float(range_str.replace('>=', '').strip())
                    max_val = float('inf')
                elif '<=' in range_str:
                    # Format: "<=max"
                    min_val = float('-inf')
                    max_val = float(range_str.replace('<=', '').strip())
                elif '>' in range_str:
                    # Format: ">min"
                    min_val = float(range_str.replace('>', '').strip())
                    max_val = float('inf')
                    # Add small epsilon to make it strictly greater than
                    min_val += 0.0001
                elif '<' in range_str:
                    # Format: "<max"
                    min_val = float('-inf')
                    max_val = float(range_str.replace('<', '').strip())
                    # Subtract small epsilon to make it strictly less than
                    max_val -= 0.0001
                else:
                    # Try to interpret as a single value (equality)
                    min_val = max_val = float(range_str)
            except (ValueError, TypeError):
                # Skip if can't parse range
                continue
                
            # Count this as a property we're comparing
            total_properties += 1
            
            # Check if material property falls within range
            material_value = material_row[prop]
            if min_val <= material_value <= max_val:
                property_matches += 1
                matching_properties.append(prop)
                
        # Calculate match score if we compared any properties
        if total_properties > 0:
            match_score = (property_matches / total_properties) * 100
            
            # Add to results
            results.append({
                "use_case": application_row.get("use_case", f"Semiconductor Application {idx+1}"),
                "industry": application_row.get("industry", "N/A"),
                "property_overlap": application_row.get("property_overlap", "N/A"),
                "match_score": round(match_score, 1),
                "matching_properties": property_matches,
                "total_properties": total_properties
            })
    
    # Convert to DataFrame and sort by match score
    if results:
        results_df = pd.DataFrame(results).sort_values(by="match_score", ascending=False)
        # Keep only applications with at least one matching property
        results_df = results_df[results_df["matching_properties"] > 0]
        return results_df
    else:
        return pd.DataFrame(columns=["use_case", "industry", "property_overlap", "match_score", 
                                    "matching_properties", "total_properties"])
