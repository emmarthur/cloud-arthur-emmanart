"""
REST Countries API Tool: Retrieve country/region data for logistics and geographic analysis.
"""
import requests
import json
import os
from datetime import datetime

# Logging setup
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
REST_COUNTRIES_LOG_FILE = os.path.join(LOG_DIR, "rest_countries.log")

def _log_to_file(log_file: str, message: str):
    """Log message to file and stdout (for Cloud Run logging)."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        # Write to file (for local development)
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"{log_entry}\n")
        except Exception as file_error:
            # If file writing fails (e.g., in Cloud Run with read-only filesystem), continue
            pass
        
        # Also print to stdout/stderr for Cloud Run logging
        # Cloud Run automatically captures stdout/stderr and makes it available in Cloud Logging
        print(log_entry, flush=True)
    except Exception as e:
        print(f"Error in logging: {e}", flush=True)

def rest_countries(country: str = None, region: str = None) -> str:
    """Retrieve country/region data from REST Countries API.
    
    Args:
        country: Optional country name (e.g., "United States"). Can be None or empty string.
        region: Optional region name (e.g., "Europe"). Can be None or empty string.
    
    Returns:
        JSON string with country/region data including supply chain metrics
    """
    try:
        # Normalize empty strings to None for consistent processing
        country = country if country and country.strip() else None
        region = region if region and region.strip() else None
        
        _log_to_file(REST_COUNTRIES_LOG_FILE, f"Function called with country={country}, region={region}")
        
        # Call REST Countries API based on filter parameters
        if country:
            # Search by country name
            response = requests.get(f"https://restcountries.com/v3.1/name/{country}?fields=name,region,subregion,population,area,capital")
        elif region:
            # Filter by region
            response = requests.get(f"https://restcountries.com/v3.1/region/{region}?fields=name,region,subregion,population,area,capital")
        else:
            # Get all countries (limit fields for performance)
            response = requests.get("https://restcountries.com/v3.1/all?fields=name,region,subregion,population,area,capital")
        
        response.raise_for_status()
        countries_data = response.json()
        
        # Normalize: wrap single dict result in list for consistent processing
        if isinstance(countries_data, dict):
            countries_data = [countries_data]
        
        # Calculate supply chain and logistics metrics
        regions = {}
        total_population = 0
        region_populations = {}
        
        for country_data in countries_data:
            region = country_data.get('region', 'Unknown')
            population = country_data.get('population', 0)
            country_name = country_data.get('name', {}).get('common', 'Unknown')
            
            # Aggregate metrics by region
            regions[region] = regions.get(region, 0) + 1
            if region not in region_populations:
                region_populations[region] = 0
            region_populations[region] += population
            total_population += population
        
        # Calculate supply chain network metrics
        total_countries = len(countries_data)
        avg_countries_per_region = total_countries / len(regions) if regions else 0
        avg_population_per_region = {region: pop / regions[region] 
                                     for region, pop in region_populations.items() 
                                     if regions[region] > 0}
        
        # Build regional breakdown for analysis
        regional_breakdown = []
        for region in sorted(regions.keys()):
            if region != 'Unknown':
                countries_count = regions[region]
                population = region_populations.get(region, 0)
                avg_pop = avg_population_per_region.get(region, 0)
                regional_breakdown.append({
                    "region": region,
                    "countries_count": countries_count,
                    "total_population": population,
                    "avg_population_per_country": round(avg_pop, 0),
                    "complexity": "High" if countries_count > 10 else "Medium" if countries_count > 5 else "Low"
                })
        
        # Build raw data dictionary
        data = {
            "filter": {
                "country": country,
                "region": region
            },
            "supply_chain_network": {
                "total_countries": total_countries,
                "total_regions": len(regions),
                "avg_countries_per_region": round(avg_countries_per_region, 2),
                "total_market_population": total_population
            },
            "regional_breakdown": regional_breakdown,
            "countries": countries_data[:50] if len(countries_data) > 50 else countries_data  # Limit response size
        }
        
        result_json = json.dumps(data)
        _log_to_file(REST_COUNTRIES_LOG_FILE, f"SUCCESS: Retrieved {total_countries} countries")
        _log_to_file(REST_COUNTRIES_LOG_FILE, f"Response: {result_json[:500]}...")
        return result_json
    except requests.RequestException as e:
        error_data = {
            "error": True,
            "error_message": f"Error fetching country data: {str(e)}",
            "country": country,
            "region": region
        }
        _log_to_file(REST_COUNTRIES_LOG_FILE, f"ERROR: RequestException - {str(e)}")
        return json.dumps(error_data)

