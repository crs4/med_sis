// dataset 
const AoiSoilIndicators = {
    'datasets': [
        { "name":"Enrichment factor - Pb", "unit": "MEASURE_UNITS:unitless", "abstract:":"Enrichment factor for Lead (Pb)", "code":"labdata_geo", "type": "soil_chemical_health" },
        { "name":"Enrichment factor - Hg", "unit": "MEASURE_UNITS:unitless", "abstract:":"Enrichment factor for Mercury (Hg)", "code":"labdata_geo", "type": "soil_chemical_health" },
        { "name":"Enrichment factor - Cd", "unit": "MEASURE_UNITS:unitless", "abstract:":"Enrichment factor for Cadmium (Cd)", "code":"labdata_geo", "type": "soil_chemical_health" },
        { "name":"Enrichment factor - Ni", "unit": "MEASURE_UNITS:unitless", "abstract:":"Enrichment factor for Nichel (Ni)", "code":"labdata_geo", "type": "soil_chemical_health" },
        { "name":"Enrichment factor - Cu", "unit": "MEASURE_UNITS:unitless", "abstract:":"Enrichment factor for Copper (Cu)", "code":"labdata_geo", "type": "soil_chemical_health" },
        { "name":"Enrichment factor - Sb", "unit": "MEASURE_UNITS:unitless", "abstract:":"Enrichment factor for Antimony (Sb)", "code":"labdata_geo", "type": "soil_chemical_health" },
        { "name":"Enrichment factor - Mn", "unit": "MEASURE_UNITS:unitless", "abstract:":"Enrichment factor for Manganese (Mn)", "code":"labdata_geo", "type": "soil_chemical_health" },
        { "name":"Enrichment factor - Cr", "unit": "MEASURE_UNITS:unitless", "abstract:":"Enrichment factor for Chromium (Cr)", "code":"labdata_geo", "type": "soil_chemical_health"},
        { "name":"Enrichment factor - Co", "unit": "MEASURE_UNITS:unitless", "abstract:":"Enrichment factor for Cobalt  (Co)", "code":"labdata_geo", "type": "soil_chemical_health"},
        { "name":"Enrichment factor - V",  "unit": "MEASURE_UNITS:unitless", "abstract:":"Enrichment factor for Vanadium (V)", "code":"labdata_geo", "type": "soil_chemical_health"},
        { "name":"Enrichment factor - As", "unit": "MEASURE_UNITS:unitless", "abstract:":"Enrichment factor for Vanadium (Arsenic)", "code":"labdata_geo", "type": "soil_chemical_health"},
    ],
    'hydroPTF': { "name":"Hydro PTF input data", "unit": "MEASURE_UNITS:unitless", "abstract":"Hydro PTF input data: sand(percentage), clay (percentage), org_car (percentage), bulk_dens (g/cm3)", "code":"hydro_ptf_input_data_geo", "type": "points_soil_data"}     
}

export default AoiSoilIndicators
