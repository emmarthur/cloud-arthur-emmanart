"""
Fake Store API Tool: Retrieve product data for product portfolio analysis and e-commerce metrics.
"""
import requests
import json
import os
import time
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for metrics import
sys.path.insert(0, str(Path(__file__).parent.parent))
from metrics import track_api_call

# Logging setup
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
FAKE_STORE_LOG_FILE = os.path.join(LOG_DIR, "fake_store.log")

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

def fake_store(category: str = None) -> str:
    """Retrieve product data from Fake Store API.
    
    Args:
        category: Optional category (e.g., "electronics", "jewelery"). None = all products.
    
    Returns:
        JSON string with product data including pricing and category breakdowns
    """
    try:
        _log_to_file(FAKE_STORE_LOG_FILE, f"Function called with category={category}")
        
        # Track API call with metrics
        start_time = time.time()
        # Call Fake Store API (filtered by category or all products)
        if category:
            # Filter by category
            response = requests.get(f"https://fakestoreapi.com/products/category/{category}")
        else:
            # Get all products
            response = requests.get("https://fakestoreapi.com/products")
        
        response.raise_for_status()
        products_data = response.json()
        response_time_ms = (time.time() - start_time) * 1000
        
        # Track successful API call
        track_api_call(
            api_name="Fake Store",
            tool_name="fake_store_api",
            success=True,
            response_time_ms=response_time_ms,
            parameters={"category": category}
        )
        
        # Calculate product analytics metrics
        total_products = len(products_data)
        categories = {}
        price_ranges = {"Low": 0, "Medium": 0, "High": 0}
        total_price = 0
        
        # Aggregate product data by category and price range
        for product in products_data:
            product_category = product.get('category', 'Unknown')
            categories[product_category] = categories.get(product_category, 0) + 1
            
            price = product.get('price', 0)
            total_price += price
            # Categorize by price range
            if price < 20:
                price_ranges["Low"] += 1
            elif price < 100:
                price_ranges["Medium"] += 1
            else:
                price_ranges["High"] += 1
        
        avg_price = total_price / total_products if total_products > 0 else 0
        
        # Build category breakdown (sorted by count)
        category_breakdown = []
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        for product_category, count in sorted_categories:
            category_breakdown.append({
                "category": product_category,
                "product_count": count,
                "percentage": round((count / total_products) * 100, 1)
            })
        
        # Build price distribution breakdown
        price_distribution = []
        for range_name, count in price_ranges.items():
            price_label = "<$20" if range_name == "Low" else "<$100" if range_name == "Medium" else "$100+"
            price_distribution.append({
                "range": range_name,
                "price_label": price_label,
                "product_count": count,
                "percentage": round((count / total_products) * 100, 1)
            })
        
        # Calculate price positioning
        min_price = min([p.get('price', 0) for p in products_data]) if products_data else 0
        max_price = max([p.get('price', 0) for p in products_data]) if products_data else 0
        price_position = "value" if avg_price < 50 else "mid-market" if avg_price < 150 else "premium"
        
        # Build raw data dictionary
        data = {
            "filter": {
                "category": category
            },
            "product_portfolio_metrics": {
                "total_products": total_products,
                "product_categories": len(categories),
                "average_product_price": round(avg_price, 2),
                "min_price": round(min_price, 2),
                "max_price": round(max_price, 2),
                "price_positioning": price_position
            },
            "category_breakdown": category_breakdown,
            "price_distribution": price_distribution,
            "products": products_data  # Include full product data for detailed analysis
        }
        
        result_json = json.dumps(data)
        _log_to_file(FAKE_STORE_LOG_FILE, f"SUCCESS: Retrieved {total_products} products")
        _log_to_file(FAKE_STORE_LOG_FILE, f"Response: {result_json[:500]}...")
        return result_json
    except requests.RequestException as e:
        response_time_ms = (time.time() - start_time) * 1000 if 'start_time' in locals() else 0
        error_data = {
            "error": True,
            "error_message": f"Error fetching product data: {str(e)}",
            "category": category
        }
        _log_to_file(FAKE_STORE_LOG_FILE, f"ERROR: RequestException - {str(e)}")
        
        # Track failed API call
        track_api_call(
            api_name="Fake Store",
            tool_name="fake_store_api",
            success=False,
            response_time_ms=response_time_ms,
            error_message=str(e),
            parameters={"category": category}
        )
        
        return json.dumps(error_data)

