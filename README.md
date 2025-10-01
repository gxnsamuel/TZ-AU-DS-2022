# Tanzania Administrative Units Dataset 2022

A comprehensive, structured dataset of Tanzania's administrative divisions extracted from the official 2022 Population and Housing Census (PHC) report.

## 📊 Dataset Overview

This repository contains a complete hierarchical dataset of Tanzania's administrative structure, including:

- **31 Regions** (Mikoa)
- **194 Councils** (District Councils, Municipal Councils, Town Councils, and City Councils)
- **4,296 Wards** (Kata)

The data is structured in a JSON format that reflects the administrative hierarchy of the United Republic of Tanzania.

## 🗂️ Data Structure

The dataset follows a hierarchical structure:

```json
{
  "country": "Tanzania",
  "regions": [
    {
      "region": "Dodoma",
      "data": [
        {
          "district_council": "Kondoa",
          "wards": ["Changaa", "Hondomairo", "Thawi", "..."]
        },
        {
          "town_council": "Kondoa",
          "wards": ["Kondoa Mjini", "Kilimani", "..."]
        },
        {
          "city_council": "Dodoma",
          "wards": ["Hazina", "Madukani", "..."]
        }
      ]
    }
  ]
}
```

### Administrative Levels

1. **Country Level**: Tanzania (United Republic of Tanzania)
2. **Regional Level** (Mkoa): 31 regions across mainland Tanzania and Zanzibar
3. **Council Level** (Halmashauri): Four types of councils:
   - **District Councils** (Halmashauri za Wilaya): Rural administrative units
   - **Municipal Councils** (Halmashauri za Manispaa): Semi-urban administrative units
   - **Town Councils** (Halmashauri za Miji): Urban administrative units
   - **City Councils** (Halmashauri za Jiji): Major urban centers
4. **Ward Level** (Kata): The smallest administrative unit in this dataset

## 📈 Statistical Summary

### Regional Distribution

| Region | Councils | Wards | Region | Councils | Wards |
|--------|----------|-------|--------|----------|-------|
| Dodoma | 8 | 209 | Rukwa | 4 | 97 |
| Arusha | 7 | 155 | Kigoma | 8 | 139 |
| Kilimanjaro | 7 | 165 | Shinyanga | 5 | 130 |
| Tanga | 11 | 242 | Kagera | 8 | 192 |
| Morogoro | 9 | 192 | Mwanza | 8 | 191 |
| Pwani | 9 | 132 | Mara | 9 | 178 |
| Dar es Salaam | 5 | 102 | Manyara | 7 | 141 |
| Lindi | 6 | 151 | Njombe | 6 | 107 |
| Mtwara | 9 | 190 | Katavi | 5 | 57 |
| Ruvuma | 8 | 171 | Simiyu | 6 | 133 |
| Iringa | 5 | 102 | Geita | 6 | 122 |
| Mbeya | 7 | 177 | Songwe | 5 | 93 |
| Singida | 7 | 136 | Kaskazini Unguja | 2 | 75 |
| Tabora | 8 | 206 | Kusini Unguja | 2 | 63 |
| Mjini Magharibi | 3 | 119 | Kaskazini Pemba | 2 | 61 |
| Kusini Pemba | 2 | 68 | | | |

### Council Type Distribution

- **District Councils**: 136 councils (majority, serving rural areas)
- **Municipal Councils**: 32 councils (serving semi-urban areas)
- **Town Councils**: 21 councils (serving urban areas)
- **City Councils**: 5 councils (Dodoma, Arusha, Tanga, Dar es Salaam, Mwanza)

## 💾 Data Files

- **`dataset.json`**: The complete administrative units dataset in JSON format (UTF-8 encoded)
- **`extract_admin_units.py`**: Python script used to extract data from the PDF report
- **`Administrative_units_Population_Distribution_Report_Tanzania_volume1a.pdf`**: Source PDF document

## 🔍 Data Source & Reliability

### Official Source

This dataset is extracted from the **official 2022 Population and Housing Census (PHC) report** published by:

- **Publisher**: National Bureau of Statistics (NBS), Tanzania
- **Document**: "Population Distribution Report Volume 1a" 
- **Year**: 2022
- **Authority**: Government of the United Republic of Tanzania

### Data Trustworthiness

✅ **Highly Reliable** - The data comes from:

1. **Official Government Census**: The 2022 PHC is Tanzania's official census conducted by the National Bureau of Statistics
2. **Legal Authority**: Census data is collected under the Statistics Act
3. **Comprehensive Coverage**: The census covers all administrative units in Tanzania
4. **Recent Data**: Reflects the most current administrative structure as of 2022
5. **Primary Source**: Extracted directly from the official PDF report (pages 54-286)

### Data Extraction Methodology

- **Method**: Automated extraction using pdfplumber library
- **Verification**: Manual spot-checking against source document
- **Accuracy**: High accuracy with systematic pattern matching
- **Completeness**: All 31 regions, 194 councils, and 4,296 wards captured

## 🚀 Usage Examples

### Python

```python
import json

# Load the dataset
with open('dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get all regions
regions = [region['region'] for region in data['regions']]
print(f"Total regions: {len(regions)}")

# Get all councils in Dodoma region
dodoma = next(r for r in data['regions'] if r['region'] == 'Dodoma')
for council in dodoma['data']:
    council_type = list(council.keys())[0]  # district_council, town_council, etc.
    council_name = council[council_type]
    print(f"{council_type}: {council_name} - {len(council['wards'])} wards")

# Count total wards
total_wards = sum(
    len(council['wards']) 
    for region in data['regions'] 
    for council in region['data']
)
print(f"Total wards: {total_wards}")
```

### JavaScript

```javascript
// Load the dataset
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('dataset.json', 'utf8'));

// Get all regions
const regions = data.regions.map(r => r.region);
console.log(`Total regions: ${regions.length}`);

// Get all wards in Dar es Salaam
const darEsSalaam = data.regions.find(r => r.region === 'Dar es Salaam');
darEsSalaam.data.forEach(council => {
  const councilType = Object.keys(council).find(k => k !== 'wards');
  console.log(`${council[councilType]}: ${council.wards.length} wards`);
});
```

### Command Line (jq)

```bash
# Get all region names
jq '.regions[].region' dataset.json

# Count councils per region
jq '.regions[] | {region: .region, councils: (.data | length)}' dataset.json

# Get all wards in a specific region
jq '.regions[] | select(.region == "Arusha") | .data[].wards[]' dataset.json

# Count total administrative units
jq '{regions: (.regions | length), councils: [.regions[].data[]] | length, wards: [.regions[].data[].wards[]] | length}' dataset.json
```

## 🌍 Use Cases

### Urban Planning & Development
- Planning infrastructure projects at ward level
- Resource allocation based on administrative divisions
- Identifying urban vs rural areas through council types

### Government & Public Administration
- Electoral boundary management
- Service delivery planning
- Administrative correspondence

### Research & Academia
- Demographic studies
- Regional development research
- Comparative analysis of administrative structures

### Technology & Software Development
- Location-based services
- Address validation systems
- Geographic information systems (GIS)
- Mobile applications requiring administrative data

### Business & Commerce
- Market segmentation
- Distribution network planning
- Location-based analytics

### Non-Governmental Organizations (NGOs)
- Program implementation planning
- Community development initiatives
- Resource mapping

## 🗣️ Multi-Language Reference

### English Terms
- **Region**: Administrative division (31 total)
- **District Council**: Rural administrative unit
- **Municipal Council**: Semi-urban administrative unit
- **Town Council**: Urban administrative unit
- **City Council**: Major urban center
- **Ward**: Smallest administrative unit

### Swahili (Kiswahili) Terms
- **Mkoa** (Mikoa - plural): Region
- **Wilaya**: District
- **Halmashauri ya Wilaya**: District Council
- **Halmashauri ya Manispaa**: Municipal Council
- **Halmashauri ya Mji**: Town Council
- **Halmashauri ya Jiji**: City Council
- **Kata**: Ward

### Example Regions (Swahili)
- Dodoma (Capital region)
- Dar es Salaam (Commercial capital)
- Arusha (Northern highlands)
- Mwanza (Lake Victoria region)
- Zanzibar regions: Kaskazini Unguja, Kusini Unguja, Mjini Magharibi, Kaskazini Pemba, Kusini Pemba

## 📝 Data Maintenance

### Version
- **Current Version**: 2022 PHC
- **Last Updated**: 2022
- **Next Update**: Expected with next census (typically every 10 years)

### Known Limitations
1. This dataset does not include:
   - Sub-ward divisions (Mtaa/Vitongoji)
   - Population figures (available in the source PDF)
   - Geographic coordinates
   - Demographic details

2. Administrative boundaries may change between censuses due to:
   - Creation of new regions
   - Elevation of town councils to municipalities
   - Ward boundary adjustments

## 🤝 Contributing

Contributions are welcome! Please:
1. Verify changes against official government sources
2. Maintain the existing JSON structure
3. Update this README if adding new features
4. Submit pull requests with clear descriptions

## 📄 License

This dataset is derived from official government publications and is made available for public use. Please cite the original source:

**National Bureau of Statistics, Tanzania. (2022). Population Distribution Report - 2022 Population and Housing Census, Volume 1a. United Republic of Tanzania.**

## 🔗 Related Resources

- [National Bureau of Statistics, Tanzania](https://www.nbs.go.tz/)
- [Tanzania Government Portal](https://www.tanzania.go.tz/)
- [OpenStreetMap Tanzania](https://www.openstreetmap.org/relation/195270)

## 📧 Contact & Support

For questions, corrections, or suggestions regarding this dataset, please:
- Open an issue in this repository
- Refer to the official NBS Tanzania website for authoritative information

---

**Disclaimer**: While this dataset is extracted from official sources, users should verify critical information with the National Bureau of Statistics, Tanzania. This dataset is provided "as is" without warranties of any kind.