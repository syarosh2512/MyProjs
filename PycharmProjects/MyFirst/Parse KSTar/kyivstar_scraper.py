import requests
import csv
import re

def scrape_kyivstar():
    """Scrape Kyivstar B2B subscriptions page."""
    
    url = "https://b2b-new.kyivstar.ua/company-subscriptions"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        html = response.text
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', html)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Split into lines and filter
        lines = [line.strip() for line in text.split('.') if line.strip() and len(line.strip()) > 10]
        
        data = []
        for i, line in enumerate(lines[:30]):
            data.append({'line_number': i+1, 'content': line})
        
        # Save to CSV
        filename = 'kyivstar_content.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['line_number', 'content'])
            writer.writeheader()
            writer.writerows(data)
            
        print(f"✓ Kyivstar content saved to {filename}")
        print(f"✓ Total records: {len(data)}")
        return filename
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    scrape_kyivstar()