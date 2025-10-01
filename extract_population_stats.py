#!/usr/bin/env python3
"""
Extract population statistics from Tanzania Population Distribution Report 2022
Extracts data from pages 23-255, including regional, council, and ward-level statistics
"""

import pdfplumber
import re
import json

def clean_text(text):
    """Clean and normalize text"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_number(text):
    """Parse a number from text, handling commas"""
    if not text or text.strip() == '-':
        return None
    text = text.strip().replace(',', '')
    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return None

def extract_population_stats(pdf_path, start_page=54, end_page=286):
    """
    Extract population statistics from the PDF
    Returns structured data with regions, councils, and wards
    """
    data = {
        "country": "Tanzania",
        "source": "2022 Population and Housing Census (PHC)",
        "regions": []
    }
    
    current_region = None
    current_council = None
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(start_page - 1, min(end_page, len(pdf.pages))):
            page = pdf.pages[page_num]
            text = page.extract_text()
            
            if not text:
                continue
            
            lines = text.split('\n')
            
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                if not line:
                    i += 1
                    continue
                
                # Check if this line and next line together form a region header
                combined = line
                if i + 1 < len(lines):
                    combined = line + " " + lines[i + 1].strip()
                
                # Detect Region summary table header (e.g., "Table 1. 0: Population Distribution...")
                # More specific pattern: "by Council, RegionName Region; 2022 PHC"
                region_match = re.search(r'by\s+Council[,\s]+([A-Z][a-zA-Z\s]{3,25}?)\s+Region[;\s,]+2022\s+PHC', combined, re.IGNORECASE)
                
                if not region_match:
                    # Fallback pattern for when region name comes right before "Region"
                    region_match = re.search(r'Council\s+([A-Z][a-zA-Z\s]{3,25}?)\s+Region[;\s,]+2022\s+PHC', combined, re.IGNORECASE)
                
                if region_match:
                    region_name = clean_text(region_match.group(1))
                    
                    # Skip if it's not a valid region name
                    if 'Household' in region_name or 'Number' in region_name or 'Average' in region_name or 'Size' in region_name or 'by' in region_name.lower():
                        i += 1
                        continue
                    
                    # Check if region already exists
                    existing_region = None
                    for reg in data["regions"]:
                        if reg["region"] == region_name:
                            existing_region = reg
                            break
                    
                    if not existing_region:
                        current_region = {
                            "region": region_name,
                            "population": {},
                            "councils": []
                        }
                        data["regions"].append(current_region)
                        print(f"Found region: {region_name}")
                    else:
                        current_region = existing_region
                    
                    current_council = None
                    i += 1
                    continue
                
                # Extract regional-level statistics (appears after region header)
                if current_region and not current_region.get("population"):
                    # Look for lines with region name followed by numbers
                    region_stats = re.match(r'^' + re.escape(current_region['region']) + r'\s+Region\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+(\d+)\s+([\d,]+)\s+([\d.]+)', line)
                    if region_stats:
                        current_region["population"] = {
                            "both_sexes": parse_number(region_stats.group(1)),
                            "male": parse_number(region_stats.group(2)),
                            "female": parse_number(region_stats.group(3)),
                            "sex_ratio": parse_number(region_stats.group(4)),
                            "households": parse_number(region_stats.group(5)),
                            "average_household_size": parse_number(region_stats.group(6))
                        }
                        print(f"  Region stats: {current_region['population']['both_sexes']:,} people")
                        i += 1
                        continue
                
                # Detect Council section headers (e.g., "14.1 NZEGA TOWN COUNCIL")
                council_section = re.match(r'^\d+\.\s*\d+\s+([A-Z][A-Z\s\'\-]+(?:DISTRICT|MUNICIPAL|TOWN|CITY)\s+COUNCIL)', line)
                
                if council_section and current_region:
                    council_full = clean_text(council_section.group(1))
                    
                    # Determine council type and name
                    if 'DISTRICT COUNCIL' in council_full:
                        council_type = 'district_council'
                        council_name = council_full.replace('DISTRICT COUNCIL', '').strip().title()
                    elif 'MUNICIPAL COUNCIL' in council_full or 'MUNICIPAL' in council_full:
                        council_type = 'municipal_council'
                        council_name = council_full.replace('MUNICIPAL COUNCIL', '').replace('MUNICIPAL', '').strip().title()
                    elif 'TOWN COUNCIL' in council_full:
                        council_type = 'town_council'
                        council_name = council_full.replace('TOWN COUNCIL', '').strip().title()
                    elif 'CITY COUNCIL' in council_full:
                        council_type = 'city_council'
                        council_name = council_full.replace('CITY COUNCIL', '').strip().title()
                    else:
                        i += 1
                        continue
                    
                    # Check if council already exists
                    existing_council = None
                    for council_item in current_region["councils"]:
                        if council_item["type"] == council_type and council_item["name"] == council_name:
                            existing_council = council_item
                            break
                    
                    if not existing_council:
                        current_council = {
                            "type": council_type,
                            "name": council_name,
                            "population": {},
                            "wards": []
                        }
                        current_region["councils"].append(current_council)
                        print(f"  Found {council_type}: {council_name}")
                    else:
                        current_council = existing_council
                    
                    i += 1
                    continue
                
                # Extract council-level statistics (first line after council header in table)
                if current_council and not current_council.get("population"):
                    # Look for lines with council name followed by numbers
                    council_stats = re.match(r'^' + re.escape(current_council['name']) + r'\s+(?:District|Municipal|Town|City)?\s*(?:Council)?\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+(\d+)\s+([\d,]+)\s+([\d.]+)', line, re.IGNORECASE)
                    if council_stats:
                        current_council["population"] = {
                            "both_sexes": parse_number(council_stats.group(1)),
                            "male": parse_number(council_stats.group(2)),
                            "female": parse_number(council_stats.group(3)),
                            "sex_ratio": parse_number(council_stats.group(4)),
                            "households": parse_number(council_stats.group(5)),
                            "average_household_size": parse_number(council_stats.group(6))
                        }
                        print(f"    Council stats: {current_council['population']['both_sexes']:,} people")
                        i += 1
                        continue
                
                # Detect ward entries with population data (numbered list at start of line)
                ward_match = re.match(r'^(\d+)\.\s+([A-Z][a-zA-Z\s\'\-]+?)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+(\d+)\s+([\d,]+)\s+([\d.]+)', line)
                
                if ward_match and current_council:
                    ward_name = clean_text(ward_match.group(2))
                    
                    # Skip if it looks like a council or district
                    skip_terms = ['Council', 'Municipal', 'District', 'Region', 'Town', 'City']
                    if any(term in ward_name for term in skip_terms):
                        i += 1
                        continue
                    
                    # Skip very short names
                    if len(ward_name) < 3:
                        i += 1
                        continue
                    
                    # Check if ward already exists
                    ward_exists = any(w["name"] == ward_name for w in current_council["wards"])
                    
                    if not ward_exists:
                        ward_data = {
                            "name": ward_name,
                            "population": {
                                "both_sexes": parse_number(ward_match.group(3)),
                                "male": parse_number(ward_match.group(4)),
                                "female": parse_number(ward_match.group(5)),
                                "sex_ratio": parse_number(ward_match.group(6)),
                                "households": parse_number(ward_match.group(7)),
                                "average_household_size": parse_number(ward_match.group(8))
                            }
                        }
                        current_council["wards"].append(ward_data)
                
                i += 1
    
    return data

def main():
    pdf_path = '/home/runner/work/TZ-AU-DS-2022/TZ-AU-DS-2022/Administrative_units_Population_Distribution_Report_Tanzania_volume1a.pdf'
    output_path = '/home/runner/work/TZ-AU-DS-2022/TZ-AU-DS-2022/population_stats.json'
    
    print("="*80)
    print("Extracting population statistics from Tanzania Population Distribution Report")
    print(f"Processing pages 54-286 (population data pages)")
    print("="*80)
    
    data = extract_population_stats(pdf_path, start_page=54, end_page=286)
    
    print("\n" + "="*80)
    print("Extraction complete!")
    print("="*80)
    print(f"Regions found: {len(data['regions'])}")
    
    total_councils = 0
    total_wards = 0
    total_population = 0
    
    for region in data['regions']:
        region_councils = len(region['councils'])
        region_wards = sum(len(council['wards']) for council in region['councils'])
        region_pop = region.get('population', {}).get('both_sexes', 0) or 0
        
        total_councils += region_councils
        total_wards += region_wards
        total_population += region_pop
        
        print(f"\n  {region['region']}: {region_councils} councils, {region_wards} wards, {region_pop:,} people")
    
    print(f"\nTotal councils: {total_councils}")
    print(f"Total wards: {total_wards}")
    print(f"Total population: {total_population:,}")
    
    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Data saved to: {output_path}")
    print("="*80)

if __name__ == '__main__':
    main()
