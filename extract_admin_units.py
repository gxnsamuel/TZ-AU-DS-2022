#!/usr/bin/env python3
"""
Extract administrative units from Tanzania Population Distribution Report 2022
The data starts around page 170 and continues through page 285
"""

import pdfplumber
import re
import json

def clean_text(text):
    """Clean and normalize text"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_administrative_units(pdf_path, start_page=54, end_page=286):
    """
    Extract regions, councils, and wards from the PDF
    """
    data = {
        "country": "Tanzania",
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
                # Pattern: "Table X.0: ..." on one line, "... Region; 2022 PHC" on next
                combined = line
                if i + 1 < len(lines):
                    combined = line + " " + lines[i + 1].strip()
                
                # Detect Region header
                # Try specific pattern first: "by Council, RegionName Region"
                region_match = re.search(r'by\s+Council[,\s]+([A-Z][a-zA-Z\s]+?)\s+Region[;\s,]+2022\s+PHC', combined, re.IGNORECASE)
                
                if not region_match:
                    # Fallback to less specific pattern
                    region_match = re.search(r'Table\s+\d+\.\s*0[:\s]+.*?([A-Z][a-zA-Z\s]{3,25}?)\s+Region[;\s,]+2022\s+PHC', combined, re.IGNORECASE)
                
                if region_match:
                    region_name = clean_text(region_match.group(1))
                    
                    # Skip if it's just text before the actual region name
                    if 'Household' in region_name or 'Number' in region_name or 'Average' in region_name:
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
                            "data": []
                        }
                        data["regions"].append(current_region)
                        print(f"Found region: {region_name}")
                    else:
                        current_region = existing_region
                    
                    current_council = None
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
                    for council_item in current_region["data"]:
                        if council_type in council_item and council_item[council_type] == council_name:
                            existing_council = council_item
                            break
                    
                    if not existing_council:
                        current_council = {
                            council_type: council_name,
                            "wards": []
                        }
                        current_region["data"].append(current_council)
                        print(f"  Found {council_type}: {council_name}")
                    else:
                        current_council = existing_council
                    
                    i += 1
                    continue
                
                # Detect ward entries (numbered list at start of line)
                ward_match = re.match(r'^(\d+)\.\s+([A-Z][a-zA-Z\s\'\-]+?)(?:\s+\d|$)', line)
                
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
                    
                    if ward_name not in current_council["wards"]:
                        current_council["wards"].append(ward_name)
                
                i += 1
    
    return data

def main():
    pdf_path = '/home/runner/work/TZ-AU-DS-2022/TZ-AU-DS-2022/Administrative_units_Population_Distribution_Report_Tanzania_volume1a.pdf'
    output_path = '/home/runner/work/TZ-AU-DS-2022/TZ-AU-DS-2022/dataset.json'
    
    print("="*80)
    print("Extracting administrative units from Tanzania Population Distribution Report")
    print(f"Processing pages 54-286 (actual data pages)")
    print("="*80)
    
    data = extract_administrative_units(pdf_path, start_page=54, end_page=286)
    
    print("\n" + "="*80)
    print("Extraction complete!")
    print("="*80)
    print(f"Regions found: {len(data['regions'])}")
    
    total_councils = 0
    total_wards = 0
    
    for region in data['regions']:
        region_councils = len(region['data'])
        region_wards = sum(len(council['wards']) for council in region['data'])
        total_councils += region_councils
        total_wards += region_wards
        print(f"\n  {region['region']}: {region_councils} councils, {region_wards} wards")
    
    print(f"\nTotal councils: {total_councils}")
    print(f"Total wards: {total_wards}")
    
    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Data saved to: {output_path}")
    print("="*80)

if __name__ == '__main__':
    main()
