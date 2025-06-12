#!/usr/bin/env python3
import os
import requests
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_marvin_api(api_key=None, test_projects=False):
    """Test connection to Amazing Marvin API"""
    if not api_key:
        api_key = os.getenv("AMAZING_MARVIN_API_KEY")
        if not api_key:
            raise ValueError("API key not provided. Set AMAZING_MARVIN_API_KEY environment variable or pass with --api-key")
    
    base_url = "https://serv.amazingmarvin.com/api"
    headers = {"X-API-Token": api_key}
    
    # Test API endpoints one by one to provide better error info
    endpoints = {
        "/todayItems": "Get all scheduled tasks and projects (today)",
        "/categories": "Get all categories (including projects)", 
    }
    
    print("Testing Amazing Marvin API...")
    
    for endpoint, description in endpoints.items():
        url = base_url + endpoint
        print(f"Testing endpoint: {endpoint} - {description}")
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            print(f"✅ Success! Received {len(data) if isinstance(data, list) else 'response'}")
            # Print sample data safely
            if isinstance(data, list) and data:
                print(f"Sample data: {data[0]}")
            elif isinstance(data, dict):
                print(f"Sample keys: {list(data.keys())[:3]}")
            print("-" * 50)
        except requests.exceptions.HTTPError as e:
            print(f"❌ Error: {e}")
            print(f"Response content: {response.text}")
            print(f"Request URL: {url}")
            print(f"Request headers: {headers}")
            print("-" * 50)
    
    # Let's try getting me endpoint which should always work if API key is valid
    try:
        me_url = base_url + "/me"
        print(f"Testing authentication with /me endpoint")
        response = requests.get(me_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Authentication successful! User: {data.get('email', 'Unknown')}")
    except requests.exceptions.HTTPError as e:
        print(f"❌ Authentication Error: {e}")
        print(f"Response content: {response.text}")
        return False
    
    if test_projects:
        # Fetch categories and filter for projects
        print("Fetching projects (type == 'project') from /categories ...")
        url = base_url + "/categories"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            categories = response.json()
            projects = [cat for cat in categories if cat.get("type") == "project"]
            print(f"Found {len(projects)} projects.")
            # Highlight default projects if present
            default_names = {"Work", "Personal"}
            for proj in projects:
                name = proj.get("title", "")
                is_default = " (default)" if name in default_names else ""
                print(f"- {name}{is_default}")
            print("-" * 50)
        except Exception as e:
            print(f"❌ Error fetching projects: {e}")
            print("-" * 50)

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Amazing Marvin API connection")
    parser.add_argument("--api-key", help="Your Amazing Marvin API key")
    parser.add_argument("--test-projects", action="store_true", help="Test fetching projects (filtered from categories)")
    args = parser.parse_args()
    
    test_marvin_api(args.api_key, test_projects=args.test_projects)
