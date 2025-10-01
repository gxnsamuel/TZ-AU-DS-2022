# Tanzania Administrative Units Dataset 2022

A comprehensive, structured dataset of Tanzania's administrative divisions extracted from the official 2022 Population and Housing Census (PHC) report.

## 📊 Dataset Overview

This repository contains comprehensive datasets of Tanzania's administrative structure and population statistics:

### Administrative Units Dataset
- **31 Regions** (Mikoa)
- **194 Councils** (District Councils, Municipal Councils, Town Councils, and City Councils)
- **4,296 Wards** (Kata)

### Population Statistics Dataset (NEW!)
Complete population statistics from the 2022 Population and Housing Census including:
- **Population by Sex**: Total, Male, Female populations at all administrative levels
- **Sex Ratio**: Male to female ratio per 100 females
- **Households**: Total number of households
- **Average Household Size**: Mean household size
- **Coverage**: All 31 regions, 194 councils, and 4,295 wards
- **Total Population**: 59,716,173 people

All data is structured in JSON format that reflects the administrative hierarchy of the United Republic of Tanzania.

## 🗂️ Data Structure

### Administrative Units Dataset (`dataset.json`)

The administrative units dataset follows a hierarchical structure:

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

### Population Statistics Dataset (`population_stats.json`)

The population statistics dataset extends the hierarchical structure with comprehensive demographic data:

```json
{
  "country": "Tanzania",
  "source": "2022 Population and Housing Census (PHC)",
  "regions": [
    {
      "region": "Dodoma",
      "population": {
        "both_sexes": 3085625,
        "male": 1512760,
        "female": 1572865,
        "sex_ratio": 96,
        "households": 757821,
        "average_household_size": 4.1
      },
      "councils": [
        {
          "type": "district_council",
          "name": "Kondoa",
          "population": {
            "both_sexes": 244854,
            "male": 124379,
            "female": 120475,
            "sex_ratio": 103,
            "households": 52677,
            "average_household_size": 4.6
          },
          "wards": [
            {
              "name": "Changaa",
              "population": {
                "both_sexes": 8436,
                "male": 4340,
                "female": 4096,
                "sex_ratio": 106,
                "households": 1871,
                "average_household_size": 4.5
              }
            }
          ]
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

### National Statistics

- **Total Population**: 59,716,173 people
- **Male**: 29,445,413 (49.3%)
- **Female**: 30,270,760 (50.7%)
- **Sex Ratio**: 97 males per 100 females
- **Total Households**: 14,455,335
- **Average Household Size**: 4.1 people per household

### Regional Distribution (with Population)

| Region | Councils | Wards | Population | Region | Councils | Wards | Population |
|--------|----------|-------|------------|--------|----------|-------|------------|
| Dodoma | 8 | 209 | 3,085,625 | Rukwa | 4 | 97 | 1,540,519 |
| Arusha | 7 | 155 | 2,356,255 | Kigoma | 8 | 139 | 2,470,967 |
| Kilimanjaro | 7 | 165 | 1,861,934 | Shinyanga | 5 | 130 | 2,241,299 |
| Tanga | 11 | 242 | 2,615,597 | Kagera | 8 | 192 | 2,989,299 |
| Morogoro | 9 | 192 | 3,197,104 | Mwanza | 8 | 191 | 3,699,872 |
| Pwani | 9 | 132 | 1,425,131 | Mara | 9 | 178 | 2,372,015 |
| Dar es Salaam | 5 | 102 | 5,383,728 | Manyara | 7 | 141 | 1,892,502 |
| Lindi | 6 | 151 | 1,015,393 | Njombe | 6 | 107 | 889,946 |
| Mtwara | 9 | 190 | 1,457,670 | Katavi | 5 | 57 | 1,152,958 |
| Ruvuma | 8 | 171 | 1,848,794 | Simiyu | 6 | 133 | 2,140,497 |
| Iringa | 5 | 102 | 1,192,728 | Geita | 6 | 122 | 2,977,608 |
| Mbeya | 7 | 177 | 2,343,754 | Songwe | 5 | 93 | 1,344,687 |
| Singida | 7 | 136 | 2,008,058 | Kaskazini Unguja | 2 | 75 | 257,290 |
| Tabora | 8 | 206 | 3,391,679 | Kusini Unguja | 2 | 63 | 195,873 |
| Mjini Magharibi | 3 | 119 | 893,169 | Kaskazini Pemba | 2 | 61 | 272,091 |
| Kusini Pemba | 2 | 68 | 271,350 | | | | |

### Council Type Distribution

- **District Councils**: 136 councils (majority, serving rural areas)
- **Municipal Councils**: 32 councils (serving semi-urban areas)
- **Town Councils**: 21 councils (serving urban areas)
- **City Councils**: 5 councils (Dodoma, Arusha, Tanga, Dar es Salaam, Mwanza)

## 💾 Data Files

### Core Datasets

- **`dataset.json`**: Complete administrative units dataset with regions, councils, and wards in hierarchical JSON format (UTF-8 encoded)
- **`population_stats.json`**: Comprehensive population statistics for all administrative units including population by sex, sex ratio, households, and average household size (1.4MB, UTF-8 encoded)

### Extraction Scripts

- **`extract_admin_units.py`**: Python script to extract administrative units (regions, councils, wards) from the PDF report
- **`extract_population_stats.py`**: Python script to extract population statistics from pages 54-286 of the PDF report

### Source Document

- **`Administrative_units_Population_Distribution_Report_Tanzania_volume1a.pdf`**: Official source PDF document from the 2022 Population and Housing Census

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

### Python - Administrative Units

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

### Python - Population Statistics

```python
import json

# Load the population statistics
with open('population_stats.json', 'r', encoding='utf-8') as f:
    pop_data = json.load(f)

# Get total population
total_pop = sum(
    region['population'].get('both_sexes', 0)
    for region in pop_data['regions']
)
print(f"Total Tanzania population: {total_pop:,}")

# Get top 5 most populous regions
regions_by_pop = sorted(
    pop_data['regions'],
    key=lambda r: r['population'].get('both_sexes', 0),
    reverse=True
)[:5]

print("\nTop 5 most populous regions:")
for region in regions_by_pop:
    pop = region['population']
    print(f"{region['region']}: {pop['both_sexes']:,} people")
    print(f"  Male: {pop['male']:,}, Female: {pop['female']:,}")
    print(f"  Households: {pop['households']:,}, Avg size: {pop['average_household_size']}")

# Analyze a specific council
dodoma_region = next(r for r in pop_data['regions'] if r['region'] == 'Dodoma')
kondoa_council = next(c for c in dodoma_region['councils'] if c['name'] == 'Kondoa')

print(f"\nKondoa District Council:")
print(f"  Population: {kondoa_council['population']['both_sexes']:,}")
print(f"  Number of wards: {len(kondoa_council['wards'])}")

# Get ward-level statistics
ward_populations = [w['population']['both_sexes'] for w in kondoa_council['wards']]
print(f"  Largest ward: {max(ward_populations):,} people")
print(f"  Smallest ward: {min(ward_populations):,} people")
print(f"  Average ward size: {sum(ward_populations) // len(ward_populations):,} people")
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
- Resource allocation based on administrative divisions and population density
- Identifying urban vs rural areas through council types and population statistics
- Population-based service planning (schools, hospitals, water systems)

### Government & Public Administration
- Electoral boundary management with population data
- Service delivery planning based on population distribution
- Administrative correspondence
- Budget allocation based on population and household counts

### Research & Academia
- Demographic studies and population analysis
- Regional development research
- Comparative analysis of administrative structures
- Population density and urbanization studies
- Household size and family structure research

### Healthcare & Social Services
- Healthcare facility planning based on population distribution
- Disease surveillance and health program targeting
- Social welfare program implementation
- Family planning initiatives using household data

### Technology & Software Development
- Location-based services with population context
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

#### Administrative Units Dataset (`dataset.json`)
1. This dataset does not include:
   - Sub-ward divisions (Mtaa/Vitongoji)
   - Population figures (see `population_stats.json`)
   - Geographic coordinates
   - Demographic details beyond administrative structure

#### Population Statistics Dataset (`population_stats.json`)
1. This dataset does not include:
   - Sub-ward population breakdown
   - Age and gender disaggregation beyond male/female totals
   - Socioeconomic indicators
   - Geographic coordinates
   - Historical population trends

#### General Limitations
1. Administrative boundaries may change between censuses due to:
   - Creation of new regions
   - Elevation of town councils to municipalities
   - Ward boundary adjustments

2. Data completeness:
   - All 4,295 wards have complete population statistics
   - 191 of 194 councils have council-level population totals
   - 30 of 31 regions have regional-level population totals
   - Some regional/council totals are missing due to PDF formatting variations

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