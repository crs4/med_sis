from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_percentage(value):
    if value is not None and (value < 0 or value > 100):
        raise ValidationError(_('Il valore deve essere compreso tra 0 e 100'))

def validate_positive(value):
    if value is not None and value < 0:
        raise ValidationError(_('Il valore deve essere positivo'))

def validate_latitude(value):
    if value is not None and (value < -90 or value > 90):
        raise ValidationError(_('La latitudine deve essere compresa tra -90 e 90'))

def validate_longitude(value):
    if value is not None and (value < -180 or value > 180):
        raise ValidationError(_('La longitudine deve essere compresa tra -180 e 180'))


###########################
## XLSx Uploads
###########################
UPLOAD_RESULTS = [
    ("UPLOADED" , "UPLOADED"),
    ("IN_PROCESS" , "IN_PROCESS"),
    ("IMPORT_SUCCESS" , "IMPORT_SUCCESS"),
    ("IMPORT_WITH_ERROR" , "IMPORT_WITH_ERROR"),
    ("CRITICAL_ERROR" , "CRITICAL_ERROR"),
]  
UPLOAD_TYPES = [
    ("XLS_P" , "XLSx Profiles upload"),
    ("XLS_S" , "XLSx Samples upload"),
    ("XLS_PG" , "XLSx Profiles Genealogy upload"),
    ("XLS_SG" , "XLSx Samples Genealogy upload"),
    ("XLS_PH" , "XLSx Photo metadata upload")
]
UPLOAD_OPERATION = [
    ("POST" , "Create new"),
    ("PUT" , "Create or Update all fields"),
    ("PATCH" , "If exist update some fields")
]

class XLSxUpload(models.Model):
    type = models.TextField(choices=UPLOAD_TYPES, db_comment='Type of the upload')
    title = models.TextField(db_comment='sheet name')
    report = models.JSONField( db_comment='Report of the upload')
    data = models.JSONField( db_comment='Data uploaded')
    editor = models.TextField( db_comment='Owner of the upload', null=True, blank=True)
    date = models.DateTimeField( db_comment='Date of the upload')
    status = models.TextField( choices=UPLOAD_RESULTS, db_comment='Status of the upload' )
    operation = models.TextField( choices=UPLOAD_OPERATION, db_comment='http method POST/PUT/PATCH ' )

    objects = models.Manager().using('backoffice')

    def start_processing(self):
        """Avvia il processo di importazione dei dati"""
        from .tasks import process_xlsx_upload
        if self.status == "UPLOADED":
            self.status = "IN_PROCESS"
            self.save()
            process_xlsx_upload.delay(self.id)
            return True
        return False


    class Meta:
        managed = True
        db_table = 'xlsx_upload'
        db_table_comment = 'XLSx Data Uploads'
        permissions = (
            ('view', 'can view data'),
            ('add', 'can add data'),
            ('change', 'can change data'),
            ('delete', 'can delete data'),
        )

###########################
# Profile\Samples Genealogy
###########################
class Project(models.Model):
    id = models.TextField(primary_key=True, db_comment='Project identifier ')
    old_code = models.TextField(blank=True, null=True, db_comment='Original project id')
    title = models.TextField(blank=True, null=True, db_comment='project name')
    descr = models.TextField(blank=True, null=True, db_comment='project description')
    refer = models.TextField(blank=True, null=True, db_comment='reference')
    pub_year = models.IntegerField(blank=True, null=True, db_comment='year of pubblication')
    web_link = models.TextField(blank=True, null=True)
    avail = models.TextField(blank=True, null=True, db_comment='Data availability and/or use restrictions')
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'projects'
        db_table_comment = 'projects descriptor'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

####CHOICES
#General
SHAPES = [
    ("nd", "No Data"),
    ("CL", "vertical curvature Concave, horizontal curvature Linear"),
    ("CV", "vertical curvature Concave, horizontal curvature Convex"),
    ("CC", "vertical curvature Concave, horizontal curvature Concave"),
    ("no", "no slope"),
    ("LL", "vertical curvature Linear, horizontal curvature Linear"),
    ("LV", "vertical curvature Linear, horizontal curvature Convex"),
    ("LC", "vertical curvature Linear, horizontal curvature Concave"),
    ("VL", "vertical curvature Convex, horizontal curvature Linear"),
    ("VV", "vertical curvature Convex, horizontal curvature Convex"),
    ("VC", "vertical curvature Convex, horizontal curvature Concave"),
]
POSITION = [
    ("nd", "No Data"),
    ("no", "no uneven terrain"),
    ("SU", "Summit"),
    ("SH", "Shoulder"),
    ("BS", "Backslope"),
    ("FS", "Footslope"),
    ("TS", "Toeslope"),
    ("VB", "Valley bottom"),
    ("OB", "Basin with outflow"),
    ("EB", "Endorheic basin")
]
LANDFORMS = [
    ("AA", "Area of accumulation"),
    ("AAW", "Landfill of anthropic origin waste"),
    ("AAR", "Landfill of remoulded natural material"),
    ("AM", "Mining area"),
    ("AMQ", "Abandoned quarry"),
    ("AMA", "Active quarry"),
    ("AC", "Embankment for canal/river or other constructions"),
    ("AT", "Terraced slope"),
    ("ATD", "Deteriorated terraced slope"),
    ("ATI", "Intact terraced slope"),
    ("ATM", "Mechanizable terraced slope, with connected levels"),
    ("AR", "Grading, reshaped slope"),
    ("AS", "Anthropic sinkhole"),
    ("KD", "Karst depression"),
    ("KDD", "Sinkhole (Doline)"),
    ("KDU", "Uvala"),
    ("KDP", "Poje"),
    ("KDR", "Residual relief (hum)"),
    ("KK", "Karren (field), grooves"),
    ("KG", "Griza"),
    ("KF", "Fluvio-karst valley"),
    ("KFB", "Blind valley"),
    ("KFC", "Closed valley"),
    ("KFD", "Dry valley"),
    ("KC", "Cave"),
    ("SD", "Slope deposit (talus)"),
    ("ST", "Talus deposit"),
    ("SL", "Translational/ Rotational Landslide"),
    ("SLN", "Landslide niche"),
    ("SLD", "Landslide deposit"),
    ("SF", "Debris/Mud flow deposit"),
    ("SA", "Deep-seated gravitational slope deformations (trenches, counter slopes)"),
    ("SC", "Soil creep terraces"),
    ("SS", "Solifluction lobes"),
    ("SG", "Gelifluction lobes"),
    ("SO", "Soil slips deposit"),
    ("SR", "Rockfall and toppling "),
    ("SRN", "Landslide niche"),
    ("SRD", "Landslide deposit"),
    ("WH", "Hanging valley step"),
    ("WV", "V shaped small Valley "),
    ("WW", "Wide fluvial valley"),
    ("WF", "Flat bottom fluvial valley"),
    ("WL", "Rills and gullies"),
    ("WG", "Gorge"),
    ("WB", "Badlands"),
    ("WBC", "Calanco"),
    ("WBB", "Badlands"),
    ("WP", "Earth pyramids"),
    ("WC", "Glacis"),
    ("WA", "Alluvial fan"),
    ("WD", "Colluvial deposit"),
    ("WT", "Fluvial terrace"),
    ("WTE", "Erosion scarp"),
    ("WTS", "Surface"),
    ("WU", "Alluvial plain "),
    ("WUB", "Reclaimed alluvial plain"),
    ("WUD", "Depressed area in an alluvial plain"),
    ("WR", "Riverbed"),
    ("WRB", "Braided"),
    ("WRF", "Floodplain and overflow area"),
    ("WRE", "Ephemeral"),
    ("WRC", "Crevasse splay"),
    ("WRS", "Single channel"),
    ("WRM", "Meandering"),
    ("WRA", "Anastomosing"),
    ("WRI", "Fluvial island"),
    ("WRR", "River bank"),
    ("WS", "Spring depression"),
    ("GB", "Block stream/field"),
    ("GR", "Rock glacier"),
    ("GC", "Glacier cirque"),
    ("GU", "Crioturbation unevenness"),
    ("GH", "Hummock"),
    ("GP", "Poligonal soil"),
    ("GF", "Fluvio-glacial deposit"),
    ("GFE", "Esker"),
    ("GFK", "Kame terrace"),
    ("GFS", "Sandur"),
    ("GV", "Glacial valley"),
    ("GVH", "Hanging glacial valley"),
    ("GD", "Glacial deposit"),
    ("GDS", "Subglacial deposit"),
    ("GDA", "Ablation moraine"),
    ("GDF", "Lateral/Frontal moraine"),
    ("GDI", "Intermoraine depression"),
    ("GDD", "Drumlin"),
    ("GN", "Nivations niche"),
    ("GS", "Bowl shaped depression"),
    ("GSI", "Infilled bowl shaped depression"),
    ("GT", "Glacial terrace"),
    ("GA", "Snow Avalanche channel"),
    ("GAC", "Channel"),
    ("GAD", "Deposit"),
    ("GO", "Protalus ramparts"),
    ("MA", "Abrasion platform"),
    ("MAC", "Cliff foot (talus)"),
    ("ML", "Lacustrine terrace"),
    ("MP", "Lacustrine plain"),
    ("MPM", "Mineral deposit infill"),
    ("MPO", "Organic deposit infill (peat bog)"),
    ("MR", "Reclaimed draining lacustrine plain"),
    ("MRM", "Mineral deposit infill"),
    ("MRO", "Organic deposit infill (peat bog)"),
    ("MC", "Coastal plain"),
    ("MCT", "Tidal plain"),
    ("MCR", "Coastal ribbon"),
    ("MCM", "Mud plain"),
    ("MCC", "Tidal canal"),
    ("MCS", "Sand plain"),
    ("MT", "Marine terrace"),
    ("MD", "River delta"),
    ("MDR", "Reclaimed delta"),
    ("MO", "Lagoon"),
    ("TC", "Cuesta"),
    ("TD", "Structural depression (graben)"),
    ("TG", "Irregular slopes due to tectonic structure influence"),
    ("TR", "Structural relief (horst)"),
    ("TS", "Structural surface "),
    ("TSD", "Dissected structural surface "),
    ("TSW", "Wavy structural surface"),
    ("TV", "Fault slope"),
    ("VA", "Caldera"),
    ("VR", "Volcanic crater"),
    ("VRM", "Maar crater"),
    ("VC", "Volcanic cone"),
    ("VCA", "Volcanic ash cone "),
    ("VCL", "Volcanic lava cone"),
    ("VCP", "Polygenic volcanic cone "),
    ("VCS", "Scoria volcanic cone"),
    ("VD", "Lava dome"),
    ("VL", "Lava flow"),
    ("VH", "Lahar deposit"),
    ("VF", "Pyroclastic flow deposit"),
    ("VP", "Volcanic Plateau"),
    ("nd", "no data"),
    ("VT", "Structural – Volcanic depression"),
    ("ES", "Aeolian deflation surface"),
    ("ED", "Aeolian deposit"),
    ("EDL", "Loess"),
    ("EDD", "Dune"),
    ("EDE", "Dune affected by erosion"),
    ("EDS", "Stabilized dune"),
    ("EDA", "Dune affected by anthropic influence"),
    ("EI", "Interdune area"),
    ("EIL", "Interdune area periodically inundated"),
    ("UN", "Unknown"),
    ("A", "Anthropogenic landforms"),
    ("K", "Karst landforms"),
    ("S", "Slope landforms"),
    ("W", "Water related landforms"),
    ("G", "Glacial and periglacial landforms "),
    ("M", "Marine and Lacustrine landforms"),
    ("T", "Structural landforms"),
    ("V", "Volcanic landforms"),
    ("E", "Aeolian landform")
]
ACTIVITIES = [
    ("nd", "no data"),
    ("A", "Active or Quiescent"),
    ("I", "Inactive"),
    ("R", "Relict"),
    ("UN", "Unknown")
]
SIZES = [
    ("nd", "size_cm: nd; description: no data"),
    ("F", "size_cm: > 0.2 - 0.6; description: Fine gravel"),
    ("M", "size_cm: > 0.6 - 2; description: Medium gravel"),
    ("C", "size_cm: > 2 - 6; description: Coarse gravel"),
    ("S", "size_cm: > 6 - 20; description: Stones"),
    ("B", "size_cm: > 20 - 60; description: Boulders"),
    ("L", "size_cm: > 60; description: Large boulders"),
    ("N", "size_cm: none; description: No coarse surface fragments"),
    ("G", "size_cm: > 0.2 - 6; description: Gravel")
]
CLIMATE_KOPPEN = [
    ("Af", "Tropical rainforest climate"),
    ("Aw", "Tropical savanna climate with dry-winter characteristics"),
    ("As", "Tropical savanna climate with dry-summer characteristics"),
    ("Am", "Tropical monsoon climate"),
    ("BWh", "Hot arid climate"),
    ("BWc", "Cold arid climate"),
    ("BSh", "Hot semi-arid climate"),
    ("BSc", "Cold semi-arid climate"),
    ("Csa", "Mediterranean hot summer climate"),
    ("Csb", "Mediterranean warm/cool summer climate"),
    ("Csc", "Mediterranean cold summer climate"),
    ("Cfa", "Humid subtropical climate"),
    ("Cfb", "Oceanic climate"),
    ("Cfc", "Subpolar oceanic climate"),
    ("Cwa", "Dry-winter humid subtropical climate"),
    ("Cwb", "Dry-winter subtropical highland climate"),
    ("Cwc", "Dry-winter subpolar oceanic climate"),
    ("Dfa", "Hot-summer humid continental climate"),
    ("Dfb", "Warm-summer humid continental climate"),
    ("Dfc", "Subarctic climate"),
    ("Dfd", "Extremely cold subarctic climate"),
    ("Dwa", "Monsoon-influenced hot-summer humid continental climate"),
    ("Dwb", "Monsoon-influenced warm-summer humid continental climate"),
    ("Dwc", "Monsoon-influenced subarctic climate"),
    ("Dwd", "Monsoon-influenced extremely cold subarctic climate"),
    ("Dsa", "Mediterranean-influenced hot-summer humid continental climate"),
    ("Dsb", "Mediterranean-influenced warm-summer humid continental climate"),
    ("Dsc", "Mediterranean-influenced subarctic climate"),
    ("Dsd", "Mediterranean-influenced extremely cold subarctic climate"),
    ("ET", "Tundra climate"),
    ("EF", "Ice cap climate"),
    ("", ""),
    ("nd", "no data"),
    ("A", "Tropical climates"),
    ("B", "Dry climates"),
    ("C", "Temperate climates"),
    ("D", "Continental climates"),
    ("E", "Polar and alpine climates")
]
CURRENT_WEATHER = [
    ("nd", "no data"),
    ("SU", "Sunny/clear"),
    ("PC", "Partly cloudy"),
    ("OV", "Overcast"),
    ("RA", "Rain"),
    ("WS", "Sleet"),
    ("SL", "Snow")
]
ECOZONE_SHULTZ = [
    ("nd", "no data"),
    ("TYR", "Tropics with year-round rain"),
    ("TSR", "Tropics with summer rain"),
    ("TSD", "Dry tropics and subtropics"),
    ("SYR", "Subtropics with year-round rain"),
    ("SWR", "Subtropics with winter rain (Mediterranean climate)"),
    ("MHU", "Humid mid-latitudes"),
    ("MDR", "Dry mid-latitudes"),
    ("BOR", "Boreal zone"),
    ("POS", "Polar-subpolar zone")
]
PAST_WEATHER= [
    ("nd", "no data"),
    ("NM", "No rain in the last month"),
    ("NW", "No rain in the last week"),
    ("ND", "No rain in the last 24 hours"),
    ("RD", "Rain but no heavy rain in the last 24 hours"),
    ("RH", "Heavy rain for some days or excessive rain in the last 24 hours"),
    ("RE", "Extremely rainy or snow melting")
]
SEASON = [
    ("nd", "no data"),
    ("SP", "Spring"),
    ("SU", "Summer"),
    ("AU", "Autumn"),
    ("WI", "Winter"),
    ("WS", "Wet season"),
    ("DS", "Dry season"),
    ("NS", "No significant seasonality for plant growth")
]
SOIL_MOIST_REGIME= [
    ("nd", "no data"),
    ("Aq", "Aquic"),
    ("Ud", "Udic"),
    ("Us", "Ustic"),
    ("Xe", "Xeric"),
    ("Ar", "Aridic"),
    ("Pa", "Peraquic"),
    ("Pu", "Perudic"),
    ("To", "Torric")
]
SOIL_TEMP_REGIME = [
    ("nd", "no data"),
    ("Pe", "Pergelic"),
    ("Cr", "Cryic"),
    ("Fr", "Frigid"),
    ("Me", "Mesic"),
    ("Th", "Thermic"),
    ("Ht", "Hyperthermic"),
    ("If", "Isofrigid"),
    ("Im", "Isomesic"),
    ("It", "Isothermic"),
    ("Ih", "Isohyperthermic")
]   
CULTIVATION_TYPE = [
    ("nd", "no data"),
    ("ACP", "Simultaneous agroforestry system with trees and perennial crops"),
    ("ACA", "Simultaneous agroforestry system with trees and annual crops"),
    ("ACB", "Simultaneous agroforestry system with trees, perennial and annual crops"),
    ("AGG", "Simultaneous agroforestry system with trees and grassland"),
    ("ACG", "Simultaneous agroforestry system with trees, crops and grassland"),
    ("GNP", "Pasture on (semi-)natural vegetation"),
    ("GIP", "Intensively-managed grassland, pastured"),
    ("GIN", "Intensively-managed grassland, not pastured"),
    ("CPP", "Perennial crop production (e.g. food, fodder, fuel, fiber, ornamental plants)"),
    ("CPA", "Annual crop production (e.g. food, fodder, fuel, fiber, ornamental plants)"),
    ("FYO", "Fallow, less than 12 months, with spontaneous vegetation"),
    ("FOL", "Fallow, at least 12 months, with spontaneous vegetation"),
    ("FDF", "Fallow, all plants constantly removed (dry farming)")
]
PROD_TECHNIQUES = [
    ("nd", "no data"),
    ("DC", "Drainage by open canals"),
    ("DU", "Underground drainage"),
    ("CW", "Wet cultivation"),
    ("IR", "Irrigation"),
    ("RB", "Raised beds"),
    ("HT", "Human-made terraces"),
    ("LO", "Local raise of land surface"),
    ("OT", "Other"),
    ("NO", "None")
]
USES = [
    ("AA", "Annual field cropping"),
    ("AA1", "Fallow system cultivation"),
    ("AA2", "Ley system cultivation"),
    ("AA3", "Rainfed arable cultivation"),
    ("AA4", "Shifting cultivation"),
    ("AA5", "Wet rice cultivation"),
    ("AA6", "Irrigated cultivation"),
    ("AP", "Perennial field cropping"),
    ("AP1", "Non-irrigated cultivation"),
    ("AP2", "Irrigated cultivation"),
    ("AT", "Tree and shrub cropping"),
    ("AT1", "Non-irrigated tree crop cultivation"),
    ("AT2", "Irrigated tree crop cultivation"),
    ("AT3", "Non-irrigated shrub crop cultivation"),
    ("AT4", "Irrigated shrub crop cultivation"),
    ("MF", "Agroforestry"),
    ("MP", "Agropastoralism"),
    ("HE", "Extensive grazing"),
    ("HE1", "Nomadism"),
    ("HE2", "Semi-nomadism"),
    ("HE3", "Ranching"),
    ("HI", "Intensive grazing"),
    ("HI1", "Animal production"),
    ("HI2", "Dairyng"),
    ("FN", "Natural forest and woodland"),
    ("FN1", "Selective felling"),
    ("FN2", "Clear felling"),
    ("FP", "Plantation forestry"),
    ("PN", "Nature and game preservation"),
    ("PN1", "Reserves"),
    ("PN2", "Parks"),
    ("PN3", "Wildfire management"),
    ("PD", "Degradation control"),
    ("PD1", "Without interface"),
    ("PD2", "With interface"),
    ("SR", "Residential Use"),
    ("SI", "Industrial Use"),
    ("ST", "Transport"),
    ("SC", "Recreational Use"),
    ("SX", "Excavations"),
    ("SD", "Disposal sites"),
    ("nd", "no data"),
    ("A", "Crop agriculture (cropping)"),
    ("M", "Mixed farming"),
    ("H", "Animal husbandry"),
    ("F", "Forestry"),
    ("P", "Natural protection"),
    ("S", "Settlement, Industry"),
    ("Y", "Military area"),
    ("O", "Other land uses"),
    ("U", "Not used and not managed")
]
CORINE = [
    ("1", "Artificial areas."),   
    ("11" , "Urban fabric Areas"),
    ("111", "Continuous urban fabric"),
    ("112", "Discontinuous urban fabric"),
    ("12"  , "Industrial, commercial and transport units"),
    ("121", "Industrial or commercial units and public facilities"),
    ("122", "Road and rail networks"),
    ("123", "Port areas"),
    ("124", "Airports"),
    ("13"  , "Mine, dump and construction sites"),
    ("131", "Mineral extraction sites"),
    ("132", "Dump sites."),
    ("133", "Construction sites."),
    ("14"  , "Artificial non-agricultural vegetated areas."),
    ("141", "Green urban areas"),
    ("142", "Sport and leisure facilities"),
    ("2"    , "Agricultural areas"),
    ("21"  , "Arable land"),
    ("211", "Non-irrigated arable land"),
    ("212", "Permanently irrigated arable land"),
    ("213", "Rice fields"),
    ("22"  , "Permanent crops"),
    ("221", "Vineyards"),
    ("222", "Fruit tree and berry plantations"),
    ("223", "Olive groves"),
    ("23"  , "Pastures"),
    ("231", "Pastures, meadows and other permanent grasslands"),
    ("24"  , "Heterogeneous agricultural areas"),
    ("241", "Annual crops associated with permanent crops"),
    ("242", "Complex cultivation patterns"),
    ("243", "Land principally occupied by agriculture"),
    ("244", "Agro-forestry areas"),
    ("3" , "Forest and semi-natural areas"), 
    ("31"  , "Forests"),
    ("311", "Broad-leaved forest"),
    ("312", "Coniferous forest"),
    ("313", "Mixed forest"),
    ("32"  , "Shrubs and/or herbaceous vegetation associations"),
    ("321", "Natural grassland"),
    ("322", "Moors and heathland"),
    ("323", "Sclerophyllous vegetation"),
    ("324", "Transitional woodland/shrub"),
    ("33"  , "Open spaces with little or no vegetation"),
    ("331", "Beaches, dunes, and sand plains"),
    ("332", "Bare rock"),
    ("333", "Sparsely vegetated areas"),
    ("334", "Burnt areas"),
    ("335", "Glaciers and perpetual snow"),
    ("4"    , "Wetlands"), 
    ("41"  , "Inland wetlands"),
    ("411", "Inland marshes"),
    ("412", "Peat bogs"),
    ("42"  , "Coastal wetland"),
    ("421", "Coastal salt marshes"),
    ("422", "Salines"),
    ("423", "Intertidal flats"),
    ("5"    , "Water bodies."),
    ("51"  , "Inland waters"),
    ("511", "Water courses"),
    ("512", "Water bodies"),
    ("52"  , "Marine waters"),
    ("521", "Coastal lagoons"),
    ("522", "Estuaries"),
    ("523", "Sea and ocean") 
]    
VEGETATION_TYPES = [
    ("nd", "life_form: no data; description: no data"),
    ("AF", "life_form: Aquatic; description: Algae: fresh or brackish"),
    ("AM", "life_form: Aquatic; description: Algae: marine"),
    ("AH", "life_form: Aquatic; description: Higher aquatic plants (woody or non-woody)"),
    ("CR", "life_form: Surface crusts; description: Biological crust (of cyanobacteria, algae, fungi, lichens and/or mosses)"),
    ("NF", "life_form: Terrestrial non-woody plants; description: Fungi"),
    ("NL", "life_form: Terrestrial non-woody plants; description: Lichens"),
    ("NM", "life_form: Terrestrial non-woody plants; description: Mosses (non-peat)"),
    ("NP", "life_form: Terrestrial non-woody plants; description: Peat"),
    ("NG", "life_form: Terrestrial non-woody plants; description: Grasses and/or herbs"),
    ("WH", "life_form: Terrestrial woody plants; description: Heath or dwarf shrubs"),
    ("WG", "life_form: Terrestrial woody plants; description: Evergreen shrubs"),
    ("WS", "life_form: Terrestrial woody plants; description: Seasonally green shrubs"),
    ("WE", "life_form: Terrestrial woody plants; description: Evergreen trees (mainly not planted)"),
    ("WT", "life_form: Terrestrial woody plants; description: Seasonally green trees (mainly not planted)"),
    ("WP", "life_form: Terrestrial woody plants; description: Plantation forest, not in rotation with cropland or grassland"),
    ("WR", "life_form: Terrestrial woody plants; description: Plantation forest, in rotation with cropland or grassland"),
    ("NO", "life_form: None (barren); description: Water, rock, or soil surface with < 0.5% vegetation cover")
]
STRATUM = [
    ("nd", "no data"),
    ("GS", "Ground stratum"),
    ("MS", "Mid-stratum"),
    ("US", "Upper stratum")
]
GROUND_FORMS = [
    ("nd", "no data"),
    ("R", "Rings"),
    ("P", "Polygons"),
    ("S", "Stripes"),
    ("N", "None")
]
TECH_ALTERATIONS = [
    ("nd", "no data"),
    ("SC", "Sealing by concrete"),
    ("SA", "Sealing by asphalt"),
    ("SO", "Other types of sealing"),
    ("TR", "Topsoil removal"),
    ("LV", "Levelling"),
    ("OT", "Other"),
    ("NO", "None")
]
PARENT_MATERIALS = [
    ("I", "Igneous Rock"),
    ("IF", "Igneous Rock/Felsic igneous"),
    ("IF1", "Igneous Rock/Felsic igneous/Granite"),
    ("IF2", "Igneous Rock/Felsic igneous/Quartz-diorite"),
    ("IF3", "Igneous Rock/Felsic igneous/Grano-diorite"),
    ("IF4", "Igneous Rock/Felsic igneous/Diorite"),
    ("IF5", "Igneous Rock/Felsic igneous/Rhyolite"),
    ("II", "Igneous Rock/Intermediate igneous"),
    ("II1", "Igneous Rock/Intermediate igneous/Andesite, trachyte, phonolite"),
    ("II2", "Igneous Rock/Intermediate igneous/Diorite-syenite"),
    ("IM", "Igneous Rock/Mafic igneous"),
    ("IM1", "Igneous Rock/Mafic igneous/Gabbro"),
    ("IM2", "Igneous Rock/Mafic igneous/Basalt"),
    ("IM3", "Igneous Rock/Mafic igneous/Dolerite"),
    ("IU", "Igneous Rock/Ultramafic igneous"),
    ("IU1", "Igneous Rock/Ultramafic igneous/Peridotite"),
    ("IU2", "Igneous Rock/Ultramafic igneous/Peridotite"),
    ("IU3", "Igneous Rock/Ultramafic igneous/Serpentinite"),
    ("IP", "Igneous Rock/Pyroclastic"),
    ("IP1", "Igneous Rock/Pyroclastic/Tuff, tuffite"),
    ("IP2", "Igneous Rock/Pyroclastic/Volcanic scoria/breccia"),
    ("IP3", "Igneous Rock/Pyroclastic/Volcanic ash"),
    ("IP4", "Igneous Rock/Pyroclastic/Ignimbrite"),
    ("MF", "Metamorphic rock/Felsic metamorphic"),
    ("MF1", "Metamorphic rock/Felsic metamorphic/Quartzite"),
    ("MF2", "Metamorphic rock/Felsic metamorphic/Gneiss, migmatite"),
    ("MF3", "Metamorphic rock/Felsic metamorphic/Slate, phyllite (pelitic rocks)"),
    ("MF4", "Metamorphic rock/Felsic metamorphic/Schist"),
    ("MM", "Metamorphic rock/Mafic metamorphic"),
    ("MM1", "Metamorphic rock/Mafic metamorphic/Slate, phyllite (pelitic rocks)"),
    ("MM2", "Metamorphic rock/Mafic metamorphic/(Green)schist"),
    ("MM3", "Metamorphic rock/Mafic metamorphic/Gneiss rich in Fe-Mg minerals"),
    ("MM4", "Metamorphic rock/Mafic metamorphic/Metamorphic limestone (marble)"),
    ("MM5", "Metamorphic rock/Mafic metamorphic/Amphibolite"),
    ("MM6", "Metamorphic rock/Mafic metamorphic/Eclogite"),
    ("MU", "Metamorphic rock/Ultramafic metamorphic"),
    ("MU1", "Metamorphic rock/Ultramafic metamorphic/Serpentinite, greenstone"),
    ("SC", "Sedimentary rock (consolidated)/Clastic sediments"),
    ("SC1", "Sedimentary rock (consolidated)/Clastic sediments/Conglomerate, breccia"),
    ("SC2", "Sedimentary rock (consolidated)/Clastic sediments/Sandstone, greywacke, arkose"),
    ("SC3", "Sedimentary rock (consolidated)/Clastic sediments/Silt-, mud-, claystone"),
    ("SC4", "Sedimentary rock (consolidated)/Clastic sediments/Shale"),
    ("SC5", "Sedimentary rock (consolidated)/Clastic sediments/Ironstone"),
    ("SO", "Sedimentary rock (consolidated)/Carbonatic, organic"),
    ("SO1", "Sedimentary rock (consolidated)/Carbonatic, organic/Limestone, other carbonate rock"),
    ("SO2", "Sedimentary rock (consolidated)/Carbonatic, organic/Marl and other mixtures"),
    ("SO3", "Sedimentary rock (consolidated)/Carbonatic, organic/Coals, bitumen and related rocks"),
    ("SE", "Sedimentary rock (consolidated)/Evaporites"),
    ("SE1", "Sedimentary rock (consolidated)/Evaporites/Anhydrite, gypsum"),
    ("SE2", "Sedimentary rock (consolidated)/Evaporites/Halite"),
    ("UR", "Sedimentary rock (unconsolidated)/Weathered residuum"),
    ("UR1", "Sedimentary rock (unconsolidated)/Weathered residuum/Bauxite, laterite"),
    ("UF", "Sedimentary rock (unconsolidated)/Fluvial"),
    ("UF1", "Sedimentary rock (unconsolidated)/Fluvial/Sand and gravel"),
    ("UF2", "Sedimentary rock (unconsolidated)/Fluvial/Clay, silt and loam"),
    ("UL", "Sedimentary rock (unconsolidated)/Lacustrine"),
    ("UL1", "Sedimentary rock (unconsolidated)/Lacustrine/Sand"),
    ("UL2", "Sedimentary rock (unconsolidated)/Lacustrine/Silt and clay, < 20% CaCO3 equivalent, little or no diatoms"),
    ("UL3", "Sedimentary rock (unconsolidated)/Lacustrine/Silt and clay, < 20% CaCO3 equivalent, many diatoms"),
    ("UL4", "Sedimentary rock (unconsolidated)/Lacustrine/Silt and clay, ≥ 20% CaCO3 equivalent (marl)"),
    ("UM", "Sedimentary rock (unconsolidated)/Marine, estuarine"),
    ("UM1", "Sedimentary rock (unconsolidated)/Marine, estuarine/Sand"),
    ("UM2", "Sedimentary rock (unconsolidated)/Marine, estuarine/Clay and silt"),
    ("UC", "Sedimentary rock (unconsolidated)/Colluvial"),
    ("UC1", "Sedimentary rock (unconsolidated)/Colluvial/Slope deposits"),
    ("UC2", "Sedimentary rock (unconsolidated)/Colluvial/Lahar"),
    ("UC3", "Sedimentary rock (unconsolidated)/Colluvial/Deposit of soil material"),
    ("UE", "Sedimentary rock (unconsolidated)/Aeolian"),
    ("UE1", "Sedimentary rock (unconsolidated)/Aeolian/Loess"),
    ("UE2", "Sedimentary rock (unconsolidated)/Aeolian/Sand"),
    ("UG", "Sedimentary rock (unconsolidated)/Glacial"),
    ("UG1", "Sedimentary rock (unconsolidated)/Glacial/Moraine"),
    ("UG2", "Sedimentary rock (unconsolidated)/Glacial/Glacio-fluvial sand"),
    ("UG3", "Sedimentary rock (unconsolidated)/Glacial/Glacio-fluvial gravel"),
    ("UK", "Sedimentary rock (unconsolidated)/Cryogenic"),
    ("UK1", "Sedimentary rock (unconsolidated)/Cryogenic/Periglacial rock debris"),
    ("UK2", "Sedimentary rock (unconsolidated)/Cryogenic/Periglacial solifluction layer"),
    ("UO", "Sedimentary rock (unconsolidated)/Organic"),
    ("UO1", "Sedimentary rock (unconsolidated)/Organic/Rainwater-fed peat (bog)"),
    ("UO2", "Sedimentary rock (unconsolidated)/Organic/Groundwater-fed peat (fen)"),
    ("UO3", "Sedimentary rock (unconsolidated)/Organic/Lacustrine (organic limnic sediments)"),
    ("UA", "Sedimentary rock (unconsolidated)/Anthropogenic, technogenic"),
    ("UA1", "Sedimentary rock (unconsolidated)/Anthropogenic, technogenic/Redeposited natural material"),
    ("UA2", "Sedimentary rock (unconsolidated)/Anthropogenic, technogenic/Industrial/artisanal deposits"),
    ("UU", "Sedimentary rock (unconsolidated)/Unspecified deposits"),
    ("UU1", "Sedimentary rock (unconsolidated)/Unspecified deposits/Clay"),
    ("UU2", "Sedimentary rock (unconsolidated)/Unspecified deposits/Loam and silt"),
    ("UU3", "Sedimentary rock (unconsolidated)/Unspecified deposits/Sand"),
    ("UU4", "Sedimentary rock (unconsolidated)/Unspecified deposits/Gravelly sand"),
    ("UU5", "Sedimentary rock (unconsolidated)/Unspecified deposits/Gravel, broken rock"),
    ("nd", "no data"),
    ("M", "Metamorphic rock"),
    ("S", "Sedimentary rock (consolidated)"),
    ("U", "Sedimentary rock (unconsolidated)")
]
WATER_ABOVE = [
    ("MP", "Permanently submerged by seawater (below mean low water springs)"),
    ("MT", "Tidal area (between mean low and mean high water springs)"),
    ("MO", "Occasional storm surges (above mean high water springs)"),
    ("FP", "Permanently submerged by inland water"),
    ("FF", "Submerged by remote flowing inland water at least once a year"),
    ("FO", "Submerged by remote flowing inland water less than once a year"),
    ("GF", "Submerged by rising local groundwater at least once a year"),
    ("GO", "Submerged by rising local groundwater less than once a year"),
    ("RF", "Submerged by local rainwater at least once a year"),
    ("RO", "Submerged by local rainwater less than once a year"),
    ("UF", "Submerged by inland water of unknown origin at least once a year"),
    ("UO", "Submerged by inland water of unknown origin less than once a year"),
    ("NO", "None of the above"),
    ("nd", "No Data"),
    ("R", "Water stands for ≥ 60 seconds"),
    ("N", "Water infiltrates completely within < 60 seconds")
]
DRAINAGE_CONDITIONS = [
    ("nd", "no data"),
    ("ED", "Excessively drained"),
    ("SED", "Somewhat excessively drained"),
    ("WD", "Well drained"),
    ("MWD", "Moderately well drained"),
    ("SPD", "Somewhat poorly drained"),
    ("PD", "Poorly drained"),
    ("VPD", "Very poorly drained"),
    ("SA", "Subaqueous")
]
WATER_REPELLENCE = [
    ("nd", "No Data"),
    ("R", "Water stands for ≥ 60 seconds"),
    ("N", "Water infiltrates completely within < 60 seconds")
]
WIDTH_TYPES = [
    ("nd", "width_cm: no data; description: no data"),
    ("VF", "width_cm: ≤ 1; description: Very fine"),
    ("FI", "width_cm: > 1 - 2; description: Fine"),
    ("ME", "width_cm: > 2 - 5; description: Medium"),
    ("WI", "width_cm: > 5 - 10; description: Wide"),
    ("VW", "width_cm: > 10; description: Very wide"),
    ("NO", "width_cm: none; description: No surface cracks")
]
DISTANCE_TYPES = [
    ("nd", "distance_cm: no data; description: no data"),
    ("TI", "distance_cm: ≤ 0.5; description: Tiny"),
    ("VS", "distance_cm: > 0.5 - 2; description: Very small"),
    ("SM", "distance_cm: > 2 - 5; description: Small"),
    ("ME", "distance_cm: > 5 - 20; description: Medium"),
    ("LA", "distance_cm: > 20 - 50; description: Large"),
    ("VL", "distance_cm: > 50 -200; description: Very large"),
    ("HU", "distance_cm: > 200 - 500; description: Huge"),
    ("VH", "distance_cm: > 500; description: Very huge")
]
ARRANGEMENT = [
    ("P", "Polygonal"),
    ("N", "Non-polygonal"),
    ("nd", "No Data"),
    ("R", "Reversible (open and close with changing moisture, e.g., in Vertisols and in soils with the Vertic or the Protovertic qualifier)"),
    ("I", "Irreversible (persist year-round, e.g., drained polder cracks, cracks in cemented layers)")
]
PERSISTENCE = [
    ("nd", "No Data"),
    ("R", "Reversible (open and close with changing moisture, e.g., in Vertisols and in soils with the Vertic or the Protovertic qualifier)"),
    ("I", "Irreversible (persist year-round, e.g., drained polder cracks, cracks in cemented layers)")
]
PROFILE_POSITION = [
    ("nd", "no data"),
    ("H", "On the high"),
    ("S", "On the slope"),
    ("L", "In the low"),
    ("E", "On an unaffected surface")
]
EROSION_ACTIVITY = [
    ("nd", "no data"),
    ("PR", "Active at present"),
    ("RE", "Active in recent past (within the last 100 years)"),
    ("HI", "Active in historical times"),
    ("NK", "Period of activity not known")
]
EROSION_DEGREE = [
    ("nd", "degree: no data; description: no data"),
    ("S", "degree: Slight; description: Some evidence of damage to surface layers, original ecological functions largely intact"),
    ("M", "degree: Moderate; description: Clear evidence of removal of surface layers, original ecological functions partly destroyed"),
    ("V", "degree: Severe; description: Surface layers completely removed and subsurface layers exposed, original ecological functions largely destroyed"),
    ("E", "degree: Extreme; description: Substantial removal of deeper subsurface layers, original ecological functions fully destroyed (badlands)")
]
EROSION_TYPE = [
    ("WS", "Sheet erosion"),
    ("WR", "Rill erosion"),
    ("WG", "Gully erosion"),
    ("WT", "Tunnel erosion"),
    ("AS", "Shifting sands"),
    ("AO", "Other types of wind erosion"),
    ("nd", "no data"),
    ("W", "Water erosion"),
    ("A", "Aeolian (wind) erosion"),
    ("WA", "Water and aeolian (wind) erosion"),
    ("MM", "Mass movement (landslides and similar phenomena)"),
    ("NC", "Erosion, not categorized"),
    ("NO", "No evidence of erosion")
]
HUMAN_MADE_TYPE = [
    ("nd", "no data"),
    ("HT", "Human-made terraces"),
    ("RB", "Raised beds"),
    ("EL", "Other longitudinal elevations"),
    ("EP", "Polygonal elevations"),
    ("ER", "Rounded elevations"),
    ("CD", "Drainage canals"),
    ("CI", "Irrigation canals"),
    ("CO", "Other canals"),
    ("HP", "Polygonal holes"),
    ("HR", "Rounded holes"),
    ("OT", "Other"),
    ("NO", "None")
]
NATURAL_TYPE = [
    ("nd", "no data"),
    ("P", "Unevenness caused by permafrost (palsa, pingo, mud boils, thufurs etc.)"),
    ("G", "Unevenness caused by shrink-swell clays (gilgai relief)"),
    ("O", "Other"),
    ("N", "None")
]
SURVEY_METHODS = [
    ("nd", "No Data"),
    ("US52", "method: USDA soil survey manual ; year: 1952"),
    ("US62", "method: USDA soil survey manual ; year: 1962"),
    ("US75", "method: USDA soil survey manual ; year: 1975"),
    ("US93", "method: USDA soil survey manual ; year: 1993"),
    ("US18", "method: USDA soil survey manual ; year: 2018"),
    ("FA52", "method: FAO; year: 1952"),
    ("FA77", "method: FAO; year: 1977"),
    ("FA90", "method: FAO; year: 1990"),
    ("FA06", "method: FAO; year: 2006"),
    ("WR22", "method: WRB; year: 2022"),
    ("US", "method: USDA soil survey manual ; year:NULL"),
    ("FA", "method: FAO ; year:NULL"),
    ("WR", "method: WRB; year:NULL"),
    ("CP", "method: CPCS; year:NULL"),
    ("OTH", "method: OTHER; year:NULL"),
    ("UN", "method: UNKNOWN; year:NULL")
]
CLASSIFICATION_SYSTEMS = [
    ("nd", "No Data"),
    ("US60", "class_sys: USDA; year:1960"),
    ("US75", "class_sys: USDA; year:1975"),
    ("US90", "class_sys: USDA; year:1990"),
    ("US91", "class_sys: USDA; year:1991"),
    ("US94", "class_sys: USDA; year:1994"),
    ("US98", "class_sys: USDA; year:1998"),
    ("US99", "class_sys: USDA; year:1999"),
    ("US06", "class_sys: USDA; year:2006"),
    ("US10", "class_sys: USDA; year:2010"),
    ("US14", "class_sys: USDA; year:2014"),
    ("US22", "class_sys: USDA; year:2022"),
    ("FA67", "class_sys: FAO; year:1967"),
    ("FA74", "class_sys: FAO; year:1974"),
    ("FA85", "class_sys: FAO; year:1985"),
    ("FA88", "class_sys: FAO; year:1988"),
    ("FA94", "class_sys: FAO; year:1994"),
    ("WR98", "class_sys: WRB; year:1998"),
    ("WR06", "class_sys: WRB; year:2006"),
    ("WR15", "class_sys: WRB; year:2015"),
    ("WR22", "class_sys: WRB; year:2022"),
    ("RP95", "class_sys: Referentiel Pedologique; year:1995"),
    ("RP08", "class_sys: Referentiel Pedologique; year:2008"),
    ("US", "class_sys: USDA; year:NULL"),
    ("FA", "class_sys: FAO ; year:NULL"),
    ("WR", "class_sys: WRB; year:NULL"),
    ("CP", "class_sys: CPCS; year:NULL"),
    ("RP", "class_sys: Referentiel Pedologique; year:NULL"),
    ("KU", "class_sys: KUBIENA; year:NULL"),
    ("OTH", "class_sys: OTHER; year:NULL"),
    ("UN", "class_sys: UNKNOWN; year:NULL")
]

#LabData
MN_ZN_CU_METHODS = [
    ("nd", "No Data"),
    ("UN", "Unknown method"),
    ("OTH", "Other method"),
    ("EF", "EDTA, FAAS"),
    ("DF", "DTPA, FAAS")
]
N_CONTENT_METHODS = [
    ("nd", "No Data"),
    ("UN", "Unknown method"),
    ("OTH", "Other method"),
    ("KJ", "Kjeldahl"),
    ("EA", "Elemental analyzer"),
    ("CA", "Coleman nitrogen analyzer")
]
ORGANIC_CARBON_METHODS = [
    ("nd", "No Data"),
    ("UN", "Unknown method"),
    ("OTH", "Other method"),
    ("WB", "Sieving"),
    ("EA", "Hydrometer method"),
    ("SK", "Springer & Klee")
]
ORGANIC_MATTER_CONTENT_METHODS = [
    ("nd", "No Data"),
    ("UN", "Unknown method"),
    ("OTH", "Other method"),
    ("MF", "Muffle")
]
P_CONTENT_METHODS = [
    ("nd", "No Data"),
    ("UN", "Unknown method"),
    ("OTH", "Other method"),
    ("BR", "Bray"),
    ("MN", "Mehlich No.3"),
    ("OL", "Olsen")
]
G_CLASSIFICATION_SYSTEMS = [
    ("U", "USDA"),
    ("W", "WRB"),
    ("OT", "OTHER"),
    ("UN", "UNKNOWN")
]
SAND_CONTENT_METHODS = [
    ("BH" , "Hydrometer method"),
    ("PR" , "Pipette and gravimetric method"),
    ("LD" , "Laser diffraction"),
    ("SV" , "Sieving"),
    ("OTH" , "Other method"),
    ("UN" , "Unknown method")
]
SILT_CLAY_CONTENT_METHODS = [
    ("BH" , "Hydrometer method"),
    ("PR" , "Pipette and gravimetric method"),
    ("LD" , "Laser diffraction"),
    ("OTH" , "Other method"),
    ("UN" , "Unknown method")
]
CACO3_CONTENT_METHODS = [
    ("nd", "No Data"),
    ("UN", "Unknown method"),
    ("OTH", "Other method"),
    ("GV", "Calcimeter - Gas volumetric method"),
    ("GM", "Carbonate equivalent, Gravimetric method"),
    ("TM", "Titration method")
]
CEC_CA_MG_NA_K_METHODS = [
    ("nd", "No Data"),
    ("UN", "Unknown method"),
    ("OTH", "Other method"),
    ("BM", "BaCl2/MgSO4 method"),
    ("AA", "Ammonium Acetate (CH3COONH4)"),
    ("ME", "Mehlich Extraction")
]
EL_CONDUCTIVITY_PH_METHODS = [
    ("nd", "No Data"),
    ("UN", "Unknown method"),
    ("OTH", "Other method"),
    ("SP", "Saturated paste"),
    ("OP", "Soil to water 1:2.5"),
    ("OF", "Soil to water 1:5"),
    ("OO", "Soil to water 1:1"),
    ("OT", "Soil to water 1:2")
]
GYPSUM_CONTENT_METHODS = [
    ("nd", "No Data"),
    ("UN", "Unknown method"),
    ("OTH", "Other method"),
    ("FA", "Soluble Calcium, FAAS"),
    ("AT", "Acetone, EDTA titration (George Holmgren)")
]
HIDRAULIC_CONDUCTIVITY_METHODS = [
    ("nd", "No Data"),
    ("UN", "Unknown method"),
    ("OTH", "Other method"),
    ("IN", "Infiltrometer")
]
WILTING_POINT_METHODS = [
    ("PP" , "Pressure Plate Method"),
    ("OTH" , "Other method"),
    ("UN" , "Unknown method"),
    ("nd" , "No Data")
]
TEXTURE_CLASSES = [
    ("S", "class: Sand, sand:> 85, silt: < 15, clay:< 10"),
    ("LS", "class: Loamy sand, sand:> 70 to ≤ 90, silt: < 30, clay:< 15"),
    ("Si", "class: Silt, sand:≤ 20, silt: ≥ 80, clay:< 12"),
    ("SiL", "class: Silt loam, sand:≤ 50 -- ≤ 8, silt: ≥ 50 to < 80 -- ≥ 80 to < 88, clay:< 27 -- ≥ 12 to ≤ 20"),
    ("SL", "class: Sandy loam, sand:> 52 to ≤ 85 -- > 43 to ≤ 52, silt: ≤ 48 -- ≥ 41 to < 50, clay:< 20 -- < 7"),
    ("L", "class: Loam, sand:> 23 to ≤ 52, silt: ≥ 28 to < 50, clay:≥ 7 to < 27"),
    ("SCL", "class: Sandy clay loam, sand:> 45 to ≤ 80, silt: < 28, clay:≥ 20 to < 35"),
    ("SiCL", "class: Silty clay loam, sand:≤ 20, silt: > 40 to ≤ 73, clay:≥ 27 to < 40"),
    ("CL", "class: Clay loam, sand:> 20 to ≤ 45, silt: > 15 to < 53, clay:≥ 27 to < 40"),
    ("SC", "class: Sandy clay, sand:> 45 to ≤ 65, silt: < 20, clay:≥ 35 to < 55"),
    ("SiC", "class: Silty clay, sand:≤ 20, silt: ≥ 40 to ≤ 60, clay:≥ 40 to ≤ 60"),
    ("C", "class: Clay, sand:≤ 45, silt: < 40, clay:≥ 40")
]

#Layer
CEMENTING_AGENT = [
    ("CA", "Secondary carbonates"),
    ("GY", "Secondary gypsum"),
    ("SI", "Secondary silica"),
    ("FI", "Fe oxides, predominantly inside (former) soil aggregates, no significant concentration of organic matter"),
    ("FO", "Fe oxides, predominantly on the surfaces of (former) soil aggregates, no significant concentration of organic matter"),
    ("FN", "Fe oxides, no relationship to (former) soil aggregates, no significant concentration of organic matter"),
    ("FH", "Fe oxides in the presence of a significant concentration of organic matter"),
    ("F", "Fe oxides"),
    ("nd", "no data")
]
SIZE_SHAPE_TYPES = [
    ("GR", "Rounded"),
    ("GA", "Angular"),
    ("GB", "Rounded and angular"),
    ("GS", "Subrounded"),
    ("GF", "Flat"),
    ("FR", "Rounded"),
    ("FA", "Angular"),
    ("FB", "Rounded and angular"),
    ("FS", "Subrounded"),
    ("FF", "Flat"),
    ("MR", "Rounded"),
    ("MA", "Angular"),
    ("MB", "Rounded and angular"),
    ("MS", "Subrounded"),
    ("MF", "Flat"),
    ("CR", "Rounded"),
    ("CA", "Angular"),
    ("CB", "Rounded and angular"),
    ("CS", "Subrounded"),
    ("CF", "Flat"),
    ("SR", "Rounded"),
    ("SA", "Angular"),
    ("SB", "Rounded and angular"),
    ("SS", "Subrounded"),
    ("SF", "Flat"),
    ("BR", "Rounded"),
    ("BA", "Angular"),
    ("BB", "Rounded and angular"),
    ("BS", "Subrounded"),
    ("BF", "Flat"),
    ("LR", "Rounded"),
    ("LA", "Angular"),
    ("LB", "Rounded and angular"),
    ("LS", "Subrounded"),
    ("LF", "Flat"),
    ("F", "size: > 0.2 - 0.6, size_class: Fine gravel"),
    ("M", "size: > 0.2 - 0.6, size_class: Medium gravel"),
    ("C", "size: > 2 - 6, size_class: Coarse gravel"),
    ("S", "size: > 6 - 20, size_class: Stones"),
    ("B", "size: > 20 - 60, size_class: Boulders"),
    ("L", "size: > 60, size_class: Large boulders"),
    ("G", "size: > 0.2 - 6, size_class: gravel"),
    ("NO", "None"),
    ("nd", "no data")
]
WEATHERING_STAGE = [
    ("F", "weathering_stage: Fresh; description: No or little signs of weathering"),
    ("M", "weathering_stage: Moderately weathered; description: Loss of original rock colour and loss of crystal form in the outer parts; centres remain relatively fresh; original strength relatively well preserved"),
    ("S", "weathering_stage: Strongly weathered; description: All but the most resistant minerals weathered; original rock colour lost throughout; tend to disintegrate under only moderate pressure"),
    ("nd", "weathering_stage: no data; description: no data")
]
ARTEFACT_TYPES = [
    ("PO", "Processed oil products"),
    ("RU", "Rubber (tires etc.)"),
    ("BT", "Bitumen (asphalt), continuous"),
    ("BF", "Bitumen (asphalt), fragments"),
    ("BC", "Black carbon (e.g. charcoal, partly charred particles, soot)"),
    ("BS", "Boiler slag"),
    ("BA", "Bottom ash"),
    ("BR", "Bricks, adobes"),
    ("CE", "Ceramics"),
    ("CL", "Cloth, carpet"),
    ("CU", "Coal combustion byproducts"),
    ("CR", "Concrete, continuous"),
    ("CF", "Concrete, fragments"),
    ("CO", "Crude oil"),
    ("DE", "Debitage (stone tool flakes)"),
    ("DS", "Dressed or crushed stones"),
    ("FA", "Fly ash"),
    ("GM", "Geomembrane, continuous"),
    ("GF", "Geomembrane, fragments"),
    ("GL", "Glass"),
    ("GC", "Gold coins"),
    ("HW", "Household waste (undifferentiated)"),
    ("IW", "Industrial waste"),
    ("LL", "Lumps of applied lime"),
    ("ME", "Metal"),
    ("MS", "Mine spoil"),
    ("OW", "Organic waste"),
    ("PA", "Paper, cardboard"),
    ("PB", "Plasterboard"),
    ("PT", "Plastic"),
    ("TW", "Treated wood"),
    ("OT", "Other"),
    ("NO", "None"),
    ("nd", "no data")
]
ARTEFACT_SIZES = [
    ("E", "size_class: Fine earth; size: ≤ 0.2"),
    ("F", "size_class: Fine gravel; size: > 0.2 - 0.6"),
    ("M", "size_class: Medium gravel; size: > 0.6 - 2"),
    ("C", "size_class: Coarse gravel; size: > 2 - 6"),
    ("S", "size_class: Stones; size: > 6 - 20"),
    ("B", "size_class: Boulders; size: > 20 - 60"),
    ("L", "size_class: Large boulders; size: > 60"),
    ("nd", "size_class: no data; size: no data")
]
CRACKS_PERSISTENCE = [
    ("RT", "Reversible (open and close with changing soil moisture)"),
    ("IT", "Irreversible (persist year-round)"),
    ("NO", "No cracks"),
    ("nd", "no data")
]
CRACKS_CONTINUITY = [
    ("AC", "All cracks continue into the underlying layer"),
    ("HC", "At least half, but not all of the cracks continue into the underlying layer"),
    ("SC", "At least one, but less than half of the cracks continue into the underlying layer"),
    ("NC", "Cracks do not continue into the underlying layer"),
    ("nd", "no data")
]
LITHOGENIC_SIZES = [
    ("F", "class: Fine; size: > 2 - 6"),
    ("V", "class: Very fine; size: ≤ 2"),
    ("M", "class: Medium; size: > 6 - 20"),
    ("C", "class: Coarse; size: > 20"),
    ("nd", "class: no data; size: no data")
]   
REDOXIMORPHIC_SUBSTANCES = [
    ("FE", "Fe oxides"),
    ("MN", "Mn oxides"),
    ("FM", "Fe and Mn oxides"),
    ("JA", "Jarosite"),
    ("SM", "Schwertmannite"),
    ("AS", "Fe and Al sulfates (not specified)"),
    ("FS", "Fe sulfides"),
    ("NV", "No visible accumulation"),
    ("nd", "no data")
]
REDOXIMORPHIC_LOCATIONS = [
    ("OIM", "Inner parts, Inside soil aggregates: masses"),
    ("OIC", "Inner parts, Inside soil aggregates: concretions"),
    ("OIN", "Inner parts, Inside soil aggregates: nodules"),
    ("OIB", "Inner parts, Inside soil aggregates: both concretions and/or nodules (not possible to distinguish)"),
    ("OOA", "Outer parts, On surfaces of soil aggregates"),
    ("OOH", "Outer parts, Adjacent to surfaces of soil aggregates, infused into the matrix (hypocoats)"),
    ("OOE", "Outer parts, On biopore walls, lining the entire wall surface"),
    ("OON", "Outer parts, On biopore walls, not lining the entire wall surface"),
    ("OOI", "Outer parts, Adjacent to biopores, infused into the matrix (hypocoats)"),
    ("ORN", "Random (not associated with aggregate surfaces or pores), Distributed over the layer, no order visible"),
    ("ORS", "Random (not associated with aggregate surfaces or pores), Distributed over the layer, surrounding areas with reductimorphic features"),
    ("ORT", "Random (not associated with aggregate surfaces or pores), Throughout"),
    ("OM", "Mottles"),
    ("OI", "Inner parts, Inside soil aggregates"),
    ("OO", "Outer parts"),
    ("OR", "Random (not associated with aggregate surfaces or pores)"),
    ("nd", "no data")
]
OXIMORPHIC_SIZES = [
    ("VF", "class: Very fine; size: ≤ 2"),
    ("FI", "class: Fine; size: > 2 - 6"),
    ("ME", "class: Medium; size: > 6 - 20"),
    ("CO", "class: Coarse; size: > 20 - 60"),
    ("VC", "class: Very coarse; size: > 60"),
    ("nd", "class: no data; size: no data")
]
MOTTLES_BOUNDARY_TYPES = [
    ("S", "class: Sharp; size: < 0.5"),
    ("C", "class: Clear; size: 0.5 - 2"),
    ("D", "class: Diffuse; size: > 2"),
    ("nd", "class: no data; size: no data")
]
MOTTLES_CONTRAST = [
    ("F", "class: Faint; description: The mottles are evident only on close examination. Soil colours in both the matrix and mottles have closely related hues, chromas and value"),
    ("D", "class: Distinct; description: Although not striking, the mottles are readly seen. The hue, chroma and value of the matrix are easily distinguished from those of the mottles. They may vary by as much as 2.5 units of hue or several units in chroma or value"),
    ("P", "class: Prominent; description: The mottles are conspicuous and mottling is one of the outstanding features of the horizon. Hue, chroma and value alone or in combination are at least several units apart"),
    ("nd", "class: no data; description: no data")
]
OXIMORPHIC_CEMENTATION = [
    ("NC", "class: Not cemented; description: Intact specimen not obtainable or very slight force between fingers, < 8 N"),
    ("EWC", "class: Extremely weakly cemented; description: Slight force between fingers, 8 - < 20 N"),
    ("VWC", "class: Very weakly cemented; description: Moderate force between fingers, 20 - < 40 N"),
    ("WEC", "class: Weakly cemented; description: Strong force between fingers, 40 - < 80 N"),
    ("MOC", "class: Moderately or more cemented; description: Does not fail when applying force between fingers, ≥ 80 N"),
    ("nd", "class: no data; description: no data")
]
FORM_COATINGS = [
    ("C", "Continuous"),
    ("CI", "Continuous irregular (non-uniform, heterogeneous)"),
    ("DI", "Discontinuous irregular"),
    ("DE", "Dendroidal"),
    ("DC", "Discontinuous circular"),
    ("O", "Other"),
    ("nd", "no data")
]
ORGANIC_COATINGS = [
    ("C", "Cracked coatings on sand grains"),
    ("U", "Uncoated sand and/or coarse silt grains"),
    ("A", "All sand and coarse silt grains coated without cracks"),
    ("nd", "no data")
]
ABUNDANCE_PARTICLES_TYPES = [
    ("N", "class: None; description: 0"),
    ("F", "class: Few; description: > 0 - 5"),
    ("C", "class: Common; description: > 5 - 30"),
    ("M", "class: Many; description: > 30"),
    ("nd", "class: no data; description: no data")
]
TEXTURE_SUBCLASSES = [
    ("CS", "subclass: Coarse sand, feel:Grainy, very_coarse_sand: ≥ 25, medium_sand:< 50, sum: Not defined, fine_sand: < 50, very_fine_sand: < 50"),
    ("MS", "subclass: Medium sand, feel:Grainy, very_coarse_sand: < 25 -- ≥ 25, medium_sand:Not defined -- ≥ 50, sum: ≥ 25 -- Not defined, fine_sand: < 50 -- Not defined, very_fine_sand: < 50 -- Not defined"),
    ("FS", "subclass: Fine sand, feel:Grainy, very_coarse_sand: Not defined, medium_sand:Not defined, sum: Not defined -- < 25, fine_sand: ≥ 50 -- Not defined, very_fine_sand: Not defined -- < 50"),
    ("VFS", "subclass: Very fine sand, feel:Tending to be floury, very_coarse_sand: Not defined, medium_sand:Not defined, sum: Not defined, fine_sand: Not defined, very_fine_sand: ≥ 50"),
    ("LCS", "subclass: Loamy coarse sand, feel:Grainy, very_coarse_sand: ≥ 25, medium_sand:< 50, sum: Not defined, fine_sand: < 50, very_fine_sand: < 50"),
    ("LMS", "subclass: Loamy medium sand, feel:Grainy, very_coarse_sand: < 25 -- ≥ 25, medium_sand:Not defined -- ≥ 50, sum: ≥ 25 -- Not define, fine_sand: < 50 -- Not define, very_fine_sand: < 50 -- Not define"),
    ("LFS", "subclass: Loamy fine sand, feel:Grainy, very_coarse_sand: Not defined, medium_sand:Not defined, sum: Not defined -- < 25, fine_sand: ≥ 50 -- < 25, very_fine_sand: Not defined -- < 50"),
    ("LVFS", "subclass: Loamy very fine sand, feel:Tending to be floury, very_coarse_sand: Not defined, medium_sand:Not defined, sum: Not defined, fine_sand: Not defined, very_fine_sand: ≥ 50"),
    ("nd", "subclass: no data, feel:no data, very_coarse_sand: no data, medium_sand:no data, sum: no data, fine_sand: no data, very_fine_sand: no data")
]
RH_VALUE = [
    ("R6A", "processes: Strongly aerated; rh_value: > 33; description: No redoximorphic features"),
    ("R6D", "processes: Denitrification; rh_value: 29 - 33; description: No redoximorphic features"),
    ("R5", "processes: Redox reactions of Mn; rh_value: temporally 20 - 29; description: Oximorphic features of Mn; temporally no free oxygen present"),
    ("R4", "processes: Redox reactions of Fe; rh_value: temporally < 20; description: Oximorphic features of Fe"),
    ("R3", "processes: Formation of FeII/FeIII oxides (green rust); rh_value: 13 - 20; description: Blue-green to grey colour, Fe2+ ions always present (reduced areas show a positive alfa, alfa - dipyridyl test)"),
    ("R2", "processes: Sulfide formation; rh_value: 10 - 13; description: Black colour due to metal sulfides (spraying with a 10% HCl solution causes the formation of H2S)"),
    ("R1", "processes: Methane formation; rh_value: < 10; description: Flammable methane present"),
    ("nd", "processes: no data; rh_value: no data; description: no data")
]
POTENZIOMETRIC_MEASURES = [
    ("nd", "class: no data; solution: no data"),
    ("W11", "class: 1:1; solution: Distilled water (H2O)"),
    ("W15", "class: 1:5; solution: Distilled water (H2O)"),
    ("C15", "class: 1:5; solution: CaCl2, 0.01 M"),
    ("K15", "class: 1:5; solution: KCl, 1 M")
]
THIXOTROPY_NAF = [
    ("NF", "Positive NaF test"),
    ("TH", "Thixotropy"),
    ("NT", "Positive NaF test and thixotropy"),
    ("NO", "None of the above"),
    ("nd", "no data")
]
PACKING_DENSITIES = [
    ("VL", "class: Very loose; description: Knife penetrates completely even when applying low forces"),
    ("LO", "class: Loose; description: Knife penetrates completely when forces are applied"),
    ("IN", "class: Intermediate; description: Knife penetrates half when forces are applied"),
    ("FR", "class: Firm; description: Only the knifepoint penetrates when forces are applied"),
    ("VR", "class: Very firm; description: Knife does not (or only a little bit) penetrate when forces are applied"),
    ("nd", "class: no data; description: no data")
]
WIND = [
    ("CB", "Aeroturbation (cross-bedding)"),
    ("RH", "≥ 10% of the particles of medium sand or coarser are rounded or subangular and have a matt surface"),
    ("RC", "≥ 10% of the particles of medium sand or coarser are rounded or subangular and have a matt surface, but only in in-blown material that has filled cracks"),
    ("OT", "Other"),
    ("NO", "No evidence of wind deposition"),
    ("nd", "no data")
]
SHAPE_TYPES = [
    ("S", "shape: Smooth; description: Nearly plane surface"),
    ("W", "shape: Wavy; description: Pockets less deep than wide"),
    ("I", "shape: Irregular; description: Pockets more deep than wide"),
    ("B", "shape: Broken; description: Discontinuous"),
    ("nd", "shape: no data; description: no data")
]
BOUNDARIES = [
    ("V", "distinctness: Very Abrupt; mineral_organic: ≤ 0.5; terrestrial_organic: ≤ 0.1"),
    ("A", "distinctness: Abrupt; mineral_organic: > 0.5 - 2; terrestrial_organic: > 0.1 - 0.2"),
    ("C", "distinctness: Clear; mineral_organic: > 2 - 5; terrestrial_organic: > 0.2 - 0.5"),
    ("G", "distinctness: Gradual; mineral_organic: > 5 - 15; terrestrial_organic: > 0.5 - 1"),
    ("D", "distinctness: Diffuse; mineral_organic: > 15; terrestrial_organic: > 1"),
    ("U", "Unknow")
]
ORGANIC_MINERAL_TYPES = [
    ("OH", "Organic hydromorphic"),
    ("OT", "Organic terrestrial"),
    ("TH", "Organotechnic hydromorphic"),
    ("TT", "Organotechnic terrestrial"),
    ("MI", "Mineral"),
    ("nd", "no data")
]
WATER_STATUS = [
    ("VD", "moisture_class: Very dry; moistening: Going very dark; crushing: Dusty or hard"),
    ("DR", "moisture_class: Dry; moistening: Going dark; crushing: Makes no dust"),
    ("SM", "moisture_class: Slightly moist; moistening: Going slightly dark; crushing: Makes no dust"),
    ("MO", "moisture_class: Moist; moistening: No change of colour; crushing: Makes no dust"),
    ("WE", "moisture_class: Wet; moistening: No change of colour; crushing: Drops of water"),
    ("nd", "moisture_class: no data; moistening: no data; crushing: no data")
]
WATER_SATURATION = [
    ("GF", "Saturated by groundwater or flowing water for ≥ 30 consecutive days with water that has an electrical conductivity of < 4 dS m-1"),
    ("GS", "Saturated by groundwater or flowing water for ≥ 30 consecutive days with water that has an electrical conductivity of ≥ 4 dS m-1"),
    ("MI", "Saturated by water from melted ice for ≥ 30 consecutive days"),
    ("MS", "Saturated by seawater for ≥ 30 consecutive days"),
    ("MT", "Saturated by seawater according to tidal changes"),
    ("NO", "None of the above"),
    ("PW", "Pure water, covered by floating organic material"),
    ("RA", "Saturated by rainwater for ≥ 30 consecutive days"),
    ("nd", "no data")
]
ALLUVIAL_TEPHRA = [
    ("A", "Layer is composed of two or more alluvial strata"),
    ("B", "Layer is composed of two or more alluvial strata containing tephra"),
    ("N", "Layer is not composed of different strata"),
    ("T", "Layer is composed of two or more tephra strata"),
    ("nd", "no data")
]
RIBBONLIKE_SUBSTANCES = [
    ("CC", "Clay minerals"),
    ("OO", "Fe oxides and/or Mn oxides"),
    ("HH", "Organic matter"),
    ("CO", "Clay minerals and Fe oxides and/or Mn oxides"),
    ("CH", "Clay minerals and organic matter"),
    ("OH", "Fe oxides and/or Mn oxides and organic matter"),
    ("TO", "Clay minerals, Fe oxides and/or Mn oxides and organic matter"),
    ("NO", "No ribbon-like accumulations"),
    ("nd", "no data")
]
CARBONATE_CONTENTS = [
    ("SL", "content: Slightly calcareous; description: Audible effervescence but not visible; mass: > 0 - 2"),
    ("MO", "content: Moderately calcareous; description: Visible effervescence; mass: > 2 - 10"),
    ("ST", "content: Strongly calcareous; description: Strong visible effervescence, bubbles form a low foam; mass: > 10 - 25"),
    ("EX", "content: Extremely calcareous; description: Extremely strong reaction, thick foam forms quickly; mass: > 25"),
    ("nd", "content: no data; description: no data; mass: no data"),
    ("NC", "content: Non-calcareous; description: No visible or audible effervescence; mass: 0")
]
RETARDED_REACTION = [
    ("I", "Reaction with 1 M HCl immediate"),
    ("H", "Reaction with 1 M HCl only after heating"),
    ("nd", "no data")
]
SECONDARY_CARBONATE_TYPES = [
    ("nd", "no data"),
    ("MA", "Masses (including spheroidal aggregations like white eyes (byeloglaska))"),
    ("NC", "Nodules and/or concretions"),
    ("FI", "Filaments (including continuous filaments like pseudomycelia)"),
    ("AS", "Coatings on soil aggregate surfaces or biopore walls"),
    ("UR", "Coatings on undersides of coarse fragments and of remnants of broken-up cemented layers"),
    ("NO", "No secondary carbonates")
]
GYPSUM_CONTENT_TYPES = [
    ("NG", "content: Non-gypsiferous; mass: O; conductivity: ≤ 1.8 dS m-1 in 10 g soil / 25 ml H2O or ≤ 0.18 dS m-1 in 10 g soil / 250 ml H2O"),
    ("SL", "content: Slightly gypsiferous; mass: > 0 - 5; conductivity: > 0.18 - ≤ 1.8 dS m-1 in 10 g soil / 250 ml H2O"),
    ("MO", "content: Moderately gypsiferous; mass: > 5 - 15; conductivity: > 1.8 dS m-1 in 10 g soil / 250 ml H2O"),
    ("ST", "content: Strongly gypsiferous; mass: > 15 - 60; conductivity: > 1.8 dS m-1 in 10 g soil / 250 ml H2O"),
    ("EX", "content: Extremely calcareous; mass: > 60; conductivity: > 1.8 dS m-1 in 10 g soil / 250 ml H2O"),
    ("nd", "content: no data; mass: no data; conductivity: no data")
]
SGYPSUM_TYPES = [
    ("CR", "Gypsum crystal intergrowths or nodules"),
    ("SC", "Soft concrections"),
    ("DP", "Disperse powdery gypsum"),
    ("FL", "Filaments (vermiform gypsum, pseudomycelia)"),
    ("OT", "Other"),
    ("nd", "no data")
]
MINERAL_SIZES = [
    ("V", "class: Very fine; size: < 2"),
    ("F", "class: Fine; size: 2 - 6"),
    ("M", "class: Medium; size: 6 - 20"),
    ("C", "class: Coarse; size: > 20"),
    ("nd", "class: no data; size: no data")
]
MINERAL_SHAPES = [
    ("R", "Very fine"),
    ("E", "Fine"),
    ("F", "Medium"),
    ("I", "Irregular"),
    ("A", "Angular"),
    ("nd", "no data")
]
SECONDARY_SILICA_TYPES = [
    ("DN", "Nodules (durinodes)"),
    ("CH", "Accumulations within a layer, cemented by secondary silica"),
    ("FC", "Remnants of a layer that has been cemented by secondary silica"),
    ("OT", "Other accumulations"),
    ("NO", "No secondary silica"),
    ("nd", "no data")
]
DNFC_SIZES = [
    ("VF", "class: Very fine; size: ≤ 0.5"),
    ("FI", "class: Fine; size: > 0.5 - 1"),
    ("ME", "class: Medium; size: > 1 - 2"),
    ("CO", "class: Coarse; size: > 2 - 6"),
    ("VC", "class: Very coarse; size: > 6"),
    ("nd", "class: no data; size: no data")
]
CEMENTING_AGENTS = [
    ("CA", "Secondary carbonates"),
    ("GY", "Secondary gypsum"),
    ("SI", "Secondary silica"),
    ("FI", "Fe oxides, predominantly inside (former) soil aggregates, no significant concentration of organic matter"),
    ("FO", "Fe oxides, predominantly on the surfaces of (former) soil aggregates, no significant concentration of organic matter"),
    ("FN", "Fe oxides, no relationship to (former) soil aggregates, no significant concentration of organic matter"),
    ("FH", "Fe oxides in the presence of a significant concentration of organic matter"),
    ("F", "Fe oxides"),
    ("nd", "no data")
]
CEMENTATION_CLASSES = [
    ("NOC", "class: Not cemented; description: Intact specimen not obtainable or very slight force between fingers, < 8 N"),
    ("EWC", "class: Extremely weakly cemented; description: Slight force between fingers, 8 - < 20 N"),
    ("VWC", "class: Very weakly cemented; description: Moderate force between fingers, 20 - < 40 N"),
    ("WEC", "class: Weakly cemented; description: Strong force between fingers, 40 - < 80 N"),
    ("MOC", "class: Moderately cemented; description: Moderate force between hands, 80 - < 160 N"),
    ("STC", "class: Strongly cemented; description: Foot pressure by full body weight, 160 - < 800 N"),
    ("VSC", "class: Very strongly cemented; description: Blow of < 3 J (3 J = 2 kg dropped 15 cm) and does not fail under foot pressure by full body weight (800 N)"),
    ("EXC", "class: Extremely strongly cemented; description: Blow of ≥ 3 J (3 J = 2 kg dropped 15 cm)"),
    ("nd", "class: no data; description: no data")
]
RRCLASSES_MOIST = [
    ("LO", "class: Loose; description: Intact specimen not obtainable"),
    ("VF", "class: Very friable; description: Very slight force between fingers, < 8 N"),
    ("FR", "class: Friable; description: Slight force between fingers, 8 - < 20"),
    ("FI", "class: Firm; description: Moderate force between fingers, 20 - < 40 N"),
    ("VI", "class: Very firm; description: Strong force between fingers, 40 - < 80 N"),
    ("EI", "class: Extremely firm; description: Moderate force between hands, 80 - < 160 N"),
    ("SR", "class: Slightly rigid; description: Foot pressure by full body weight, 160 - < 800 N"),
    ("RI", "class: Rigid; description: Blow of < 3 J (3 J = 2 kg dropped 15 cm) and does not fail under foot pressure by full body weight (800 N)"),
    ("VR", "class: Very rigid; description: Blow of ≥ 3 J (3 J = 2 kg dropped 15 cm)"),
    ("nd", "class: no data; description: no data")
]
RRCLASSES_DRY = [
    ("LO", "class: Loose; description: Intact specimen not obtainable"),
    ("SO", "class: Soft; description: Very slight force between fingers, < 8 N"),
    ("SH", "class: Slightly hard; description: Slight force between fingers, 8 - < 20"),
    ("MH", "class: Moderately hard; description: Moderate force between fingers, 20 - < 40 N"),
    ("HA", "class: Hard; description: Strong force between fingers, 40 - < 80 N"),
    ("VH", "class: Very hard; description: Moderate force between hands, 80 - < 160 N"),
    ("EH", "class: Extremely hard; description: Foot pressure by full body weight, 160 - < 800 N"),
    ("RI", "class: Rigid; description: Blow of < 3 J (3 J = 2 kg dropped 15 cm) and does not fail under foot pressure by full body weight (800 N)"),
    ("VR", "class: Very rigid; description: Blow of ≥ 3 J (3 J = 2 kg dropped 15 cm)"),
    ("nd", "class: no data; description: no data")
]
SUSCEPTIBILITY = [
    ("CW", "Cementation after repeated drying and wetting"),
    ("NO", "No cementation after repeated drying and wetting"),
    ("nd", "no data")
]
MANNER_FAILURE = [
    ("BR", "type: Brittle; description: Abruptly (pops or shatters)"),
    ("SD", "type: Semi-deformable; description: Before compression to one half the original thickness"),
    ("DF", "type: Deformable; description: After compression to one half the original thickness"),
    ("nd", "type: no data; description: no data")
]
PLASTICITY = [
    ("NP", "type: Non-plastic; description: Does not form a roll 6 mm in diameter, or if a roll is formed, it cannot support itself if held on end"),
    ("SP", "type: Slightly plastic; description: 6 mm diameter roll supports itself; 4 mm diameter roll does not"),
    ("MP", "type: Moderately plastic; description: 4 mm diameter roll supports itself; 2 mm diameter roll does not"),
    ("VP", "type: Very plastic; description: 2 mm diameter roll supports itself"),
    ("nd", "type: no data; description: no data")
]
STICKINESS = [
    ("NST", "type: Non-sticky; description: After release of pressure, pratically no soil material adheres to thumb and finger"),
    ("SST", "type: Slightly sticky; description: After pressure, soil material adheres to both thumb and finger but comes off one or the other rather cleany. It is not appreciably stretched when the digit are separated"),
    ("ST", "type: Sticky; description: After pressure, soil material adheres to both thumb and finger and tends to stretch somewhat and pull apart rather than pulling free from either digit"),
    ("VST", "type: Very sticky; description: After pressure, soil material adheres strongly to both thumb and finger and is decidedly stretched when they are separated"),
    ("nd", "type: no data; description: no data")
]
CRYOGENIC_ALTERATION = [
    ("IW", "Ice wedge"),
    ("IL", "Ice lens"),
    ("DB", "Disrupted lower layer boundary"),
    ("OI", "Organic involutions in a mineral layer"),
    ("MI", "Mineral involutions in an organic layer"),
    ("CF", "Separation of coarse material and fine material"),
    ("OT", "Other"),
    ("NO", "None"),
    ("nd", "no data")
]
PERMAFROST_TYPE = [
    ("I", "Massive ice, cementation by ice or readily visible ice crystals"),
    ("T", "Soil temperature of < 0 °C and insufficient water to form readily visible ice crystals"),
    ("N", "No permafrost"),
    ("nd", "no data"),
]
SEALING_AGENT = [
    ("PP", "Physical, permanent"),
    ("PD", "Physical, only when dry"),
    ("CC", "Chemical, by carbonates"),
    ("CG", "Chemical, by gypsum"),
    ("CR", "Chemical, by readily soluble salts"),
    ("CS", "Chemical, by silica"),
    ("BC", "Biological, by cyanobacteria"),
    ("BA", "Biological, by algae"),
    ("BF", "Biological, by fungi"),
    ("BL", "Biological, by lichens"),
    ("BM", "Biological, by mosses"),
    ("NO", "No crust present"),
    ("nd", "no data")
]
ACCUMULATION_TYPES = [
    ("BU", "Filled earthworm burrows"),
    ("KR", "Filled krotowinas"),
    ("CO", "Organic matter coatings at surfaces of soil aggregates and biopore walls (no visible other material in the coatings)"),
    ("BC", "Black carbon (e.g. charcoal, partly charred particles, soot)"),
    ("NO", "No visible accumulation of organic matter"),
    ("nd", "no data")
]
ROOT_ABUNDANCE_CLASSES = [
    ("N", "class: None; number<=2mm: 0; number<0.5mm: 0; number0.5to2mm: 0; number>2mm: 0; number2to5mm: 0; number>5mm: 0"),
    ("V", "class: Very few; number<=2mm: 1 - 5; number<0.5mm: 1 - 5; number0.5to2mm: 1 - 5; number>2mm: 1 - 2; number2to5mm: 1 - 2; number>5mm: 1 - 2"),
    ("F", "class: Few; number<=2mm: 6 - 10; number<0.5mm: 6 - 10; number0.5to2mm: 6 - 10; number>2mm: 3 - 5; number2to5mm: 3 - 5; number>5mm: 3 - 5"),
    ("C", "class: Common; number<=2mm: 11 - 20; number<0.5mm: 11 - 20; number0.5to2mm: 11 - 20; number>2mm: 6 - 10; number2to5mm: 6 - 10; number>5mm: 6 - 10"),
    ("M", "class: Many; number<=2mm: 21 - 50; number<0.5mm: 21 - 50; number0.5to2mm: 21 - 50; number>2mm: 11 - 20; number2to5mm: 11 - 20; number>5mm: 11 - 20"),
    ("A", "class: Abundant; number<=2mm: > 50; number<0.5mm: > 50; number0.5to2mm: > 50; number>2mm: > 20; number2to5mm: > 20; number>5mm: > 20"),
    ("nd", "class: no data; number<=2mm: no data; number<0.5mm: no data; number0.5to2mm: no data; number>2mm: no data; number2to5mm: no data; number>5mm: no data")
]
ANIMAL_ACTIVITY_TYPES = [
    ("W", "Worm activity"),
    ("M", "Mammal activity"),
    ("MO", "Open large burrows"),
    ("MI", "Infilled large burrows (krotovinas)"),
    ("B", "Bird activity"),
    ("BA", "Bones, feathers, sorted gravel of similar size"),
    ("WE", "Earthworm channels"),
    ("WC", "Worm casts"),
    ("I", "Insect activity"),
    ("IT", "Termite channels and nests"),
    ("IA", "Ant channels and nests"),
    ("IO", "Other insect activity"),
    ("BU", "Burrows (unspecified)"),
    ("NO", "No visible results of animal activity"),
    ("nd", "no data")
]
NATURAL_MATERIAL_TYPES = [
    ("OR", "Organic"),
    ("ML", "Mineral, > 2 mm"),
    ("MS", "Mineral, ≤ 2 mm"),
    ("NO", "No additions"),
    ("nd", "no data")
]
TEXTURE_CLASSES = [
    ("S", "class: Sand, sand:> 85, silt: < 15, clay:< 10"),
    ("LS", "class: Loamy sand, sand:> 70 to ≤ 90, silt: < 30, clay:< 15"),
    ("Si", "class: Silt, sand:≤ 20, silt: ≥ 80, clay:< 12"),
    ("SiL", "class: Silt loam, sand:≤ 50 -- ≤ 8, silt: ≥ 50 to < 80 -- ≥ 80 to < 88, clay:< 27 -- ≥ 12 to ≤ 20"),
    ("SL", "class: Sandy loam, sand:> 52 to ≤ 85 -- > 43 to ≤ 52, silt: ≤ 48 -- ≥ 41 to < 50, clay:< 20 -- < 7"),
    ("L", "class: Loam, sand:> 23 to ≤ 52, silt: ≥ 28 to < 50, clay:≥ 7 to < 27"),
    ("SCL", "class: Sandy clay loam, sand:> 45 to ≤ 80, silt: < 28, clay:≥ 20 to < 35"),
    ("SiCL", "class: Silty clay loam, sand:≤ 20, silt: > 40 to ≤ 73, clay:≥ 27 to < 40"),
    ("CL", "class: Clay loam, sand:> 20 to ≤ 45, silt: > 15 to < 53, clay:≥ 27 to < 40"),
    ("SC", "class: Sandy clay, sand:> 45 to ≤ 65, silt: < 20, clay:≥ 35 to < 55"),
    ("SiC", "class: Silty clay, sand:≤ 20, silt: ≥ 40 to ≤ 60, clay:≥ 40 to ≤ 60"),
    ("C", "class: Clay, sand:≤ 45, silt: < 40, clay:≥ 40")
]
SECONDARY_CARBONATE_TYPES = [
    ("nd", "no data"),
    ("MA", "Masses (including spheroidal aggregations like white eyes (byeloglaska))"),
    ("NC", "Nodules and/or concretions"),
    ("FI", "Filaments (including continuous filaments like pseudomycelia)"),
    ("AS", "Coatings on soil aggregate surfaces or biopore walls"),
    ("UR", "Coatings on undersides of coarse fragments and of remnants of broken-up cemented layers"),
    ("NO", "No secondary carbonates")
]
ALTERATIONS_TYPES = [
    ("PA", "Ploughing, annually"),
    ("PO", "Ploughing, at least once every 5 years"),
    ("PP", "Ploughing in the past, not ploughed since > 5 years"),
    ("PU", "Ploughing, unspecified"),
    ("RM", "Remodelled (e.g. single ploughing)"),
    ("LO", "Loosening"),
    ("CP", "Compaction, other than a plough pan"),
    ("SD", "Structure deterioration, other than by ploughing or remodelling"),
    ("OT", "Other"),
    ("NO", "No in-situ alteration"),
    ("nd", "no data")
]
AGGREGATE_FORMATION = [
    ("T", "New granular structure present throughout the layer"),
    ("P", "New granular structure present in places, but in other places the added or mixed materials and the previously present materials lie isolated from each other"),
    ("N", "No new granular structure present"),
    ("nd", "no data")
]
SUBDVISION_HORIZON = [
    ("SE", "type: Sharp-edged; description: Breaks into longitudinal pieces with sharp edges"),
    ("CO", "type: Compact; description: Breaks into longitudinal pieces with unsharp edges"),
    ("CR", "type: Crumbly; description: Breaks into crumbly pieces or breaks powdery"),
    ("nd", "type: no data; description: no data")
]
DEAD_PLANT_TYPES = [
    ("W", "Wood"),
    ("S", "Moss fibres"),
    ("O", "Other plants"),
    ("N", "No dead plant residues"),
    ("nd", "no data")
]
NONMATRIX_PORES_TYPES = [
    ("TU", "type: Tubular; description: Cylindrical and elongated voids; e.g., worm tunnels"),
    ("DT", "type: Dendritic Tubular; description: Cylindrical, elongated, branching voids; e.g., empty root channels"),
    ("VE", "type: Vesicular; description: Ovoid to spherical voids; e.g., solidified pseudomorphs of entrapped gas bubbles concentrated below a crust; most common in arid and semiarid environments and in permafrost soils"),
    ("IG", "type: Irregular; description: Non-connected cavities, chambers; e.g., vughs; various shapes"),
    ("OT", "type: Other; description: Pores not attributable to any of the previous classes"),
    ("NO", "type: No non-matrix pores; description: No non-matrix pores"),
    ("nd", "type: no data; description: no data")
]
PORE_SIZES = [
    ("VF", "class: Very Fine; area: 1 cm²; diameter: ≤ 1 mm"),
    ("FI", "class: Fine; area: 1 cm²; diameter: > 1 - 2 mm"),
    ("ME", "class: Medium; area: 1 dm²; diameter: > 2 - 5 mm"),
    ("CO", "class: Coarse; area: 1 dm²; diameter: > 5 - 10 mm"),
    ("VC", "class: Very Coarse; area: 1 m²; diameter: > 10 mm"),
    ("nd", "class: no data; area: no data; diameter: no data")
]
PORE_ABUNDANCE = [
    ("V", "class: Very Fine; number: ≤ 1"),
    ("F", "class: Few; number: > 1 - 3"),
    ("C", "class: Common; number: > 3 - 5"),
    ("M", "class: Many; number: > 5"),
    ("nd", "class: no data; number: no data")
]
STRUCTURE_LEVELS = [
    ("1", "First Level Structure Type 1"),
    ("2", "First Level Structure Type 2"),
    ("3", "First Level Structure Type 3"),
    ("4", "Second Level Structure Type 1.1"),
    ("5", "Second Level Structure Type 1.2"),
    ("6", "Second Level Structure Type 2.1"),
    ("7", "Second Level Structure Type 2.2"),
    ("8", "Second Level Structure Type 3.1"),
    ("9", "Second Level Structure Type 3.2"),
    ("10", "Third Level Structure Type 1.1.1"),
    ("11", "Third Level Structure Type 1.2.1"),
    ("12", "Third Level Structure Type 2.1.1"),
    ("13", "Third Level Structure Type 2.2.1"),
    ("14", "Third Level Structure Type 3.1.1"),
    ("15", "Third Level Structure Type 3.2.1"),   
]
STRUCTURE_TYPES = [
    ("GR", "type: Granular; formation: Soil aggregate structure, natural"),
    ("BS", "type: Subangular blocky; formation: Soil aggregate structure, natural"),
    ("BA", "type: Angular blocky; formation: Soil aggregate structure, natural"),
    ("LC", "type: Lenticular; formation: Soil aggregate structure, natural"),
    ("WE", "type: Wedge-shaped; formation: Soil aggregate structure, natural"),
    ("PR", "type: Prismatic; formation: Soil aggregate structure, natural"),
    ("CO", "type: Columnar; formation: Soil aggregate structure, natural"),
    ("PH", "type: Polyhedral; formation: Soil aggregate structure, natural"),
    ("FE", "type: Flat-edged; formation: Soil aggregate structure, natural"),
    ("PS", "type: Pseudosand/Pseudosilt; formation: Soil aggregate structure, natural"),
    ("PL", "type: Platy; formation: Soil aggregate structure, natural or resulting from artificial pressure"),
    ("SR", "type: Single grain; formation: No structural units, rock structure, inherited from the parent material"),
    ("MS", "type: Massive; formation: No structural units, soil structure, present when moist and changing into soil aggregate structure when dry"),
    ("M", "type: Massive; No structural units"),
    ("S", "type: Single grain;  No structural units"),
    ("SS", "type: Single grain; formation: No structural units, soil structure, resulting from soil-forming processes, like loss of organic matter and/or oxides and/or clay minerals or loss of stratification"),
    ("MR", "type: Massive; formation: No structural units, rock structure, inherited from the parent material, structure not changing with soil moisture, not or only slightly chemically weathered"),
    ("MW", "type: Massive; formation: No structural units, rock structure, inherited from the parent material, structure not changing with soil moisture, strongly chemically weathered (e.g. saprolite)"),
    ("ST", "type: Stratified; formation: No structural units, rock structure, visible stratification from sedimentation"),
    ("CL", "type: Cloddy; formation: Artificial structural elements"),
    ("nd", "type: no data; formation: no data")
]
STRUCTURE_GRADES = [
    ("W", "grade: Weak; description: The units are barely observable in place. When gently disturbed, the soil material parts into a mixture of whole and broken units, the majority of which exhibit no surfaces of weakness. The surfaces differ in some way from the interiors."),
    ("M", "grade: Moderate; description: The units are well formed and evident in place. When disturbed, the soil material parts into a mixture of mostly whole units, some broken units, and material that is not in units. Aggregates part from adjoining aggregates to reveal nearly entire faces that have properties distinct from those of fractured surfaces."),
    ("S", "grade: Strong; description: The units are distinct in place. When disturbed, they separate cleanly, mainly into whole units. Aggregates have distinct surface properties."),
    ("nd", "grade: no data; description: no data")
]
AGGREGATE_PENETRABILITY = [
    ("P", "All aggregates with dense outer rim"),
    ("S", "Some aggregates with dense outer rim"),
    ("N", "No aggregate with dense outer rim"),
    ("nd", "no data")
]
AGGREGATE_SIZES = [
    ("VF", "size: Very fine; criterion_gfp: ≤ 1; criterion_salpc: ≤ 5"),
    ("FI", "size: Fine; criterion_gfp: > 1 - 2; criterion_salpc: > 5 - 10"),
    ("ME", "size: Medium; criterion_gfp: > 2 - 5; criterion_salpc: > 10 - 20"),
    ("CO", "size: Coarse; criterion_gfp: > 5 - 10; criterion_salpc: > 20 - 50"),
    ("VC", "size: Very coarse; criterion_gfp: > 10 - 20; criterion_salpc: > 50 - 100"),
    ("EC", "size: Fine; criterion_gfp: > 20; criterion_salpc: > 100"),
    ("nd", "size: no data; criterion_gfp: no data; criterion_salpc: no data")
]

###########################
# Profile General
###########################
class LandformTopography(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    grad_ups = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Ground surface upslope inclination with respect to the horizontal plane. If the profile lies on a flat surface, the gradient is 0%. ')
    grad_downs = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Ground surface downslope inclination with respect to the horizontal plane. If the profile lies on a flat surface, the gradient is 0%. ')
    slope_asp = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_positive], blank=True, null=True, db_comment='If the profile lies on a slope, report the compass direction that the slope faces, viewed downslope; e.g., 225°')
    slope_shp = models.TextField(choices=SHAPES, blank=True, null=True, db_comment='If the profile lies on a slope, report the slope shape in 2 directions: up-/downslope (perpendicular to the elevation contour, i.e. the vertical curvature) and across slope (along the elevation contour, i.e. the horizontal curvature); e.g., Linear (L), Convex (V) or Concave (C).')
    position = models.TextField(choices=POSITION, blank=True, null=True, db_comment='If the profile lies in an uneven terrain, report the profile position.')
    landform1 = models.TextField(choices=LANDFORMS, blank=True, null=True, db_comment='Landform1 type.')
    landform2 = models.TextField(choices=LANDFORMS, blank=True, null=True, db_comment='Landform2 type.')
    activity1 = models.TextField(choices=ACTIVITIES, blank=True, null=True, db_comment='Activity.')
    activity2 = models.TextField(choices=ACTIVITIES, blank=True, null=True, db_comment='Activity.')
    geo_descr = models.TextField(blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'landform_topography'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class CoarseFragments(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    total_area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    class1size = models.TextField(choices=SIZES, blank=True, null=True)
    class2size = models.TextField(choices=SIZES,  blank=True, null=True)
    class3size = models.TextField(choices=SIZES,  blank=True, null=True)
    class1area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    class2area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    class3area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'coarse_fragments'
        db_table_comment = 'Report the total percentage of the area that is covered by coarse surface fragments. In addition, report at least one and up to three size classes and report the percentage of the area that is covered by the coarse surface fragments of the respective size class, the dominant one first.\r\nClasses size are in p_coarse_size'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class ClimateAndWeather(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    clim_koppen = models.TextField(choices=CLIMATE_KOPPEN, blank=True, null=True)
    eco_shultz = models.TextField(choices=ECOZONE_SHULTZ,   blank=True, null=True)
    season = models.TextField(choices=SEASON,   blank=True, null=True)
    curr_weath = models.TextField(choices=CURRENT_WEATHER,  blank=True, null=True)
    past_weath = models.TextField(choices=PAST_WEATHER,   blank=True, null=True)
    soil_temp = models.TextField(choices=SOIL_TEMP_REGIME,  blank=True, null=True)
    soil_moist = models.TextField(choices=SOIL_MOIST_REGIME,   blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'climate_weather'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class Cultivated(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    type = models.TextField(choices=CULTIVATION_TYPE, blank=True, null=True, db_comment='value from p_cultivation_type ')
    actual1 = models.TextField(blank=True, null=True, db_comment='actual dominant specie')
    actual2 = models.TextField(blank=True, null=True, db_comment='actual second specie')
    actual3 = models.TextField(blank=True, null=True, db_comment='actual third specie')
    cessation = models.DateField(blank=True, null=True, db_comment='editable if last dominant specie is NOT NULL')
    area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    prod1_tech = models.TextField(choices=PROD_TECHNIQUES, blank=True, null=True, db_comment='Report the techniques that refer to the surrounding area of the soil profile. If more than one type of technique is present, report in the array up to three, the dominant one first. Value from p_productivity_techniques')
    prod2_tech = models.TextField(choices=PROD_TECHNIQUES, blank=True, null=True)
    prod3_tech = models.TextField(choices=PROD_TECHNIQUES, blank=True, null=True)
    last1 = models.TextField(blank=True, null=True, db_comment="last dominant specie, editable if actual_species1 is NULL")
    last2 = models.TextField(blank=True, null=True, db_comment="Second last specie, editable if actual_species2 is NULL ")
    last3 = models.TextField(blank=True, null=True, db_comment="Third last specie, editable if actual_species3 is NULL ")
    rotation1 = models.TextField(blank=True, null=True, db_comment='Report the dominant specie that have been cultivated in the last five years in rotation with the actual or last species (the first is the most frequent)')
    rotation2 = models.TextField(blank=True, null=True, db_comment='Report the second specie that have been cultivated in the last five years in rotation with the actual or last species (the first is the mostfrequent)')
    rotation3 = models.TextField(blank=True, null=True, db_comment='Report the third specie that have been cultivated in the last five years in rotation with the actual or last species (the first is the mostfrequent)')
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'cultivated'
        db_table_comment = 'Report up to three actual cultivated species (in the array "actual_species") using the scientific name. If currently under fallow, report the up to 3 last species (in the array "last_species") and indicate month and year of harvest or of cultivation cessation. Insert the species in the sequence of the area covered starting with the species that covers the largest area. Report the up to 3 species that have been cultivated in the last five years in rotation with the actual or last species (1 is the most frequent) in the array column "rotational_species"'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
     
class LandUse(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    land_use = models.TextField(choices=USES, blank=True, null=True)
    corine = models.TextField(choices=CORINE, blank=True, null=True)
    cultivated =  models.OneToOneField(Cultivated, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Cultivated Land')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'land_use'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
     
class NotCultivated(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    landuse = models.ForeignKey(LandUse, on_delete=models.CASCADE, related_name='notcultivated_landuse_set')
    veget1 = models.TextField(choices=VEGETATION_TYPES, blank=True, null=True)
    veget2 = models.TextField(choices=VEGETATION_TYPES, blank=True, null=True)
    veget3 = models.TextField(choices=VEGETATION_TYPES, blank=True, null=True)
    stratum = models.TextField(choices=STRATUM )
    avg_height = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    max_height = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    area = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    species1 = models.TextField(blank=True, null=True)
    species2 = models.TextField(blank=True, null=True)
    species3 = models.TextField(blank=True, null=True)

    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'not_cultivated'
        unique_together = (('stratum', 'landuse'),)
        db_table_comment = 'For each profile, compile as many rows as the vegetation strata (STRATA_TYPES) are. Report the average height and the maximum height in m above ground for each stratum separately. Report the vegetation cover. For the upper stratum and the mid-stratum, report the percentage (by area) of the crown cover. For the ground stratum, report the percentage (by area) of the ground cover. Report up to three important species per stratum, e.g., Fagus orientalis. If you do not know the species, report the next higher taxonomic rank. The (maximum 3) species must be insert in the array column species.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class Surface(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    crust_area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    ground_form = models.TextField(choices=GROUND_FORMS, blank=True, null=True, db_comment='Patterned ground form field')
    tech_alter = models.TextField(choices=TECH_ALTERATIONS, blank=True, null=True)
    bedr_form = models.TextField(blank=True, null=True)
    bedr_lith = models.TextField(choices=PARENT_MATERIALS, blank=True, null=True)
    outc_area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    outc_dist = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    outc_size = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    ground_wat = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_positive], blank=True, null=True)
    wat_above = models.TextField(choices=WATER_ABOVE, blank=True, null=True)
    wat_drain = models.TextField(choices=DRAINAGE_CONDITIONS, blank=True, null=True)
    wat_repell = models.TextField(choices=WATER_REPELLENCE, blank=True, null=True)
    desert_ven = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    desert_var = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'surface'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class SurfaceCracks(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    width1 = models.TextField(choices=WIDTH_TYPES, blank=True, null=True)
    dist1 = models.TextField(choices=DISTANCE_TYPES, blank=True, null=True)
    spat_arr1 = models.TextField(choices=ARRANGEMENT, blank=True, null=True)
    persist1 = models.TextField(choices=PERSISTENCE, blank=True, null=True)
    width2 = models.TextField(choices=WIDTH_TYPES, blank=True, null=True)
    dist2 = models.TextField(choices=DISTANCE_TYPES, blank=True, null=True)
    spat_arr2 = models.TextField(choices=ARRANGEMENT, blank=True, null=True)
    persist2 = models.TextField(choices=PERSISTENCE, blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'surface_cracks'
        db_table_comment = 'For each profile, compile as many rows as the width classes are. If surface cracks are present, report the average width of the cracks. If the soil surface between cracks of larger width classes is regularly divided by cracks of smaller width classes, report the two width classes.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LitterLayer(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    avg_thick = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    area = models.DecimalField(max_digits=12, decimal_places=6, validators=[validate_positive], blank=True, null=True)
    max_thick = models.DecimalField(max_digits=12, decimal_places=6, validators=[validate_positive], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'litter_layer'
        db_table_comment = 'Observe an area of 5 m x 5 m with the profile at its centre. Report the average and the maximum thickness of the litter layer in cm. If there is no litter layer, report 0 cm as thickness.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
 
class SurfaceUnevenness(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    position = models.TextField(choices=PROFILE_POSITION, blank=True, null=True)
    nat_type = models.TextField(choices=NATURAL_TYPE, blank=True, null=True)
    nat_avg_h = models.DecimalField( max_digits=20, decimal_places=8, validators=[validate_positive], blank=True, null=True)
    nat_elev = models.DecimalField( max_digits=20, decimal_places=8, validators=[validate_positive], blank=True, null=True)
    nat_dist = models.DecimalField(max_digits=20, decimal_places=8, validators=[validate_positive], blank=True, null=True)
    hum_type1 = models.TextField(choices=HUMAN_MADE_TYPE, blank=True, null=True)
    hum_type2 = models.TextField(choices=HUMAN_MADE_TYPE, blank=True, null=True)
    hum_ter_h = models.DecimalField( max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    hum_noter_h = models.DecimalField( max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    hum_noter_w = models.DecimalField( max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    hum_noter_d = models.DecimalField( max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    ero_area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    ero_type = models.TextField(choices=EROSION_TYPE, blank=True, null=True)
    ero_degree = models.TextField(choices=EROSION_DEGREE, blank=True, null=True)
    ero_activ = models.TextField(choices=EROSION_ACTIVITY, blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'surface_unevenness'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
    
class ProfileGeneral(models.Model):
    id = models.TextField(primary_key=True, db_comment='profile identifier')
    date = models.DateField(blank=True, null=True, db_comment='date of the description')
    surveyors = models.TextField(blank=True, null=True, db_comment='surveyors names comma separated')
    location = models.TextField(blank=True, null=True, db_comment='Name of the profile location')
    lat_wgs84 = models.DecimalField(max_digits=14, decimal_places=8, db_comment='WGS84 Latitude in decimal degree')
    lon_wgs84 = models.DecimalField(max_digits=14, decimal_places=8, db_comment='WGS84 Longitude in decimal degree')
    gps = models.BooleanField(blank=True, null=True, db_comment='is a gps acquisition?')
    elev_m_asl = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, db_comment='Altitude above the sea level in meter')
    elev_dem = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, db_comment='Altitude in meters retrived from a dem in meter')
    survey_m = models.TextField(choices=SURVEY_METHODS,  blank=True, null=True, db_comment='The code of the survey method')
    notes = models.TextField(blank=True, null=True)

    horizons = models.TextField(blank=True, null=True, db_comment='Horizons sequence of the profile')
    old_cls = models.TextField(blank=True, null=True, db_comment='Old classification of the profile ')
    new_cls = models.TextField(blank=True, null=True, db_comment='New classification of the profile ')
    cls_sys = models.TextField(choices=CLASSIFICATION_SYSTEMS, blank=True, null=True, db_comment='value from p_classification_system ')
    old_code = models.TextField(blank=True, null=True, db_comment='profile original code')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True, related_name='profilegeneral_project_set', db_comment='Survey/Project identifier')
    
    coarsefragments =  models.OneToOneField(CoarseFragments, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Coarse Fragments')
    litterlayer =  models.OneToOneField(LitterLayer, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Litter Layer')
    landuse =  models.OneToOneField(LandUse, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Land Use ')
    surface =  models.OneToOneField(Surface, on_delete=models.SET_DEFAULT,default=None, blank=True, null=True, db_comment='Surface ')
    surfacecracks =  models.OneToOneField(SurfaceCracks, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Surface cracks')
    landformtopography = models.OneToOneField(LandformTopography, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='landform_topography')
    climateandweather = models.OneToOneField(ClimateAndWeather, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Climate weather')
    surfaceunevenness =  models.OneToOneField(SurfaceUnevenness, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Surface Unevenness')
    
    ## profilelayer_profile_set ProfileLayer

    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'profile_general'
        db_table_comment = 'The Soil Profile main table'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

#########################################
## Profile Lab Data 
#########################################
class LabData(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    gravel = models.DecimalField(max_digits=40, decimal_places=6, validators=[validate_percentage],  db_comment='Gravel content (%)' , blank=True, null=True)
    cls_sys =  models.TextField(choices=G_CLASSIFICATION_SYSTEMS, db_comment='Classification system used for texture of fine earth', blank=True, null=True)
    texture = models.TextField(choices=TEXTURE_CLASSES, db_comment='texture class', blank=True, null=True)      
    sand = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Sand  (percentage of the fine earth)', blank=True, null=True)
    v_c_sand = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage],db_comment='Very coarse sand (percentage of the fine earth)', blank=True, null=True)
    c_sand = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage],db_comment='Coarse sand (percentage of the fine earth)', blank=True, null=True)
    m_sand = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage],db_comment='Medium sand (percentage of the fine earth)', blank=True, null=True)
    f_sand = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage],db_comment='Fine sand (percentage of the fine earth)', blank=True, null=True)
    v_f_sand  = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Very Fine sand (percentage of the fine earth)', blank=True, null=True)
    met_sand = models.TextField(choices=SAND_CONTENT_METHODS, blank=True, null=True)
    silt = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Silt (percentage of the fine earth)', blank=True, null=True)
    c_silt = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Coarse silt (percentage of the fine earth)', blank=True, null=True)
    f_silt = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Fine silt  (percentage of the fine earth)', blank=True, null=True)
    met_silt = models.TextField(choices=SILT_CLAY_CONTENT_METHODS,  blank=True, null=True)
    clay = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Clay  (percentage of the fine earth)', blank=True, null=True)
    met_clay = models.TextField(choices=SILT_CLAY_CONTENT_METHODS, blank=True, null=True)
    bulk_dens = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Bulk density (g/cm3)'	, blank=True, null=True)
    el_cond = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Electric conductivity (dS/m)', blank=True, null=True)
    met_el_cond = models.TextField(choices=EL_CONDUCTIVITY_PH_METHODS, db_comment='Method used for Electric conductivity', blank=True, null=True)
    hy_cond = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Hydraulic conductivity at saturation (mm/h)', blank=True, null=True)
    met_hy_cond = models.TextField(choices=HIDRAULIC_CONDUCTIVITY_METHODS, db_comment='Method used for Hydraulic conductivity at saturation', blank=True, null=True)
    satur = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Saturation (percentage)', blank=True, null=True)
    field_cap = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Field capacity (percentage)', blank=True, null=True)
    wilting_p = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Wilting point (percentage)', blank=True, null=True)
    met_s_f_w = models.TextField(choices=WILTING_POINT_METHODS, db_comment='Method used for saturation, field capacity, wilting point', blank=True, null=True)
    acidity = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Soil acidity: Exchangeable Al (meq/100g)', blank=True, null=True)
    met_acidity = models.TextField(db_comment='Method used for Soil acidity: Exchangeable Al (meq/100g)', blank=True, null=True)
    ph_h2o = models.DecimalField( max_digits=30, decimal_places=10, db_comment='pH (H2O)', blank=True, null=True)
    met_ph_h20 = models.TextField(choices=EL_CONDUCTIVITY_PH_METHODS, db_comment='Method used for pH (H2O)', blank=True, null=True)
    ph_kcl = models.DecimalField( max_digits=30, decimal_places=10, db_comment='pH (KCl)', blank=True, null=True)
    met_ph_kcl = models.TextField(choices=EL_CONDUCTIVITY_PH_METHODS, db_comment='Method used for pH (KCl)', blank=True, null=True)
    ph_ccl = models.DecimalField( max_digits=30, decimal_places=10, db_comment='pH (CaCl2)', blank=True, null=True)
    met_ph_ccl = models.TextField(choices=EL_CONDUCTIVITY_PH_METHODS, db_comment='Method used for pH (CaCl2)',  blank=True, null=True)
    org_car = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Organic Carbon content (g/kg)', blank=True, null=True)
    met_org_car = models.TextField( choices=ORGANIC_CARBON_METHODS, db_comment='Method used for Organic Carbon content', blank=True, null=True)
    org_mat = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Organic matter content (percentage)', blank=True, null=True)
    met_org_mat = models.TextField(choices=ORGANIC_MATTER_CONTENT_METHODS, db_comment='Method used for organic matter content', blank=True, null=True)
    caco3 = models.DecimalField( max_digits=30, decimal_places=10, db_comment='CaCO3 content (percentage)', blank=True, null=True)
    met_caco3 = models.TextField(choices=CACO3_CONTENT_METHODS, db_comment='Method used CaCO3 content',  blank=True, null=True)
    gypsum = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Gypsum content (percentage)', blank=True, null=True)
    met_gypsum = models.TextField(choices=GYPSUM_CONTENT_METHODS, db_comment='Method used for Gypsum content',  blank=True, null=True)
    cec = models.DecimalField( max_digits=30, decimal_places=10, db_comment='CEC (cmol/Kg)', blank=True, null=True)
    met_cec = models.TextField(choices=CEC_CA_MG_NA_K_METHODS, db_comment='Method used for CEC',  blank=True, null=True)
    ca = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Ca++ (cmol/Kg)', blank=True, null=True)
    met_ca = models.TextField(choices=CEC_CA_MG_NA_K_METHODS, db_comment='Method used for Ca++', blank=True, null=True)
    mg = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Mg++ (cmol/Kg)', blank=True, null=True)
    met_mg = models.TextField(choices=CEC_CA_MG_NA_K_METHODS, db_comment='Method used for Mg++',  blank=True, null=True)
    na = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Na+ (cmol/Kg)', blank=True, null=True)
    met_na = models.TextField(choices=CEC_CA_MG_NA_K_METHODS, db_comment='Method used for Na+',  blank=True, null=True)
    k = models.DecimalField( max_digits=30, decimal_places=10, db_comment='K+ (cmol/Kg)', blank=True, null=True)
    met_k = models.TextField(choices=CEC_CA_MG_NA_K_METHODS, db_comment='Method used for K+',  blank=True, null=True)
    n_tot = models.DecimalField( max_digits=30, decimal_places=10, db_comment='N tot content (g/Kg)', blank=True, null=True)
    met_n_tot = models.TextField(choices=N_CONTENT_METHODS, db_comment='Method used for N tot content',  blank=True, null=True)
    p_cont = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Available P content(mg/kg)', blank=True, null=True)
    met_p_cont = models.TextField(choices=P_CONTENT_METHODS, db_comment='Method used for available P content',  blank=True, null=True)
    feox = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Feox (g/kg)', blank=True, null=True)
    fed = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Fed (g/kg)', blank=True, null=True)
    fep = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Fep (g/kg)', blank=True, null=True)
    fe_tot = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Fe tot (g/kg)', blank=True, null=True)
    mn = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Mn (mg/kg)', blank=True, null=True)
    met_mn = models.TextField(choices=MN_ZN_CU_METHODS, db_comment='Method used for Mn', blank=True, null=True)
    zn = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Zn (mg/kg)', blank=True, null=True)
    met_zn = models.TextField(choices=MN_ZN_CU_METHODS, db_comment='Method used for Zn', blank=True, null=True)
    cu = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Cu (mg/kg)', blank=True, null=True)
    met_cu = models.TextField(choices=MN_ZN_CU_METHODS, db_comment='Method used for Cu', blank=True, null=True) 
    act_caco3 = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Active CaCO3 (%)', blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'lab_data'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )


###########################
# Profile Layer
###########################
class LayerRemnants(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    abundance = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    cementing1 = models.TextField(choices=CEMENTING_AGENT, blank=True, null=True)
    cementing2 = models.TextField(choices=CEMENTING_AGENT, blank=True, null=True)
    size1 = models.TextField(choices=SIZE_SHAPE_TYPES, blank=True, null=True)
    size2 = models.TextField(choices=SIZE_SHAPE_TYPES, blank=True, null=True)
    abundance1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_remnants'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerCoarseFragments(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    litho_type1 = models.TextField(choices=PARENT_MATERIALS, blank=True, null=True)
    litho_type2 = models.TextField(choices=PARENT_MATERIALS, blank=True, null=True)
    litho_type3 = models.TextField(choices=PARENT_MATERIALS, blank=True, null=True)
    litho_type4 = models.TextField(choices=PARENT_MATERIALS, blank=True, null=True)
    size1 = models.TextField(choices=SIZE_SHAPE_TYPES, blank=True, null=True)
    size2 = models.TextField(choices=SIZE_SHAPE_TYPES, blank=True, null=True)
    size3 = models.TextField(choices=SIZE_SHAPE_TYPES, blank=True, null=True)
    size4 = models.TextField(choices=SIZE_SHAPE_TYPES, blank=True, null=True)
    weath1 = models.TextField(choices=WEATHERING_STAGE, blank=True, null=True)
    weath2 = models.TextField(choices=WEATHERING_STAGE, blank=True, null=True)
    weath3 = models.TextField(choices=WEATHERING_STAGE, blank=True, null=True)
    weath4 = models.TextField(choices=WEATHERING_STAGE, blank=True, null=True)
    abundance1 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage], db_comment='Report the total percentage of the volume occupied by coarse fragments for class1.')
    abundance2 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage], db_comment='Report the total percentage of the volume occupied by coarse fragments for class2.')
    abundance3 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage], db_comment='Report the total percentage of the volume occupied by coarse fragments for class3.')
    abundance4 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage], db_comment='Report the total percentage of the volume occupied by coarse fragments for class4.')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_coarse_fragments'
        db_table_comment = 'Coarse fragments. A coarse fragment is a mineral particle, derived from the parent material, > 2 mm in its equivalent diameter'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
       
class LayerArtefacts(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    abundance = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    black_carb = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    type1 = models.TextField(choices=ARTEFACT_TYPES, blank=True, null=True)
    type2 = models.TextField(choices=ARTEFACT_TYPES, blank=True, null=True)
    type3 = models.TextField(choices=ARTEFACT_TYPES, blank=True, null=True)
    type4 = models.TextField(choices=ARTEFACT_TYPES, blank=True, null=True)
    type5 = models.TextField(choices=ARTEFACT_TYPES, blank=True, null=True)
    size1 = models.TextField(choices=ARTEFACT_SIZES, blank=True, null=True)
    size2 = models.TextField(choices=ARTEFACT_SIZES, blank=True, null=True)
    size3 = models.TextField(choices=ARTEFACT_SIZES, blank=True, null=True)
    size4 = models.TextField(choices=ARTEFACT_SIZES, blank=True, null=True)
    size5 = models.TextField(choices=ARTEFACT_SIZES, blank=True, null=True)
    abundance1 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    abundance2 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    abundance3 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    abundance4 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    abundance5 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_artefacts'
        db_table_comment = 'Artefacts are solid or liquid substances that are: created or substantially modified by humans as part of an industrial or artisanal manufacturing process, or brought to the surface by human activity from a depth, where they were not influenced by surface processes, and deposited in an environment, where they do not commonly occur.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )


    """
    def clean(self):
            if self.type1 is not None and self.type1.startswith("l_artefacts."):
                    raise ValidationError({'type1': ('Wrong classification.')})
            if self.type2 is not None and self.type2.startswith("l_artefacts."):
                    raise ValidationError({'type2': ('Wrong classification.')})
            if self.type3 is not None and self.type3.startswith("l_artefacts."):
                    raise ValidationError({'type3': ('Wrong classification.')})
            if self.type4 is not None and self.type4.startswith("l_artefacts."):
                    raise ValidationError({'type4': ('Wrong classification.')})
            if self.type5 is not None and self.type5.startswith("l_artefacts."):
                    raise ValidationError({'type5': ('Wrong classification.')})
            if self.size_type1 is not None and self.size_type1.startswith("l_artefacts_size."):
                    raise ValidationError({'size_type1': ('Wrong classification.')})
            if self.size_type2 is not None and self.size_type2.startswith("l_artefacts_size."):
                    raise ValidationError({'size_type2': ('Wrong classification.')})
            if self.size_type3 is not None and self.size_type3.startswith("l_artefacts_size."):
                    raise ValidationError({'size_type3': ('Wrong classification.')})
            if self.size_type4 is not None and self.size_type4.startswith("l_artefacts_size."):
                    raise ValidationError({'size_type4': ('Wrong classification.')})
            if self.size_type5 is not None and self.size_type5.startswith("l_artefacts_size."):
                    raise ValidationError({'size_type5': ('Wrong classification.')})         
    """    

class LayerCracks(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    persistenc = models.TextField(choices=CRACKS_PERSISTENCE, blank=True, null=True)
    continuity = models.TextField(choices=CRACKS_CONTINUITY, blank=True, null=True)
    avg_width = models.DecimalField(max_digits=16, decimal_places=2, validators=[validate_positive], blank=True, null=True)
    abundance = models.PositiveIntegerField(blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_cracks'
        db_table_comment = 'Report persistence and continuity'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
   
class LayerStressFeatures(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    pressfaces = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Pressure faces in % of the surfaces of soil aggregates')
    slicksides = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Slickensides in % of the surfaces of soil aggregates.')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_stress_features'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

        db_table_comment = 'Stress features result from soil aggregates that are pressed against each other due to swelling clays. The aggregate surfaces may be shiny. There are two types: Pressure faces do not slide past each other and have no striations, slickensides slide past each other and have striations.'

class LayerMatrixColours(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    munsell_m1 = models.TextField(blank=True, null=True)
    munsell_d1 = models.TextField(blank=True, null=True)
    area1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    munsell_m2 = models.TextField(blank=True, null=True)
    munsell_d2 = models.TextField(blank=True, null=True)
    area2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    munsell_m3 = models.TextField(blank=True, null=True)
    munsell_d3 = models.TextField(blank=True, null=True)
    area3 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_matrix_colour'
        db_table_comment = 'Report the colour of the soil matrix. If there is more than one matrix colour, report up to three, the dominant one first, and give the percentage of the exposed area'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerCoarserTextured(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    coars_text = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='the percentage (by exposed area) occupied by coarser-textured parts of any orientation (vertical, horizontal, inclined) having a width of ≥ 0.5 cm')
    v_tongues = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='the percentage (by exposed area) occupied by continuous vertical tongues of coarser-textured parts with a horizontal extension of ≥ 1 cm (if these tongues are absent, report 0%)')
    depth = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='the depth range in cm, where these tongues cover ≥ 10% of the exposed area (if they extend across several layers, the length is only reported in the description of that layer, where they start at the layer’s upper limit).')
    h_area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='In the middle of the layer, prepare a horizontal surface, 50 cm x 50 cm, and report the percentage (by horizontal area covered) of the coarser-textured parts.')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_coarser_textured'
        db_table_comment = 'If a layer consists of darker-coloured finer-textured and lighter-coloured coarser-textured parts that do not form horizontal layers but can easily be distinguished, describe them separately'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerLithogenicVariegates(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier') 
    munsell_m1 = models.TextField(blank=True, null=True)
    size1 = models.TextField(choices=LITHOGENIC_SIZES, blank=True, null=True)
    area1 = models.DecimalField(max_digits=6 , decimal_places=2 , validators=[validate_percentage],  blank=True, null=True)
    munsell_m2 = models.TextField(blank=True, null=True)
    size2 = models.TextField(choices=LITHOGENIC_SIZES, blank=True, null=True)
    area2 = models.DecimalField(max_digits=6 , decimal_places=2 , validators=[validate_percentage],  blank=True, null=True)
    munsell_m3 = models.TextField(blank=True, null=True)
    size3 = models.TextField(choices=LITHOGENIC_SIZES, blank=True, null=True)
    area3 = models.DecimalField(max_digits=6 , decimal_places=2 , validators=[validate_percentage],  blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_lithogenic_variegates'
        db_table_comment = 'Report colour, size class, and abundance. If more than one colour occurs, report up to three, the dominant one first, and give size class and abundance for each colour separately.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
          
class LayerRedoximorphicFeatures(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    oxi_inner = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    oxi_outer = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    oxi_random = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    red_inner = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    red_outer = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    red_random = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abund_oxi = models.DecimalField(max_digits=12, decimal_places=4, validators=[validate_percentage], db_comment='Abundance of cemented oximorphic features, by volume [%]')
    
    #redoximorphic_colour_redoximorphic_features_set from LayerRedoximorphicColour
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_redoximorphic'
        db_table_comment = ''
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerRedoximorphicColour(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    features = models.ForeignKey(LayerRedoximorphicFeatures, on_delete=models.CASCADE, related_name='layerredoximorphiccolour_features_set', db_comment='LayerRedoximorphicFeatures')  
    colour_nr = models.SmallIntegerField(validators=[validate_positive], db_comment='layer redoximorphic colour number')
    munsell_m = models.TextField(blank=True, null=True)
    munsell_d = models.TextField(blank=True, null=True)
    substance = models.TextField(choices=REDOXIMORPHIC_SUBSTANCES, blank=True, null=True)
    location = models.TextField(choices=REDOXIMORPHIC_LOCATIONS,blank=True, null=True)
    size1 = models.TextField(choices=OXIMORPHIC_SIZES,blank=True, null=True)
    size2 = models.TextField(choices=OXIMORPHIC_SIZES,blank=True, null=True)
    mottles_c = models.TextField(choices=MOTTLES_CONTRAST,blank=True, null=True)
    mottles_b = models.TextField(choices=MOTTLES_BOUNDARY_TYPES,blank=True, null=True)
    cement = models.TextField(choices=OXIMORPHIC_CEMENTATION,blank=True, null=True)
    area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_redoximorphic_colour'
        db_table_comment = 'Report the colour according to the Munsell Color Charts'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
  
class LayerCoatingsBridges(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    clay_coat = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of clay coatings in percentage')
    form_coat = models.TextField(choices=FORM_COATINGS, blank=True, null=True, db_comment='refer to clay coatings')
    org_coat = models.TextField(choices=ORGANIC_COATINGS, blank=True, null=True, db_comment='Organic matter coatings and oxide coatings on sand and/or coarse silt grains')
    crack_coat = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of cracked coatings in percentage')
    clay_bridg = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of clay bridges in percentage')
    form_bridg = models.TextField(choices=FORM_COATINGS, blank=True, null=True, db_comment='refer to clay bridge')
    form_org = models.TextField(choices=FORM_COATINGS, blank=True, null=True, db_comment='refer to organic matter coatings and oxide coatings (report only if matrix colour value ≤ 3)')
    sand_silt = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of uncoated sand and coarse silt grains in percentage')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_coatings_bridges'
        db_table_comment = 'Report the abundance of clay coatings in % of the surfaces of soil aggregates, coarse fragments and/or biopore walls clay bridges between sand grains in % of involved sand grains.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
                  
class LayerRibbonlikeAccumulations(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    substances = models.TextField(choices=RIBBONLIKE_SUBSTANCES, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    comb_thick = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_positive], blank=True, null=True, db_comment='If there are 2 or more ribbon-like accumulations in one layer, report the number of the accumulations and their combined thickness in cm')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_ribbonlike_accumulations'
        db_table_comment = 'Ribbon-like accumulations are thin, horizontally continuous accumulations within the matrix of another layer. Report the accumulated substance(s).'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
           
class LayerCarbonates(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    matr_c = models.TextField(choices=CARBONATE_CONTENTS, blank=True, null=True)
    matr_c_ret = models.TextField(choices=RETARDED_REACTION, blank=True, null=True)
    sec_type1 = models.TextField(choices=SECONDARY_CARBONATE_TYPES, blank=True, null=True)
    sec_type2 = models.TextField(choices=SECONDARY_CARBONATE_TYPES, blank=True, null=True)
    sec_type3 = models.TextField(choices=SECONDARY_CARBONATE_TYPES, blank=True, null=True)
    sec_type4 = models.TextField(choices=SECONDARY_CARBONATE_TYPES, blank=True, null=True)
    sec_size1 = models.TextField(choices=MINERAL_SIZES, blank=True, null=True)
    sec_size2 = models.TextField(choices=MINERAL_SIZES, blank=True, null=True)
    sec_size3 = models.TextField(choices=MINERAL_SIZES, blank=True, null=True)
    sec_size4 = models.TextField(choices=MINERAL_SIZES, blank=True, null=True)
    sec_shape1 = models.TextField(choices=MINERAL_SHAPES, blank=True, null=True)
    sec_shape2 = models.TextField(choices=MINERAL_SHAPES, blank=True, null=True)
    sec_shape3 = models.TextField(choices=MINERAL_SHAPES, blank=True, null=True)
    sec_shape4 = models.TextField(choices=MINERAL_SHAPES, blank=True, null=True)
    sec_abund1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    sec_abund2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    sec_abund3 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    sec_abund4 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_carbonates'
        db_table_comment = 'Layer Carbonates'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerGypsum(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    content = models.TextField(choices=GYPSUM_CONTENT_TYPES, blank=True, null=True)
    sec_gypsum = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    sgypsum1 = models.TextField(choices=SGYPSUM_TYPES, blank=True, null=True)
    sgypsum2 = models.TextField(choices=SGYPSUM_TYPES, blank=True, null=True)
    type1_size = models.TextField(choices=MINERAL_SIZES, blank=True, null=True)
    type2_size = models.TextField(choices=MINERAL_SIZES, blank=True, null=True)
    type1_shape = models.TextField(choices=MINERAL_SHAPES, blank=True, null=True)
    type2_shape = models.TextField(choices=MINERAL_SHAPES, blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_gypsum'
        db_table_comment = 'Report the gypsum content in the soil matrix. If readily soluble salts are absent or present in small amounts only, gypsum can be estimated by measuring the electrical conductivity in soil suspensions of different soil-water relations after 30 minutes (in the case of fine-grained gypsum). This method detects primary and secondary gypsum. Note: Higher gypsum contents may be differentiated by abundance of H2O-soluble pseudomycelia/crystals and a soil colour with high value and low chroma'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerSecondarySilica(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    type1 = models.TextField(choices=SECONDARY_SILICA_TYPES, blank=True, null=True, db_comment='Report the type of secondary silica, type1 is dominant')
    type2 = models.TextField(choices=SECONDARY_SILICA_TYPES, blank=True, null=True, db_comment='Report the type of secondary silica')
    dnfcsize1 = models.TextField(choices=DNFC_SIZES, blank=True, null=True, db_comment='If a layer shows durinodes and/or remnants of a layer that has been cemented by secondary silica, report their size class for type1')
    dnfcsize2 = models.TextField(choices=DNFC_SIZES, blank=True, null=True, db_comment='If a layer shows durinodes and/or remnants of a layer that has been cemented by secondary silica, report their size class for type2')
    abund = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Report the total percentage (by exposed area) of secondary silica')
    abund_dnfc = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='If a layer shows durinodes and/or remnants of a cemented layer, report in addition the percentage (by volume) of those durinodes and remnants that have a diameter ≥ 1 cm')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_secondary_silica'
        db_table_comment = 'Secondary silica (SiO2) is off-white and predominantly consisting of opal and microcrystalline forms. It occurs as laminar caps, lenses, (partly) filled interstices, bridges between sand grains, and as coatings at surfaces of soil aggregates, biopore walls, coarse fragments, and remnants of broken-up cemented layers. Report the type of secondary silica. If more than one type occurs, report up to two, the dominant one first.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerConsistence(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    cement = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Report the percentage (by volume, related to the whole soil) of the layer that is cemented.')
    cement_ag1 = models.TextField(choices=CEMENTING_AGENTS, blank=True, null=True, db_comment='Report the cementing agents')
    cement_ag2 = models.TextField(choices=CEMENTING_AGENTS, blank=True, null=True)
    cement_ag3 = models.TextField(choices=CEMENTING_AGENTS, blank=True, null=True)
    cement_cls = models.TextField(choices=CEMENTATION_CLASSES, blank=True, null=True)
    rrclass_m = models.TextField(choices=RRCLASSES_MOIST, blank=True, null=True, db_comment='Rupture resistance, non-cemented soil moist')
    rrclass_d = models.TextField(choices=RRCLASSES_DRY, blank=True, null=True, db_comment='Rupture resistance, non-cemented soil dry')
    susceptib = models.TextField(choices=SUSCEPTIBILITY, blank=True, null=True, db_comment='Some layers are prone to cementation after repeated drying and wetting. Report the susceptibility')
    m_failure = models.TextField(choices=MANNER_FAILURE, blank=True, null=True, db_comment='Report the manner of failure (brittleness)')
    plastic = models.TextField(choices=PLASTICITY, blank=True, null=True, db_comment='Plasticity is the degree to which reworked soil can be permanently deformed without rupturing')
    penet_res = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    stickiness = models.TextField(choices=STICKINESS, blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_consistence'
        db_table_comment = 'Consistence is the degree and kind of cohesion and adhesion that soil exhibits. Consistence is reported separately for cemented and non-cemented (parts of) layers. If a specimen of soil does not fall into pieces by applying low forces, one has to check, whether it is cemented'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerSurfaceCrusts(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    sealing1 = models.TextField(choices=SEALING_AGENT, blank=True, null=True)
    sealing2 = models.TextField(choices=SEALING_AGENT, blank=True, null=True)
    sealing3 = models.TextField(choices=SEALING_AGENT, blank=True, null=True)
    avg_thickn = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_surface_crusts'
        db_table_comment = 'A crust is a thin layer of soil constituents bound together into a horizontal mat or into small polygonal plates (see Schoeneberger et al., 2012). Soil crusts develop in the first mineral layer(s) and are formed by a sealing agent of physical, chemical and/or biological origin.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerPermafrostFeatures(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    cry_alter1 = models.TextField(choices=CRYOGENIC_ALTERATION, blank=True, null=True)
    cry_alter2 = models.TextField(choices=CRYOGENIC_ALTERATION, blank=True, null=True)
    cry_alter3 = models.TextField(choices=CRYOGENIC_ALTERATION, blank=True, null=True)
    permafrost = models.TextField(choices=PERMAFROST_TYPE, blank=True, null=True)
    cry_abund1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    cry_abund2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    cry_abund3 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_permafrost_features'
        db_table_comment = 'Estimate the total percentage (by exposed area, related to the whole soil) affected by cryogenic alteration. Report up to three features, the dominant one first, and report the percentage for each feature separately.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerOrganicCarbon(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    contentmin = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    contentmax = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    nat_accum1 = models.TextField(choices=ACCUMULATION_TYPES, blank=True, null=True)
    nat_accum2 = models.TextField(choices=ACCUMULATION_TYPES, blank=True, null=True)
    nat_accum3 = models.TextField(choices=ACCUMULATION_TYPES, blank=True, null=True)
    abundance1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance3 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    black_carb = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_organic_carbon'
        db_table_comment = 'Report the estimated organic carbon content. It is based on the Munsell value, moist, and the texture'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
 
class LayerRoots(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    a_lt2mm = models.TextField(choices=ROOT_ABUNDANCE_CLASSES, blank=True, null=True, db_comment='diameter <= 2mm')
    a_lt05mm = models.TextField(choices=ROOT_ABUNDANCE_CLASSES, blank=True, null=True, db_comment='diameter < 0,5mm')
    a_05to2mm = models.TextField(choices=ROOT_ABUNDANCE_CLASSES, blank=True, null=True, db_comment='diameter from 0.5 to 2 mm')
    a_gt2mm = models.TextField(choices=ROOT_ABUNDANCE_CLASSES, blank=True, null=True, db_comment='diameter > 2mm')
    a_2to5mm = models.TextField(choices=ROOT_ABUNDANCE_CLASSES, blank=True, null=True, db_comment='diameter from 2 to 5 mm')
    a_gt5mm = models.TextField(choices=ROOT_ABUNDANCE_CLASSES, blank=True, null=True, db_comment='diameter > 5mm')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_roots'
        db_table_comment = 'Count the number of roots per dm2, separately for the six diameter classes, and report the abundance classes'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerAnimalActivity(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    type1 = models.TextField(choices=ANIMAL_ACTIVITY_TYPES, blank=True, null=True)
    type2 = models.TextField(choices=ANIMAL_ACTIVITY_TYPES, blank=True, null=True)
    type3 = models.TextField(choices=ANIMAL_ACTIVITY_TYPES, blank=True, null=True)
    type4 = models.TextField(choices=ANIMAL_ACTIVITY_TYPES, blank=True, null=True)
    type5 = models.TextField(choices=ANIMAL_ACTIVITY_TYPES, blank=True, null=True)
    mammal = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    bird = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    worm = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    insect = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    unspecify = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_animal_activity'
        db_table_comment = 'Report the animal activity that has visibly changed the features of the layer. If applicable, report up to 5 types, the dominant one first. Report the percentage (by exposed area), separately for mammal activity, bird activity, worm activity, insect activity and unspecified activity'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerHumanAlterations(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    nat_mat1 =models.TextField(choices=NATURAL_MATERIAL_TYPES, blank=True, null=True)
    nat_mat2 = models.TextField(choices=NATURAL_MATERIAL_TYPES, blank=True, null=True)
    nat_mat3 = models.TextField(choices=NATURAL_MATERIAL_TYPES, blank=True, null=True)
    abundance1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance3 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    texture = models.TextField(choices=TEXTURE_CLASSES, blank=True, null=True)
    carbonate = models.TextField(choices=SECONDARY_CARBONATE_TYPES, blank=True, null=True)
    carbon = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    alter1 = models.TextField(choices=ALTERATIONS_TYPES,  blank=True, null=True)
    alter2 = models.TextField(choices=ALTERATIONS_TYPES, blank=True, null=True)
    aggregate = models.TextField(choices=AGGREGATE_FORMATION, blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_human_alterations'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerDegreeDecomposition(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    vis_plant = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    sbdiv_horz = models.TextField(choices=SUBDVISION_HORIZON, blank=True, null=True)
    plant_res1 = models.TextField(choices=DEAD_PLANT_TYPES, blank=True, null=True)
    plant_res2 = models.TextField(choices=DEAD_PLANT_TYPES, blank=True, null=True)
    abundance1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_degree_decomposition'
        db_table_comment = 'Refer to the transformation of visible plant tissues into visibly homogeneous organic matter.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerNonMatrixPore(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    type1 = models.TextField(choices=NONMATRIX_PORES_TYPES, blank=True, null=True)
    size1 = models.TextField(choices=PORE_SIZES, blank=True, null=True)
    abund1 = models.TextField(choices=PORE_ABUNDANCE, blank=True, null=True)
    type2 = models.TextField(choices=NONMATRIX_PORES_TYPES, blank=True, null=True)
    size2 = models.TextField(choices=PORE_SIZES, blank=True, null=True)
    abund2 = models.TextField(choices=PORE_ABUNDANCE, blank=True, null=True)
    type3 = models.TextField(choices=NONMATRIX_PORES_TYPES, blank=True, null=True)
    size3 = models.TextField(choices=PORE_SIZES, blank=True, null=True)
    abund3 = models.TextField(choices=PORE_ABUNDANCE, blank=True, null=True)
    type4 = models.TextField(choices=NONMATRIX_PORES_TYPES, blank=True, null=True)
    size4 = models.TextField(choices=PORE_SIZES, blank=True, null=True)
    abund4 = models.TextField(choices=PORE_ABUNDANCE, blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_nonmatrix_pore'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class ProfileLayer(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    profile = models.ForeignKey(ProfileGeneral, on_delete=models.CASCADE, related_name='profilelayer_profile_set', db_comment='Foreign Key field: profile') 
    design = models.TextField(db_comment='layer horizon designation')
    number = models.SmallIntegerField(validators=[validate_positive], db_comment='layer order in profile')
    upper = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_positive], db_comment='upper depth in cm',blank=True, null=True)
    lower = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_positive], db_comment='lower depth in cm',blank=True, null=True)
    lower_bound = models.TextField(db_comment='layer lower boundary ', blank=True, null=True )
    hom_part = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Described parts, by exposed area [%]')
    hom_alluvt = models.TextField(choices=ALLUVIAL_TEPHRA, blank=True, null=True, db_comment='Layer composed of several strata of alluvial sediments or of tephra')
    wat_satur = models.TextField(choices=WATER_SATURATION, blank=True, null=True, db_comment='Types of water saturation')
    wat_status = models.TextField(choices=WATER_STATUS, blank=True, null=True, db_comment='Soil water status')
    o_mineral =  models.TextField(choices=ORGANIC_MINERAL_TYPES, blank=True, null=True, db_comment='organic, organotechnic or mineral layer')
    bounddist = models.TextField(choices=BOUNDARIES, blank=True, null=True, db_comment="Distinctness of the layer's lower boundary")
    boundshape = models.TextField(choices=SHAPE_TYPES, blank=True, null=True)
    wind = models.TextField(choices=WIND, blank=True, null=True, db_comment='Wind deposition')
    tex_cls = models.TextField(choices=TEXTURE_CLASSES, blank=True, null=True, db_comment='Texture class') 
    tex_subcls = models.TextField(choices=TEXTURE_SUBCLASSES, blank=True, null=True, db_comment='Texture subclass')
    struct_w_s = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Structure Wedge-shaped aggregates tilted between ≥ 10° and ≤ 60° from the horizontal: abundance, by volume [%]')
    rh_value = models.TextField(choices=RH_VALUE, blank=True, null=True, db_comment='Rh Value')
    weathering = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Initial weathering abundance')
    sol_salts = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='ECSE [dS m-1m-1]')
    ph_value = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, db_comment='Potentiometric pH measurement - Measured value')
    ph_solution = models.TextField(choices=POTENZIOMETRIC_MEASURES, blank=True, null=True, db_comment='Potentiometric pH measurement - Solution and mixing ratio')
    fracts = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    avg_fracts = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    volc_abund = models.TextField(choices=ABUNDANCE_PARTICLES_TYPES, blank=True, null=True)
    volc_thnaf = models.TextField(choices=THIXOTROPY_NAF, blank=True, null=True)
    bulk_dens = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    pack_dens = models.TextField(choices=PACKING_DENSITIES, blank=True, null=True, db_comment='Estimate the packing density using a knife with a blade approx. 10 cm long')
    parent_mat = models.TextField(choices=PARENT_MATERIALS, blank=True, null=True, db_comment='Report the parent material. Use the help of a geological map.')
    note = models.TextField(blank=True, null=True)

    remnants = models.OneToOneField(LayerRemnants, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Remnants of broken-up cemented layers')
    coarsefragments = models.OneToOneField(LayerCoarseFragments, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Coarse fragments')
    artefacts = models.OneToOneField(LayerArtefacts, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Artefacts')
    cracks = models.OneToOneField(LayerCracks, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Cracks')
    stressfeatures = models.OneToOneField(LayerStressFeatures, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Stress Features')
    coatingsbridges = models.OneToOneField(LayerCoatingsBridges, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerCoatingsBridges')
    ribbonlikeaccumulations = models.OneToOneField(LayerRibbonlikeAccumulations, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerRibbonlikeAccumulations')
    carbonates = models.OneToOneField(LayerCarbonates, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Section Layer Carbonates')
    gypsum = models.OneToOneField(LayerGypsum, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerGypsum')
    secondarysilica = models.OneToOneField(LayerSecondarySilica, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerSecondarySilica')
    consistence = models.OneToOneField(LayerConsistence, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerConsistence')
    surfacecrusts = models.OneToOneField(LayerSurfaceCrusts, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerSurfaceCrusts')   
    permafrost =  models.OneToOneField(LayerPermafrostFeatures, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerPermafrostFeatures')   
    organiccarbon =  models.OneToOneField(LayerOrganicCarbon, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerOrganicCarbon')   
    roots =  models.OneToOneField(LayerRoots, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerRoots')   
    animalactivity  =  models.OneToOneField(LayerAnimalActivity, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerAnimalActivity')   
    humanalterations =  models.OneToOneField(LayerHumanAlterations, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerHumanAlterations')   
    degreedecomposition =  models.OneToOneField(LayerDegreeDecomposition, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerDegreeDecomposition')   
    nonmatrixpore = models.OneToOneField(LayerNonMatrixPore, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerNonMatrixPore')   
    labdata =  models.OneToOneField(LabData, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Layer Laboratory data')
    matrixcolours = models.OneToOneField(LayerMatrixColours, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Matrix colour')   
    texturecolour = models.OneToOneField(LayerCoarserTextured, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Combinations of darker-coloured finer-textured and lighter-coloured coarser-textured parts')
    lithogenicvariegates = models.OneToOneField(LayerLithogenicVariegates, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerLithogenicVariegates')
    redoximorphicfeatures = models.OneToOneField(LayerRedoximorphicFeatures, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerRedoximorphicFeatures')
    
    ## layerstructure_layer_set LayerStructure

    def _get_thickness(self):
        if self.lower and self.upper: 
            return self.lower - self.upper
        else: return None
    thickness = property(_get_thickness)   
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'layer'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerStructure(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')  
    layer = models.ForeignKey(ProfileLayer, on_delete=models.CASCADE, related_name='layerstructure_layer_set', db_comment='Profile Layer' )
    level = models.TextField(choices=STRUCTURE_LEVELS, blank=True, null=True)
    type = models.TextField(choices=STRUCTURE_TYPES, blank=True, null=True)
    grade = models.TextField(choices=STRUCTURE_GRADES, blank=True, null=True)
    penetrab = models.TextField(choices=AGGREGATE_PENETRABILITY, blank=True, null=True)
    size1 = models.TextField(choices=AGGREGATE_SIZES, blank=True, null=True)
    size2 = models.TextField(choices=AGGREGATE_SIZES, blank=True, null=True)
    abundance_vol = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_structure_types'
        unique_together = (('layer', 'level'),)
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

###########################
# Monitoring General
###########################
class MonitoringLandformTopography(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    grad_ups = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Ground surface upslope inclination with respect to the horizontal plane. If the monitoring site lies on a flat surface, the gradient is 0%. ')
    grad_downs = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Ground surface downslope inclination with respect to the horizontal plane. If the monitoring site lies on a flat surface, the gradient is 0%. ')
    slope_asp = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_positive], blank=True, null=True, db_comment='If the monitoring site lies on a slope, report the compass direction that the slope faces, viewed downslope; e.g., 225°')
    slope_shp = models.TextField(choices=SHAPES, blank=True, null=True, db_comment='If the monitoring site lies on a slope, report the slope shape in 2 directions: up-/downslope (perpendicular to the elevation contour, i.e. the vertical curvature) and across slope (along the elevation contour, i.e. the horizontal curvature); e.g., Linear (L), Convex (V) or Concave (C).')
    position = models.TextField(choices=POSITION, blank=True, null=True, db_comment='If the monitoring site lies in an uneven terrain, report the monitoring site position.')
    landform1 = models.TextField(choices=LANDFORMS, blank=True, null=True, db_comment='Landform1 type.')
    landform2 = models.TextField(choices=LANDFORMS, blank=True, null=True, db_comment='Landform2 type.')
    activity1 = models.TextField(choices=ACTIVITIES, blank=True, null=True, db_comment='Activity.')
    activity2 = models.TextField(choices=ACTIVITIES, blank=True, null=True, db_comment='Activity.')
    geo_descr = models.TextField(blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 's_landform_topography'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringCoarseFragments(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    total_area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    class1size = models.TextField(choices=SIZES, blank=True, null=True)
    class2size = models.TextField(choices=SIZES,  blank=True, null=True)
    class3size = models.TextField(choices=SIZES,  blank=True, null=True)
    class1area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    class2area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    class3area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 's_coarse_fragments'
        db_table_comment = 'Report the total percentage of the area that is covered by coarse surface fragments. In addition, report at least one and up to three size classes and report the percentage of the area that is covered by the coarse surface fragments of the respective size class, the dominant one first.\r\nClasses size are in p_coarse_size'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringClimateAndWeather(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    clim_koppen = models.TextField(choices=CLIMATE_KOPPEN, blank=True, null=True)
    eco_shultz = models.TextField(choices=ECOZONE_SHULTZ,   blank=True, null=True)
    season = models.TextField(choices=SEASON,   blank=True, null=True)
    curr_weath = models.TextField(choices=CURRENT_WEATHER,  blank=True, null=True)
    past_weath = models.TextField(choices=PAST_WEATHER,   blank=True, null=True)
    soil_temp = models.TextField(choices=SOIL_TEMP_REGIME,  blank=True, null=True)
    soil_moist = models.TextField(choices=SOIL_MOIST_REGIME,   blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 's_climate_weather'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringCultivated(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    type = models.TextField(choices=CULTIVATION_TYPE, blank=True, null=True, db_comment='value from p_cultivation_type ')
    actual1 = models.TextField(blank=True, null=True, db_comment='actual dominant specie')
    actual2 = models.TextField(blank=True, null=True, db_comment='actual second specie')
    actual3 = models.TextField(blank=True, null=True, db_comment='actual third specie')
    cessation = models.DateField(blank=True, null=True, db_comment='editable if last dominant specie is NOT NULL')
    area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    prod1_tech = models.TextField(choices=PROD_TECHNIQUES, blank=True, null=True, db_comment='Report the techniques that refer to the surrounding area of the soil monitoring site. If more than one type of technique is present, report in the array up to three, the dominant one first. Value from p_productivity_techniques')
    prod2_tech = models.TextField(choices=PROD_TECHNIQUES, blank=True, null=True)
    prod3_tech = models.TextField(choices=PROD_TECHNIQUES, blank=True, null=True)
    last1 = models.TextField(blank=True, null=True, db_comment="last dominant specie, editable if actual_species1 is NULL")
    last2 = models.TextField(blank=True, null=True, db_comment="Second last specie, editable if actual_species2 is NULL ")
    last3 = models.TextField(blank=True, null=True, db_comment="Third last specie, editable if actual_species3 is NULL ")
    rotation1 = models.TextField(blank=True, null=True, db_comment='Report the dominant specie that have been cultivated in the last five years in rotation with the actual or last species (the first is the most frequent)')
    rotation2 = models.TextField(blank=True, null=True, db_comment='Report the second specie that have been cultivated in the last five years in rotation with the actual or last species (the first is the mostfrequent)')
    rotation3 = models.TextField(blank=True, null=True, db_comment='Report the third specie that have been cultivated in the last five years in rotation with the actual or last species (the first is the mostfrequent)')
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 's_cultivated'
        db_table_comment = 'Report up to three actual cultivated species (in the array "actual_species") using the scientific name. If currently under fallow, report the up to 3 last species (in the array "last_species") and indicate month and year of harvest or of cultivation cessation. Insert the species in the sequence of the area covered starting with the species that covers the largest area. Report the up to 3 species that have been cultivated in the last five years in rotation with the actual or last species (1 is the most frequent) in the array column "rotational_species"'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
     
class MonitoringLandUse(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    land_use = models.TextField(choices=USES, blank=True, null=True)
    corine = models.TextField(choices=CORINE, blank=True, null=True)
    cultivated =  models.OneToOneField(MonitoringCultivated, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Cultivated Land')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_land_use'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
     
class MonitoringNotCultivated(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    landuse = models.ForeignKey(MonitoringLandUse, on_delete=models.CASCADE, related_name='monitoringnotcultivated_landuse_set')
    veget1 = models.TextField(choices=VEGETATION_TYPES, blank=True, null=True)
    veget2 = models.TextField(choices=VEGETATION_TYPES, blank=True, null=True)
    veget3 = models.TextField(choices=VEGETATION_TYPES, blank=True, null=True)
    stratum = models.TextField(choices=STRATUM )
    avg_height = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    max_height = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    area = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    species1 = models.TextField(blank=True, null=True)
    species2 = models.TextField(blank=True, null=True)
    species3 = models.TextField(blank=True, null=True)

    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_not_cultivated'
        unique_together = (('stratum', 'landuse'),)
        db_table_comment = 'For each monitoring  site, compile as many rows as the vegetation strata (STRATA_TYPES) are. Report the average height and the maximum height in m above ground for each stratum separately. Report the vegetation cover. For the upper stratum and the mid-stratum, report the percentage (by area) of the crown cover. For the ground stratum, report the percentage (by area) of the ground cover. Report up to three important species per stratum, e.g., Fagus orientalis. If you do not know the species, report the next higher taxonomic rank. The (maximum 3) species must be insert in the array column species.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringSurface(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    ground_form = models.TextField(choices=GROUND_FORMS, blank=True, null=True, db_comment='Patterned ground form field')
    tech_alter = models.TextField(choices=TECH_ALTERATIONS, blank=True, null=True)
    bedr_form = models.TextField(blank=True, null=True)
    bedr_lith = models.TextField(choices=PARENT_MATERIALS, blank=True, null=True)
    outc_area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    outc_dist = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    outc_size = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    ground_wat = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_positive], blank=True, null=True)
    wat_above = models.TextField(choices=WATER_ABOVE, blank=True, null=True)
    wat_drain = models.TextField(choices=DRAINAGE_CONDITIONS, blank=True, null=True)
    wat_repell = models.TextField(choices=WATER_REPELLENCE, blank=True, null=True)
    desert_ven = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    desert_var = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 's_surface'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringSurfaceCracks(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    width1 = models.TextField(choices=WIDTH_TYPES, blank=True, null=True)
    dist1 = models.TextField(choices=DISTANCE_TYPES, blank=True, null=True)
    spat_arr1 = models.TextField(choices=ARRANGEMENT, blank=True, null=True)
    persist1 = models.TextField(choices=PERSISTENCE, blank=True, null=True)
    width2 = models.TextField(choices=WIDTH_TYPES, blank=True, null=True)
    dist2 = models.TextField(choices=DISTANCE_TYPES, blank=True, null=True)
    spat_arr2 = models.TextField(choices=ARRANGEMENT, blank=True, null=True)
    persist2 = models.TextField(choices=PERSISTENCE, blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_surface_cracks'
        db_table_comment = 'For each monitoring  site, compile as many rows as the width classes are. If surface cracks are present, report the average width of the cracks. If the soil surface between cracks of larger width classes is regularly divided by cracks of smaller width classes, report the two width classes.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringLitterLayer(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    avg_thick = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    area = models.DecimalField(max_digits=12, decimal_places=6, validators=[validate_positive], blank=True, null=True)
    max_thick = models.DecimalField(max_digits=12, decimal_places=6, validators=[validate_positive], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_litter_layer'
        db_table_comment = 'Observe an area of 5 m x 5 m with the monitoring  site at its centre. Report the average and the maximum thickness of the litter layer in cm. If there is no litter layer, report 0 cm as thickness.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
 
class MonitoringSurfaceUnevenness(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    position = models.TextField(choices=PROFILE_POSITION, blank=True, null=True)
    nat_type = models.TextField(choices=NATURAL_TYPE, blank=True, null=True)
    nat_avg_h = models.DecimalField( max_digits=20, decimal_places=8, validators=[validate_positive], blank=True, null=True)
    nat_elev = models.DecimalField( max_digits=20, decimal_places=8, validators=[validate_positive], blank=True, null=True)
    nat_dist = models.DecimalField(max_digits=20, decimal_places=8, validators=[validate_positive], blank=True, null=True)
    hum_type1 = models.TextField(choices=HUMAN_MADE_TYPE, blank=True, null=True)
    hum_type2 = models.TextField(choices=HUMAN_MADE_TYPE, blank=True, null=True)
    hum_ter_h = models.DecimalField( max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    hum_noter_h = models.DecimalField( max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    hum_noter_w = models.DecimalField( max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    hum_noter_d = models.DecimalField( max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    ero_area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    ero_type = models.TextField(choices=EROSION_TYPE, blank=True, null=True)
    ero_degree = models.TextField(choices=EROSION_DEGREE, blank=True, null=True)
    ero_activ = models.TextField(choices=EROSION_ACTIVITY, blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_surface_unevenness'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringSurfaceCrusts(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    sealing1 = models.TextField(choices=SEALING_AGENT, blank=True, null=True)
    sealing2 = models.TextField(choices=SEALING_AGENT, blank=True, null=True)
    sealing3 = models.TextField(choices=SEALING_AGENT, blank=True, null=True)
    avg_thickn = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    

    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_surface_crusts'
        db_table_comment = 'A crust is a thin layer of soil constituents bound together into a horizontal mat or into small polygonal plates (see Schoeneberger et al., 2012). Soil crusts develop in the first mineral layer(s) and are formed by a sealing agent of physical, chemical and/or biological origin.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringGeneral(models.Model):
    id = models.TextField(primary_key=True, db_comment='monitoring site identifier')
    date = models.DateField(blank=True, null=True, db_comment='date of the description')
    surveyors = models.TextField(blank=True, null=True, db_comment='surveyors names comma separated')
    location = models.TextField(blank=True, null=True, db_comment='Name of the monitoring location')
    lat_wgs84 = models.DecimalField(max_digits=14, decimal_places=8, db_comment='WGS84 Latitude in decimal degree')
    lon_wgs84 = models.DecimalField(max_digits=14, decimal_places=8, db_comment='WGS84 Longitude in decimal degree')
    gps = models.BooleanField(blank=True, null=True, db_comment='is a gps acquisition?')
    elev_m_asl = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, db_comment='Altitude above the sea level in meter')
    elev_dem = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, db_comment='Altitude in meters retrived from a dem in meter')
    survey_m = models.TextField(choices=SURVEY_METHODS,  blank=True, null=True, db_comment='The code of the survey method')
    notes = models.TextField(blank=True, null=True)

    ## s_ploughing = models.TextField( blank=True, null=True, db_comment='')
    ## d_ploughing = models.TextField( blank=True, null=True, db_comment='')
    ## tillage = models.TextField( blank=True, null=True, db_comment='')
    ## use_inputs = models.TextField( blank=True, null=True, db_comment='')
    ## irrigation = models.TextField( blank=True, null=True, db_comment='')
    ## conserv_measure = models.TextField( blank=True, null=True, db_comment='')
    ## worm_casts = models.DecimalField( max_digits=6, decimal_places=0, validators=[validate_positive],db_comment='', blank=True, null=True)
    ## disturbed0_20 = models.BooleanField(blank=True, null=True, db_comment='')
    ## disturbed20_50 = models.BooleanField(blank=True, null=True, db_comment='')
    ## sampler_type = models.TextField( blank=True, null=True, db_comment='')
    ## indisturbed0_20_1 = models.BooleanField(blank=True, null=True, db_comment='')
    ## indisturbed0_20_2 = models.BooleanField(blank=True, null=True, db_comment='')
    ## indisturbed0_20_3 = models.BooleanField(blank=True, null=True, db_comment='')
    ## indisturbed20_50 = models.BooleanField(blank=True, null=True, db_comment='')
    
    cls_sys = models.TextField(choices=CLASSIFICATION_SYSTEMS, blank=True, null=True, db_comment='Classification system')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True, related_name='monitoringgeneral_project_set', db_comment='Survey/Project identifier')
    
    coarsefragments =  models.OneToOneField(MonitoringCoarseFragments, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Sample -Coarse Fragments')
    litterlayer =  models.OneToOneField(MonitoringLitterLayer, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Sample - Litter Layer')
    landuse =  models.OneToOneField(MonitoringLandUse, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Sample - Land Use ')
    surface =  models.OneToOneField(MonitoringSurface, on_delete=models.SET_DEFAULT,default=None, blank=True, null=True, db_comment='Sample - Surface ')
    surfacecracks =  models.OneToOneField(MonitoringSurfaceCracks, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Sample - Surface cracks')
    landformtopography = models.OneToOneField(MonitoringLandformTopography, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Sample - Landform Topography')
    climateandweather = models.OneToOneField(MonitoringClimateAndWeather, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Sample - Climate weather')
    surfaceunevenness =  models.OneToOneField(MonitoringSurfaceUnevenness, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Sample - Surface Unevenness')
    surfacecrusts = models.OneToOneField(MonitoringSurfaceCrusts, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Sample - Surface Crusts')   

    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'monitoring_general'
        db_table_comment = 'The Soil Monitoring main table'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )


###########################
# Sample Layer
###########################
class MonitoringLayerRemnants(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    abundance = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    cementing1 = models.TextField(choices=CEMENTING_AGENT, blank=True, null=True)
    cementing2 = models.TextField(choices=CEMENTING_AGENT, blank=True, null=True)
    size1 = models.TextField(choices=SIZE_SHAPE_TYPES, blank=True, null=True)
    size2 = models.TextField(choices=SIZE_SHAPE_TYPES, blank=True, null=True)
    abundance1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_remnants'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringLayerCoarseFragments(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    litho_type1 = models.TextField(choices=PARENT_MATERIALS, blank=True, null=True)
    litho_type2 = models.TextField(choices=PARENT_MATERIALS, blank=True, null=True)
    litho_type3 = models.TextField(choices=PARENT_MATERIALS, blank=True, null=True)
    litho_type4 = models.TextField(choices=PARENT_MATERIALS, blank=True, null=True)
    size1 = models.TextField(choices=SIZE_SHAPE_TYPES, blank=True, null=True)
    size2 = models.TextField(choices=SIZE_SHAPE_TYPES, blank=True, null=True)
    size3 = models.TextField(choices=SIZE_SHAPE_TYPES, blank=True, null=True)
    size4 = models.TextField(choices=SIZE_SHAPE_TYPES, blank=True, null=True)
    weath1 = models.TextField(choices=WEATHERING_STAGE, blank=True, null=True)
    weath2 = models.TextField(choices=WEATHERING_STAGE, blank=True, null=True)
    weath3 = models.TextField(choices=WEATHERING_STAGE, blank=True, null=True)
    weath4 = models.TextField(choices=WEATHERING_STAGE, blank=True, null=True)
    abundance1 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage], db_comment='Report the total percentage of the volume occupied by coarse fragments for class1.')
    abundance2 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage], db_comment='Report the total percentage of the volume occupied by coarse fragments for class2.')
    abundance3 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage], db_comment='Report the total percentage of the volume occupied by coarse fragments for class3.')
    abundance4 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage], db_comment='Report the total percentage of the volume occupied by coarse fragments for class4.')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_coarse_fragments'
        db_table_comment = 'Coarse fragments. A coarse fragment is a mineral particle, derived from the parent material, > 2 mm in its equivalent diameter'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
       
class MonitoringLayerArtefacts(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    abundance = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    black_carb = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    type1 = models.TextField(choices=ARTEFACT_TYPES, blank=True, null=True)
    type2 = models.TextField(choices=ARTEFACT_TYPES, blank=True, null=True)
    type3 = models.TextField(choices=ARTEFACT_TYPES, blank=True, null=True)
    type4 = models.TextField(choices=ARTEFACT_TYPES, blank=True, null=True)
    type5 = models.TextField(choices=ARTEFACT_TYPES, blank=True, null=True)
    size1 = models.TextField(choices=ARTEFACT_SIZES, blank=True, null=True)
    size2 = models.TextField(choices=ARTEFACT_SIZES, blank=True, null=True)
    size3 = models.TextField(choices=ARTEFACT_SIZES, blank=True, null=True)
    size4 = models.TextField(choices=ARTEFACT_SIZES, blank=True, null=True)
    size5 = models.TextField(choices=ARTEFACT_SIZES, blank=True, null=True)
    abundance1 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    abundance2 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    abundance3 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    abundance4 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    abundance5 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_artefacts'
        db_table_comment = 'Artefacts are solid or liquid substances that are: created or substantially modified by humans as part of an industrial or artisanal manufacturing process, or brought to the surface by human activity from a depth, where they were not influenced by surface processes, and deposited in an environment, where they do not commonly occur.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )


    """
    def clean(self):
            if self.type1 is not None and self.type1.startswith("l_artefacts."):
                    raise ValidationError({'type1': ('Wrong classification.')})
            if self.type2 is not None and self.type2.startswith("l_artefacts."):
                    raise ValidationError({'type2': ('Wrong classification.')})
            if self.type3 is not None and self.type3.startswith("l_artefacts."):
                    raise ValidationError({'type3': ('Wrong classification.')})
            if self.type4 is not None and self.type4.startswith("l_artefacts."):
                    raise ValidationError({'type4': ('Wrong classification.')})
            if self.type5 is not None and self.type5.startswith("l_artefacts."):
                    raise ValidationError({'type5': ('Wrong classification.')})
            if self.size_type1 is not None and self.size_type1.startswith("l_artefacts_size."):
                    raise ValidationError({'size_type1': ('Wrong classification.')})
            if self.size_type2 is not None and self.size_type2.startswith("l_artefacts_size."):
                    raise ValidationError({'size_type2': ('Wrong classification.')})
            if self.size_type3 is not None and self.size_type3.startswith("l_artefacts_size."):
                    raise ValidationError({'size_type3': ('Wrong classification.')})
            if self.size_type4 is not None and self.size_type4.startswith("l_artefacts_size."):
                    raise ValidationError({'size_type4': ('Wrong classification.')})
            if self.size_type5 is not None and self.size_type5.startswith("l_artefacts_size."):
                    raise ValidationError({'size_type5': ('Wrong classification.')})         
    """    

class MonitoringLayerCracks(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    persistenc = models.TextField(choices=CRACKS_PERSISTENCE, blank=True, null=True)
    continuity = models.TextField(choices=CRACKS_CONTINUITY, blank=True, null=True)
    avg_width = models.DecimalField(max_digits=16, decimal_places=2, validators=[validate_positive], blank=True, null=True)
    abundance = models.PositiveIntegerField(blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_cracks'
        db_table_comment = 'Report persistence and continuity'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
   
class MonitoringLayerStressFeatures(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    pressfaces = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Pressure faces in % of the surfaces of soil aggregates')
    slicksides = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Slickensides in % of the surfaces of soil aggregates.')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_stress_features'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

        db_table_comment = 'Stress features result from soil aggregates that are pressed against each other due to swelling clays. The aggregate surfaces may be shiny. There are two types: Pressure faces do not slide past each other and have no striations, slickensides slide past each other and have striations.'

class MonitoringLayerMatrixColours(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    munsell_m1 = models.TextField(blank=True, null=True)
    munsell_d1 = models.TextField(blank=True, null=True)
    area1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    munsell_m2 = models.TextField(blank=True, null=True)
    munsell_d2 = models.TextField(blank=True, null=True)
    area2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    munsell_m3 = models.TextField(blank=True, null=True)
    munsell_d3 = models.TextField(blank=True, null=True)
    area3 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_matrix_colour'
        db_table_comment = 'Report the colour of the soil matrix. If there is more than one matrix colour, report up to three, the dominant one first, and give the percentage of the exposed area'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringLayerCoarserTextured(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    coars_text = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='the percentage (by exposed area) occupied by coarser-textured parts of any orientation (vertical, horizontal, inclined) having a width of ≥ 0.5 cm')
    v_tongues = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='the percentage (by exposed area) occupied by continuous vertical tongues of coarser-textured parts with a horizontal extension of ≥ 1 cm (if these tongues are absent, report 0%)')
    depth = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='the depth range in cm, where these tongues cover ≥ 10% of the exposed area (if they extend across several layers, the length is only reported in the description of that layer, where they start at the layer’s upper limit).')
    h_area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='In the middle of the layer, prepare a horizontal surface, 50 cm x 50 cm, and report the percentage (by horizontal area covered) of the coarser-textured parts.')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_coarser_textured'
        db_table_comment = 'If a layer consists of darker-coloured finer-textured and lighter-coloured coarser-textured parts that do not form horizontal layers but can easily be distinguished, describe them separately'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringLayerLithogenicVariegates(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier') 
    munsell_m1 = models.TextField(blank=True, null=True)
    size1 = models.TextField(choices=LITHOGENIC_SIZES, blank=True, null=True)
    area1 = models.DecimalField(max_digits=6 , decimal_places=2 , validators=[validate_percentage],  blank=True, null=True)
    munsell_m2 = models.TextField(blank=True, null=True)
    size2 = models.TextField(choices=LITHOGENIC_SIZES, blank=True, null=True)
    area2 = models.DecimalField(max_digits=6 , decimal_places=2 , validators=[validate_percentage],  blank=True, null=True)
    munsell_m3 = models.TextField(blank=True, null=True)
    size3 = models.TextField(choices=LITHOGENIC_SIZES, blank=True, null=True)
    area3 = models.DecimalField(max_digits=6 , decimal_places=2 , validators=[validate_percentage],  blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_lithogenic_variegates'
        db_table_comment = 'Report colour, size class, and abundance. If more than one colour occurs, report up to three, the dominant one first, and give size class and abundance for each colour separately.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
          
class MonitoringLayerRedoximorphicFeatures(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    oxi_inner = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    oxi_outer = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    oxi_random = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    red_inner = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    red_outer = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    red_random = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abund_oxi = models.DecimalField(max_digits=12, decimal_places=4, validators=[validate_percentage], db_comment='Abundance of cemented oximorphic features, by volume [%]')
    
    #redoximorphic_colour_redoximorphic_features_set from LayerRedoximorphicColour
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_redoximorphic'
        db_table_comment = ''
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringLayerRedoximorphicColour(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    features = models.ForeignKey(MonitoringLayerRedoximorphicFeatures, on_delete=models.CASCADE, related_name='monitoringlayerredoximorphiccolour_features_set', db_comment='LayerRedoximorphicFeatures')  
    colour_nr = models.SmallIntegerField(validators=[validate_positive], db_comment='layer redoximorphic colour number')
    munsell_m = models.TextField(blank=True, null=True)
    munsell_d = models.TextField(blank=True, null=True)
    substance = models.TextField(choices=REDOXIMORPHIC_SUBSTANCES, blank=True, null=True)
    location = models.TextField(choices=REDOXIMORPHIC_LOCATIONS,blank=True, null=True)
    size1 = models.TextField(choices=OXIMORPHIC_SIZES,blank=True, null=True)
    size2 = models.TextField(choices=OXIMORPHIC_SIZES,blank=True, null=True)
    mottles_c = models.TextField(choices=MOTTLES_CONTRAST,blank=True, null=True)
    mottles_b = models.TextField(choices=MOTTLES_BOUNDARY_TYPES,blank=True, null=True)
    cement = models.TextField(choices=OXIMORPHIC_CEMENTATION,blank=True, null=True)
    area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_redoximorphic_colour'
        db_table_comment = 'Report the colour according to the Munsell Color Charts'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
  
class MonitoringLayerCoatingsBridges(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    clay_coat = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of clay coatings in percentage')
    form_coat = models.TextField(choices=FORM_COATINGS, blank=True, null=True, db_comment='refer to clay coatings')
    org_coat = models.TextField(choices=ORGANIC_COATINGS, blank=True, null=True, db_comment='Organic matter coatings and oxide coatings on sand and/or coarse silt grains')
    crack_coat = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of cracked coatings in percentage')
    clay_bridg = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of clay bridges in percentage')
    form_bridg = models.TextField(choices=FORM_COATINGS, blank=True, null=True, db_comment='refer to clay bridge')
    form_org = models.TextField(choices=FORM_COATINGS, blank=True, null=True, db_comment='refer to organic matter coatings and oxide coatings (report only if matrix colour value ≤ 3)')
    sand_silt = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of uncoated sand and coarse silt grains in percentage')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_coatings_bridges'
        db_table_comment = 'Report the abundance of clay coatings in % of the surfaces of soil aggregates, coarse fragments and/or biopore walls clay bridges between sand grains in % of involved sand grains.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
                  
class MonitoringLayerRibbonlikeAccumulations(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    substances = models.TextField(choices=RIBBONLIKE_SUBSTANCES, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    comb_thick = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_positive], blank=True, null=True, db_comment='If there are 2 or more ribbon-like accumulations in one layer, report the number of the accumulations and their combined thickness in cm')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_ribbonlike_accumulations'
        db_table_comment = 'Ribbon-like accumulations are thin, horizontally continuous accumulations within the matrix of another layer. Report the accumulated substance(s).'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
           
class MonitoringLayerCarbonates(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    matr_c = models.TextField(choices=CARBONATE_CONTENTS, blank=True, null=True)
    matr_c_ret = models.TextField(choices=RETARDED_REACTION, blank=True, null=True)
    sec_type1 = models.TextField(choices=SECONDARY_CARBONATE_TYPES, blank=True, null=True)
    sec_type2 = models.TextField(choices=SECONDARY_CARBONATE_TYPES, blank=True, null=True)
    sec_type3 = models.TextField(choices=SECONDARY_CARBONATE_TYPES, blank=True, null=True)
    sec_type4 = models.TextField(choices=SECONDARY_CARBONATE_TYPES, blank=True, null=True)
    sec_size1 = models.TextField(choices=MINERAL_SIZES, blank=True, null=True)
    sec_size2 = models.TextField(choices=MINERAL_SIZES, blank=True, null=True)
    sec_size3 = models.TextField(choices=MINERAL_SIZES, blank=True, null=True)
    sec_size4 = models.TextField(choices=MINERAL_SIZES, blank=True, null=True)
    sec_shape1 = models.TextField(choices=MINERAL_SHAPES, blank=True, null=True)
    sec_shape2 = models.TextField(choices=MINERAL_SHAPES, blank=True, null=True)
    sec_shape3 = models.TextField(choices=MINERAL_SHAPES, blank=True, null=True)
    sec_shape4 = models.TextField(choices=MINERAL_SHAPES, blank=True, null=True)
    sec_abund1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    sec_abund2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    sec_abund3 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    sec_abund4 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_carbonates'
        db_table_comment = 'Layer Carbonates'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringLayerGypsum(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    content = models.TextField(choices=GYPSUM_CONTENT_TYPES, blank=True, null=True)
    sec_gypsum = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    sgypsum1 = models.TextField(choices=SGYPSUM_TYPES, blank=True, null=True)
    sgypsum2 = models.TextField(choices=SGYPSUM_TYPES, blank=True, null=True)
    type1_size = models.TextField(choices=MINERAL_SIZES, blank=True, null=True)
    type2_size = models.TextField(choices=MINERAL_SIZES, blank=True, null=True)
    type1_shape = models.TextField(choices=MINERAL_SHAPES, blank=True, null=True)
    type2_shape = models.TextField(choices=MINERAL_SHAPES, blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_gypsum'
        db_table_comment = 'Report the gypsum content in the soil matrix. If readily soluble salts are absent or present in small amounts only, gypsum can be estimated by measuring the electrical conductivity in soil suspensions of different soil-water relations after 30 minutes (in the case of fine-grained gypsum). This method detects primary and secondary gypsum. Note: Higher gypsum contents may be differentiated by abundance of H2O-soluble pseudomycelia/crystals and a soil colour with high value and low chroma'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringLayerSecondarySilica(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    type1 = models.TextField(choices=SECONDARY_SILICA_TYPES, blank=True, null=True, db_comment='Report the type of secondary silica, type1 is dominant')
    type2 = models.TextField(choices=SECONDARY_SILICA_TYPES, blank=True, null=True, db_comment='Report the type of secondary silica')
    dnfcsize1 = models.TextField(choices=DNFC_SIZES, blank=True, null=True, db_comment='If a layer shows durinodes and/or remnants of a layer that has been cemented by secondary silica, report their size class for type1')
    dnfcsize2 = models.TextField(choices=DNFC_SIZES, blank=True, null=True, db_comment='If a layer shows durinodes and/or remnants of a layer that has been cemented by secondary silica, report their size class for type2')
    abund = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Report the total percentage (by exposed area) of secondary silica')
    abund_dnfc = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='If a layer shows durinodes and/or remnants of a cemented layer, report in addition the percentage (by volume) of those durinodes and remnants that have a diameter ≥ 1 cm')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_secondary_silica'
        db_table_comment = 'Secondary silica (SiO2) is off-white and predominantly consisting of opal and microcrystalline forms. It occurs as laminar caps, lenses, (partly) filled interstices, bridges between sand grains, and as coatings at surfaces of soil aggregates, biopore walls, coarse fragments, and remnants of broken-up cemented layers. Report the type of secondary silica. If more than one type occurs, report up to two, the dominant one first.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringLayerConsistence(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    cement = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Report the percentage (by volume, related to the whole soil) of the layer that is cemented.')
    cement_ag1 = models.TextField(choices=CEMENTING_AGENTS, blank=True, null=True, db_comment='Report the cementing agents')
    cement_ag2 = models.TextField(choices=CEMENTING_AGENTS, blank=True, null=True)
    cement_ag3 = models.TextField(choices=CEMENTING_AGENTS, blank=True, null=True)
    cement_cls = models.TextField(choices=CEMENTATION_CLASSES, blank=True, null=True)
    rrclass_m = models.TextField(choices=RRCLASSES_MOIST, blank=True, null=True, db_comment='Rupture resistance, non-cemented soil moist')
    rrclass_d = models.TextField(choices=RRCLASSES_DRY, blank=True, null=True, db_comment='Rupture resistance, non-cemented soil dry')
    susceptib = models.TextField(choices=SUSCEPTIBILITY, blank=True, null=True, db_comment='Some layers are prone to cementation after repeated drying and wetting. Report the susceptibility')
    m_failure = models.TextField(choices=MANNER_FAILURE, blank=True, null=True, db_comment='Report the manner of failure (brittleness)')
    plastic = models.TextField(choices=PLASTICITY, blank=True, null=True, db_comment='Plasticity is the degree to which reworked soil can be permanently deformed without rupturing')
    penet_res = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    stickiness = models.TextField(choices=STICKINESS, blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_consistence'
        db_table_comment = 'Consistence is the degree and kind of cohesion and adhesion that soil exhibits. Consistence is reported separately for cemented and non-cemented (parts of) layers. If a specimen of soil does not fall into pieces by applying low forces, one has to check, whether it is cemented'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringLayerPermafrostFeatures(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    cry_alter1 = models.TextField(choices=CRYOGENIC_ALTERATION, blank=True, null=True)
    cry_alter2 = models.TextField(choices=CRYOGENIC_ALTERATION, blank=True, null=True)
    cry_alter3 = models.TextField(choices=CRYOGENIC_ALTERATION, blank=True, null=True)
    permafrost = models.TextField(choices=PERMAFROST_TYPE, blank=True, null=True)
    cry_abund1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    cry_abund2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    cry_abund3 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_permafrost_features'
        db_table_comment = 'Estimate the total percentage (by exposed area, related to the whole soil) affected by cryogenic alteration. Report up to three features, the dominant one first, and report the percentage for each feature separately.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringLayerOrganicCarbon(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    contentmin = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    contentmax = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    nat_accum1 = models.TextField(choices=ACCUMULATION_TYPES, blank=True, null=True)
    nat_accum2 = models.TextField(choices=ACCUMULATION_TYPES, blank=True, null=True)
    nat_accum3 = models.TextField(choices=ACCUMULATION_TYPES, blank=True, null=True)
    abundance1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance3 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    black_carb = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_organic_carbon'
        db_table_comment = 'Report the estimated organic carbon content. It is based on the Munsell value, moist, and the texture'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
 
class MonitoringLayerRoots(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    a_lt2mm = models.TextField(choices=ROOT_ABUNDANCE_CLASSES, blank=True, null=True, db_comment='diameter <= 2mm')
    a_lt05mm = models.TextField(choices=ROOT_ABUNDANCE_CLASSES, blank=True, null=True, db_comment='diameter < 0,5mm')
    a_05to2mm = models.TextField(choices=ROOT_ABUNDANCE_CLASSES, blank=True, null=True, db_comment='diameter from 0.5 to 2 mm')
    a_gt2mm = models.TextField(choices=ROOT_ABUNDANCE_CLASSES, blank=True, null=True, db_comment='diameter > 2mm')
    a_2to5mm = models.TextField(choices=ROOT_ABUNDANCE_CLASSES, blank=True, null=True, db_comment='diameter from 2 to 5 mm')
    a_gt5mm = models.TextField(choices=ROOT_ABUNDANCE_CLASSES, blank=True, null=True, db_comment='diameter > 5mm')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_roots'
        db_table_comment = 'Count the number of roots per dm2, separately for the six diameter classes, and report the abundance classes'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringLayerAnimalActivity(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    type1 = models.TextField(choices=ANIMAL_ACTIVITY_TYPES, blank=True, null=True)
    type2 = models.TextField(choices=ANIMAL_ACTIVITY_TYPES, blank=True, null=True)
    type3 = models.TextField(choices=ANIMAL_ACTIVITY_TYPES, blank=True, null=True)
    type4 = models.TextField(choices=ANIMAL_ACTIVITY_TYPES, blank=True, null=True)
    type5 = models.TextField(choices=ANIMAL_ACTIVITY_TYPES, blank=True, null=True)
    mammal = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    bird = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    worm = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    insect = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    unspecify = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_animal_activity'
        db_table_comment = 'Report the animal activity that has visibly changed the features of the layer. If applicable, report up to 5 types, the dominant one first. Report the percentage (by exposed area), separately for mammal activity, bird activity, worm activity, insect activity and unspecified activity'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringLayerHumanAlterations(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    nat_mat1 =models.TextField(choices=NATURAL_MATERIAL_TYPES, blank=True, null=True)
    nat_mat2 = models.TextField(choices=NATURAL_MATERIAL_TYPES, blank=True, null=True)
    nat_mat3 = models.TextField(choices=NATURAL_MATERIAL_TYPES, blank=True, null=True)
    abundance1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance3 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    texture = models.TextField(choices=TEXTURE_CLASSES, blank=True, null=True)
    carbonate = models.TextField(choices=SECONDARY_CARBONATE_TYPES, blank=True, null=True)
    carbon = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    alter1 = models.TextField(choices=ALTERATIONS_TYPES,  blank=True, null=True)
    alter2 = models.TextField(choices=ALTERATIONS_TYPES, blank=True, null=True)
    aggregate = models.TextField(choices=AGGREGATE_FORMATION, blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_human_alterations'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringLayerDegreeDecomposition(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    vis_plant = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    sbdiv_horz = models.TextField(choices=SUBDVISION_HORIZON, blank=True, null=True)
    plant_res1 = models.TextField(choices=DEAD_PLANT_TYPES, blank=True, null=True)
    plant_res2 = models.TextField(choices=DEAD_PLANT_TYPES, blank=True, null=True)
    abundance1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_degree_decomposition'
        db_table_comment = 'Refer to the transformation of visible plant tissues into visibly homogeneous organic matter.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringLayerNonMatrixPore(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    type1 = models.TextField(choices=NONMATRIX_PORES_TYPES, blank=True, null=True)
    size1 = models.TextField(choices=PORE_SIZES, blank=True, null=True)
    abund1 = models.TextField(choices=PORE_ABUNDANCE, blank=True, null=True)
    type2 = models.TextField(choices=NONMATRIX_PORES_TYPES, blank=True, null=True)
    size2 = models.TextField(choices=PORE_SIZES, blank=True, null=True)
    abund2 = models.TextField(choices=PORE_ABUNDANCE, blank=True, null=True)
    type3 = models.TextField(choices=NONMATRIX_PORES_TYPES, blank=True, null=True)
    size3 = models.TextField(choices=PORE_SIZES, blank=True, null=True)
    abund3 = models.TextField(choices=PORE_ABUNDANCE, blank=True, null=True)
    type4 = models.TextField(choices=NONMATRIX_PORES_TYPES, blank=True, null=True)
    size4 = models.TextField(choices=PORE_SIZES, blank=True, null=True)
    abund4 = models.TextField(choices=PORE_ABUNDANCE, blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_nonmatrix_pore'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringLayer(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    site = models.ForeignKey(MonitoringGeneral, on_delete=models.CASCADE, related_name='monitoringlayer_site_set', db_comment='Foreign Key field: site') 
    design = models.TextField(db_comment='layer horizon designation')
    number = models.SmallIntegerField(validators=[validate_positive], db_comment='layer order in monitoring site')
    upper = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_positive], db_comment='upper depth in cm',blank=True, null=True)
    lower = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_positive], db_comment='lower depth in cm',blank=True, null=True)
    lower_bound = models.TextField(db_comment='layer lower boundary', blank=True, null=True )
    hom_part = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Described parts, by exposed area [%]')
    hom_alluvt = models.TextField(choices=ALLUVIAL_TEPHRA, blank=True, null=True, db_comment='Layer composed of several strata of alluvial sediments or of tephra')
    wat_satur = models.TextField(choices=WATER_SATURATION, blank=True, null=True, db_comment='Types of water saturation')
    wat_status = models.TextField(choices=WATER_STATUS, blank=True, null=True, db_comment='Soil water status')
    o_mineral =  models.TextField(choices=ORGANIC_MINERAL_TYPES, blank=True, null=True, db_comment='organic, organotechnic or mineral layer')
    bounddist = models.TextField(choices=BOUNDARIES, blank=True, null=True, db_comment="Distinctness of the layer's lower boundary")
    boundshape = models.TextField(choices=SHAPE_TYPES, blank=True, null=True)
    wind = models.TextField(choices=WIND, blank=True, null=True, db_comment='Wind deposition')
    tex_cls = models.TextField(choices=TEXTURE_CLASSES, blank=True, null=True, db_comment='Texture class') 
    tex_subcls = models.TextField(choices=TEXTURE_SUBCLASSES, blank=True, null=True, db_comment='Texture subclass')
    struct_w_s = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Structure Wedge-shaped aggregates tilted between ≥ 10° and ≤ 60° from the horizontal: abundance, by volume [%]')
    rh_value = models.TextField(choices=RH_VALUE, blank=True, null=True, db_comment='Rh Value')
    weathering = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Initial weathering abundance')
    sol_salts = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='ECSE [dS m-1m-1]')
    ph_value = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, db_comment='Potentiometric pH measurement - Measured value')
    ph_solution = models.TextField(choices=POTENZIOMETRIC_MEASURES, blank=True, null=True, db_comment='Potentiometric pH measurement - Solution and mixing ratio')
    fracts = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    avg_fracts = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    volc_abund = models.TextField(choices=ABUNDANCE_PARTICLES_TYPES, blank=True, null=True)
    volc_thnaf = models.TextField(choices=THIXOTROPY_NAF, blank=True, null=True)
    bulk_dens = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    pack_dens = models.TextField(choices=PACKING_DENSITIES, blank=True, null=True, db_comment='Estimate the packing density using a knife with a blade approx. 10 cm long')
    parent_mat = models.TextField(choices=PARENT_MATERIALS, blank=True, null=True, db_comment='Report the parent material. Use the help of a geological map.')
    note = models.TextField(blank=True, null=True)

    remnants = models.OneToOneField(MonitoringLayerRemnants, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Remnants of broken-up cemented layers')
    coarsefragments = models.OneToOneField(MonitoringLayerCoarseFragments, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Coarse fragments')
    artefacts = models.OneToOneField(MonitoringLayerArtefacts, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Artefacts')
    cracks = models.OneToOneField(MonitoringLayerCracks, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Cracks')
    stressfeatures = models.OneToOneField(MonitoringLayerStressFeatures, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Stress Features')
    coatingsbridges = models.OneToOneField(MonitoringLayerCoatingsBridges, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerCoatingsBridges')
    ribbonlikeaccumulations = models.OneToOneField(MonitoringLayerRibbonlikeAccumulations, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerRibbonlikeAccumulations')
    carbonates = models.OneToOneField(MonitoringLayerCarbonates, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Section Layer Carbonates')
    gypsum = models.OneToOneField(MonitoringLayerGypsum, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerGypsum')
    secondarysilica = models.OneToOneField(MonitoringLayerSecondarySilica, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerSecondarySilica')
    consistence = models.OneToOneField(MonitoringLayerConsistence, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerConsistence')
    permafrost =  models.OneToOneField(MonitoringLayerPermafrostFeatures, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerPermafrostFeatures')   
    organiccarbon =  models.OneToOneField(MonitoringLayerOrganicCarbon, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerOrganicCarbon')   
    roots =  models.OneToOneField(MonitoringLayerRoots, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerRoots')   
    animalactivity  =  models.OneToOneField(MonitoringLayerAnimalActivity, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerAnimalActivity')   
    humanalterations =  models.OneToOneField(MonitoringLayerHumanAlterations, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerHumanAlterations')   
    degreedecomposition =  models.OneToOneField(MonitoringLayerDegreeDecomposition, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerDegreeDecomposition')   
    nonmatrixpore = models.OneToOneField(MonitoringLayerNonMatrixPore, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerNonMatrixPore')   
    matrixcolours = models.OneToOneField(MonitoringLayerMatrixColours, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Matrix colour')   
    texturecolour = models.OneToOneField(MonitoringLayerCoarserTextured, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Combinations of darker-coloured finer-textured and lighter-coloured coarser-textured parts')
    lithogenicvariegates = models.OneToOneField(MonitoringLayerLithogenicVariegates, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerLithogenicVariegates')
    redoximorphicfeatures = models.OneToOneField(MonitoringLayerRedoximorphicFeatures, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerRedoximorphicFeatures')
    
    ## layerstructure_layer_set LayerStructure

    def _get_thickness(self):
        if self.lower and self.upper: 
            return self.lower - self.upper
        else: return None
    thickness = property(_get_thickness)   
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 's_layer'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class MonitoringLayerStructure(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')  
    layer = models.ForeignKey(MonitoringLayer, on_delete=models.CASCADE, related_name='monitoringlayerstructure_layer_set', db_comment='Sample Layer' )
    level = models.TextField(choices=STRUCTURE_LEVELS, blank=True, null=True)
    type = models.TextField(choices=STRUCTURE_TYPES, blank=True, null=True)
    grade = models.TextField(choices=STRUCTURE_GRADES, blank=True, null=True)
    penetrab = models.TextField(choices=AGGREGATE_PENETRABILITY, blank=True, null=True)
    size1 = models.TextField(choices=AGGREGATE_SIZES, blank=True, null=True)
    size2 = models.TextField(choices=AGGREGATE_SIZES, blank=True, null=True)
    abundance_vol = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_layer_structure_types'
        unique_together = (('layer', 'level'),)
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

#########################################
## Monitoring Lab Data 
#########################################

class MonitoringLabData(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    site = models.ForeignKey(MonitoringGeneral, on_delete=models.CASCADE, related_name='monitoringlabdata_site_set', db_comment='Foreign Key field: monitoring site') 
    upper = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_positive], db_comment='upper depth in cm',blank=True, null=True)
    lower = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_positive], db_comment='lower depth in cm',blank=True, null=True)
    gravel = models.DecimalField(max_digits=40, decimal_places=6, validators=[validate_percentage],  db_comment='Gravel content (%)' , blank=True, null=True)
    cls_sys =  models.TextField(choices=CLASSIFICATION_SYSTEMS, db_comment='Classification system used for texture of fine earth', blank=True, null=True)
    texture = models.TextField(choices=TEXTURE_CLASSES, db_comment='texture class', blank=True, null=True)      
    sand = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Sand  (percentage of the fine earth)', blank=True, null=True)
    v_c_sand = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage],db_comment='Very coarse sand (percentage of the fine earth)', blank=True, null=True)
    c_sand = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage],db_comment='Coarse sand (percentage of the fine earth)', blank=True, null=True)
    m_sand = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage],db_comment='Medium sand (percentage of the fine earth)', blank=True, null=True)
    f_sand = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage],db_comment='Fine sand (percentage of the fine earth)', blank=True, null=True)
    v_f_sand  = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Very Fine sand (percentage of the fine earth)', blank=True, null=True)
    met_sand = models.TextField(choices=SAND_CONTENT_METHODS, blank=True, null=True)
    silt = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Silt (percentage of the fine earth)', blank=True, null=True)
    c_silt = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Coarse silt (percentage of the fine earth)', blank=True, null=True)
    f_silt = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Fine silt  (percentage of the fine earth)', blank=True, null=True)
    met_silt = models.TextField(choices=SILT_CLAY_CONTENT_METHODS,  blank=True, null=True)
    clay = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Clay  (percentage of the fine earth)', blank=True, null=True)
    met_clay = models.TextField(choices=SILT_CLAY_CONTENT_METHODS, blank=True, null=True)
    bulk_dens = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Bulk density (g/cm3)'	, blank=True, null=True)
    el_cond = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Electric conductivity (dS/m)', blank=True, null=True)
    met_el_cond = models.TextField(choices=EL_CONDUCTIVITY_PH_METHODS, db_comment='Method used for Electric conductivity', blank=True, null=True)
    hy_cond = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Hydraulic conductivity at saturation (mm/h)', blank=True, null=True)
    met_hy_cond = models.TextField(choices=HIDRAULIC_CONDUCTIVITY_METHODS, db_comment='Method used for Hydraulic conductivity at saturation', blank=True, null=True)
    satur = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Saturation (percentage)', blank=True, null=True)
    field_cap = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Field capacity (percentage)', blank=True, null=True)
    wilting_p = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Wilting point (percentage)', blank=True, null=True)
    met_s_f_w = models.TextField(choices=WILTING_POINT_METHODS, db_comment='Method used for saturation, field capacity, wilting point', blank=True, null=True)
    acidity = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Soil acidity: Exchangeable Al (meq/100g)', blank=True, null=True)
    met_acidity = models.TextField(db_comment='Method used for Soil acidity: Exchangeable Al (meq/100g)', blank=True, null=True)
    ph_h2o = models.DecimalField( max_digits=30, decimal_places=10, db_comment='pH (H2O)', blank=True, null=True)
    met_ph_h20 = models.TextField(choices=EL_CONDUCTIVITY_PH_METHODS, db_comment='Method used for pH (H2O)', blank=True, null=True)
    ph_kcl = models.DecimalField( max_digits=30, decimal_places=10, db_comment='pH (KCl)', blank=True, null=True)
    met_ph_kcl = models.TextField(choices=EL_CONDUCTIVITY_PH_METHODS, db_comment='Method used for pH (KCl)', blank=True, null=True)
    ph_ccl = models.DecimalField( max_digits=30, decimal_places=10, db_comment='pH (CaCl2)', blank=True, null=True)
    met_ph_ccl = models.TextField(choices=EL_CONDUCTIVITY_PH_METHODS, db_comment='Method used for pH (CaCl2)',  blank=True, null=True)
    org_car = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Organic Carbon content (g/kg)', blank=True, null=True)
    met_org_car = models.TextField( choices=ORGANIC_CARBON_METHODS, db_comment='Method used for Organic Carbon content', blank=True, null=True)
    org_mat = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Organic matter content (percentage)', blank=True, null=True)
    met_org_mat = models.TextField(choices=ORGANIC_MATTER_CONTENT_METHODS, db_comment='Method used for organic matter content', blank=True, null=True)
    caco3 = models.DecimalField( max_digits=30, decimal_places=10, db_comment='CaCO3 content (percentage)', blank=True, null=True)
    met_caco3 = models.TextField(choices=CACO3_CONTENT_METHODS, db_comment='Method used CaCO3 content',  blank=True, null=True)
    gypsum = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Gypsum content (percentage)', blank=True, null=True)
    met_gypsum = models.TextField(choices=GYPSUM_CONTENT_METHODS, db_comment='Method used for Gypsum content',  blank=True, null=True)
    cec = models.DecimalField( max_digits=30, decimal_places=10, db_comment='CEC (cmol/Kg)', blank=True, null=True)
    met_cec = models.TextField(choices=CEC_CA_MG_NA_K_METHODS, db_comment='Method used for CEC',  blank=True, null=True)
    ca = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Ca++ (cmol/Kg)', blank=True, null=True)
    met_ca = models.TextField(choices=CEC_CA_MG_NA_K_METHODS, db_comment='Method used for Ca++', blank=True, null=True)
    mg = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Mg++ (cmol/Kg)', blank=True, null=True)
    met_mg = models.TextField(choices=CEC_CA_MG_NA_K_METHODS, db_comment='Method used for Mg++',  blank=True, null=True)
    na = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Na+ (cmol/Kg)', blank=True, null=True)
    met_na = models.TextField(choices=CEC_CA_MG_NA_K_METHODS, db_comment='Method used for Na+',  blank=True, null=True)
    k = models.DecimalField( max_digits=30, decimal_places=10, db_comment='K+ (cmol/Kg)', blank=True, null=True)
    met_k = models.TextField(choices=CEC_CA_MG_NA_K_METHODS, db_comment='Method used for K+',  blank=True, null=True)
    n_tot = models.DecimalField( max_digits=30, decimal_places=10, db_comment='N tot content (g/Kg)', blank=True, null=True)
    met_n_tot = models.TextField(choices=N_CONTENT_METHODS, db_comment='Method used for N tot content',  blank=True, null=True)
    p_cont = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Available P content(mg/kg)', blank=True, null=True)
    met_p_cont = models.TextField(choices=P_CONTENT_METHODS, db_comment='Method used for available P content',  blank=True, null=True)
    feox = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Feox (g/kg)', blank=True, null=True)
    fed = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Fed (g/kg)', blank=True, null=True)
    fep = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Fep (g/kg)', blank=True, null=True)
    fe_tot = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Fe tot (g/kg)', blank=True, null=True)
    mn = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Mn (mg/kg)', blank=True, null=True)
    met_mn = models.TextField(choices=MN_ZN_CU_METHODS, db_comment='Method used for Mn', blank=True, null=True)
    zn = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Zn (mg/kg)', blank=True, null=True)
    met_zn = models.TextField(choices=MN_ZN_CU_METHODS, db_comment='Method used for Zn', blank=True, null=True)
    cu = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Cu (mg/kg)', blank=True, null=True)
    met_cu = models.TextField(choices=MN_ZN_CU_METHODS, db_comment='Method used for Cu', blank=True, null=True) 
    act_caco3 = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Active CaCO3 (%)', blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 's_lab_data'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )


## All the Indicators are preconfigured and stored in Geonode
## new Indicator 
class Indicator(models.Model):
    INDICATOR_DOMAINS = []
    INDICATOR_TYPES = []
    INDICATOR_MEASURES = []

    id = models.TextField(primary_key=True, db_comment='identifier')    
    name = models.TextField( db_comment='Name') 
    creation = models.DateField( blank=True, null=True, db_comment='Date of the creation')
    description = models.TextField( db_comment='Description') 
    domain = models.TextField(choices=INDICATOR_DOMAINS, db_comment='Type of the indicator', blank=True, null=True)
    type = models.TextField(choices=INDICATOR_TYPES, db_comment='Type of the indicator', blank=True, null=True)
    measure = models.TextField(choices=INDICATOR_MEASURES, db_comment='Type of the indicator', blank=True, null=True)
    keywords = models.TextField( db_comment='Geonode dataset id')

    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'indicators'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class Request(models.Model):
    REQUEST_STATUS = []
    user = models.TextField( db_comment='Identifier of the User')
    username = models.TextField( db_comment='Name of the User')
    useremail = models.TextField( db_comment='Email of the User')
    creation = models.DateField( db_comment='Creation date')
    mgr = models.TextField( db_comment='Assigned To - Id')
    mgrname = models.TextField( db_comment='Assigned To - Name')
    mgremail = models.TextField( db_comment='Assigned To - Email')
    mgrmsg  = models.TextField( db_comment='Message to the user')
    type = models.TextField( db_comment='Data type: Profiles/Samples/Indicator')
    dataid = models.TextField( db_comment='Data keys: fields of Profile, Sample or an Indicator id')
    purpose = models.TextField( db_comment='Purpose')
    aoi = models.JSONField( db_comment='AOI in geoJSON format') 
    anchor = models.JSONField( db_comment='AOI anchor in geoJSON format') 
    datefrom = models.DateField( db_comment='Date of the creation', blank=True, null=True)
    dateto = models.DateField( db_comment='Date of the creation', blank=True, null=True)
    depth = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_positive], blank=True, null=True)
    cancelled = models.BooleanField(blank=True, null=True, db_comment='Request cancelled')
    status = models.TextField(choices=REQUEST_STATUS, db_comment='status of Request', blank=True, null=True)
    geonode = models.TextField( db_comment='Geonode Dataset Id', blank=True, null=True)   
    
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'requests'
        permissions = (
            ('access', 'Can access backoffice data'),
            ('view', 'Can view backoffice data'),
            ('write', 'Can write backoffice data'),
        )

