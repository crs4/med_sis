//  upload_type:sheet_name  
const Indicators =   {
    'SOC-CONTENT'  : { 'code' : 'SOC-CONTENT', 'name' : 'Soil organic carbon (SOC) content', 'type' : 'Chemical', 'purpose' : 'SOC', 'reference' : 'Dry combustion (Paterson, 2021a)'},
    'SOC-QUALITY-1'  : { 'code' : 'SOC-QUALITY-1', 'name' : 'Soil organic carbon quality 1', 'type' : 'Chemical', 'purpose' : 'SOC', 'reference' : 'Near-infrared (for the partners with required equipment) (Ge et al., 2024)'},
    'SOC-QUALITY-2'  : { 'code' : 'SOC-QUALITY-2', 'name' : 'Soil organic carbon quality 1', 'type' : 'Chemical', 'purpose' : 'SOC', 'reference' : 'C/N ratio'},
    'SOC-STOCK'  : { 'code' : 'SOC-STOCK', 'name' : 'Soil organic carbon stock', 'type' : 'Chemical', 'purpose' : 'SOC', 'reference' : 'PTF'},
    'TOT-NITROGEN'  : { 'code' : 'TOT-NITROGEN', 'name' : 'Total Nitrogen', 'type' : 'Chemical', 'purpose' : 'NITROGEN', 'reference' : 'Dry combustion (Yeomans and Bremner, 1991)'},
    'NUTRIENTS-1'  : { 'code' : 'NUTRIENTS-1', 'name' : 'Available nutrients (nitrogen and phosphorus) 1', 'type' : 'Chemical', 'purpose' : 'NUTRIENTS', 'reference' : 'Extraction KCl 2M for nitrate and ammonium quantification (Ryan et al., 2001)'},
    'NUTRIENTS-2'  : { 'code' : 'NUTRIENTS-2', 'name' : 'Available nutrients (nitrogen and phosphorus) 2', 'type' : 'Chemical', 'purpose' : 'NUTRIENTS', 'reference' : 'Olsen P extraction (Paterson, 2021b)'},
    'SOIL-REACTION'  : { 'code' : 'SOIL-REACTION', 'name' : 'Soil reaction', 'type' : 'Chemical', 'purpose' : 'SOIL-REACTION', 'reference' : 'pHH2O, pHCaCl2/KCl by suspension in water 1:5 (w:v) (IUSS Working Group WRB, 2022a)'},
    'CARBONATES-1'  : { 'code' : 'CARBONATES-1', 'name' : 'Carbonates - 1', 'type' : 'Chemical', 'purpose' : 'CARBONATES', 'reference' : 'Total CaCO3 equivalent (based on the ISO 10694:1995'},
    'CARBONATES-2'  : { 'code' : 'CARBONATES-2', 'name' : 'Carbonates - 2', 'type' : 'Chemical', 'purpose' : 'CARBONATES', 'reference' : ' cited by Paterson, 2021c)'},
    'CARBONATES-3'  : { 'code' : 'CARBONATES-3', 'name' : 'Carbonates - 3', 'type' : 'Chemical', 'purpose' : 'CARBONATES', 'reference' : 'Active CaCO3 (Sheikh-Abdullah et al., 2023)'},
    'SALINITY-1'  : { 'code' : 'SALINITY-1', 'name' : 'Salinity - 1', 'type' : 'Chemical', 'purpose' : 'SALINITY', 'reference' : 'Electrical conductivity 1:5 and saturated soil extracts (Rhoades, 1996) (Annex 3)'},
    'SALINITY-2'  : { 'code' : 'SALINITY-2', 'name' : 'Salinity - 2', 'type' : 'Chemical', 'purpose' : 'SALINITY', 'reference' : 'Sodium saturation percentage (Annex 3)'},
    'CEC'  : { 'code' : 'CEC', 'name' : 'Cation Exchange Capacity (CEC)', 'type' : 'Chemical', 'purpose' : 'EXCHANGE', 'reference' : 'Extraction ammonium acetate (Sumner and Miller, 1996) or Barium chloride (Annex 3) (Kalra and Maynard, 1994)'},
    'EXCHANGEABLE_BASES'  : { 'code' : 'EXCHANGEABLE_BASES', 'name' : 'Exchangeable bases', 'type' : 'Chemical', 'purpose' : 'EXCHANGE', 'reference' : 'Extraction ammonium acetate (Sumner and Miller, 1996) or Barium chloride (Annex 3) (Kalra and Maynard, 1994)'},
    'METALS'  : { 'code' : 'METALS', 'name' : 'Metals and Metalloids content', 'type' : 'Chemical', 'purpose' : 'METALS', 'reference' : 'Total and bioavailable fraction by DTPA and ammonium bicarbonate solution (Paterson, 2021d; Soltanpour, 1985)'},
    'TEXTURE'  : { 'code' : 'TEXTURE', 'name' : 'Soil texture', 'type' : 'Physical', 'purpose' : 'PHYSICAL', 'reference' : 'Particle size distribution by pipette method (Chaudhari et al., 2008), textural class by WRB Ultimate Soil Texture Flow Chart (IUSS Working Group WRB, 2022b), Coarse material by sieving (>2 mm) (Paterson, 2021e)'},
    'POROSITY-1'  : { 'code' : 'POROSITY-1', 'name' : 'Soil porosity 1', 'type' : 'Physical', 'purpose' : 'PHYSICAL', 'reference' : 'Soil bulk density by cylinder method (IUSS Working Group WRB, 2022a)'},
    'POROSITY-2'  : { 'code' : 'POROSITY-2', 'name' : 'Soil porosity 2', 'type' : 'Physical', 'purpose' : 'PHYSICAL', 'reference' : 'Dry density'},
    'STABILITY'  : { 'code' : 'STABILITY', 'name' : 'Soil aggregate stability', 'type' : 'Physical', 'purpose' : 'PHYSICAL', 'reference' : 'Slake application (Rieke et al., 2022)'},
    'VULNERABILTY'  : { 'code' : 'VULNERABILTY', 'name' : 'Structure vulnerability index', 'type' : 'Physical', 'purpose' : 'PHYSICAL', 'reference' : 'SOC %/Clay % (Johannes et al., 2017)'},
    'WATER_INFILTRATION'  : { 'code' : 'WATER_INFILTRATION', 'name' : 'Water infiltration', 'type' : 'Physical', 'purpose' : 'PHYSICAL', 'reference' : 'Hydraulic conductivity at saturation by PTF and/or in the field by Beerkan test (Lassabatère et al., 2006)'},
    'WATER_STORAGE_CAPACITY'  : { 'code' : 'WATER_STORAGE_CAPACITY', 'name' : 'Water storage capacity', 'type' : 'Physical', 'purpose' : 'PHYSICAL', 'reference' : 'Water content at field capacity, water content at wilting point and water holding capacity by PTF and Water content saturation by cylinder method (Uhland, 1950) or PTF'},
    'MICROBIAL'  : { 'code' : 'MICROBIAL', 'name' : 'Microbial activity', 'type' : 'Biological', 'purpose' : 'BIOLOGICAL', 'reference' : 'PLFA (Siles et al., 2024)'},
    'EARTHWORMS'  : { 'code' : 'EARTHWORMS', 'name' : 'Earthworms abundance and diversity', 'type' : 'Biological', 'purpose' : 'BIOLOGICAL', 'reference' : '(Shepherd et al., 2008)'},
}
									
									
									
									
									
									
									
									
									
									
									
									
									
									
									
