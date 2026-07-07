from django.db import migrations
  
SQL_CREATE = f"""
-- ISO 28258
-- 
--1) unit_of_measure
CREATE OR REPLACE VIEW iso28258_unit_of_measure AS
SELECT id as unit_of_measure_id, value as label, uri 
FROM taxonomy_value 
WHERE taxonomy_id = 'MEASURE_UNITS'

--2)procedure_desc_id WRB fourth edition 2022
CREATE TABLE iso28258_procedure_desc (
    procedure_desc_id text NOT NULL,
    reference character varying,
    uri character varying NOT NULL
);
fixture: 
'WRB fourth edition 2022', 'WRB fourth edition 2022', 'https://www.fao.org/soils-portal/data-hub/soil-classification/world-reference-base/en/'
\.

--3)
CREATE TABLE iso28258_property_desc (
    property_desc_id text NOT NULL,
    property_pretty_name text,
    uri text
);
COPY core.property_desc (property_desc_id, property_pretty_name, uri) FROM stdin;
"MineralConcentrationsNature"	"Mineral Concentrations Nature"	http://w3id.org/glosis/model/layerhorizon/mineralConcNatureProperty

--4)
CREATE TABLE iso28258_category_desc (
    category_desc_id text NOT NULL,
    uri text
);

--5) iso28258_observation_desc_plot
CREATE TABLE iso28258_observation_desc_plot (
    procedure_desc_id text NOT NULL,
    property_desc_id text NOT NULL,
    category_desc_id text NOT NULL,
    category_order smallint
);

--5) iso28258_observation_desc_profile
CREATE TABLE iso28258_observation_desc_profile (
    procedure_desc_id text NOT NULL,
    property_desc_id text NOT NULL,
    category_desc_id text NOT NULL,
    category_order smallint
);

--6) iso28258_observation_phys_chem    ::: SIS_MEASURE
CREATE TABLE core.observation_phys_chem (
    observation_phys_chem_id integer NOT NULL, labdata_id ???????
    property_phys_chem_id text NOT NULL,   measure
    procedure_phys_chem_id text NOT NULL,  method
    unit_of_measure_id text NOT NULL, unit
    value_min real, ?
    value_max real, ?
);


lat * 100000    parte intera   
CREATE TABLE core.plot (
    plot_id integer NOT NULL, no
    site_id integer NOT NULL, no ????????
    plot_code character varying,   key
    altitude smallint, ok [-100,8000]
    time_stamp date, ok > 1900
    map_sheet_code character varying, no
    positional_accuracy smallint, no
    "position" public.geometry(Point,4326), ok
    type text, trialPit or Borehole
);
COMMENT ON TABLE core.plot IS 'Elementary area or location where individual observations are made and/or samples are taken. Plot is the main spatial feature of interest in ISO-28258. Plot has three sub-classes: Borehole, Pit and Surface. Surface features its own table since it has its own properties and a different geometry.';

CREATE TABLE core.profile (
    profile_id integer NOT NULL,
    plot_id integer,      plot_id === text
    surface_id integer,   null
    profile_code character varying, key
    CONSTRAINT site_mandatory_foi CHECK ((((plot_id IS NOT NULL) OR (surface_id IS NOT NULL)) AND (NOT ((plot_id IS NOT NULL) AND (surface_id IS NOT NULL)))))
);
COMMENT ON TABLE core.profile IS 'An abstract, ordered set of soil horizons and/or layers.';

CREATE TABLE core.project (
    project_id integer NOT NULL, no
    project_id : text
    name character varying NOT NULL ok
);
COMMENT ON TABLE core.project IS 'Provides the context of the data collection as a prerequisite for the proper use or reuse of these data.';

CREATE TABLE core.project_site (
    project_id integer NOT NULL,
    site_id integer NOT NULL
);
COMMENT ON TABLE core.project_site IS 'Many to many relation between Site and Project.';

CREATE TABLE core.result_phys_chem (
    result_phys_chem_id integer NOT NULL,
    observation_phys_chem_id integer NOT NULL,
    specimen_id integer NOT NULL,
    individual_id integer,
    value real NOT NULL
);
COMMENT ON TABLE core.result_phys_chem IS 'Numerical results for the Specimen feature interest.';

CREATE TABLE core.site (
    site_id integer NOT NULL,  *********
    site_code character varying, key
    typical_profile integer,
    "position" public.geometry(Point,4326), 5 decimal
);
COMMENT ON TABLE core.site IS 'Defined area which is subject to a soil quality investigation. Site is not a spatial feature of interest, but provides the link between the spatial features of interest (Plot) to the Project. The geometry can either be a location (point) or extent (polygon) but not both at the same time.';


CREATE VIEW core.profiles AS
 SELECT r.result_phys_chem_id AS gid,
    p.name AS project_name,
    s.site_id,
    p3.profile_id,
    r.specimen_id, no
    e.upper_depth, upper
    e.lower_depth, lower
    o.property_phys_chem_id, measure
    o.procedure_phys_chem_id, method
    r.value, value
    o.unit_of_measure_id, uom
    p2."position" AS geom, point
   FROM ((((((((core.project p
     LEFT JOIN core.project_site sp ON ((sp.project_id = p.project_id)))
     LEFT JOIN core.site s ON ((s.site_id = sp.site_id)))
     LEFT JOIN core.plot p2 ON ((p2.site_id = s.site_id)))
     LEFT JOIN core.profile p3 ON ((p3.plot_id = p2.plot_id)))
     LEFT JOIN core.element e ON ((e.profile_id = p3.profile_id)))
     LEFT JOIN core.specimen s2 ON ((s2.element_id = e.element_id)))
     LEFT JOIN core.result_phys_chem r ON ((r.specimen_id = s2.specimen_id)))
     LEFT JOIN core.observation_phys_chem o ON ((o.observation_phys_chem_id = r.observation_phys_chem_id)))
  ORDER BY p.name, s.site_id, p3.profile_id, e.upper_depth, o.property_phys_chem_id;

  

  CREATE TABLE core.property_phys_chem (
    property_phys_chem_id text NOT NULL,
    uri character varying NOT NULL
  );

  CREATE TABLE core.result_desc_element (
    element_id integer NOT NULL,
    property_desc_id text NOT NULL,
    category_desc_id text NOT NULL
  );


  CREATE TABLE core.result_desc_plot (
    plot_id integer NOT NULL,
    property_desc_id text NOT NULL,
    category_desc_id text NOT NULL
  );

  CREATE TABLE core.result_desc_profile (
    profile_id integer NOT NULL,
    property_desc_id text NOT NULL,
    category_desc_id text NOT NULL
  );






CREATE TABLE core.element (
    element_id integer NOT NULL, code === text labdata
    profile_id integer NOT NULL, code === text
    order_element integer, (0-20) or (0-50) or n layer
    upper_depth integer NOT NULL,
    lower_depth integer NOT NULL,
    type text NOT NULL,    (Horizon or Layer)
    CONSTRAINT element_check CHECK ((lower_depth > upper_depth)),
    CONSTRAINT element_order_element_check CHECK ((order_element > 0)),
    CONSTRAINT element_type_check CHECK ((type = ANY (ARRAY['Horizon'::text, 'Layer'::text]))),
    CONSTRAINT element_upper_depth_check CHECK ((upper_depth >= 0)),
    CONSTRAINT element_upper_depth_check1 CHECK ((upper_depth <= 1000))
);



CREATE TABLE core.observation_desc_element (
    procedure_desc_id text NOT NULL,   method
    property_desc_id text NOT NULL,      
    category_desc_id text NOT NULL,
    category_order smallint  ??????????????
);


CREATE TABLE core.observation_desc_plot (
    procedure_desc_id text NOT NULL, 
    property_desc_id text NOT NULL, 
    category_desc_id text NOT NULL, 
    category_order smallint 
);


CREATE TABLE core.observation_desc_profile (
    procedure_desc_id text NOT NULL,
    property_desc_id text NOT NULL,
    category_desc_id text NOT NULL,
    category_order smallint
);

CREATE TABLE core.observation_phys_chem (
    observation_phys_chem_id integer NOT NULL,
    property_phys_chem_id text NOT NULL,
    procedure_phys_chem_id text NOT NULL,
    unit_of_measure_id text NOT NULL,
    value_min real,
    value_max real
);

ALTER TABLE core.observation_phys_chem ALTER COLUMN observation_phys_chem_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME core.observation_phys_chem_element_observation_phys_chem_element_seq
    START WITH 1008
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


CREATE TABLE core.plot (
    plot_id integer NOT NULL,
    site_id integer NOT NULL,
    plot_code character varying,
    altitude smallint,
    time_stamp date,
    map_sheet_code character varying,
    positional_accuracy smallint,
    "position" public.geometry(Point,4326),
    type text,
    CONSTRAINT plot_altitude_check CHECK (((altitude)::numeric > ('-100'::integer)::numeric)),
    CONSTRAINT plot_altitude_check1 CHECK (((altitude)::numeric < (8000)::numeric)),
    CONSTRAINT plot_time_stamp_check CHECK ((time_stamp > '1900-01-01'::date)),
    CONSTRAINT plot_type_check CHECK ((type = ANY (ARRAY['TrialPit'::text, 'Borehole'::text])))
);


CREATE TABLE core.plot_individual (
    plot_id integer NOT NULL,
    individual_id integer NOT NULL
);





CREATE TABLE core.procedure_phys_chem (
    procedure_phys_chem_id text NOT NULL,
    broader_id text,
    uri character varying NOT NULL,
    definition text,
    reference text,
    citation text
);


CREATE TABLE core.profile (
    profile_id integer NOT NULL,
    plot_id integer,
    surface_id integer,
    profile_code character varying,
    CONSTRAINT site_mandatory_foi CHECK ((((plot_id IS NOT NULL) OR (surface_id IS NOT NULL)) AND (NOT ((plot_id IS NOT NULL) AND (surface_id IS NOT NULL)))))
);


CREATE TABLE core.project (
    project_id integer NOT NULL,
    name character varying NOT NULL
);

CREATE TABLE core.project_site (
    project_id integer NOT NULL,
    site_id integer NOT NULL
);


CREATE TABLE core.result_phys_chem (
    result_phys_chem_id integer NOT NULL,
    observation_phys_chem_id integer NOT NULL,
    specimen_id integer NOT NULL,
    individual_id integer,
    value real NOT NULL
);


CREATE TABLE core.site (
    site_id integer NOT NULL,
    site_code character varying,
    typical_profile integer,
    "position" public.geometry(Point,4326),
    extent public.geometry(Polygon,4326),
    CONSTRAINT site_mandatory_geometry CHECK (((("position" IS NOT NULL) OR (extent IS NOT NULL)) AND (NOT (("position" IS NOT NULL) AND (extent IS NOT NULL)))))
);

CREATE VIEW core.profiles AS
 SELECT r.result_phys_chem_id AS gid,
    p.name AS project_name,
    s.site_id,
    p3.profile_id,
    r.specimen_id,
    e.upper_depth,
    e.lower_depth,
    o.property_phys_chem_id,
    o.procedure_phys_chem_id,
    r.value,
    o.unit_of_measure_id,
    p2."position" AS geom
   FROM ((((((((core.project p
     LEFT JOIN core.project_site sp ON ((sp.project_id = p.project_id)))
     LEFT JOIN core.site s ON ((s.site_id = sp.site_id)))
     LEFT JOIN core.plot p2 ON ((p2.site_id = s.site_id)))
     LEFT JOIN core.profile p3 ON ((p3.plot_id = p2.plot_id)))
     LEFT JOIN core.element e ON ((e.profile_id = p3.profile_id)))
     LEFT JOIN core.specimen s2 ON ((s2.element_id = e.element_id)))
     LEFT JOIN core.result_phys_chem r ON ((r.specimen_id = s2.specimen_id)))
     LEFT JOIN core.observation_phys_chem o ON ((o.observation_phys_chem_id = r.observation_phys_chem_id)))
  ORDER BY p.name, s.site_id, p3.profile_id, e.upper_depth, o.property_phys_chem_id;

ALTER TABLE core.project ALTER COLUMN project_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME core.project_project_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE core.project_related (
    project_source_id integer NOT NULL,
    project_target_id integer NOT NULL,
    role character varying NOT NULL
);



CREATE TABLE core.property_phys_chem (
    property_phys_chem_id text NOT NULL,
    uri character varying NOT NULL
);

CREATE TABLE core.result_desc_element (
    element_id integer NOT NULL,
    property_desc_id text NOT NULL,
    category_desc_id text NOT NULL
);

CREATE TABLE core.result_desc_plot (
    plot_id integer NOT NULL,
    property_desc_id text NOT NULL,
    category_desc_id text NOT NULL
);

CREATE TABLE core.result_desc_profile (
    profile_id integer NOT NULL,
    property_desc_id text NOT NULL,
    category_desc_id text NOT NULL
);


CREATE TABLE core.result_desc_surface (
    surface_id integer NOT NULL,
    property_desc_id text NOT NULL,
    category_desc_id text NOT NULL
);
--

--
-- TOC entry 259 (class 1259 OID 54923058)
-- Name: unit_of_measure; Type: TABLE; Schema: core; Owner: glosis
--

CREATE TABLE core.unit_of_measure (
    unit_of_measure_id text NOT NULL,
    label character varying NOT NULL,
    uri character varying NOT NULL
);



--
-- TOC entry 4961 (class 0 OID 54922797)
-- Dependencies: 224
-- Data for Name: observation_desc_element; Type: TABLE DATA; Schema: core; Owner: glosis
--   classificazioni osservazioni tassonomia!!!!

COPY core.observation_desc_element (procedure_desc_id, property_desc_id, category_desc_id, category_order) FROM stdin;
WRB fourth edition 2022	,AndicCharacteristics	NF - Positive NaF test	1
WRB fourth edition 2022	,1AndicCharacteristics	NO - None of the above	4
WRB fourth edition 2022	,AndicCharacteristics	NT - Positive NAF test and thixotropy	3
WRB fourth edition 2022	,AndicCharacteristics	TH - Thixotropy	2
\.


--
-- TOC entry 4962 (class 0 OID 54922800)
-- Dependencies: 225
-- Data for Name: observation_desc_plot; Type: TABLE DATA; Schema: core; Owner: glosis
--

taxonomy_values
COPY core.observation_desc_plot (procedure_desc_id, property_desc_id, category_desc_id, category_order) FROM stdin;

WRB fourth edition 2022	PresenceOfWater	FF - Submerged by remote flowing inland water at least once a year	5
WRB fourth edition 2022	PresenceOfWater	FO - Submerged by remote flowing inland water less than once a year	6
WRB fourth edition 2022	PresenceOfWater	FP - Permanently submerged by inland water	4
WRB fourth edition 2022	PresenceOfWater	GF - Submerged by rising local groundwater at least once a year	7
WRB fourth edition 2022	PresenceOfWater	GO - Submerged by rising local groundwater less than once a year	8
WRB fourth edition 2022	PresenceOfWater	MO - Occasional storm surges (above mean high water springs)	3
WRB fourth edition 2022	PresenceOfWater	MP - Permanently submerged by seawater (below mean low water springs)	1
WRB fourth edition 2022	PresenceOfWater	MT - Tidal area (between mean low and mean high water springs)	2
WRB fourth edition 2022	PresenceOfWater	NO - None of the above	13
WRB fourth edition 2022	PresenceOfWater	RF - Submerged by local rainwater at least once a year	9
WRB fourth edition 2022	PresenceOfWater	RO - Submerged by local rainwater less than once a year	10
WRB fourth edition 2022	PresenceOfWater	UF - Submerged by inland water of unknown origin at least once a year	11
WRB fourth edition 2022	PresenceOfWater	UO - Submerged by inland water of unknown origin less than once a year	12
\.


--
-- TOC entry 4963 (class 0 OID 54922803)
-- Dependencies: 226
-- Data for Name: observation_desc_profile; Type: TABLE DATA; Schema: core; Owner: glosis
--

COPY core.observation_desc_profile (procedure_desc_id, property_desc_id, category_desc_id, category_order) FROM stdin;

Keys to Soil Taxonomy 13th edition 2022	formativeElementUSDA	Abruptic	1

\.


--
-- TOC entry 4964 (class 0 OID 54922820)
-- Dependencies: 227
-- Data for Name: observation_phys_chem; Type: TABLE DATA; Schema: core; Owner: glosis
--
labdata schema mapping
COPY core.observation_phys_chem (observation_phys_chem_id, property_phys_chem_id, procedure_phys_chem_id, unit_of_measure_id, value_min, value_max) FROM stdin;
543	pHProperty	pHH2O	pH	1.5	13
175	Boron (B) - extractable	Extr_ap14	%	0	100
514	pH - Hydrogen potential	pHH2O	pH	1.5	13
508	pH - Hydrogen potential	pHCaCl2_ratio1-1	pH	1.5	13
537	pHProperty	pHCaCl2_ratio1-1	pH	1.5	13
509	pH - Hydrogen potential	pHCaCl2_ratio1-10	pH	1.5	13
538	pHProperty	pHCaCl2_ratio1-10	pH	1.5	13
510	pH - Hydrogen potential	pHCaCl2_ratio1-2	pH	1.5	13
539	pHProperty	pHCaCl2_ratio1-2	pH	1.5	13
511	pH - Hydrogen potential	pHCaCl2_ratio1-2.5	pH	1.5	13
540	pHProperty	pHCaCl2_ratio1-2.5	pH	1.5	13
512	pH - Hydrogen potential	pHCaCl2_ratio1-5	pH	1.5	13
541	pHProperty	pHCaCl2_ratio1-5	pH	1.5	13
513	pH - Hydrogen potential	pHCaCl2_sat	pH	1.5	13
542	pHProperty	pHCaCl2_sat	pH	1.5	13
515	pH - Hydrogen potential	pHH2O_ratio1-1	pH	1.5	13
544	pHProperty	pHH2O_ratio1-1	pH	1.5	13
516	pH - Hydrogen potential	pHH2O_ratio1-10	pH	1.5	13
545	pHProperty	pHH2O_ratio1-10	pH	1.5	13
517	pH - Hydrogen potential	pHH2O_ratio1-2	pH	1.5	13
546	pHProperty	pHH2O_ratio1-2	pH	1.5	13
518	pH - Hydrogen potential	pHH2O_ratio1-2.5	pH	1.5	13
547	pHProperty	pHH2O_ratio1-2.5	pH	1.5	13
519	pH - Hydrogen potential	pHH2O_ratio1-5	pH	1.5	13
548	pHProperty	pHH2O_ratio1-5	pH	1.5	13
520	pH - Hydrogen potential	pHH2O_sat	pH	1.5	13
635	Clay texture fraction	SaSiCl_2-50-2000u-adj100	%	0	100
587	Sand texture fraction	SaSiCl_2-50-2000u-adj100	%	0	100
683	Silt texture fraction	SaSiCl_2-50-2000u-adj100	%	0	100
619	Clay texture fraction	SaSiCl_2-20-2000u-adj100	%	0	100
571	Sand texture fraction	SaSiCl_2-20-2000u-adj100	%	0	100
667	Silt texture fraction	SaSiCl_2-20-2000u-adj100	%	0	100
620	Clay texture fraction	SaSiCl_2-20-2000u-disp	%	0	100
572	Sand texture fraction	SaSiCl_2-20-2000u-disp	%	0	100
668	Silt texture fraction	SaSiCl_2-20-2000u-disp	%	0	100
621	Clay texture fraction	SaSiCl_2-20-2000u-disp-beaker	%	0	100
573	Sand texture fraction	SaSiCl_2-20-2000u-disp-beaker	%	0	100
669	Silt texture fraction	SaSiCl_2-20-2000u-disp-beaker	%	0	100
622	Clay texture fraction	SaSiCl_2-20-2000u-disp-hydrometer	%	0	100
574	Sand texture fraction	SaSiCl_2-20-2000u-disp-hydrometer	%	0	100
670	Silt texture fraction	SaSiCl_2-20-2000u-disp-hydrometer	%	0	100
623	Clay texture fraction	SaSiCl_2-20-2000u-disp-hydrometer-bouy	%	0	100
575	Sand texture fraction	SaSiCl_2-20-2000u-disp-hydrometer-bouy	%	0	100
671	Silt texture fraction	SaSiCl_2-20-2000u-disp-hydrometer-bouy	%	0	100
624	Clay texture fraction	SaSiCl_2-20-2000u-disp-laser	%	0	100
576	Sand texture fraction	SaSiCl_2-20-2000u-disp-laser	%	0	100
672	Silt texture fraction	SaSiCl_2-20-2000u-disp-laser	%	0	100
625	Clay texture fraction	SaSiCl_2-20-2000u-disp-pipette	%	0	100
577	Sand texture fraction	SaSiCl_2-20-2000u-disp-pipette	%	0	100
673	Silt texture fraction	SaSiCl_2-20-2000u-disp-pipette	%	0	100
626	Clay texture fraction	SaSiCl_2-20-2000u-disp-spec	%	0	100
578	Sand texture fraction	SaSiCl_2-20-2000u-disp-spec	%	0	100
493	Nitrogen (N) - total	TotalN_dc-ht-dumas	g/kg	0	1000
494	Nitrogen (N) - total	TotalN_dc-ht-leco	g/kg	0	1000
495	Nitrogen (N) - total	TotalN_dc-spec	g/kg	0	1000
69	electricalConductivityProperty	EC_ratio1-2	dS/m	0	60
674	Silt texture fraction	SaSiCl_2-20-2000u-disp-spec	%	0	100
706	Silt texture fraction	SaSiCl_2-64-2000u-disp-spec	%	0	100
659	Clay texture fraction	SaSiCl_2-64-2000u-fld	%	0	100
611	Sand texture fraction	SaSiCl_2-64-2000u-fld	%	0	100
707	Silt texture fraction	SaSiCl_2-64-2000u-fld	%	0	100
8	Available water capacity - volumetric (FC to WP)	PAWHC_calcul-fc100wp	m³/100 m³	0	100
9	Available water capacity - volumetric (FC to WP)	PAWHC_calcul-fc200wp	m³/100 m³	0	100
10	Available water capacity - volumetric (FC to WP)	PAWHC_calcul-fc300wp	m³/100 m³	0	100
31	carbonInorganicProperty	InOrgC_calcul-caco3	g/kg	0	1000
32	carbonInorganicProperty	InOrgC_calcul-tc-oc	g/kg	0	1000
33	Carbon (C) - organic	OrgC_acid-dc	g/kg	0	1000
34	Carbon (C) - organic	OrgC_acid-dc-ht	g/kg	0	1000
35	Carbon (C) - organic	OrgC_acid-dc-ht-analyser	g/kg	0	1000
36	Carbon (C) - organic	OrgC_acid-dc-lt	g/kg	0	1000
37	Carbon (C) - organic	OrgC_acid-dc-lt-loi	g/kg	0	1000
38	Carbon (C) - organic	OrgC_acid-dc-mt	g/kg	0	1000
39	Carbon (C) - organic	OrgC_acid-dc-spec	g/kg	0	1000
40	Carbon (C) - organic	OrgC_calcul-tc-ic	g/kg	0	1000
41	Carbon (C) - organic	OrgC_dc	g/kg	0	1000
42	Carbon (C) - organic	OrgC_dc-ht	g/kg	0	1000
43	Carbon (C) - organic	OrgC_dc-ht-analyser	g/kg	0	1000
44	Carbon (C) - organic	OrgC_dc-lt	g/kg	0	1000
45	Carbon (C) - organic	OrgC_dc-lt-loi	g/kg	0	1000
46	Carbon (C) - organic	OrgC_dc-mt	g/kg	0	1000
47	Carbon (C) - organic	OrgC_dc-spec	g/kg	0	1000
48	Carbon (C) - organic	OrgC_wc	g/kg	0	1000
49	Carbon (C) - organic	OrgC_wc-cro3-jackson	g/kg	0	1000
50	Carbon (C) - organic	OrgC_wc-cro3-kalembra	g/kg	0	1000
51	Carbon (C) - organic	OrgC_wc-cro3-knopp	g/kg	0	1000
52	Carbon (C) - organic	OrgC_wc-cro3-kurmies	g/kg	0	1000
53	Carbon (C) - organic	OrgC_wc-cro3-nelson	g/kg	0	1000
13	bulkDensityFineEarthProperty	BlkDensF_fe-cl-fc	kg/dm³	0.01	2.65
14	bulkDensityFineEarthProperty	BlkDensF_fe-cl-od	kg/dm³	0.01	2.65
15	bulkDensityFineEarthProperty	BlkDensF_fe-cl-unkn	kg/dm³	0.01	2.65
16	bulkDensityFineEarthProperty	BlkDensF_fe-co-fc	kg/dm³	0.01	2.65
17	bulkDensityFineEarthProperty	BlkDensF_fe-co-od	kg/dm³	0.01	2.65
18	bulkDensityFineEarthProperty	BlkDensF_fe-co-unkn	kg/dm³	0.01	2.65
19	bulkDensityFineEarthProperty	BlkDensF_fe-rpl-unkn	kg/dm³	0.01	2.65
20	bulkDensityFineEarthProperty	BlkDensF_fe-unkn	kg/dm³	0.01	2.65
21	bulkDensityFineEarthProperty	BlkDensF_fe-unkn-fc	kg/dm³	0.01	2.65
22	bulkDensityFineEarthProperty	BlkDensF_fe-unkn-od	kg/dm³	0.01	2.65
1	Acidity - exchangeable	ExchAcid_ph0-kcl1m	cmol/kg	0	100
2	Acidity - exchangeable	ExchAcid_ph0-nh4cl	cmol/kg	0	100
3	Acidity - exchangeable	ExchAcid_ph0-unkn	cmol/kg	0	100
4	Acidity - exchangeable	ExchAcid_ph7-caoac	cmol/kg	0	100
5	Acidity - exchangeable	ExchAcid_ph7-unkn	cmol/kg	0	100
6	Acidity - exchangeable	ExchAcid_ph8-bacl2tea	cmol/kg	0	100
7	Acidity - exchangeable	ExchAcid_ph8-unkn	cmol/kg	0	100
95	Hydrogen (H+) - exchangeable	ExchBases_ph-unkn-edta	cmol/kg	0	100
65	effectiveCecProperty	EffCEC_calcul-b	cmol/kg	0	100
66	effectiveCecProperty	EffCEC_calcul-ba	cmol/kg	0	100
23	bulkDensityWholeSoilProperty	BlkDensW_we-cl-fc	kg/dm³	0.01	3.6
24	bulkDensityWholeSoilProperty	BlkDensW_we-cl-od	kg/dm³	0.01	3.6
25	bulkDensityWholeSoilProperty	BlkDensW_we-cl-unkn	kg/dm³	0.01	3.6
26	bulkDensityWholeSoilProperty	BlkDensW_we-co-fc	kg/dm³	0.01	3.6
27	bulkDensityWholeSoilProperty	BlkDensW_we-co-od	kg/dm³	0.01	3.6
28	bulkDensityWholeSoilProperty	BlkDensW_we-co-unkn	kg/dm³	0.01	3.6
29	bulkDensityWholeSoilProperty	BlkDensW_we-rpl-unkn	kg/dm³	0.01	3.6
30	bulkDensityWholeSoilProperty	BlkDensW_we-unkn	kg/dm³	0.01	3.6
73	manganeseProperty	ExchBases_ph-unkn-edta	cmol/kg	0	1000
139	Magnesium (Mg++) - exchangeable	ExchBases_ph-unkn-edta	cmol/kg	0	100
106	Potassium (K+) - exchangeable	ExchBases_ph-unkn-edta	cmol/kg	0	100
117	Aluminium (Al+++) - exchangeable	ExchBases_ph-unkn-edta	cmol/kg	0	100
84	Sodium (Na+) - exchangeable	ExchBases_ph-unkn-edta	cmol/kg	0	100
251	Magnesium (Mg) - extractable	Extr_ap15	cmol/kg	0	1000
151	Manganese (Mn) - extractable	Extr_ap15	cmol/kg	0	1000
226	Potassium (K) - extractable	Extr_ap15	cmol/kg	0	1000
376	Sodium (Na) - extractable	Extr_ap15	cmol/kg	0	1000
326	Calcium (Ca++) - extractable	Extr_ap15	cmol/kg	0	1000
252	Magnesium (Mg) - extractable	Extr_ap20	cmol/kg	0	1000
152	Manganese (Mn) - extractable	Extr_ap20	cmol/kg	0	1000
227	Potassium (K) - extractable	Extr_ap20	cmol/kg	0	1000
377	Sodium (Na) - extractable	Extr_ap20	cmol/kg	0	1000
327	Calcium (Ca++) - extractable	Extr_ap20	cmol/kg	0	1000
253	Magnesium (Mg) - extractable	Extr_ap21	cmol/kg	0	1000
153	Manganese (Mn) - extractable	Extr_ap21	cmol/kg	0	1000
228	Potassium (K) - extractable	Extr_ap21	cmol/kg	0	1000
378	Sodium (Na) - extractable	Extr_ap21	cmol/kg	0	1000
328	Calcium (Ca++) - extractable	Extr_ap21	cmol/kg	0	1000
254	Magnesium (Mg) - extractable	Extr_c6h8o7-reeuwijk	cmol/kg	0	1000
154	Manganese (Mn) - extractable	Extr_c6h8o7-reeuwijk	cmol/kg	0	1000
229	Potassium (K) - extractable	Extr_c6h8o7-reeuwijk	cmol/kg	0	1000
379	Sodium (Na) - extractable	Extr_c6h8o7-reeuwijk	cmol/kg	0	1000
329	Calcium (Ca++) - extractable	Extr_c6h8o7-reeuwijk	cmol/kg	0	1000
255	Magnesium (Mg) - extractable	Extr_cacl2	cmol/kg	0	1000
155	Manganese (Mn) - extractable	Extr_cacl2	cmol/kg	0	1000
230	Potassium (K) - extractable	Extr_cacl2	cmol/kg	0	1000
380	Sodium (Na) - extractable	Extr_cacl2	cmol/kg	0	1000
330	Calcium (Ca++) - extractable	Extr_cacl2	cmol/kg	0	1000
256	Magnesium (Mg) - extractable	Extr_capo4	cmol/kg	0	1000
156	Manganese (Mn) - extractable	Extr_capo4	cmol/kg	0	1000
231	Potassium (K) - extractable	Extr_capo4	cmol/kg	0	1000
381	Sodium (Na) - extractable	Extr_capo4	cmol/kg	0	1000
331	Calcium (Ca++) - extractable	Extr_capo4	cmol/kg	0	1000
257	Magnesium (Mg) - extractable	Extr_dtpa	cmol/kg	0	1000
157	Manganese (Mn) - extractable	Extr_dtpa	cmol/kg	0	1000
232	Potassium (K) - extractable	Extr_dtpa	cmol/kg	0	1000
382	Sodium (Na) - extractable	Extr_dtpa	cmol/kg	0	1000
332	Calcium (Ca++) - extractable	Extr_dtpa	cmol/kg	0	1000
258	Magnesium (Mg) - extractable	Extr_edta	cmol/kg	0	1000
158	Manganese (Mn) - extractable	Extr_edta	cmol/kg	0	1000
233	Potassium (K) - extractable	Extr_edta	cmol/kg	0	1000
383	Sodium (Na) - extractable	Extr_edta	cmol/kg	0	1000
333	Calcium (Ca++) - extractable	Extr_edta	cmol/kg	0	1000
259	Magnesium (Mg) - extractable	Extr_h2so4-truog	cmol/kg	0	1000
159	Manganese (Mn) - extractable	Extr_h2so4-truog	cmol/kg	0	1000
234	Potassium (K) - extractable	Extr_h2so4-truog	cmol/kg	0	1000
384	Sodium (Na) - extractable	Extr_h2so4-truog	cmol/kg	0	1000
334	Calcium (Ca++) - extractable	Extr_h2so4-truog	cmol/kg	0	1000
260	Magnesium (Mg) - extractable	Extr_hcl-h2so4-nelson	cmol/kg	0	1000
160	Manganese (Mn) - extractable	Extr_hcl-h2so4-nelson	cmol/kg	0	1000
235	Potassium (K) - extractable	Extr_hcl-h2so4-nelson	cmol/kg	0	1000
385	Sodium (Na) - extractable	Extr_hcl-h2so4-nelson	cmol/kg	0	1000
335	Calcium (Ca++) - extractable	Extr_hcl-h2so4-nelson	cmol/kg	0	1000
261	Magnesium (Mg) - extractable	Extr_hcl-nh4f-bray1	cmol/kg	0	1000
161	Manganese (Mn) - extractable	Extr_hcl-nh4f-bray1	cmol/kg	0	1000
236	Potassium (K) - extractable	Extr_hcl-nh4f-bray1	cmol/kg	0	1000
386	Sodium (Na) - extractable	Extr_hcl-nh4f-bray1	cmol/kg	0	1000
336	Calcium (Ca++) - extractable	Extr_hcl-nh4f-bray1	cmol/kg	0	1000
262	Magnesium (Mg) - extractable	Extr_hcl-nh4f-bray2	cmol/kg	0	1000
162	Manganese (Mn) - extractable	Extr_hcl-nh4f-bray2	cmol/kg	0	1000
237	Potassium (K) - extractable	Extr_hcl-nh4f-bray2	cmol/kg	0	1000
387	Sodium (Na) - extractable	Extr_hcl-nh4f-bray2	cmol/kg	0	1000
337	Calcium (Ca++) - extractable	Extr_hcl-nh4f-bray2	cmol/kg	0	1000
263	Magnesium (Mg) - extractable	Extr_hcl-nh4f-kurtz-bray	cmol/kg	0	1000
163	Manganese (Mn) - extractable	Extr_hcl-nh4f-kurtz-bray	cmol/kg	0	1000
238	Potassium (K) - extractable	Extr_hcl-nh4f-kurtz-bray	cmol/kg	0	1000
388	Sodium (Na) - extractable	Extr_hcl-nh4f-kurtz-bray	cmol/kg	0	1000
338	Calcium (Ca++) - extractable	Extr_hcl-nh4f-kurtz-bray	cmol/kg	0	1000
264	Magnesium (Mg) - extractable	Extr_hno3	cmol/kg	0	1000
164	Manganese (Mn) - extractable	Extr_hno3	cmol/kg	0	1000
239	Potassium (K) - extractable	Extr_hno3	cmol/kg	0	1000
389	Sodium (Na) - extractable	Extr_hno3	cmol/kg	0	1000
339	Calcium (Ca++) - extractable	Extr_hno3	cmol/kg	0	1000
265	Magnesium (Mg) - extractable	Extr_hotwater	cmol/kg	0	1000
165	Manganese (Mn) - extractable	Extr_hotwater	cmol/kg	0	1000
240	Potassium (K) - extractable	Extr_hotwater	cmol/kg	0	1000
390	Sodium (Na) - extractable	Extr_hotwater	cmol/kg	0	1000
340	Calcium (Ca++) - extractable	Extr_hotwater	cmol/kg	0	1000
266	Magnesium (Mg) - extractable	Extr_m1	cmol/kg	0	1000
166	Manganese (Mn) - extractable	Extr_m1	cmol/kg	0	1000
241	Potassium (K) - extractable	Extr_m1	cmol/kg	0	1000
391	Sodium (Na) - extractable	Extr_m1	cmol/kg	0	1000
341	Calcium (Ca++) - extractable	Extr_m1	cmol/kg	0	1000
267	Magnesium (Mg) - extractable	Extr_m2	cmol/kg	0	1000
167	Manganese (Mn) - extractable	Extr_m2	cmol/kg	0	1000
242	Potassium (K) - extractable	Extr_m2	cmol/kg	0	1000
392	Sodium (Na) - extractable	Extr_m2	cmol/kg	0	1000
342	Calcium (Ca++) - extractable	Extr_m2	cmol/kg	0	1000
268	Magnesium (Mg) - extractable	Extr_m3	cmol/kg	0	1000
168	Manganese (Mn) - extractable	Extr_m3	cmol/kg	0	1000
243	Potassium (K) - extractable	Extr_m3	cmol/kg	0	1000
393	Sodium (Na) - extractable	Extr_m3	cmol/kg	0	1000
343	Calcium (Ca++) - extractable	Extr_m3	cmol/kg	0	1000
269	Magnesium (Mg) - extractable	Extr_m3-spec	cmol/kg	0	1000
169	Manganese (Mn) - extractable	Extr_m3-spec	cmol/kg	0	1000
244	Potassium (K) - extractable	Extr_m3-spec	cmol/kg	0	1000
394	Sodium (Na) - extractable	Extr_m3-spec	cmol/kg	0	1000
344	Calcium (Ca++) - extractable	Extr_m3-spec	cmol/kg	0	1000
270	Magnesium (Mg) - extractable	Extr_nahco3-olsen	cmol/kg	0	1000
170	Manganese (Mn) - extractable	Extr_nahco3-olsen	cmol/kg	0	1000
245	Potassium (K) - extractable	Extr_nahco3-olsen	cmol/kg	0	1000
395	Sodium (Na) - extractable	Extr_nahco3-olsen	cmol/kg	0	1000
345	Calcium (Ca++) - extractable	Extr_nahco3-olsen	cmol/kg	0	1000
271	Magnesium (Mg) - extractable	Extr_nahco3-olsen-dabin	cmol/kg	0	1000
171	Manganese (Mn) - extractable	Extr_nahco3-olsen-dabin	cmol/kg	0	1000
246	Potassium (K) - extractable	Extr_nahco3-olsen-dabin	cmol/kg	0	1000
396	Sodium (Na) - extractable	Extr_nahco3-olsen-dabin	cmol/kg	0	1000
346	Calcium (Ca++) - extractable	Extr_nahco3-olsen-dabin	cmol/kg	0	1000
272	Magnesium (Mg) - extractable	Extr_naoac-morgan	cmol/kg	0	1000
172	Manganese (Mn) - extractable	Extr_naoac-morgan	cmol/kg	0	1000
247	Potassium (K) - extractable	Extr_naoac-morgan	cmol/kg	0	1000
397	Sodium (Na) - extractable	Extr_naoac-morgan	cmol/kg	0	1000
347	Calcium (Ca++) - extractable	Extr_naoac-morgan	cmol/kg	0	1000
273	Magnesium (Mg) - extractable	Extr_nh4-co3-2-ambic1	cmol/kg	0	1000
173	Manganese (Mn) - extractable	Extr_nh4-co3-2-ambic1	cmol/kg	0	1000
248	Potassium (K) - extractable	Extr_nh4-co3-2-ambic1	cmol/kg	0	1000
398	Sodium (Na) - extractable	Extr_nh4-co3-2-ambic1	cmol/kg	0	1000
348	Calcium (Ca++) - extractable	Extr_nh4-co3-2-ambic1	cmol/kg	0	1000
274	Magnesium (Mg) - extractable	Extr_nh4ch3ch-oh-cooh-leuven	cmol/kg	0	1000
174	Manganese (Mn) - extractable	Extr_nh4ch3ch-oh-cooh-leuven	cmol/kg	0	1000
249	Potassium (K) - extractable	Extr_nh4ch3ch-oh-cooh-leuven	cmol/kg	0	1000
399	Sodium (Na) - extractable	Extr_nh4ch3ch-oh-cooh-leuven	cmol/kg	0	1000
299	Sulfur (S) - extractable	Extr_nh4ch3ch-oh-cooh-leuven	%	0	100
424	Zinc (Zn) - extractable	Extr_nh4ch3ch-oh-cooh-leuven	%	0	100
449	cadmiumProperty	Extr_nh4ch3ch-oh-cooh-leuven	%	0	100
224	molybdenumProperty	Extr_nh4ch3ch-oh-cooh-leuven	%	0	100
482	hydraulicConductivityProperty	KSat_calcul-ptf	cm/h	0	100
483	hydraulicConductivityProperty	KSat_calcul-ptf-genuchten	cm/h	0	100
484	hydraulicConductivityProperty	KSat_calcul-ptf-saxton	cm/h	0	100
485	hydraulicConductivityProperty	Ksat_bhole	cm/h	0	100
486	hydraulicConductivityProperty	Ksat_column	cm/h	0	100
487	hydraulicConductivityProperty	Ksat_dblring	cm/h	0	100
488	hydraulicConductivityProperty	Ksat_invbhole	cm/h	0	100
565	Phosphorus (P) - retention	RetentP_blakemore	g/hg	0	100
566	Phosphorus (P) - retention	RetentP_unkn-spec	g/hg	0	100
567	porosityProperty	Poros_calcul-pf0	m³/100 m³	0	100
489	Nitrogen (N) - total	TotalN_bremner	g/kg	0	1000
490	Nitrogen (N) - total	TotalN_calcul	g/kg	0	1000
491	Nitrogen (N) - total	TotalN_calcul-oc10	g/kg	0	1000
492	Nitrogen (N) - total	TotalN_dc	g/kg	0	1000
496	Nitrogen (N) - total	TotalN_h2so4	g/kg	0	1000
497	Nitrogen (N) - total	TotalN_kjeldahl	g/kg	0	1000
498	Nitrogen (N) - total	TotalN_kjeldahl-nh4	g/kg	0	1000
499	Nitrogen (N) - total	TotalN_nelson	g/kg	0	1000
500	Nitrogen (N) - total	TotalN_tn04	g/kg	0	1000
501	Nitrogen (N) - total	TotalN_tn06	g/kg	0	1000
502	Nitrogen (N) - total	TotalN_tn08	g/kg	0	1000
503	organicMatterProperty	FulAcidC_unkn	g/kg	0	1000
504	organicMatterProperty	HumAcidC_unkn	g/kg	0	1000
505	organicMatterProperty	OrgM_calcul-oc1.73	g/kg	0	1000
506	organicMatterProperty	TotHumC_unkn	g/kg	0	1000
568	solubleSaltsProperty	SlbAn_calcul-unkn	cmol/L	0	1000
569	solubleSaltsProperty	SlbCat_calcul-unkn	cmol/L	0	1000
349	Calcium (Ca++) - extractable	Extr_nh4ch3ch-oh-cooh-leuven	cmol/kg	0	1000
951	Calcium (Ca++) - total	Total_h2so4	cmol/kg	0	1000
761	Magnesium (Mg) - total	Total_h2so4	cmol/kg	0	1000
989	Manganese (Mn) - total	Total_h2so4	cmol/kg	0	1000
742	Potassium (K) - total	Total_h2so4	cmol/kg	0	1000
970	Sodium (Na) - total	Total_h2so4	cmol/kg	0	1000
952	Calcium (Ca++) - total	Total_hcl	cmol/kg	0	1000
762	Magnesium (Mg) - total	Total_hcl	cmol/kg	0	1000
990	Manganese (Mn) - total	Total_hcl	cmol/kg	0	1000
743	Potassium (K) - total	Total_hcl	cmol/kg	0	1000
971	Sodium (Na) - total	Total_hcl	cmol/kg	0	1000
953	Calcium (Ca++) - total	Total_hcl-aquaregia	cmol/kg	0	1000
763	Magnesium (Mg) - total	Total_hcl-aquaregia	cmol/kg	0	1000
991	Manganese (Mn) - total	Total_hcl-aquaregia	cmol/kg	0	1000
744	Potassium (K) - total	Total_hcl-aquaregia	cmol/kg	0	1000
972	Sodium (Na) - total	Total_hcl-aquaregia	cmol/kg	0	1000
954	Calcium (Ca++) - total	Total_hclo4	cmol/kg	0	1000
764	Magnesium (Mg) - total	Total_hclo4	cmol/kg	0	1000
992	Manganese (Mn) - total	Total_hclo4	cmol/kg	0	1000
745	Potassium (K) - total	Total_hclo4	cmol/kg	0	1000
973	Sodium (Na) - total	Total_hclo4	cmol/kg	0	1000
955	Calcium (Ca++) - total	Total_hno3-aquafortis	cmol/kg	0	1000
765	Magnesium (Mg) - total	Total_hno3-aquafortis	cmol/kg	0	1000
993	Manganese (Mn) - total	Total_hno3-aquafortis	cmol/kg	0	1000
746	Potassium (K) - total	Total_hno3-aquafortis	cmol/kg	0	1000
974	Sodium (Na) - total	Total_hno3-aquafortis	cmol/kg	0	1000
956	Calcium (Ca++) - total	Total_nh4-6mo7o24	cmol/kg	0	1000
766	Magnesium (Mg) - total	Total_nh4-6mo7o24	cmol/kg	0	1000
994	Manganese (Mn) - total	Total_nh4-6mo7o24	cmol/kg	0	1000
747	Potassium (K) - total	Total_nh4-6mo7o24	cmol/kg	0	1000
975	Sodium (Na) - total	Total_nh4-6mo7o24	cmol/kg	0	1000
957	Calcium (Ca++) - total	Total_tp03	cmol/kg	0	1000
767	Magnesium (Mg) - total	Total_tp03	cmol/kg	0	1000
995	Manganese (Mn) - total	Total_tp03	cmol/kg	0	1000
748	Potassium (K) - total	Total_tp03	cmol/kg	0	1000
976	Sodium (Na) - total	Total_tp03	cmol/kg	0	1000
958	Calcium (Ca++) - total	Total_tp04	cmol/kg	0	1000
768	Magnesium (Mg) - total	Total_tp04	cmol/kg	0	1000
996	Manganese (Mn) - total	Total_tp04	cmol/kg	0	1000
749	Potassium (K) - total	Total_tp04	cmol/kg	0	1000
977	Sodium (Na) - total	Total_tp04	cmol/kg	0	1000
959	Calcium (Ca++) - total	Total_tp05	cmol/kg	0	1000
769	Magnesium (Mg) - total	Total_tp05	cmol/kg	0	1000
997	Manganese (Mn) - total	Total_tp05	cmol/kg	0	1000
750	Potassium (K) - total	Total_tp05	cmol/kg	0	1000
978	Sodium (Na) - total	Total_tp05	cmol/kg	0	1000
960	Calcium (Ca++) - total	Total_tp06	cmol/kg	0	1000
770	Magnesium (Mg) - total	Total_tp06	cmol/kg	0	1000
998	Manganese (Mn) - total	Total_tp06	cmol/kg	0	1000
751	Potassium (K) - total	Total_tp06	cmol/kg	0	1000
979	Sodium (Na) - total	Total_tp06	cmol/kg	0	1000
961	Calcium (Ca++) - total	Total_tp07	cmol/kg	0	1000
771	Magnesium (Mg) - total	Total_tp07	cmol/kg	0	1000
999	Manganese (Mn) - total	Total_tp07	cmol/kg	0	1000
752	Potassium (K) - total	Total_tp07	cmol/kg	0	1000
980	Sodium (Na) - total	Total_tp07	cmol/kg	0	1000
962	Calcium (Ca++) - total	Total_tp08	cmol/kg	0	1000
772	Magnesium (Mg) - total	Total_tp08	cmol/kg	0	1000
1000	Manganese (Mn) - total	Total_tp08	cmol/kg	0	1000
753	Potassium (K) - total	Total_tp08	cmol/kg	0	1000
981	Sodium (Na) - total	Total_tp08	cmol/kg	0	1000
963	Calcium (Ca++) - total	Total_tp09	cmol/kg	0	1000
773	Magnesium (Mg) - total	Total_tp09	cmol/kg	0	1000
1001	Manganese (Mn) - total	Total_tp09	cmol/kg	0	1000
754	Potassium (K) - total	Total_tp09	cmol/kg	0	1000
982	Sodium (Na) - total	Total_tp09	cmol/kg	0	1000
964	Calcium (Ca++) - total	Total_tp10	cmol/kg	0	1000
774	Magnesium (Mg) - total	Total_tp10	cmol/kg	0	1000
1002	Manganese (Mn) - total	Total_tp10	cmol/kg	0	1000
755	Potassium (K) - total	Total_tp10	cmol/kg	0	1000
983	Sodium (Na) - total	Total_tp10	cmol/kg	0	1000
965	Calcium (Ca++) - total	Total_unkn	cmol/kg	0	1000
775	Magnesium (Mg) - total	Total_unkn	cmol/kg	0	1000
1003	Manganese (Mn) - total	Total_unkn	cmol/kg	0	1000
756	Potassium (K) - total	Total_unkn	cmol/kg	0	1000
984	Sodium (Na) - total	Total_unkn	cmol/kg	0	1000
966	Calcium (Ca++) - total	Total_xrd	cmol/kg	0	1000
776	Magnesium (Mg) - total	Total_xrd	cmol/kg	0	1000
1004	Manganese (Mn) - total	Total_xrd	cmol/kg	0	1000
757	Potassium (K) - total	Total_xrd	cmol/kg	0	1000
985	Sodium (Na) - total	Total_xrd	cmol/kg	0	1000
967	Calcium (Ca++) - total	Total_xrf	cmol/kg	0	1000
777	Magnesium (Mg) - total	Total_xrf	cmol/kg	0	1000
1005	Manganese (Mn) - total	Total_xrf	cmol/kg	0	1000
758	Potassium (K) - total	Total_xrf	cmol/kg	0	1000
986	Sodium (Na) - total	Total_xrf	cmol/kg	0	1000
968	Calcium (Ca++) - total	Total_xrf-p	cmol/kg	0	1000
778	Magnesium (Mg) - total	Total_xrf-p	cmol/kg	0	1000
1006	Manganese (Mn) - total	Total_xrf-p	cmol/kg	0	1000
759	Potassium (K) - total	Total_xrf-p	cmol/kg	0	1000
987	Sodium (Na) - total	Total_xrf-p	cmol/kg	0	1000
549	pHProperty	pHH2O_sat	pH	1.5	13
521	pH - Hydrogen potential	pHH2O_unkn-spec	pH	1.5	13
550	pHProperty	pHH2O_unkn-spec	pH	1.5	13
523	pH - Hydrogen potential	pHKCl_ratio1-1	pH	1.5	13
552	pHProperty	pHKCl_ratio1-1	pH	1.5	13
524	pH - Hydrogen potential	pHKCl_ratio1-10	pH	1.5	13
553	pHProperty	pHKCl_ratio1-10	pH	1.5	13
525	pH - Hydrogen potential	pHKCl_ratio1-2	pH	1.5	13
554	pHProperty	pHKCl_ratio1-2	pH	1.5	13
526	pH - Hydrogen potential	pHKCl_ratio1-2.5	pH	1.5	13
555	pHProperty	pHKCl_ratio1-2.5	pH	1.5	13
527	pH - Hydrogen potential	pHKCl_ratio1-5	pH	1.5	13
556	pHProperty	pHKCl_ratio1-5	pH	1.5	13
530	pH - Hydrogen potential	pHNaF_ratio1-1	pH	1.5	13
559	pHProperty	pHNaF_ratio1-1	pH	1.5	13
531	pH - Hydrogen potential	pHNaF_ratio1-10	pH	1.5	13
560	pHProperty	pHNaF_ratio1-10	pH	1.5	13
532	pH - Hydrogen potential	pHNaF_ratio1-2	pH	1.5	13
561	pHProperty	pHNaF_ratio1-2	pH	1.5	13
533	pH - Hydrogen potential	pHNaF_ratio1-2.5	pH	1.5	13
562	pHProperty	pHNaF_ratio1-2.5	pH	1.5	13
534	pH - Hydrogen potential	pHNaF_ratio1-5	pH	1.5	13
563	pHProperty	pHNaF_ratio1-5	pH	1.5	13
535	pH - Hydrogen potential	pHNaF_sat	pH	1.5	13
564	pHProperty	pHNaF_sat	pH	1.5	13
507	pH - Hydrogen potential	pHCaCl2	pH	1.5	13
536	pHProperty	pHCaCl2	pH	1.5	13
522	pH - Hydrogen potential	pHKCl	pH	1.5	13
551	pHProperty	pHKCl	pH	1.5	13
528	pH - Hydrogen potential	pHKCl_sat	pH	1.5	13
557	pHProperty	pHKCl_sat	pH	1.5	13
529	pH - Hydrogen potential	pHNaF	pH	1.5	13
558	pHProperty	pHNaF	pH	1.5	13
67	electricalConductivityProperty	EC_ratio1-1	dS/m	0	60
68	electricalConductivityProperty	EC_ratio1-10	dS/m	0	60
70	electricalConductivityProperty	EC_ratio1-2.5	dS/m	0	60
71	electricalConductivityProperty	EC_ratio1-5	dS/m	0	60
72	electricalConductivityProperty	ECe_sat	dS/m	0	60
627	Clay texture fraction	SaSiCl_2-20-2000u-fld	%	0	100
579	Sand texture fraction	SaSiCl_2-20-2000u-fld	%	0	100
675	Silt texture fraction	SaSiCl_2-20-2000u-fld	%	0	100
628	Clay texture fraction	SaSiCl_2-20-2000u-nodisp	%	0	100
580	Sand texture fraction	SaSiCl_2-20-2000u-nodisp	%	0	100
676	Silt texture fraction	SaSiCl_2-20-2000u-nodisp	%	0	100
629	Clay texture fraction	SaSiCl_2-20-2000u-nodisp-hydrometer	%	0	100
581	Sand texture fraction	SaSiCl_2-20-2000u-nodisp-hydrometer	%	0	100
677	Silt texture fraction	SaSiCl_2-20-2000u-nodisp-hydrometer	%	0	100
630	Clay texture fraction	SaSiCl_2-20-2000u-nodisp-hydrometer-bouy	%	0	100
582	Sand texture fraction	SaSiCl_2-20-2000u-nodisp-hydrometer-bouy	%	0	100
678	Silt texture fraction	SaSiCl_2-20-2000u-nodisp-hydrometer-bouy	%	0	100
631	Clay texture fraction	SaSiCl_2-20-2000u-nodisp-laser	%	0	100
583	Sand texture fraction	SaSiCl_2-20-2000u-nodisp-laser	%	0	100
679	Silt texture fraction	SaSiCl_2-20-2000u-nodisp-laser	%	0	100
632	Clay texture fraction	SaSiCl_2-20-2000u-nodisp-pipette	%	0	100
584	Sand texture fraction	SaSiCl_2-20-2000u-nodisp-pipette	%	0	100
680	Silt texture fraction	SaSiCl_2-20-2000u-nodisp-pipette	%	0	100
633	Clay texture fraction	SaSiCl_2-20-2000u-nodisp-spec	%	0	100
585	Sand texture fraction	SaSiCl_2-20-2000u-nodisp-spec	%	0	100
681	Silt texture fraction	SaSiCl_2-20-2000u-nodisp-spec	%	0	100
636	Clay texture fraction	SaSiCl_2-50-2000u-disp	%	0	100
588	Sand texture fraction	SaSiCl_2-50-2000u-disp	%	0	100
684	Silt texture fraction	SaSiCl_2-50-2000u-disp	%	0	100
637	Clay texture fraction	SaSiCl_2-50-2000u-disp-beaker	%	0	100
589	Sand texture fraction	SaSiCl_2-50-2000u-disp-beaker	%	0	100
685	Silt texture fraction	SaSiCl_2-50-2000u-disp-beaker	%	0	100
638	Clay texture fraction	SaSiCl_2-50-2000u-disp-hydrometer	%	0	100
590	Sand texture fraction	SaSiCl_2-50-2000u-disp-hydrometer	%	0	100
686	Silt texture fraction	SaSiCl_2-50-2000u-disp-hydrometer	%	0	100
639	Clay texture fraction	SaSiCl_2-50-2000u-disp-hydrometer-bouy	%	0	100
591	Sand texture fraction	SaSiCl_2-50-2000u-disp-hydrometer-bouy	%	0	100
687	Silt texture fraction	SaSiCl_2-50-2000u-disp-hydrometer-bouy	%	0	100
640	Clay texture fraction	SaSiCl_2-50-2000u-disp-laser	%	0	100
592	Sand texture fraction	SaSiCl_2-50-2000u-disp-laser	%	0	100
688	Silt texture fraction	SaSiCl_2-50-2000u-disp-laser	%	0	100
641	Clay texture fraction	SaSiCl_2-50-2000u-disp-pipette	%	0	100
593	Sand texture fraction	SaSiCl_2-50-2000u-disp-pipette	%	0	100
873	zincProperty	Total_xrf-p	%	0	100
969	Calcium (Ca++) - total	Total_xtf-t	cmol/kg	0	1000
779	Magnesium (Mg) - total	Total_xtf-t	cmol/kg	0	1000
1007	Manganese (Mn) - total	Total_xtf-t	cmol/kg	0	1000
760	Potassium (K) - total	Total_xtf-t	cmol/kg	0	1000
988	Sodium (Na) - total	Total_xtf-t	cmol/kg	0	1000
689	Silt texture fraction	SaSiCl_2-50-2000u-disp-pipette	%	0	100
642	Clay texture fraction	SaSiCl_2-50-2000u-disp-spec	%	0	100
594	Sand texture fraction	SaSiCl_2-50-2000u-disp-spec	%	0	100
690	Silt texture fraction	SaSiCl_2-50-2000u-disp-spec	%	0	100
643	Clay texture fraction	SaSiCl_2-50-2000u-fld	%	0	100
595	Sand texture fraction	SaSiCl_2-50-2000u-fld	%	0	100
691	Silt texture fraction	SaSiCl_2-50-2000u-fld	%	0	100
644	Clay texture fraction	SaSiCl_2-50-2000u-nodisp	%	0	100
596	Sand texture fraction	SaSiCl_2-50-2000u-nodisp	%	0	100
692	Silt texture fraction	SaSiCl_2-50-2000u-nodisp	%	0	100
645	Clay texture fraction	SaSiCl_2-50-2000u-nodisp-hydrometer	%	0	100
597	Sand texture fraction	SaSiCl_2-50-2000u-nodisp-hydrometer	%	0	100
693	Silt texture fraction	SaSiCl_2-50-2000u-nodisp-hydrometer	%	0	100
646	Clay texture fraction	SaSiCl_2-50-2000u-nodisp-hydrometer-bouy	%	0	100
598	Sand texture fraction	SaSiCl_2-50-2000u-nodisp-hydrometer-bouy	%	0	100
694	Silt texture fraction	SaSiCl_2-50-2000u-nodisp-hydrometer-bouy	%	0	100
647	Clay texture fraction	SaSiCl_2-50-2000u-nodisp-laser	%	0	100
599	Sand texture fraction	SaSiCl_2-50-2000u-nodisp-laser	%	0	100
695	Silt texture fraction	SaSiCl_2-50-2000u-nodisp-laser	%	0	100
648	Clay texture fraction	SaSiCl_2-50-2000u-nodisp-pipette	%	0	100
600	Sand texture fraction	SaSiCl_2-50-2000u-nodisp-pipette	%	0	100
696	Silt texture fraction	SaSiCl_2-50-2000u-nodisp-pipette	%	0	100
649	Clay texture fraction	SaSiCl_2-50-2000u-nodisp-spec	%	0	100
601	Sand texture fraction	SaSiCl_2-50-2000u-nodisp-spec	%	0	100
697	Silt texture fraction	SaSiCl_2-50-2000u-nodisp-spec	%	0	100
651	Clay texture fraction	SaSiCl_2-64-2000u-adj100	%	0	100
603	Sand texture fraction	SaSiCl_2-64-2000u-adj100	%	0	100
699	Silt texture fraction	SaSiCl_2-64-2000u-adj100	%	0	100
652	Clay texture fraction	SaSiCl_2-64-2000u-disp	%	0	100
604	Sand texture fraction	SaSiCl_2-64-2000u-disp	%	0	100
700	Silt texture fraction	SaSiCl_2-64-2000u-disp	%	0	100
653	Clay texture fraction	SaSiCl_2-64-2000u-disp-beaker	%	0	100
605	Sand texture fraction	SaSiCl_2-64-2000u-disp-beaker	%	0	100
701	Silt texture fraction	SaSiCl_2-64-2000u-disp-beaker	%	0	100
654	Clay texture fraction	SaSiCl_2-64-2000u-disp-hydrometer	%	0	100
606	Sand texture fraction	SaSiCl_2-64-2000u-disp-hydrometer	%	0	100
702	Silt texture fraction	SaSiCl_2-64-2000u-disp-hydrometer	%	0	100
655	Clay texture fraction	SaSiCl_2-64-2000u-disp-hydrometer-bouy	%	0	100
607	Sand texture fraction	SaSiCl_2-64-2000u-disp-hydrometer-bouy	%	0	100
703	Silt texture fraction	SaSiCl_2-64-2000u-disp-hydrometer-bouy	%	0	100
656	Clay texture fraction	SaSiCl_2-64-2000u-disp-laser	%	0	100
608	Sand texture fraction	SaSiCl_2-64-2000u-disp-laser	%	0	100
704	Silt texture fraction	SaSiCl_2-64-2000u-disp-laser	%	0	100
657	Clay texture fraction	SaSiCl_2-64-2000u-disp-pipette	%	0	100
609	Sand texture fraction	SaSiCl_2-64-2000u-disp-pipette	%	0	100
705	Silt texture fraction	SaSiCl_2-64-2000u-disp-pipette	%	0	100
658	Clay texture fraction	SaSiCl_2-64-2000u-disp-spec	%	0	100
610	Sand texture fraction	SaSiCl_2-64-2000u-disp-spec	%	0	100
351	Iron (Fe) - extractable	Extr_ap15	%	0	100
660	Clay texture fraction	SaSiCl_2-64-2000u-nodisp	%	0	100
612	Sand texture fraction	SaSiCl_2-64-2000u-nodisp	%	0	100
708	Silt texture fraction	SaSiCl_2-64-2000u-nodisp	%	0	100
661	Clay texture fraction	SaSiCl_2-64-2000u-nodisp-hydrometer	%	0	100
613	Sand texture fraction	SaSiCl_2-64-2000u-nodisp-hydrometer	%	0	100
709	Silt texture fraction	SaSiCl_2-64-2000u-nodisp-hydrometer	%	0	100
662	Clay texture fraction	SaSiCl_2-64-2000u-nodisp-hydrometer-bouy	%	0	100
614	Sand texture fraction	SaSiCl_2-64-2000u-nodisp-hydrometer-bouy	%	0	100
710	Silt texture fraction	SaSiCl_2-64-2000u-nodisp-hydrometer-bouy	%	0	100
663	Clay texture fraction	SaSiCl_2-64-2000u-nodisp-laser	%	0	100
615	Sand texture fraction	SaSiCl_2-64-2000u-nodisp-laser	%	0	100
711	Silt texture fraction	SaSiCl_2-64-2000u-nodisp-laser	%	0	100
664	Clay texture fraction	SaSiCl_2-64-2000u-nodisp-pipette	%	0	100
616	Sand texture fraction	SaSiCl_2-64-2000u-nodisp-pipette	%	0	100
712	Silt texture fraction	SaSiCl_2-64-2000u-nodisp-pipette	%	0	100
665	Clay texture fraction	SaSiCl_2-64-2000u-nodisp-spec	%	0	100
617	Sand texture fraction	SaSiCl_2-64-2000u-nodisp-spec	%	0	100
713	Silt texture fraction	SaSiCl_2-64-2000u-nodisp-spec	%	0	100
11	Base saturation - calculated	BSat_calcul-cec	%	0	100
12	Base saturation - calculated	BSat_calcul-ecec	%	0	100
62	coarseFragmentsProperty	CrsFrg_fld	%	0	100
63	coarseFragmentsProperty	CrsFrg_fldcls	%	0	100
64	coarseFragmentsProperty	CrsFrg_lab	%	0	100
191	Boron (B) - extractable	Extr_m1	%	0	100
300	Copper (Cu) - extractable	Extr_ap14	%	0	100
350	Iron (Fe) - extractable	Extr_ap14	%	0	100
450	Phosphorus (P) - extractable	Extr_ap14	%	0	100
275	Sulfur (S) - extractable	Extr_ap14	%	0	100
400	Zinc (Zn) - extractable	Extr_ap14	%	0	100
425	cadmiumProperty	Extr_ap14	%	0	100
200	molybdenumProperty	Extr_ap14	%	0	100
301	Copper (Cu) - extractable	Extr_ap15	%	0	100
451	Phosphorus (P) - extractable	Extr_ap15	%	0	100
276	Sulfur (S) - extractable	Extr_ap15	%	0	100
401	Zinc (Zn) - extractable	Extr_ap15	%	0	100
426	cadmiumProperty	Extr_ap15	%	0	100
201	molybdenumProperty	Extr_ap15	%	0	100
176	Boron (B) - extractable	Extr_ap15	%	0	100
302	Copper (Cu) - extractable	Extr_ap20	%	0	100
352	Iron (Fe) - extractable	Extr_ap20	%	0	100
452	Phosphorus (P) - extractable	Extr_ap20	%	0	100
277	Sulfur (S) - extractable	Extr_ap20	%	0	100
402	Zinc (Zn) - extractable	Extr_ap20	%	0	100
427	cadmiumProperty	Extr_ap20	%	0	100
202	molybdenumProperty	Extr_ap20	%	0	100
177	Boron (B) - extractable	Extr_ap20	%	0	100
303	Copper (Cu) - extractable	Extr_ap21	%	0	100
353	Iron (Fe) - extractable	Extr_ap21	%	0	100
453	Phosphorus (P) - extractable	Extr_ap21	%	0	100
278	Sulfur (S) - extractable	Extr_ap21	%	0	100
403	Zinc (Zn) - extractable	Extr_ap21	%	0	100
428	cadmiumProperty	Extr_ap21	%	0	100
203	molybdenumProperty	Extr_ap21	%	0	100
178	Boron (B) - extractable	Extr_ap21	%	0	100
304	Copper (Cu) - extractable	Extr_c6h8o7-reeuwijk	%	0	100
354	Iron (Fe) - extractable	Extr_c6h8o7-reeuwijk	%	0	100
454	Phosphorus (P) - extractable	Extr_c6h8o7-reeuwijk	%	0	100
279	Sulfur (S) - extractable	Extr_c6h8o7-reeuwijk	%	0	100
404	Zinc (Zn) - extractable	Extr_c6h8o7-reeuwijk	%	0	100
429	cadmiumProperty	Extr_c6h8o7-reeuwijk	%	0	100
204	molybdenumProperty	Extr_c6h8o7-reeuwijk	%	0	100
179	Boron (B) - extractable	Extr_c6h8o7-reeuwijk	%	0	100
305	Copper (Cu) - extractable	Extr_cacl2	%	0	100
355	Iron (Fe) - extractable	Extr_cacl2	%	0	100
455	Phosphorus (P) - extractable	Extr_cacl2	%	0	100
280	Sulfur (S) - extractable	Extr_cacl2	%	0	100
405	Zinc (Zn) - extractable	Extr_cacl2	%	0	100
430	cadmiumProperty	Extr_cacl2	%	0	100
205	molybdenumProperty	Extr_cacl2	%	0	100
180	Boron (B) - extractable	Extr_cacl2	%	0	100
306	Copper (Cu) - extractable	Extr_capo4	%	0	100
356	Iron (Fe) - extractable	Extr_capo4	%	0	100
456	Phosphorus (P) - extractable	Extr_capo4	%	0	100
281	Sulfur (S) - extractable	Extr_capo4	%	0	100
406	Zinc (Zn) - extractable	Extr_capo4	%	0	100
431	cadmiumProperty	Extr_capo4	%	0	100
206	molybdenumProperty	Extr_capo4	%	0	100
181	Boron (B) - extractable	Extr_capo4	%	0	100
307	Copper (Cu) - extractable	Extr_dtpa	%	0	100
357	Iron (Fe) - extractable	Extr_dtpa	%	0	100
457	Phosphorus (P) - extractable	Extr_dtpa	%	0	100
282	Sulfur (S) - extractable	Extr_dtpa	%	0	100
407	Zinc (Zn) - extractable	Extr_dtpa	%	0	100
432	cadmiumProperty	Extr_dtpa	%	0	100
207	molybdenumProperty	Extr_dtpa	%	0	100
182	Boron (B) - extractable	Extr_dtpa	%	0	100
308	Copper (Cu) - extractable	Extr_edta	%	0	100
358	Iron (Fe) - extractable	Extr_edta	%	0	100
458	Phosphorus (P) - extractable	Extr_edta	%	0	100
283	Sulfur (S) - extractable	Extr_edta	%	0	100
408	Zinc (Zn) - extractable	Extr_edta	%	0	100
433	cadmiumProperty	Extr_edta	%	0	100
208	molybdenumProperty	Extr_edta	%	0	100
183	Boron (B) - extractable	Extr_edta	%	0	100
309	Copper (Cu) - extractable	Extr_h2so4-truog	%	0	100
359	Iron (Fe) - extractable	Extr_h2so4-truog	%	0	100
459	Phosphorus (P) - extractable	Extr_h2so4-truog	%	0	100
284	Sulfur (S) - extractable	Extr_h2so4-truog	%	0	100
409	Zinc (Zn) - extractable	Extr_h2so4-truog	%	0	100
434	cadmiumProperty	Extr_h2so4-truog	%	0	100
209	molybdenumProperty	Extr_h2so4-truog	%	0	100
184	Boron (B) - extractable	Extr_h2so4-truog	%	0	100
310	Copper (Cu) - extractable	Extr_hcl-h2so4-nelson	%	0	100
360	Iron (Fe) - extractable	Extr_hcl-h2so4-nelson	%	0	100
460	Phosphorus (P) - extractable	Extr_hcl-h2so4-nelson	%	0	100
285	Sulfur (S) - extractable	Extr_hcl-h2so4-nelson	%	0	100
410	Zinc (Zn) - extractable	Extr_hcl-h2so4-nelson	%	0	100
435	cadmiumProperty	Extr_hcl-h2so4-nelson	%	0	100
210	molybdenumProperty	Extr_hcl-h2so4-nelson	%	0	100
185	Boron (B) - extractable	Extr_hcl-h2so4-nelson	%	0	100
311	Copper (Cu) - extractable	Extr_hcl-nh4f-bray1	%	0	100
361	Iron (Fe) - extractable	Extr_hcl-nh4f-bray1	%	0	100
461	Phosphorus (P) - extractable	Extr_hcl-nh4f-bray1	%	0	100
286	Sulfur (S) - extractable	Extr_hcl-nh4f-bray1	%	0	100
411	Zinc (Zn) - extractable	Extr_hcl-nh4f-bray1	%	0	100
436	cadmiumProperty	Extr_hcl-nh4f-bray1	%	0	100
211	molybdenumProperty	Extr_hcl-nh4f-bray1	%	0	100
186	Boron (B) - extractable	Extr_hcl-nh4f-bray1	%	0	100
312	Copper (Cu) - extractable	Extr_hcl-nh4f-bray2	%	0	100
362	Iron (Fe) - extractable	Extr_hcl-nh4f-bray2	%	0	100
462	Phosphorus (P) - extractable	Extr_hcl-nh4f-bray2	%	0	100
287	Sulfur (S) - extractable	Extr_hcl-nh4f-bray2	%	0	100
412	Zinc (Zn) - extractable	Extr_hcl-nh4f-bray2	%	0	100
437	cadmiumProperty	Extr_hcl-nh4f-bray2	%	0	100
212	molybdenumProperty	Extr_hcl-nh4f-bray2	%	0	100
187	Boron (B) - extractable	Extr_hcl-nh4f-bray2	%	0	100
313	Copper (Cu) - extractable	Extr_hcl-nh4f-kurtz-bray	%	0	100
363	Iron (Fe) - extractable	Extr_hcl-nh4f-kurtz-bray	%	0	100
463	Phosphorus (P) - extractable	Extr_hcl-nh4f-kurtz-bray	%	0	100
288	Sulfur (S) - extractable	Extr_hcl-nh4f-kurtz-bray	%	0	100
413	Zinc (Zn) - extractable	Extr_hcl-nh4f-kurtz-bray	%	0	100
438	cadmiumProperty	Extr_hcl-nh4f-kurtz-bray	%	0	100
213	molybdenumProperty	Extr_hcl-nh4f-kurtz-bray	%	0	100
188	Boron (B) - extractable	Extr_hcl-nh4f-kurtz-bray	%	0	100
314	Copper (Cu) - extractable	Extr_hno3	%	0	100
364	Iron (Fe) - extractable	Extr_hno3	%	0	100
464	Phosphorus (P) - extractable	Extr_hno3	%	0	100
289	Sulfur (S) - extractable	Extr_hno3	%	0	100
414	Zinc (Zn) - extractable	Extr_hno3	%	0	100
439	cadmiumProperty	Extr_hno3	%	0	100
214	molybdenumProperty	Extr_hno3	%	0	100
189	Boron (B) - extractable	Extr_hno3	%	0	100
315	Copper (Cu) - extractable	Extr_hotwater	%	0	100
365	Iron (Fe) - extractable	Extr_hotwater	%	0	100
465	Phosphorus (P) - extractable	Extr_hotwater	%	0	100
290	Sulfur (S) - extractable	Extr_hotwater	%	0	100
415	Zinc (Zn) - extractable	Extr_hotwater	%	0	100
440	cadmiumProperty	Extr_hotwater	%	0	100
215	molybdenumProperty	Extr_hotwater	%	0	100
190	Boron (B) - extractable	Extr_hotwater	%	0	100
316	Copper (Cu) - extractable	Extr_m1	%	0	100
366	Iron (Fe) - extractable	Extr_m1	%	0	100
466	Phosphorus (P) - extractable	Extr_m1	%	0	100
291	Sulfur (S) - extractable	Extr_m1	%	0	100
416	Zinc (Zn) - extractable	Extr_m1	%	0	100
441	cadmiumProperty	Extr_m1	%	0	100
216	molybdenumProperty	Extr_m1	%	0	100
317	Copper (Cu) - extractable	Extr_m2	%	0	100
367	Iron (Fe) - extractable	Extr_m2	%	0	100
467	Phosphorus (P) - extractable	Extr_m2	%	0	100
292	Sulfur (S) - extractable	Extr_m2	%	0	100
417	Zinc (Zn) - extractable	Extr_m2	%	0	100
442	cadmiumProperty	Extr_m2	%	0	100
217	molybdenumProperty	Extr_m2	%	0	100
192	Boron (B) - extractable	Extr_m2	%	0	100
318	Copper (Cu) - extractable	Extr_m3	%	0	100
368	Iron (Fe) - extractable	Extr_m3	%	0	100
468	Phosphorus (P) - extractable	Extr_m3	%	0	100
293	Sulfur (S) - extractable	Extr_m3	%	0	100
418	Zinc (Zn) - extractable	Extr_m3	%	0	100
443	cadmiumProperty	Extr_m3	%	0	100
218	molybdenumProperty	Extr_m3	%	0	100
193	Boron (B) - extractable	Extr_m3	%	0	100
319	Copper (Cu) - extractable	Extr_m3-spec	%	0	100
369	Iron (Fe) - extractable	Extr_m3-spec	%	0	100
469	Phosphorus (P) - extractable	Extr_m3-spec	%	0	100
294	Sulfur (S) - extractable	Extr_m3-spec	%	0	100
419	Zinc (Zn) - extractable	Extr_m3-spec	%	0	100
444	cadmiumProperty	Extr_m3-spec	%	0	100
219	molybdenumProperty	Extr_m3-spec	%	0	100
194	Boron (B) - extractable	Extr_m3-spec	%	0	100
320	Copper (Cu) - extractable	Extr_nahco3-olsen	%	0	100
370	Iron (Fe) - extractable	Extr_nahco3-olsen	%	0	100
470	Phosphorus (P) - extractable	Extr_nahco3-olsen	%	0	100
295	Sulfur (S) - extractable	Extr_nahco3-olsen	%	0	100
420	Zinc (Zn) - extractable	Extr_nahco3-olsen	%	0	100
445	cadmiumProperty	Extr_nahco3-olsen	%	0	100
220	molybdenumProperty	Extr_nahco3-olsen	%	0	100
195	Boron (B) - extractable	Extr_nahco3-olsen	%	0	100
321	Copper (Cu) - extractable	Extr_nahco3-olsen-dabin	%	0	100
371	Iron (Fe) - extractable	Extr_nahco3-olsen-dabin	%	0	100
471	Phosphorus (P) - extractable	Extr_nahco3-olsen-dabin	%	0	100
296	Sulfur (S) - extractable	Extr_nahco3-olsen-dabin	%	0	100
421	Zinc (Zn) - extractable	Extr_nahco3-olsen-dabin	%	0	100
446	cadmiumProperty	Extr_nahco3-olsen-dabin	%	0	100
221	molybdenumProperty	Extr_nahco3-olsen-dabin	%	0	100
196	Boron (B) - extractable	Extr_nahco3-olsen-dabin	%	0	100
322	Copper (Cu) - extractable	Extr_naoac-morgan	%	0	100
372	Iron (Fe) - extractable	Extr_naoac-morgan	%	0	100
472	Phosphorus (P) - extractable	Extr_naoac-morgan	%	0	100
297	Sulfur (S) - extractable	Extr_naoac-morgan	%	0	100
422	Zinc (Zn) - extractable	Extr_naoac-morgan	%	0	100
447	cadmiumProperty	Extr_naoac-morgan	%	0	100
222	molybdenumProperty	Extr_naoac-morgan	%	0	100
197	Boron (B) - extractable	Extr_naoac-morgan	%	0	100
323	Copper (Cu) - extractable	Extr_nh4-co3-2-ambic1	%	0	100
373	Iron (Fe) - extractable	Extr_nh4-co3-2-ambic1	%	0	100
473	Phosphorus (P) - extractable	Extr_nh4-co3-2-ambic1	%	0	100
298	Sulfur (S) - extractable	Extr_nh4-co3-2-ambic1	%	0	100
423	Zinc (Zn) - extractable	Extr_nh4-co3-2-ambic1	%	0	100
448	cadmiumProperty	Extr_nh4-co3-2-ambic1	%	0	100
223	molybdenumProperty	Extr_nh4-co3-2-ambic1	%	0	100
198	Boron (B) - extractable	Extr_nh4-co3-2-ambic1	%	0	100
324	Copper (Cu) - extractable	Extr_nh4ch3ch-oh-cooh-leuven	%	0	100
374	Iron (Fe) - extractable	Extr_nh4ch3ch-oh-cooh-leuven	%	0	100
474	Phosphorus (P) - extractable	Extr_nh4ch3ch-oh-cooh-leuven	%	0	100
895	Phosphorus (P) - total	Total_hcl	%	0	100
199	Boron (B) - extractable	Extr_nh4ch3ch-oh-cooh-leuven	%	0	100
475	gypsumProperty	CaSO4_gy01	%	0	100
476	gypsumProperty	CaSO4_gy02	%	0	100
477	gypsumProperty	CaSO4_gy03	%	0	100
478	gypsumProperty	CaSO4_gy04	%	0	100
479	gypsumProperty	CaSO4_gy05	%	0	100
480	gypsumProperty	CaSO4_gy06	%	0	100
481	gypsumProperty	CaSO4_gy07	%	0	100
618	Clay texture fraction	SaSiCl_2-20-2000u	%	0	100
570	Sand texture fraction	SaSiCl_2-20-2000u	%	0	100
666	Silt texture fraction	SaSiCl_2-20-2000u	%	0	100
634	Clay texture fraction	SaSiCl_2-50-2000u	%	0	100
586	Sand texture fraction	SaSiCl_2-50-2000u	%	0	100
682	Silt texture fraction	SaSiCl_2-50-2000u	%	0	100
650	Clay texture fraction	SaSiCl_2-64-2000u	%	0	100
602	Sand texture fraction	SaSiCl_2-64-2000u	%	0	100
698	Silt texture fraction	SaSiCl_2-64-2000u	%	0	100
913	aluminiumProperty	Total_h2so4	%	0	100
837	Copper (Cu) - total	Total_h2so4	%	0	100
932	Iron (Fe) - total	Total_h2so4	%	0	100
894	Phosphorus (P) - total	Total_h2so4	%	0	100
818	Sulfur (S) - total	Total_h2so4	%	0	100
875	cadmiumProperty	Total_h2so4	%	0	100
780	molybdenumProperty	Total_h2so4	%	0	100
856	zincProperty	Total_h2so4	%	0	100
799	Boron (B) - total	Total_h2so4	%	0	100
914	aluminiumProperty	Total_hcl	%	0	100
838	Copper (Cu) - total	Total_hcl	%	0	100
933	Iron (Fe) - total	Total_hcl	%	0	100
819	Sulfur (S) - total	Total_hcl	%	0	100
876	cadmiumProperty	Total_hcl	%	0	100
781	molybdenumProperty	Total_hcl	%	0	100
857	zincProperty	Total_hcl	%	0	100
800	Boron (B) - total	Total_hcl	%	0	100
915	aluminiumProperty	Total_hcl-aquaregia	%	0	100
839	Copper (Cu) - total	Total_hcl-aquaregia	%	0	100
934	Iron (Fe) - total	Total_hcl-aquaregia	%	0	100
896	Phosphorus (P) - total	Total_hcl-aquaregia	%	0	100
820	Sulfur (S) - total	Total_hcl-aquaregia	%	0	100
877	cadmiumProperty	Total_hcl-aquaregia	%	0	100
782	molybdenumProperty	Total_hcl-aquaregia	%	0	100
858	zincProperty	Total_hcl-aquaregia	%	0	100
801	Boron (B) - total	Total_hcl-aquaregia	%	0	100
916	aluminiumProperty	Total_hclo4	%	0	100
840	Copper (Cu) - total	Total_hclo4	%	0	100
935	Iron (Fe) - total	Total_hclo4	%	0	100
897	Phosphorus (P) - total	Total_hclo4	%	0	100
821	Sulfur (S) - total	Total_hclo4	%	0	100
878	cadmiumProperty	Total_hclo4	%	0	100
783	molybdenumProperty	Total_hclo4	%	0	100
859	zincProperty	Total_hclo4	%	0	100
802	Boron (B) - total	Total_hclo4	%	0	100
917	aluminiumProperty	Total_hno3-aquafortis	%	0	100
841	Copper (Cu) - total	Total_hno3-aquafortis	%	0	100
936	Iron (Fe) - total	Total_hno3-aquafortis	%	0	100
898	Phosphorus (P) - total	Total_hno3-aquafortis	%	0	100
822	Sulfur (S) - total	Total_hno3-aquafortis	%	0	100
879	cadmiumProperty	Total_hno3-aquafortis	%	0	100
784	molybdenumProperty	Total_hno3-aquafortis	%	0	100
860	zincProperty	Total_hno3-aquafortis	%	0	100
803	Boron (B) - total	Total_hno3-aquafortis	%	0	100
918	aluminiumProperty	Total_nh4-6mo7o24	%	0	100
842	Copper (Cu) - total	Total_nh4-6mo7o24	%	0	100
937	Iron (Fe) - total	Total_nh4-6mo7o24	%	0	100
899	Phosphorus (P) - total	Total_nh4-6mo7o24	%	0	100
823	Sulfur (S) - total	Total_nh4-6mo7o24	%	0	100
880	cadmiumProperty	Total_nh4-6mo7o24	%	0	100
785	molybdenumProperty	Total_nh4-6mo7o24	%	0	100
861	zincProperty	Total_nh4-6mo7o24	%	0	100
804	Boron (B) - total	Total_nh4-6mo7o24	%	0	100
919	aluminiumProperty	Total_tp03	%	0	100
843	Copper (Cu) - total	Total_tp03	%	0	100
938	Iron (Fe) - total	Total_tp03	%	0	100
900	Phosphorus (P) - total	Total_tp03	%	0	100
824	Sulfur (S) - total	Total_tp03	%	0	100
881	cadmiumProperty	Total_tp03	%	0	100
786	molybdenumProperty	Total_tp03	%	0	100
862	zincProperty	Total_tp03	%	0	100
805	Boron (B) - total	Total_tp03	%	0	100
920	aluminiumProperty	Total_tp04	%	0	100
844	Copper (Cu) - total	Total_tp04	%	0	100
939	Iron (Fe) - total	Total_tp04	%	0	100
901	Phosphorus (P) - total	Total_tp04	%	0	100
825	Sulfur (S) - total	Total_tp04	%	0	100
882	cadmiumProperty	Total_tp04	%	0	100
787	molybdenumProperty	Total_tp04	%	0	100
863	zincProperty	Total_tp04	%	0	100
806	Boron (B) - total	Total_tp04	%	0	100
921	aluminiumProperty	Total_tp05	%	0	100
845	Copper (Cu) - total	Total_tp05	%	0	100
940	Iron (Fe) - total	Total_tp05	%	0	100
902	Phosphorus (P) - total	Total_tp05	%	0	100
826	Sulfur (S) - total	Total_tp05	%	0	100
883	cadmiumProperty	Total_tp05	%	0	100
788	molybdenumProperty	Total_tp05	%	0	100
864	zincProperty	Total_tp05	%	0	100
807	Boron (B) - total	Total_tp05	%	0	100
922	aluminiumProperty	Total_tp06	%	0	100
846	Copper (Cu) - total	Total_tp06	%	0	100
941	Iron (Fe) - total	Total_tp06	%	0	100
903	Phosphorus (P) - total	Total_tp06	%	0	100
827	Sulfur (S) - total	Total_tp06	%	0	100
884	cadmiumProperty	Total_tp06	%	0	100
789	molybdenumProperty	Total_tp06	%	0	100
865	zincProperty	Total_tp06	%	0	100
808	Boron (B) - total	Total_tp06	%	0	100
923	aluminiumProperty	Total_tp07	%	0	100
847	Copper (Cu) - total	Total_tp07	%	0	100
942	Iron (Fe) - total	Total_tp07	%	0	100
904	Phosphorus (P) - total	Total_tp07	%	0	100
828	Sulfur (S) - total	Total_tp07	%	0	100
885	cadmiumProperty	Total_tp07	%	0	100
790	molybdenumProperty	Total_tp07	%	0	100
866	zincProperty	Total_tp07	%	0	100
809	Boron (B) - total	Total_tp07	%	0	100
924	aluminiumProperty	Total_tp08	%	0	100
848	Copper (Cu) - total	Total_tp08	%	0	100
943	Iron (Fe) - total	Total_tp08	%	0	100
905	Phosphorus (P) - total	Total_tp08	%	0	100
829	Sulfur (S) - total	Total_tp08	%	0	100
886	cadmiumProperty	Total_tp08	%	0	100
791	molybdenumProperty	Total_tp08	%	0	100
867	zincProperty	Total_tp08	%	0	100
810	Boron (B) - total	Total_tp08	%	0	100
925	aluminiumProperty	Total_tp09	%	0	100
849	Copper (Cu) - total	Total_tp09	%	0	100
944	Iron (Fe) - total	Total_tp09	%	0	100
906	Phosphorus (P) - total	Total_tp09	%	0	100
830	Sulfur (S) - total	Total_tp09	%	0	100
887	cadmiumProperty	Total_tp09	%	0	100
792	molybdenumProperty	Total_tp09	%	0	100
868	zincProperty	Total_tp09	%	0	100
811	Boron (B) - total	Total_tp09	%	0	100
926	aluminiumProperty	Total_tp10	%	0	100
850	Copper (Cu) - total	Total_tp10	%	0	100
945	Iron (Fe) - total	Total_tp10	%	0	100
907	Phosphorus (P) - total	Total_tp10	%	0	100
831	Sulfur (S) - total	Total_tp10	%	0	100
888	cadmiumProperty	Total_tp10	%	0	100
793	molybdenumProperty	Total_tp10	%	0	100
869	zincProperty	Total_tp10	%	0	100
812	Boron (B) - total	Total_tp10	%	0	100
927	aluminiumProperty	Total_unkn	%	0	100
851	Copper (Cu) - total	Total_unkn	%	0	100
946	Iron (Fe) - total	Total_unkn	%	0	100
908	Phosphorus (P) - total	Total_unkn	%	0	100
832	Sulfur (S) - total	Total_unkn	%	0	100
889	cadmiumProperty	Total_unkn	%	0	100
794	molybdenumProperty	Total_unkn	%	0	100
870	zincProperty	Total_unkn	%	0	100
813	Boron (B) - total	Total_unkn	%	0	100
928	aluminiumProperty	Total_xrd	%	0	100
852	Copper (Cu) - total	Total_xrd	%	0	100
947	Iron (Fe) - total	Total_xrd	%	0	100
909	Phosphorus (P) - total	Total_xrd	%	0	100
833	Sulfur (S) - total	Total_xrd	%	0	100
890	cadmiumProperty	Total_xrd	%	0	100
795	molybdenumProperty	Total_xrd	%	0	100
871	zincProperty	Total_xrd	%	0	100
814	Boron (B) - total	Total_xrd	%	0	100
929	aluminiumProperty	Total_xrf	%	0	100
853	Copper (Cu) - total	Total_xrf	%	0	100
948	Iron (Fe) - total	Total_xrf	%	0	100
910	Phosphorus (P) - total	Total_xrf	%	0	100
834	Sulfur (S) - total	Total_xrf	%	0	100
891	cadmiumProperty	Total_xrf	%	0	100
796	molybdenumProperty	Total_xrf	%	0	100
872	zincProperty	Total_xrf	%	0	100
815	Boron (B) - total	Total_xrf	%	0	100
930	aluminiumProperty	Total_xrf-p	%	0	100
854	Copper (Cu) - total	Total_xrf-p	%	0	100
949	Iron (Fe) - total	Total_xrf-p	%	0	100
911	Phosphorus (P) - total	Total_xrf-p	%	0	100
835	Sulfur (S) - total	Total_xrf-p	%	0	100
892	cadmiumProperty	Total_xrf-p	%	0	100
797	molybdenumProperty	Total_xrf-p	%	0	100
816	Boron (B) - total	Total_xrf-p	%	0	100
931	aluminiumProperty	Total_xtf-t	%	0	100
855	Copper (Cu) - total	Total_xtf-t	%	0	100
950	Iron (Fe) - total	Total_xtf-t	%	0	100
912	Phosphorus (P) - total	Total_xtf-t	%	0	100
836	Sulfur (S) - total	Total_xtf-t	%	0	100
893	cadmiumProperty	Total_xtf-t	%	0	100
798	molybdenumProperty	Total_xtf-t	%	0	100
874	zincProperty	Total_xtf-t	%	0	100
817	Boron (B) - total	Total_xtf-t	%	0	100
54	Carbon (C) - organic	OrgC_wc-cro3-nrcs6a1c	g/kg	0	1000
55	Carbon (C) - organic	OrgC_wc-cro3-tiurin	g/kg	0	1000
56	Carbon (C) - organic	OrgC_wc-cro3-walkleyblack	g/kg	0	1000
57	Carbon (C) - total	TotC_calcul-ic-oc	g/kg	0	1000
58	Carbon (C) - total	TotC_dc-ht	g/kg	0	1000
59	Carbon (C) - total	TotC_dc-ht-analyser	g/kg	0	1000
60	Carbon (C) - total	TotC_dc-ht-spec	g/kg	0	1000
61	Carbon (C) - total	TotC_dc-mt	g/kg	0	1000
714	totalCarbonateEquivalentProperty	CaCO3_acid-ch3cooh-dc	g/kg	0	1000
715	totalCarbonateEquivalentProperty	CaCO3_acid-ch3cooh-nodc	g/kg	0	1000
716	totalCarbonateEquivalentProperty	CaCO3_acid-ch3cooh-unkn	g/kg	0	1000
717	totalCarbonateEquivalentProperty	CaCO3_acid-dc	g/kg	0	1000
718	totalCarbonateEquivalentProperty	CaCO3_acid-h2so4-dc	g/kg	0	1000
719	totalCarbonateEquivalentProperty	CaCO3_acid-h2so4-nodc	g/kg	0	1000
720	totalCarbonateEquivalentProperty	CaCO3_acid-h2so4-unkn	g/kg	0	1000
721	totalCarbonateEquivalentProperty	CaCO3_acid-h3po4-dc	g/kg	0	1000
722	totalCarbonateEquivalentProperty	CaCO3_acid-h3po4-nodc	g/kg	0	1000
723	totalCarbonateEquivalentProperty	CaCO3_acid-h3po4-unkn	g/kg	0	1000
724	totalCarbonateEquivalentProperty	CaCO3_acid-hcl-dc	g/kg	0	1000
725	totalCarbonateEquivalentProperty	CaCO3_acid-hcl-nodc	g/kg	0	1000
726	totalCarbonateEquivalentProperty	CaCO3_acid-hcl-unkn	g/kg	0	1000
727	totalCarbonateEquivalentProperty	CaCO3_acid-nodc	g/kg	0	1000
728	totalCarbonateEquivalentProperty	CaCO3_acid-unkn	g/kg	0	1000
729	totalCarbonateEquivalentProperty	CaCO3_ca01	g/kg	0	1000
730	totalCarbonateEquivalentProperty	CaCO3_ca02	g/kg	0	1000
731	totalCarbonateEquivalentProperty	CaCO3_ca03	g/kg	0	1000
732	totalCarbonateEquivalentProperty	CaCO3_ca04	g/kg	0	1000
733	totalCarbonateEquivalentProperty	CaCO3_ca05	g/kg	0	1000
734	totalCarbonateEquivalentProperty	CaCO3_ca06	g/kg	0	1000
735	totalCarbonateEquivalentProperty	CaCO3_ca07	g/kg	0	1000
736	totalCarbonateEquivalentProperty	CaCO3_ca08	g/kg	0	1000
737	totalCarbonateEquivalentProperty	CaCO3_ca09	g/kg	0	1000
738	totalCarbonateEquivalentProperty	CaCO3_ca10	g/kg	0	1000
739	totalCarbonateEquivalentProperty	CaCO3_ca11	g/kg	0	1000
740	totalCarbonateEquivalentProperty	CaCO3_ca12	g/kg	0	1000
741	totalCarbonateEquivalentProperty	CaCO3_calcul-tc-oc	g/kg	0	1000
74	manganeseProperty	ExchBases_ph-unkn-m3	cmol/kg	0	1000
75	manganeseProperty	ExchBases_ph-unkn-m3-spec	cmol/kg	0	1000
76	manganeseProperty	ExchBases_ph0-cohex	cmol/kg	0	1000
77	manganeseProperty	ExchBases_ph0-nh4cl	cmol/kg	0	1000
78	manganeseProperty	ExchBases_ph7-nh4oac	cmol/kg	0	1000
79	manganeseProperty	ExchBases_ph7-nh4oac-aas	cmol/kg	0	1000
80	manganeseProperty	ExchBases_ph7-nh4oac-fp	cmol/kg	0	1000
81	manganeseProperty	ExchBases_ph7-unkn	cmol/kg	0	1000
82	manganeseProperty	ExchBases_ph8-bacl2tea	cmol/kg	0	1000
83	manganeseProperty	ExchBases_ph8-unkn	cmol/kg	0	1000
250	Magnesium (Mg) - extractable	Extr_ap14	cmol/kg	0	1000
150	Manganese (Mn) - extractable	Extr_ap14	cmol/kg	0	1000
225	Potassium (K) - extractable	Extr_ap14	cmol/kg	0	1000
375	Sodium (Na) - extractable	Extr_ap14	cmol/kg	0	1000
325	Calcium (Ca++) - extractable	Extr_ap14	cmol/kg	0	1000
128	Calcium (Ca++) - exchangeable	ExchBases_ph-unkn-edta	cmol/kg	0	100
96	Hydrogen (H+) - exchangeable	ExchBases_ph-unkn-m3	cmol/kg	0	100
140	Magnesium (Mg++) - exchangeable	ExchBases_ph-unkn-m3	cmol/kg	0	100
107	Potassium (K+) - exchangeable	ExchBases_ph-unkn-m3	cmol/kg	0	100
118	Aluminium (Al+++) - exchangeable	ExchBases_ph-unkn-m3	cmol/kg	0	100
129	Calcium (Ca++) - exchangeable	ExchBases_ph-unkn-m3	cmol/kg	0	100
97	Hydrogen (H+) - exchangeable	ExchBases_ph-unkn-m3-spec	cmol/kg	0	100
141	Magnesium (Mg++) - exchangeable	ExchBases_ph-unkn-m3-spec	cmol/kg	0	100
108	Potassium (K+) - exchangeable	ExchBases_ph-unkn-m3-spec	cmol/kg	0	100
119	Aluminium (Al+++) - exchangeable	ExchBases_ph-unkn-m3-spec	cmol/kg	0	100
130	Calcium (Ca++) - exchangeable	ExchBases_ph-unkn-m3-spec	cmol/kg	0	100
98	Hydrogen (H+) - exchangeable	ExchBases_ph0-cohex	cmol/kg	0	100
142	Magnesium (Mg++) - exchangeable	ExchBases_ph0-cohex	cmol/kg	0	100
109	Potassium (K+) - exchangeable	ExchBases_ph0-cohex	cmol/kg	0	100
120	Aluminium (Al+++) - exchangeable	ExchBases_ph0-cohex	cmol/kg	0	100
131	Calcium (Ca++) - exchangeable	ExchBases_ph0-cohex	cmol/kg	0	100
99	Hydrogen (H+) - exchangeable	ExchBases_ph0-nh4cl	cmol/kg	0	100
143	Magnesium (Mg++) - exchangeable	ExchBases_ph0-nh4cl	cmol/kg	0	100
110	Potassium (K+) - exchangeable	ExchBases_ph0-nh4cl	cmol/kg	0	100
121	Aluminium (Al+++) - exchangeable	ExchBases_ph0-nh4cl	cmol/kg	0	100
132	Calcium (Ca++) - exchangeable	ExchBases_ph0-nh4cl	cmol/kg	0	100
100	Hydrogen (H+) - exchangeable	ExchBases_ph7-nh4oac	cmol/kg	0	100
144	Magnesium (Mg++) - exchangeable	ExchBases_ph7-nh4oac	cmol/kg	0	100
111	Potassium (K+) - exchangeable	ExchBases_ph7-nh4oac	cmol/kg	0	100
122	Aluminium (Al+++) - exchangeable	ExchBases_ph7-nh4oac	cmol/kg	0	100
133	Calcium (Ca++) - exchangeable	ExchBases_ph7-nh4oac	cmol/kg	0	100
101	Hydrogen (H+) - exchangeable	ExchBases_ph7-nh4oac-aas	cmol/kg	0	100
145	Magnesium (Mg++) - exchangeable	ExchBases_ph7-nh4oac-aas	cmol/kg	0	100
112	Potassium (K+) - exchangeable	ExchBases_ph7-nh4oac-aas	cmol/kg	0	100
123	Aluminium (Al+++) - exchangeable	ExchBases_ph7-nh4oac-aas	cmol/kg	0	100
134	Calcium (Ca++) - exchangeable	ExchBases_ph7-nh4oac-aas	cmol/kg	0	100
102	Hydrogen (H+) - exchangeable	ExchBases_ph7-nh4oac-fp	cmol/kg	0	100
146	Magnesium (Mg++) - exchangeable	ExchBases_ph7-nh4oac-fp	cmol/kg	0	100
113	Potassium (K+) - exchangeable	ExchBases_ph7-nh4oac-fp	cmol/kg	0	100
124	Aluminium (Al+++) - exchangeable	ExchBases_ph7-nh4oac-fp	cmol/kg	0	100
135	Calcium (Ca++) - exchangeable	ExchBases_ph7-nh4oac-fp	cmol/kg	0	100
103	Hydrogen (H+) - exchangeable	ExchBases_ph7-unkn	cmol/kg	0	100
147	Magnesium (Mg++) - exchangeable	ExchBases_ph7-unkn	cmol/kg	0	100
114	Potassium (K+) - exchangeable	ExchBases_ph7-unkn	cmol/kg	0	100
125	Aluminium (Al+++) - exchangeable	ExchBases_ph7-unkn	cmol/kg	0	100
136	Calcium (Ca++) - exchangeable	ExchBases_ph7-unkn	cmol/kg	0	100
104	Hydrogen (H+) - exchangeable	ExchBases_ph8-bacl2tea	cmol/kg	0	100
148	Magnesium (Mg++) - exchangeable	ExchBases_ph8-bacl2tea	cmol/kg	0	100
115	Potassium (K+) - exchangeable	ExchBases_ph8-bacl2tea	cmol/kg	0	100
126	Aluminium (Al+++) - exchangeable	ExchBases_ph8-bacl2tea	cmol/kg	0	100
137	Calcium (Ca++) - exchangeable	ExchBases_ph8-bacl2tea	cmol/kg	0	100
105	Hydrogen (H+) - exchangeable	ExchBases_ph8-unkn	cmol/kg	0	100
149	Magnesium (Mg++) - exchangeable	ExchBases_ph8-unkn	cmol/kg	0	100
116	Potassium (K+) - exchangeable	ExchBases_ph8-unkn	cmol/kg	0	100
127	Aluminium (Al+++) - exchangeable	ExchBases_ph8-unkn	cmol/kg	0	100
138	Calcium (Ca++) - exchangeable	ExchBases_ph8-unkn	cmol/kg	0	100
85	Sodium (Na+) - exchangeable	ExchBases_ph-unkn-m3	cmol/kg	0	100
86	Sodium (Na+) - exchangeable	ExchBases_ph-unkn-m3-spec	cmol/kg	0	100
87	Sodium (Na+) - exchangeable	ExchBases_ph0-cohex	cmol/kg	0	100
88	Sodium (Na+) - exchangeable	ExchBases_ph0-nh4cl	cmol/kg	0	100
89	Sodium (Na+) - exchangeable	ExchBases_ph7-nh4oac	cmol/kg	0	100
90	Sodium (Na+) - exchangeable	ExchBases_ph7-nh4oac-aas	cmol/kg	0	100
91	Sodium (Na+) - exchangeable	ExchBases_ph7-nh4oac-fp	cmol/kg	0	100
92	Sodium (Na+) - exchangeable	ExchBases_ph7-unkn	cmol/kg	0	100
93	Sodium (Na+) - exchangeable	ExchBases_ph8-bacl2tea	cmol/kg	0	100
94	Sodium (Na+) - exchangeable	ExchBases_ph8-unkn	cmol/kg	0	100
\.


--
-- TOC entry 4965 (class 0 OID 54922828)
-- Dependencies: 228
-- Data for Name: plot; Type: TABLE DATA; Schema: core; Owner: glosis
--

COPY core.plot (plot_id, site_id, plot_code, altitude, time_stamp, map_sheet_code, positional_accuracy, "position", type) FROM stdin;
\.


--
-- TOC entry 4966 (class 0 OID 54922837)
-- Dependencies: 229
-- Data for Name: plot_individual; Type: TABLE DATA; Schema: core; Owner: glosis
--

COPY core.plot_individual (plot_id, individual_id) FROM stdin;
\.


--
-- TOC entry 4968 (class 0 OID 54922842)
-- Dependencies: 231
-- Data for Name: procedure_desc; Type: TABLE DATA; Schema: core; Owner: glosis
--

COPY core.procedure_desc (procedure_desc_id, reference, uri) FROM stdin;
WRB fourth edition 2022	WRB fourth edition 2022	https://www.fao.org/soils-portal/data-hub/soil-classification/world-reference-base/en/
\.


--
-- TOC entry 4969 (class 0 OID 54922850)
-- Dependencies: 232
-- Data for Name: procedure_phys_chem; Type: TABLE DATA; Schema: core; Owner: glosis
--

COPY core.procedure_phys_chem (procedure_phys_chem_id, broader_id, uri, definition, reference, citation) FROM stdin;
pHH2O	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHH2O	pHH2O (soil reaction) in a soil/water solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
TotalN_dc-ht-dumas	\N	http://w3id.org/glosis/model/procedure/nitrogenTotalProcedure-TotalN_dc-ht-dumas	Dry combustion at 800-1000 C celcius (Dumas method)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
TotalN_dc-ht-leco	\N	http://w3id.org/glosis/model/procedure/nitrogenTotalProcedure-TotalN_dc-ht-leco	Element analyzer (LECO analyzer), Dry Combustion	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHKCl	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHKCl	pHKCl (soil reaction) in a soil/KCl solution (0.01-1 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
SaSiCl_2-50-2000u-adj100	\N	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-50-2000u-adj100	\N	\N	\N
SaSiCl_2-20-2000u-adj100	\N	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-20-2000u-adj100	\N	\N	\N
SaSiCl_2-20-2000u-disp	\N	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-20-2000u-disp	\N	\N	\N
SaSiCl_2-20-2000u-fld	\N	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-20-2000u-fld	\N	\N	\N
SaSiCl_2-20-2000u-nodisp	\N	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-20-2000u-nodisp	\N	\N	\N
SaSiCl_2-50-2000u-disp	\N	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-50-2000u-disp	\N	\N	\N
SaSiCl_2-50-2000u-fld	\N	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-50-2000u-fld	\N	\N	\N
SaSiCl_2-50-2000u-nodisp	\N	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-50-2000u-nodisp	\N	\N	\N
SaSiCl_2-64-2000u-adj100	\N	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-64-2000u-adj100	\N	\N	\N
SaSiCl_2-64-2000u-disp	\N	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-64-2000u-disp	\N	\N	\N
SaSiCl_2-64-2000u-fld	\N	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-64-2000u-fld	\N	\N	\N
SaSiCl_2-64-2000u-nodisp	\N	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-64-2000u-nodisp	\N	\N	\N
SaSiCl_2-20-2000u	\N	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-20-2000u	\N	\N	\N
SaSiCl_2-50-2000u	\N	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-50-2000u	\N	\N	\N
SaSiCl_2-64-2000u	\N	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-64-2000u	\N	\N	\N
SaSiCl_2-20-2000u-disp-beaker	SaSiCl_2-20-2000u-disp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-20-2000u-disp-beaker	\N	\N	\N
SaSiCl_2-20-2000u-disp-hydrometer	SaSiCl_2-20-2000u-disp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-20-2000u-disp-hydrometer	\N	\N	\N
SaSiCl_2-20-2000u-disp-hydrometer-bouy	SaSiCl_2-20-2000u-disp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-20-2000u-disp-hydrometer-bouy	\N	\N	\N
SaSiCl_2-20-2000u-disp-laser	SaSiCl_2-20-2000u-disp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-20-2000u-disp-laser	\N	\N	\N
SaSiCl_2-20-2000u-disp-pipette	SaSiCl_2-20-2000u-disp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-20-2000u-disp-pipette	\N	\N	\N
SaSiCl_2-20-2000u-disp-spec	SaSiCl_2-20-2000u-disp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-20-2000u-disp-spec	\N	\N	\N
SaSiCl_2-20-2000u-nodisp-hydrometer	SaSiCl_2-20-2000u-nodisp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-20-2000u-nodisp-hydrometer	\N	\N	\N
SaSiCl_2-20-2000u-nodisp-hydrometer-bouy	SaSiCl_2-20-2000u-nodisp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-20-2000u-nodisp-hydrometer-bouy	\N	\N	\N
SaSiCl_2-20-2000u-nodisp-laser	SaSiCl_2-20-2000u-nodisp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-20-2000u-nodisp-laser	\N	\N	\N
SaSiCl_2-20-2000u-nodisp-pipette	SaSiCl_2-20-2000u-nodisp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-20-2000u-nodisp-pipette	\N	\N	\N
SaSiCl_2-20-2000u-nodisp-spec	SaSiCl_2-20-2000u-nodisp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-20-2000u-nodisp-spec	\N	\N	\N
SaSiCl_2-50-2000u-disp-beaker	SaSiCl_2-50-2000u-disp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-50-2000u-disp-beaker	\N	\N	\N
SaSiCl_2-50-2000u-disp-hydrometer	SaSiCl_2-50-2000u-disp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-50-2000u-disp-hydrometer	\N	\N	\N
SaSiCl_2-50-2000u-disp-hydrometer-bouy	SaSiCl_2-50-2000u-disp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-50-2000u-disp-hydrometer-bouy	\N	\N	\N
SaSiCl_2-50-2000u-disp-laser	SaSiCl_2-50-2000u-disp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-50-2000u-disp-laser	\N	\N	\N
SaSiCl_2-50-2000u-disp-pipette	SaSiCl_2-50-2000u-disp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-50-2000u-disp-pipette	\N	\N	\N
SaSiCl_2-50-2000u-disp-spec	SaSiCl_2-50-2000u-disp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-50-2000u-disp-spec	\N	\N	\N
SaSiCl_2-50-2000u-nodisp-hydrometer	SaSiCl_2-50-2000u-nodisp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-50-2000u-nodisp-hydrometer	\N	\N	\N
SaSiCl_2-50-2000u-nodisp-hydrometer-bouy	SaSiCl_2-50-2000u-nodisp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-50-2000u-nodisp-hydrometer-bouy	\N	\N	\N
SaSiCl_2-50-2000u-nodisp-laser	SaSiCl_2-50-2000u-nodisp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-50-2000u-nodisp-laser	\N	\N	\N
SaSiCl_2-50-2000u-nodisp-pipette	SaSiCl_2-50-2000u-nodisp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-50-2000u-nodisp-pipette	\N	\N	\N
SaSiCl_2-50-2000u-nodisp-spec	SaSiCl_2-50-2000u-nodisp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-50-2000u-nodisp-spec	\N	\N	\N
SaSiCl_2-64-2000u-disp-beaker	SaSiCl_2-64-2000u-disp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-64-2000u-disp-beaker	\N	\N	\N
SaSiCl_2-64-2000u-disp-hydrometer	SaSiCl_2-64-2000u-disp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-64-2000u-disp-hydrometer	\N	\N	\N
SaSiCl_2-64-2000u-disp-hydrometer-bouy	SaSiCl_2-64-2000u-disp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-64-2000u-disp-hydrometer-bouy	\N	\N	\N
SaSiCl_2-64-2000u-disp-laser	SaSiCl_2-64-2000u-disp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-64-2000u-disp-laser	\N	\N	\N
SaSiCl_2-64-2000u-disp-pipette	SaSiCl_2-64-2000u-disp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-64-2000u-disp-pipette	\N	\N	\N
SaSiCl_2-64-2000u-disp-spec	SaSiCl_2-64-2000u-disp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-64-2000u-disp-spec	\N	\N	\N
SaSiCl_2-64-2000u-nodisp-hydrometer	SaSiCl_2-64-2000u-nodisp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-64-2000u-nodisp-hydrometer	\N	\N	\N
SaSiCl_2-64-2000u-nodisp-hydrometer-bouy	SaSiCl_2-64-2000u-nodisp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-64-2000u-nodisp-hydrometer-bouy	\N	\N	\N
SaSiCl_2-64-2000u-nodisp-laser	SaSiCl_2-64-2000u-nodisp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-64-2000u-nodisp-laser	\N	\N	\N
SaSiCl_2-64-2000u-nodisp-pipette	SaSiCl_2-64-2000u-nodisp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-64-2000u-nodisp-pipette	\N	\N	\N
SaSiCl_2-64-2000u-nodisp-spec	SaSiCl_2-64-2000u-nodisp	http://w3id.org/glosis/model/procedure/textureProcedure-SaSiCl_2-64-2000u-nodisp-spec	\N	\N	\N
OrgC_wc	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_wc	Wet oxidation or wet combustion methods	\N	\N
Extr_m1	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_m1	Mehlich1 method	https://www.ncagr.gov/AGRONOMI/pdffiles/mehlich53.pdf	\N
TotalN_h2so4	\N	http://w3id.org/glosis/model/procedure/nitrogenTotalProcedure-TotalN_h2so4	H2SO4	\N	\N
TotalN_calcul	\N	http://w3id.org/glosis/model/procedure/nitrogenTotalProcedure-TotalN_calcul	OC * 1.72 / 20 (gives C/N=11.6009)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
TotalN_kjeldahl	\N	http://w3id.org/glosis/model/procedure/nitrogenTotalProcedure-TotalN_kjeldahl	Method of Kjeldahl (digestion)	https://en.wikipedia.org/wiki/Kjeldahl_method	Kjeldahl, J. (1883) ‘Neue Methode zur Bestimmung des Stickstoffs in organischen Körpern’ (New method for the determination of nitrogen in organic substances), Zeitschrift für analytische Chemie, 22 (1) : 366-383.
TotalN_dc-spec	\N	http://w3id.org/glosis/model/procedure/nitrogenTotalProcedure-TotalN_dc-spec	Spectrally measured and converted to N by dry combustion	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
TotalN_kjeldahl-nh4	\N	http://w3id.org/glosis/model/procedure/nitrogenTotalProcedure-TotalN_kjeldahl-nh4	Kjeldahl, and ammonia distillation	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
TotalN_tn08	\N	http://w3id.org/glosis/model/procedure/nitrogenTotalProcedure-TotalN_tn08	Sample digested by sulphuric acid, distillation of released ammonia, back titration against sulpuric acid	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Extr_dtpa	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_dtpa	DiethyneleTriaminePentaAcetic acid (DTPA) method	https://doi.org/10.2136/sssaj1978.03615995004200030009x	\N
TotalN_tn04	\N	http://w3id.org/glosis/model/procedure/nitrogenTotalProcedure-TotalN_tn04	Dry combustion using a CN-corder and cobalt oxide or copper oxide as an oxidation accelerator (Tanabe and Araragi, 1970)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
TotalN_calcul-oc10	\N	http://w3id.org/glosis/model/procedure/nitrogenTotalProcedure-TotalN_calcul-oc10	Calculated from OrgC and C/N ratio of 10	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
TotalN_nelson	\N	http://w3id.org/glosis/model/procedure/nitrogenTotalProcedure-TotalN_nelson	Nelson and Sommers, 1980	https://doi.org/10.1093/jaoac/63.4.770	Darrell W Nelson, Lee E Sommers, Total Nitrogen Analysis of Soil and Plant Tissues, Journal of Association of Official Analytical Chemists, Volume 63, Issue 4, 1 July 1980, Pages 770–778,
TotalN_dc	\N	http://w3id.org/glosis/model/procedure/nitrogenTotalProcedure-TotalN_dc	Dry combustion	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
TotalN_tn06	\N	http://w3id.org/glosis/model/procedure/nitrogenTotalProcedure-TotalN_tn06	Continuous flow analyser after digestion with H2SO4/salicyclic acid/H2O2/Se	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
TotalN_bremner	\N	http://w3id.org/glosis/model/procedure/nitrogenTotalProcedure-TotalN_bremner	Total N (Bremner, 1965, p. 1162-1164)	https://doi.org/10.2134/agronmonogr9.2.c32	Bremner, J. M. 1965. Total Nitrogen. In: C. A. Black (ed.) Methods of soil analysis. Part 2: Chemical and microbial properties. Number 9 in series Agronomy. American Society of Agronomy, Inc. Publisher, Madison, USA. Pp. 1049-1178
PAWHC_calcul-fc200wp	\N	http://w3id.org/glosis/model/procedure/availableWaterHoldingCapacityProcedure-PAWHC_calcul-fc200wp	Plant available water holding capacity of the soil fine earth fraction, calculated with field capacity defined at 200 cm (pF 2.3)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
PAWHC_calcul-fc300wp	\N	http://w3id.org/glosis/model/procedure/availableWaterHoldingCapacityProcedure-PAWHC_calcul-fc300wp	Plant available water holding capacity of the soil fine earth fraction, calculated with field capacity defined at 300 cm (pF 2.5)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
PAWHC_calcul-fc100wp	\N	http://w3id.org/glosis/model/procedure/availableWaterHoldingCapacityProcedure-PAWHC_calcul-fc100wp	Plant available water holding capacity of the soil fine earth fraction, calculated with field capacity defined at 100 cm (pF 2.0)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
InOrgC_calcul-caco3	\N	http://w3id.org/glosis/model/procedure/carbonInorganicProcedure-InOrgC_calcul-caco3	Indirect estimate from total carbonate equivalent, with a factor of 0.12 (molar weights: CaCO3 100g/mol, C 12g/mol)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
InOrgC_calcul-tc-oc	\N	http://w3id.org/glosis/model/procedure/carbonInorganicProcedure-InOrgC_calcul-tc-oc	Indirect estimate (total carbon minus organic carbon = inorganic carbon)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
EffCEC_calcul-b	\N	http://w3id.org/glosis/model/procedure/effectiveCecProcedure-EffCEC_calcul-b	Sum of exchangeable bases (Ca, Mg, K, Na) without exchangeable acidity (H+Al), see ExchBases and ExchAcids for methods	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Total_unkn	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_unkn	Unspecified method	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
EffCEC_calcul-ba	\N	http://w3id.org/glosis/model/procedure/effectiveCecProcedure-EffCEC_calcul-ba	Sum of exchangeable bases (Ca, Mg, K, Na) plus exchangeable acidity (H+Al), see ExchBases and ExchAcids for methods	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Total_nh4-6mo7o24	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_nh4-6mo7o24	COLORIMETRIC VANADATE MOLYBDATE. Particularly used for Total P.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Total_tp05	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_tp05	8 M HCl extraction. Particularly used for Total P.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Total_hcl-aquaregia	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_hcl-aquaregia	Hydrocloric (HCl) extraction in nitric/perchloric acid mixture (totals) aqua regia	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Total_xrf	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_xrf	XRF	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Total_xrd	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_xrd	XRD	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Total_xrf-p	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_xrf-p	PXRF	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHCaCl2_sat	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHCaCl2_sat	pHCaCl2 (soil reaction) in saturated paste	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Total_tp03	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_tp03	reagent of Baeyens. Precipitation in form of Phosphomolybdate. Particularly used for Total P.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Total_hcl	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_hcl	HCl extraction. Particularly used for Total P.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Total_hclo4	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_hclo4	Perchloric acid percolation. Particularly used for Total P.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Total_tp10	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_tp10	Colorimetric, unspecified extract	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Total_tp07	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_tp07	1:1 H2SO4 : HNO3. Particularly used for Total P.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Total_tp04	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_tp04	acid fleischman. Particularly used for Total P.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Total_tp09	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_tp09	Walker and Adams, 1958. Particularly used for Total P.	\N	WALKER, T. W., AND A. F. R. ADAMS. 1958. Studies on soil organic matter. I. Soil Sci. 85: 307-318. 
Total_tp08	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_tp08	After Nitric acid attack (boiling with HNO3), colometric determination (method of Duval).. Particularly used for Total P.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Total_h2so4	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_h2so4	Total P-/- colorimetric in H2SO4-Se-Salicylic acid digest( sulfuric acid) Particularly used for Total P.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Total_tp06	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_tp06	Molybdenum blue method, using ascorbic acid as reductant after heating of soil to 550 C and extraction with 6M sulphuric acid. Particularly used for Total P.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Total_xtf-t	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_xtf-t	TXRF	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Total_hno3-aquafortis	\N	http://w3id.org/glosis/model/procedure/totalElementsProcedure-Total_hno3-aquafortis	Nitric acid attack. Particularly used for Total P.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_ca10	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_ca10	CaCO3 Equivalent, CO2 evolution after HCl treatment. Gravimetric	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BSat_calcul-ecec	\N	http://w3id.org/glosis/model/procedure/baseSaturationProcedure-BSat_calcul-ecec	Sum of exchangeable bases (Ca++, Mg++, K+, Na+) as percentage of EffCEC (method specified with EffCEC and ExchBases)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BSat_calcul-cec	\N	http://w3id.org/glosis/model/procedure/baseSaturationProcedure-BSat_calcul-cec	Sum of exchangeable bases (Ca++, Mg++, K+, Na+) as percentage of CEC (method specified with CEC and ExchBases)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
SlbAn_calcul-unkn	\N	http://w3id.org/glosis/model/procedure/solubleSaltsProcedure-SlbAn_calcul-unkn	Sum of soluble anions (Cl, SO4, HCO2, CO3, NO3, F)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
SlbCat_calcul-unkn	\N	http://w3id.org/glosis/model/procedure/solubleSaltsProcedure-SlbCat_calcul-unkn	Sum of soluble cations (Ca, Mg, K, Na)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_acid-h3po4-dc	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_acid-h3po4-dc	Dissolution of carbonates by Phosphoric acid [H3PO4], external heat (dry combustion)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_acid-h2so4-nodc	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_acid-h2so4-nodc	Dissolution of carbonates by Sulfuric acid [H2SO4], no external (no dry combustion)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_acid-ch3cooh-unkn	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_acid-ch3cooh-unkn	Dissolution of carbonates by Acetic acid [CH3COOH], external heat unknown	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_acid-dc	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_acid-dc	Dissolution of carbonates by acid, external heat (dry combustion)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_acid-h2so4-dc	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_acid-h2so4-dc	Dissolution of carbonates by Sulfuric acid [H2SO4], external heat (dry combustion)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_ca11	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_ca11	Black, 1965-HCl	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_acid-hcl-dc	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_acid-hcl-dc	Dissolution of carbonates by Hydrochloric acid [HCl], or Perchloric acid [HClO4], external heat (dry combustion)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_calcul-tc-oc	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_calcul-tc-oc	Indirect estimate: inorganic carbon divided by 0.12 (computed as total carbon minus organic carbon)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_ca01	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_ca01	Method of Scheibler (volumetric)	\N	ON L 1084-99 (1999) Chemical analyses of soils—determination of carbonate. In: Austrian Standards Institute (ed) O‹ NORM L 1084. Austrian Standards Institute, Vienna
CaCO3_ca04	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_ca04	Calcimeter method (volumetric after adition of dilute acid)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_acid-h2so4-unkn	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_acid-h2so4-unkn	Dissolution of carbonates by Sulfuric acid [H2SO4], external heat unknown	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_acid-hcl-unkn	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_acid-hcl-unkn	Dissolution of carbonates by Hydrochloric acid [HCl], or Perchloric acid [HClO4], external heat unknown	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_ca12	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_ca12	Treatment with H2SO4 N/2 acid followed by titration with NaOH N/2 in presence of an indicator	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
OrgC_dc-ht	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_dc-ht	Unacidified. Dry combustion at high temperature (e.g. 1200 C and colometric CO2 measurement (Schlichting et al. 1995)	\N	Schlichting E, Blume HP, Stahr K (1995) Soils Practical (in German). Blackwell, Berlin
CaCO3_ca08	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_ca08	Bernard calcimeter (Total CaCO3)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_ca07	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_ca07	Pressure calcimeter (Nelson, 1982)	https://acsess.onlinelibrary.wiley.com/doi/book/10.2134/agronmonogr9.2.2ed	Nelson, D.W., and L.E. Sommers. 1982. Total carbon, organic carbon and organic matter. p. 539-579. In A.L. Page (ed.), 1983. Methods of soil analysis. Part 2. 2nd ed. Agron. Monogr. 9. ASA and SSSA, Madison, WI.
CaCO3_ca09	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_ca09	Carbonates: H3PO4 treatment at 80 deg. C and CO2 measurement like TOC (OC13), transformation into CaCO3 (Schlichting et al. 1995)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_acid-ch3cooh-nodc	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_acid-ch3cooh-nodc	Dissolution of carbonates by Acetic acid [CH3COOH], no external (no dry combustion)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_acid-ch3cooh-dc	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_acid-ch3cooh-dc	Dissolution of carbonates by Acetic acid [CH3COOH], external heat (dry combustion)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_ca06	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_ca06	H3PO4 acid at 80C, conductometric in NaOH (Schlichting & Blume, 1966)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_acid-h3po4-unkn	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_acid-h3po4-unkn	Dissolution of carbonates by Phosphoric acid [H3PO4], external heat unknown	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_ca03	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_ca03	Method of Piper (HCl)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_acid-h3po4-nodc	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_acid-h3po4-nodc	Dissolution of carbonates by Phosphoric acid [H3PO4], no external (no dry combustion)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_ca05	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_ca05	Gravimetric (USDA Agr. Hdbk 60-/- method Richards et al., 1954)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_acid-hcl-nodc	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_acid-hcl-nodc	Dissolution of carbonates by Hydrochloric acid [HCl], or Perchloric acid [HClO4], no external (no dry combustion)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_acid-unkn	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_acid-unkn	Dissolution of carbonates by acid, external heat unknown	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaCO3_ca02	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_ca02	Method of Wesemael	\N	Wesemael, J.C., 1955. De bepaling van van calciumcarbonaatgehalte van gronden. Chemisch Weekblad 51, 35-36.
CaCO3_acid-nodc	\N	http://w3id.org/glosis/model/procedure/totalCarbonateEquivalentProcedure-CaCO3_acid-nodc	Dissolution of carbonates by acid, no external (no dry combustion)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
SumTxtr_calcul	\N	http://w3id.org/glosis/model/procedure/textureSumProcedure-SumTxtr_calcul	Calculated sum of sand, silt and clay fractions	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CrsFrg_fld	\N	http://w3id.org/glosis/model/procedure/coarseFragmentsProcedure-CrsFrg_fld	Particles > 2 mm observed in the field. May include concretions and very hard aggregates	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CrsFrg_fldcls	\N	http://w3id.org/glosis/model/procedure/coarseFragmentsProcedure-CrsFrg_fldcls	Particles > 2 mm observed in the field and calculated from class values. May include concretions and very hard aggregates	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CrsFrg_lab	\N	http://w3id.org/glosis/model/procedure/coarseFragmentsProcedure-CrsFrg_lab	Particles > 2 mm measured in laboratory (sieved after light pounding). May include concretions and very hard aggregates	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Poros_calcul-pf0	\N	http://w3id.org/glosis/model/procedure/porosityProcedure-Poros_calcul-pf0	Porosity calculated from volumetric moisture content at pF 0 (1 cm)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHNaF_ratio1-5	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHNaF_ratio1-5	pHNaF (soil reaction) in 1:5 soil/NaF solution (0.01-1 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHNaF_ratio1-1	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHNaF_ratio1-1	pHNaF (soil reaction) in 1:1 soil/NaF solution (1 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHH2O_sat	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHH2O_sat	pHH2O (soil reaction) in water saturated paste	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHNaF_ratio1-2.5	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHNaF_ratio1-2.5	pHNaF (soil reaction) in 1:2.5 soil/NaF solution (0.01-1 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHCaCl2_ratio1-1	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHCaCl2_ratio1-1	pHCaCl2 (soil reaction) in 1:1 soil/1 M CaCl2 solution (1 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHKCl_sat	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHKCl_sat	pHKCl (soil reaction) in saturated paste	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHKCl_ratio1-2	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHKCl_ratio1-2	pHKCl (soil reaction) in 1:2 soil/KCl solution (0.01-1 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHH2O_unkn-spec	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHH2O_unkn-spec	Spectrally measured and converted to pHH2O (soil reaction) in unknown soil/water solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHKCl_ratio1-5	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHKCl_ratio1-5	pHKCl (soil reaction) in 1:5 soil/KCl solution (0.01-1 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHNaF_ratio1-2	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHNaF_ratio1-2	pHNaF (soil reaction) in 1:2 soil/NaF solution (0.01-1 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHH2O_ratio1-2.5	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHH2O_ratio1-2.5	pHH2O (soil reaction) in 1:2.5 soil/water solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHCaCl2_ratio1-5	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHCaCl2_ratio1-5	pHCaCl2 (soil reaction) in 1:5 soil/CaCl2 solution (0.01-1 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHH2O_ratio1-1	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHH2O_ratio1-1	pHH2O (soil reaction) in 1:1 soil/water solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHCaCl2	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHCaCl2	pHCaCl2 (soil reaction) in a soil/CaCl2 solution (0.01-1 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHH2O_ratio1-2	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHH2O_ratio1-2	pHH2O (soil reaction) in 1:2 soil/water solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHCaCl2_ratio1-10	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHCaCl2_ratio1-10	pHCaCl2 (soil reaction) in 1:10 soil/CaCl2 solution (0.01-1 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHH2O_ratio1-5	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHH2O_ratio1-5	pHH2O (soil reaction) in 1:5 soil/water solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHKCl_ratio1-1	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHKCl_ratio1-1	pHKCl (soil reaction) in 1:1 soil/KCl solution (1 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHCaCl2_ratio1-2	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHCaCl2_ratio1-2	pHCaCl2 (soil reaction) in 1:2 soil/CaCl2 solution (0.01-1 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHCaCl2_ratio1-2.5	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHCaCl2_ratio1-2.5	pHCaCl2 (soil reaction) in 1:2.5 soil/CaCl2 solution (0.01-1 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHNaF_sat	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHNaF_sat	pHNaF (soil reaction) in saturated paste	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHNaF	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHNaF	pHNaF (soil reaction) in a soil/NaF solution (0.01-1 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHKCl_ratio1-2.5	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHKCl_ratio1-2.5	pHKCl (soil reaction) in 1:2.5 soil/KCl solution (0.01-1 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHNaF_ratio1-10	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHNaF_ratio1-10	pHNaF (soil reaction) in 1:10 soil/NaF solution (0.01-1 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHH2O_ratio1-10	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHH2O_ratio1-10	pHH2O (soil reaction) in 1:10 soil/water solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
pHKCl_ratio1-10	\N	http://w3id.org/glosis/model/procedure/pHProcedure-pHKCl_ratio1-10	pHKCl (soil reaction) in 1:10 soil/KCl solution (0.01-1 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
RetentP_unkn-spec	\N	http://w3id.org/glosis/model/procedure/phosphorusRetentionProcedure-RetentP_unkn-spec	Spectrally measured and converted to P retention (P buffer index)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
RetentP_blakemore	\N	http://w3id.org/glosis/model/procedure/phosphorusRetentionProcedure-RetentP_blakemore	P retention at ~pH4.6  (acc. Blakemore 1987)	\N	Blakemore L.C. Searle P.L. and Daly, B.K. (1987) Methods for chemical analysis of soils. NZ Soil Bureau, Lower Hutt, New Zealand.
BlkDensW_we-unkn	\N	http://w3id.org/glosis/model/procedure/bulkDensityWholeSoilProcedure-BlkDensW_we-unkn	Whole earth. Type of sample unknown, at unknown humidity, not corrected for coarse fragments if any	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BlkDensW_we-cl-fc	\N	http://w3id.org/glosis/model/procedure/bulkDensityWholeSoilProcedure-BlkDensW_we-cl-fc	Whole earth. Clod samples (natural clods), at field capacity (0.33 bar, 33 kPa, 330 cm, pF 2.5), not corrected for coarse fragments if any	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BlkDensW_we-cl-od	\N	http://w3id.org/glosis/model/procedure/bulkDensityWholeSoilProcedure-BlkDensW_we-cl-od	Whole earth. Clod samples (natural clods), at oven dry, not corrected for coarse fragments if any	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BlkDensW_we-co-od	\N	http://w3id.org/glosis/model/procedure/bulkDensityWholeSoilProcedure-BlkDensW_we-co-od	Whole earth. Core sampling (pF rings), at oven dry, not corrected for coarse fragments if any	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BlkDensW_we-cl-unkn	\N	http://w3id.org/glosis/model/procedure/bulkDensityWholeSoilProcedure-BlkDensW_we-cl-unkn	Whole earth. Clod samples (natural clods), at unknown humidity, not corrected for coarse fragments if any	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BlkDensW_we-co-fc	\N	http://w3id.org/glosis/model/procedure/bulkDensityWholeSoilProcedure-BlkDensW_we-co-fc	Whole earth. Core sampling (pF rings), at field capacity (0.33 bar, 33 kPa, 336 cm, pF 2.5), not corrected for coarse fragments if any	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BlkDensW_we-co-unkn	\N	http://w3id.org/glosis/model/procedure/bulkDensityWholeSoilProcedure-BlkDensW_we-co-unkn	Whole earth. Core sampling (pF rings), at unknown humidity, not corrected for coarse fragments if any	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BlkDensW_we-rpl-unkn	\N	http://w3id.org/glosis/model/procedure/bulkDensityWholeSoilProcedure-BlkDensW_we-rpl-unkn	Whole earth. Excavation and replacement (i.e. soils too fragile to remove a stable sample) e.g. by auger, at unknown humidity, not corrected for coarse fragments if any	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CEC_ph0-cohex	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph0-cohex	CEC unbuffered at pH of the soil, in Cobalt(III) hexamine chloride solution 0,0166M (Cohex) [Co[NH3]6]Cl3 ), ISO 23470 (2007)  exchange solution	https://www.iso.org/standard/36879.html	\N
CEC_ph8-baoac	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph8-baoac	CEC buffered at pH 8.0-8.5, in 0.5 M Ba-acetate exchange solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CEC_ph8-nh4oac	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph8-nh4oac	CEC buffered at pH 8.0-8.5, in 1 M NH4-acetate exchange solution (0.25-1.0 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CEC_ph0-nh4cl	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph0-nh4cl	CEC unbuffered at pH of the soil, in 1 M NH4-chloride exchange solution (0.2-1.0 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CEC_ph8-unkn	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph8-unkn	CEC buffered at pH 8.0-8.5, in unknown exchange solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CEC_ph-unkn-m3	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph-unkn-m3	CEC at unknown buffer, in Mehlich III exchange solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CEC_ph7-nh4oac	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph7-nh4oac	CEC buffered at pH 7, in 1 M NH4-acetate (NH4OAc) exchange solution (0.25-1.0 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CEC_ph7-unkn	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph7-unkn	CEC buffered at pH 7, in unknown exchange solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CEC_ph8-naoac	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph8-naoac	CEC buffered at pH 8.0-8.5, in 1 M Na-acetate exchange solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CEC_ph-unkn-cacl2	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph-unkn-cacl2	CEC at unknown buffer, in 0.1 M CaCl2 exchange solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CEC_ph0-kcl	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph0-kcl	CEC unbuffered at pH of the soil, in 1 M KCl exchange solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CEC_ph7-edta	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph7-edta	CEC buffered at pH 7, in 0.1 M Li-EDTA exchange solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CEC_ph0-unkn	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph0-unkn	CEC unbuffered at pH of the soil, in unknown exchange solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CEC_ph8-licl2tea	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph8-licl2tea	CEC buffered at pH 8.0-8.5, in 0.5 M Li-chloride - TEA exchange solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CEC_ph0-ag-thioura	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph0-ag-thioura	CEC unbuffered at pH of the soil, in 0.01 M Ag-thioura exchange solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CEC_ph0-bacl2	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph0-bacl2	CEC unbuffered at pH o the soil, in 0.5 M BaCl2 exchange solution (0.1.1.0 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CEC_ph8-bacl2tea	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph8-bacl2tea	CEC buffered at pH 8.0-8.5, in 0.5 M BaCl2-TEA exchange solution (0.1.1.0 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CEC_ph0-nh4oac	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph0-nh4oac	CEC unbuffered at pH of the soil, in 1 M NH4-acetate (NH4OAc) exchange solution (0.25-1.0 M)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CEC_ph-unkn-lioac	\N	http://w3id.org/glosis/model/procedure/cationExchangeCapacitySoilProcedure-CEC_ph-unkn-lioac	CEC at unknown buffer, in 0.5 M Li-acetate exchange solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
VMC_ud	\N	http://w3id.org/glosis/model/procedure/moistureContentProcedure-VMC_ud	Undisturbed samples	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
VMC_d-cl-ww	\N	http://w3id.org/glosis/model/procedure/moistureContentProcedure-VMC_d-cl-ww	Pressure-plate extraction, disturbed -clod- samples (wt%) * density on weight/weight basis; to be converted to v/v (with BD at appropriate humidity)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
VMC_calcul-ptf-brookscorey	\N	http://w3id.org/glosis/model/procedure/moistureContentProcedure-VMC_calcul-ptf-brookscorey	Calculated by PTF of brooks - corey	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
VMC_d-ww	\N	http://w3id.org/glosis/model/procedure/moistureContentProcedure-VMC_d-ww	Volumetric moisture content in disturbed samples on weight/weight basis to be converted to v/v (with BD at appropriate humidity)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
VMC_calcul-ptf	\N	http://w3id.org/glosis/model/procedure/moistureContentProcedure-VMC_calcul-ptf	Calculated by PTF	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
VMC_d-cl	\N	http://w3id.org/glosis/model/procedure/moistureContentProcedure-VMC_d-cl	Pressure-plate extraction, disturbed -clod- samples (wt%) * density	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
VMC_d	\N	http://w3id.org/glosis/model/procedure/moistureContentProcedure-VMC_d	Volumetric moisture content in disturbed samples	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
VMC_ud-co	\N	http://w3id.org/glosis/model/procedure/moistureContentProcedure-VMC_ud-co	Volumetric moisture content in undisturbed samples (pF rings cores)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
VMC_ud-cl	\N	http://w3id.org/glosis/model/procedure/moistureContentProcedure-VMC_ud-cl	Natural clod	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaSO4_gy01	\N	http://w3id.org/glosis/model/procedure/gypsumProcedure-CaSO4_gy01	Dissolved in water and precipitated by acetone	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaSO4_gy06	\N	http://w3id.org/glosis/model/procedure/gypsumProcedure-CaSO4_gy06	Total-S, using LECO furnace, minus easily soluble MgSO4 and Na2SO4	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaSO4_gy07	\N	http://w3id.org/glosis/model/procedure/gypsumProcedure-CaSO4_gy07	Schleiff method, electrometric	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaSO4_gy04	\N	http://w3id.org/glosis/model/procedure/gypsumProcedure-CaSO4_gy04	In 0.1 M Na3-EDTA-/- turbidimetric (Begheijn, 1993)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaSO4_gy03	\N	http://w3id.org/glosis/model/procedure/gypsumProcedure-CaSO4_gy03	Calculated from conductivity of successive dilutions	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaSO4_gy05	\N	http://w3id.org/glosis/model/procedure/gypsumProcedure-CaSO4_gy05	Gravimetric after dissolution in 0.2 N HCl (USSR-method)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
CaSO4_gy02	\N	http://w3id.org/glosis/model/procedure/gypsumProcedure-CaSO4_gy02	Differ. between Ca-conc. in sat. extr. and Ca-conc. in 1/50 s/w solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
EC_ratio1-10	\N	http://w3id.org/glosis/model/procedure/electricalConductivityProcedure-EC_ratio1-10	Elec. conductivity at 1:10 soil/water ratio	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
EC_ratio1-2	\N	http://w3id.org/glosis/model/procedure/electricalConductivityProcedure-EC_ratio1-2	Elec. conductivity at 1:2 soil/water ratio	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
EC_ratio1-2.5	\N	http://w3id.org/glosis/model/procedure/electricalConductivityProcedure-EC_ratio1-2.5	Elec. conductivity at 1:2.5 soil/water ratio	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
EC_ratio1-5	\N	http://w3id.org/glosis/model/procedure/electricalConductivityProcedure-EC_ratio1-5	Elec. conductivity at 1:5 soil/water ratio	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
ECe_sat	\N	http://w3id.org/glosis/model/procedure/electricalConductivityProcedure-ECe_sat	Elec. conductivity in saturated paste (ECe)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
EC_ratio1-1	\N	http://w3id.org/glosis/model/procedure/electricalConductivityProcedure-EC_ratio1-1	Elec. conductivity at 1:1 soil/water ratio	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
ExchBases_ph7-nh4oac-fp	\N	http://w3id.org/glosis/model/procedure/exchangeableBasesProcedure-ExchBases_ph7-nh4oac-fp	Exch bases (Ca, Mg, K, Na) buffered at pH 7, in 1M NH4OAc, K and Na with FP (Flame Photometry)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
ExchBases_ph8-bacl2tea	\N	http://w3id.org/glosis/model/procedure/exchangeableBasesProcedure-ExchBases_ph8-bacl2tea	Exch bases (Ca, Mg, K, Na) buffered at pH 8.0-8.5, in 0.5 M BaCl2 - TEA solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
ExchBases_ph-unkn-edta	\N	http://w3id.org/glosis/model/procedure/exchangeableBasesProcedure-ExchBases_ph-unkn-edta	Exch bases (Ca, Mg, K, Na) unknown buffer, in EDTA solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
ExchBases_ph-unkn-m3	\N	http://w3id.org/glosis/model/procedure/exchangeableBasesProcedure-ExchBases_ph-unkn-m3	Exch bases (Ca, Mg, K, Na) unknown buffer, in Mehlich3 solution with extractable ppm assumed exchangeable cmolc/kg	https://doi.org/10.1080/00103628409367568	\N
ExchBases_ph0-nh4cl	\N	http://w3id.org/glosis/model/procedure/exchangeableBasesProcedure-ExchBases_ph0-nh4cl	Exch bases (Ca, Mg, K, Na) unbuffered, in 1 M NH4Cl (0.05-1.0 m?)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
ExchBases_ph8-unkn	\N	http://w3id.org/glosis/model/procedure/exchangeableBasesProcedure-ExchBases_ph8-unkn	Exch bases (Ca, Mg, K, Na) buffered at pH 8.0-8.5, in unknown solution	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
ExchBases_ph7-nh4oac	\N	http://w3id.org/glosis/model/procedure/exchangeableBasesProcedure-ExchBases_ph7-nh4oac	Exch bases (Ca, Mg, K, Na) buffered at pH 7, in 1M NH4OAc	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
ExchBases_ph0-cohex	\N	http://w3id.org/glosis/model/procedure/exchangeableBasesProcedure-ExchBases_ph0-cohex	Exch bases (Ca, Mg, K, Na) unbuffered, in Cobalt(III) hexamine chloride solution 0,0166M (Cohex) [Co[NH3]6]Cl3 ), ISO 23470 (2007)	https://www.iso.org/standard/36879.html	\N
ExchBases_ph7-unkn	\N	http://w3id.org/glosis/model/procedure/exchangeableBasesProcedure-ExchBases_ph7-unkn	Exch bases (Ca, Mg, K, Na) buffered at pH 7, in unknown solution	https://www.isric.org/sites/default/files/WOSISprocedureManual_2020nov17web.pdf#page=70	\N
ExchBases_ph-unkn-m3-spec	\N	http://w3id.org/glosis/model/procedure/exchangeableBasesProcedure-ExchBases_ph-unkn-m3-spec	Exch bases (Ca, Mg, K, Na) spectrally measured and converted to, unknown buffer, in Mehlich3 solution with extractable ppm assumed exchangeable cmolc/kg	https://doi.org/10.1080/00103628409367568	\N
ExchBases_ph7-nh4oac-aas	\N	http://w3id.org/glosis/model/procedure/exchangeableBasesProcedure-ExchBases_ph7-nh4oac-aas	Exch bases (Ca, Mg, K, Na) buffered at pH 7, in 1M NH4OAc, Ca and Mg with AAS (Atomic Absorption Spectrometry)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
OrgC_dc-lt-loi	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_dc-lt-loi	Unacidified. Loss on ignition (NL) is total Organic Carbon	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
OrgC_calcul-tc-ic	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_calcul-tc-ic	Calculated as total carbon minus inorganic carbon	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
OrgC_wc-cro3-tiurin	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_wc-cro3-tiurin	Wet oxidation according to Tiurin with K-dichromate	\N	I. V. TIURIN, Pochvovodenie (Pedology), (1931) 36.
OrgC_dc-lt	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_dc-lt	Unacidified. Dry combustion at low temperature e.g. 500 C	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
OrgC_acid-dc	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_acid-dc	Acidified dry combustion or dry oxidation methods (after removal of carbonates)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
OrgC_acid-dc-ht-analyser	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_acid-dc-ht-analyser	Acidified. Furnace combustion (e.g., LECO combustion analyzer, Dumas method)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
OrgC_acid-dc-lt	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_acid-dc-lt	Acidified. Dry combustion at 500 C	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
OrgC_wc-cro3-nelson	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_wc-cro3-nelson	Wet oxidation according to Nelson and Sommers (1996)	\N	Nelson and Sommers (1996) in: Sparks DL (ed.). Soil Sci. Soc. Am. book series 5, part 3, pp 961-1010.
OrgC_dc	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_dc	Unacidified. Dry combustion or dry oxidation methods (without prior removal of carbonates)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
OrgC_acid-dc-lt-loi	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_acid-dc-lt-loi	Acidified. Loss on ignition (NL)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
OrgC_wc-cro3-walkleyblack	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_wc-cro3-walkleyblack	Walkley-Black method (chromic acid digestion)	\N	Walkley, A. and I. A. Black. 1934. An Examination of Degtjareff Method for Determining Soil Organic Matter and a Proposed Modification of the Chromic Acid Titration Method. Soil Sci. 37:29–37.
OrgC_acid-dc-ht	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_acid-dc-ht	Acidified. Dry combustion at 1200 C and colometric CO2 measurement (Schlichting et al. 1995)	\N	Schlichting E, Blume HP, Stahr K (1995) Soils Practical (in German). Blackwell, Berlin
OrgC_dc-spec	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_dc-spec	Spectrally measured and converted to Unacidified Dry combustion or dry oxidation methods	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
OrgC_wc-cro3-knopp	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_wc-cro3-knopp	Wet oxidation according to Knopp with chromic acid and gravimetric determination of CO2	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
OrgC_dc-ht-analyser	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_dc-ht-analyser	Unacidified. Dry combustion by furnace (e.g., LECO combustion analyzer, Dumas method). Is total Carbon?	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
OrgC_wc-cro3-nrcs6a1c	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_wc-cro3-nrcs6a1c	Wet oxidation according to USDA-NRCS method 6A1c with acid dichromate digestion, FeSO4 titration, automatic titrator	https://www.nrcs.usda.gov/Internet/FSE_DOCUMENTS/stelprdb1253872.pdf	\N
OrgC_wc-cro3-kalembra	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_wc-cro3-kalembra	Wet oxidation according to Kalembra and Jenkinson (1973) with acid dichromate	https://doi.org/10.1002/jsfa.2740240910	\N
OrgC_acid-dc-mt	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_acid-dc-mt	Acidified. Dry combustion at 840 C	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
OrgC_wc-cro3-jackson	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_wc-cro3-jackson	Wet oxidation according to Jackson (1958) with chromic acid digestion	\N	Jackson, M. L. (1958) Soil Chemical Analysis. Prentice-Hall, Englewood Cliffs, New Jersey.
OrgC_acid-dc-spec	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_acid-dc-spec	Spectrally measured and converted to Acidified dry combustion or dry oxidation methods (after removal of carbonates)	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
OrgC_wc-cro3-kurmies	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_wc-cro3-kurmies	Wet oxidation according to Kurmies with K2Cr2O7+H2SO4	\N	B. KURMIES, Z. Pflanzenernühr. Dung. u Bodenk., 44 (1949) 121
OrgC_dc-mt	\N	http://w3id.org/glosis/model/procedure/carbonOrganicProcedure-OrgC_dc-mt	Unacidified. Dry combustion at medium temperature e.g. 840 C	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
ExchAcid_ph7-unkn	\N	http://w3id.org/glosis/model/procedure/acidityExchangeableProcedure-ExchAcid_ph7-unkn	Exch acidity (H+Al) buffered at pH 7, in unknown extract	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
ExchAcid_ph0-unkn	\N	http://w3id.org/glosis/model/procedure/acidityExchangeableProcedure-ExchAcid_ph0-unkn	Exch acidity (H+Al) unbuffered, in unknown extract	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
ExchAcid_ph8-bacl2tea	\N	http://w3id.org/glosis/model/procedure/acidityExchangeableProcedure-ExchAcid_ph8-bacl2tea	Exch (extractable / potential) acidity (Al) buffered at pH 8.0-8.5, in 1 M BaCl2 - TEA	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
ExchAcid_ph0-kcl1m	\N	http://w3id.org/glosis/model/procedure/acidityExchangeableProcedure-ExchAcid_ph0-kcl1m	Exch acidity (H+Al) unbuffered, in 1 M KCl extract	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
ExchAcid_ph0-nh4cl	\N	http://w3id.org/glosis/model/procedure/acidityExchangeableProcedure-ExchAcid_ph0-nh4cl	Exch acidity (H+Al) unbuffered, in 0.05-0.1 M NH4Cl extract	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
ExchAcid_ph7-caoac	\N	http://w3id.org/glosis/model/procedure/acidityExchangeableProcedure-ExchAcid_ph7-caoac	Exch acidity (H+Al) buffered at pH 7, in 1M Ca-acetate extract	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
ExchAcid_ph8-unkn	\N	http://w3id.org/glosis/model/procedure/acidityExchangeableProcedure-ExchAcid_ph8-unkn	Exch (extractable / potential) acidity (Al) buffered at pH 8.0-8.5, in unknown extract	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
HumAcidC_unkn	\N	http://w3id.org/glosis/model/procedure/organicMatterProcedure-HumAcidC_unkn	Humic acid carbon_unknown method	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
FulAcidC_unkn	\N	http://w3id.org/glosis/model/procedure/organicMatterProcedure-FulAcidC_unkn	Fulvic acid carbon_unknown method	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
TotHumC_unkn	\N	http://w3id.org/glosis/model/procedure/organicMatterProcedure-TotHumC_unkn	Total humic carbon_unknown method	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
OrgM_calcul-oc1.73	\N	http://w3id.org/glosis/model/procedure/organicMatterProcedure-OrgM_calcul-oc1.73	Organic carbon * 1,73	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BlkDensF_fe-co-od	\N	http://w3id.org/glosis/model/procedure/bulkDensityFineEarthProcedure-BlkDensF_fe-co-od	Fine earth. Core sampling (pF rings), at oven dry, corrected for coarse fragments if any	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BlkDensF_fe-co-unkn	\N	http://w3id.org/glosis/model/procedure/bulkDensityFineEarthProcedure-BlkDensF_fe-co-unkn	Fine earth. Core sampling (pF rings), at unknown humidity, corrected for coarse fragments if any	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BlkDensF_fe-unkn-od	\N	http://w3id.org/glosis/model/procedure/bulkDensityFineEarthProcedure-BlkDensF_fe-unkn-od	Fine earth. Type of sample unknown, at oven dry, corrected for coarse fragments if any	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BlkDensF_fe-co-fc	\N	http://w3id.org/glosis/model/procedure/bulkDensityFineEarthProcedure-BlkDensF_fe-co-fc	Fine earth. Core sampling (pF rings), at field capacity (0.33 bar, 33 kPa, 336 cm, pF 2.5), corrected for coarse fragments if any	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BlkDensF_fe-rpl-unkn	\N	http://w3id.org/glosis/model/procedure/bulkDensityFineEarthProcedure-BlkDensF_fe-rpl-unkn	Fine earth. Excavation and replacement (i.e. soils too fragile to remove a stable sample) e.g. by auger, at unknown humidity, corrected for coarse fragments if any	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BlkDensF_fe-cl-unkn	\N	http://w3id.org/glosis/model/procedure/bulkDensityFineEarthProcedure-BlkDensF_fe-cl-unkn	Fine earth. Clod samples (natural clods or reconstituted from < 2mm sample), at unknown humidity, corrected for coarse fragments if any	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BlkDensF_fe-unkn-fc	\N	http://w3id.org/glosis/model/procedure/bulkDensityFineEarthProcedure-BlkDensF_fe-unkn-fc	Fine earth. Type of sample unknown, at field capacity (0.33 bar, 33 kPa, 330 cm, pF 2.5), corrected for coarse fragments if any	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BlkDensF_fe-cl-od	\N	http://w3id.org/glosis/model/procedure/bulkDensityFineEarthProcedure-BlkDensF_fe-cl-od	Fine earth. Clod samples (natural clods or reconstituted from < 2mm sample), at oven dry, corrected for coarse fragments if any	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BlkDensF_fe-cl-fc	\N	http://w3id.org/glosis/model/procedure/bulkDensityFineEarthProcedure-BlkDensF_fe-cl-fc	Fine earth. Clod samples (natural clods or reconstituted from < 2mm sample), at field capacity (0.33 bar, 33 kPa, 330 cm, pF 2.5), corrected for coarse fragments if any	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
BlkDensF_fe-unkn	\N	http://w3id.org/glosis/model/procedure/bulkDensityFineEarthProcedure-BlkDensF_fe-unkn	Fine earth. Type of sample unknown, at unknown humidity, corrected for coarse fragments if any	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
KSat_calcul-ptf-saxton	\N	http://w3id.org/glosis/model/procedure/hydraulicConductivityProcedure-KSat_calcul-ptf-saxton	Saturated hydraulic conductivity.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Ksat_invbhole	\N	http://w3id.org/glosis/model/procedure/hydraulicConductivityProcedure-Ksat_invbhole	Saturated hydraulic conductivity. Inverse bore hole method	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
KSat_calcul-ptf	\N	http://w3id.org/glosis/model/procedure/hydraulicConductivityProcedure-KSat_calcul-ptf	Saturated hydraulic conductivity.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
KSat_calcul-ptf-genuchten	\N	http://w3id.org/glosis/model/procedure/hydraulicConductivityProcedure-KSat_calcul-ptf-genuchten	Saturated and not saturated hydraulic conductivity.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Ksat_column	\N	http://w3id.org/glosis/model/procedure/hydraulicConductivityProcedure-Ksat_column	Saturated hydraulic conductivity. Permeability in cm/hr determined in column filled with fine earth fraction	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Ksat_dblring	\N	http://w3id.org/glosis/model/procedure/hydraulicConductivityProcedure-Ksat_dblring	Saturated hydraulic conductivity. Double ring method	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Ksat_bhole	\N	http://w3id.org/glosis/model/procedure/hydraulicConductivityProcedure-Ksat_bhole	Saturated hydraulic conductivity. Bore hole method	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Extr_ap15	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_ap15	Method of Hunter (1975) modified after ISFEI method. Particularly used for available P.	\N	Hunter, A. 1975. New techniques and equipment for routine soil/plant analytical procedures. In: Soil Management in Tropical America. (eds E. Borremiza & A. Alvarado). N.C. State University, Raleigh, NC.
Extr_edta	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_edta	EthyleneDiamineTetraAcetic acid (EDTA) method	https://journals.lww.com/soilsci/Citation/1954/10000/SOIL_AND_PLANT_STUDIES_WITH_CHELATES_OF.8.aspx	\N
Extr_nahco3-olsen	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_nahco3-olsen	Method of Olsen (0.5 M Sodium Bicarbonate (NaHCO3) extraction at pH8.5). Particularly used for available P.	https://acsess.onlinelibrary.wiley.com/doi/book/10.2134/agronmonogr9.2	\N
Extr_hcl-nh4f-bray1	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_hcl-nh4f-bray1	Method of Bray I  (dilute HCl/NH4F). Particularly used for available P.	https://doi.org/10.1097/00010694-194501000-00006	\N
Extr_ap20	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_ap20	Olsen (not acid soils) resp. Bray I (acid soils). Particularly used for available P.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Extr_hotwater	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_hotwater	Hot water. Particularly used for available B	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Extr_m3	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_m3	Mehlich3 method (extractant 0.2 N CH3COOH + 0.25 N NH4NO3 + 0.015 N NH4F + 0.013 N HNO3 + 0.001 M EDTA)	https://doi.org/10.1080/00103628409367568	\N
Extr_nahco3-olsen-dabin	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_nahco3-olsen-dabin	Method of Olsen, modified by Dabin (ORSTOM). Particularly used for available P.	https://docplayer.fr/81912854-Application-des-dosages-automatiques-a-l-analyse-des-sols-2e-partie-par.html	\N
Extr_hcl-nh4f-kurtz-bray	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_hcl-nh4f-kurtz-bray	Method of Kurtz-Bray I (0.025 M HCl + 0.03 M NH4F). Particularly used for available P.	https://doi.org/10.1097/00010694-194501000-00006	\N
Extr_ap21	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_ap21	Olsen (if pH > 7) resp. Mehlich (if pH < 7). Particularly used for available P.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Extr_capo4	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_capo4	Ca phosphate. Particularly used for available S.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Extr_hcl-h2so4-nelson	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_hcl-h2so4-nelson	Method of Nelson (dilute HCl/H2SO4). Particularly used for available P.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Extr_nh4ch3ch-oh-cooh-leuven	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_nh4ch3ch-oh-cooh-leuven	NH4-lactate extraction method (KU-Leuven). Particularly used for available P.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Extr_cacl2	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_cacl2	CaCl2. Particularly used for soluble P.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Extr_c6h8o7-reeuwijk	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_c6h8o7-reeuwijk	Complexation with citric acid (van Reeuwijk). Particularly used for available P.	https://www.isric.org/documents/document-type/technical-paper-09-procedures-soil-analysis-6th-edition	\N
Extr_hno3	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_hno3	Nitric acid (HNO3) method	https://www.iso.org/standard/60060.html	ISO. ISO/DIS 17586 Soil Quality - Extraction of Trace Elements Using Dilute Nitric Acid, 2016; p 14
Extr_m2	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_m2	Mehlich2 method	https://doi.org/10.1080/00103627609366673	\N
Extr_m3-spec	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_m3-spec	Spectrally measured and converted to Mehlich3 method (extractant 0.2 N CH3COOH + 0.25 N NH4NO3 + 0.015 N NH4F + 0.013 N HNO3 + 0.001 M EDTA)	https://doi.org/10.1080/00103628409367568	\N
Extr_naoac-morgan	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_naoac-morgan	Method of Morgan (Na-acetate/acetic acid). Particularly used for available P.	https://portal.ct.gov/-/media/CAES/DOCUMENTS/Publications/Bulletins/B450pdf.pdf?la=en	\N
Extr_h2so4-truog	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_h2so4-truog	Method of Truog (dilute H2SO4). Particularly used for available P.	https://doi.org/10.2134/agronj1930.00021962002200100008x	\N
Extr_nh4-co3-2-ambic1	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_nh4-co3-2-ambic1	Ambic1 method (ammonium bicarbonate) (South Africa). Particularly used for available P.	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
Extr_ap14	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_ap14	Method of Saunders and Metelerkamp (anion-exch. resin). Particularly used for available P.	\N	Saunders and Metelerkamp
Extr_hcl-nh4f-bray2	\N	http://w3id.org/glosis/model/procedure/extractableElementsProcedure-Extr_hcl-nh4f-bray2	Method of Bray II (dilute HCl/NH4F). Particularly used for available P.	https://doi.org/10.1097/00010694-194501000-00006	\N
TotC_dc-mt	\N	http://w3id.org/glosis/model/procedure/carbonTotalProcedure-TotC_dc-mt	Unacidified dry combustion at medium temperature (550-950 C).	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
TotC_dc-ht-analyser	\N	http://w3id.org/glosis/model/procedure/carbonTotalProcedure-TotC_dc-ht-analyser	Unacidified dry combustion at high temperature (950-1400 C). Total Carbon (USDA-NRCS method 6A), LECO analyzer at 1140 C	https://www.nrcs.usda.gov/Internet/FSE_DOCUMENTS/stelprdb1253872.pdf	\N
TotC_dc-ht-spec	\N	http://w3id.org/glosis/model/procedure/carbonTotalProcedure-TotC_dc-ht-spec	Spectrally measured and converted to Unacidified dry combustion at high temperature (950-1400 C).	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
TotC_calcul-ic-oc	\N	http://w3id.org/glosis/model/procedure/carbonTotalProcedure-TotC_calcul-ic-oc	Calculated as sum of inorganic carbon and organic carbon	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
TotC_dc-ht	\N	http://w3id.org/glosis/model/procedure/carbonTotalProcedure-TotC_dc-ht	Unacidified dry combustion at high temperature (950-1400 C). Total Carbon	https://www.isric.org/sites/default/files/isric_report_2014_01.pdf	Leenaars J.G.B., A.J.M. van Oostrum and M. Ruiperez Gonzalez, 2014. Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01. Africa Soil Information Service (AfSIS) project and ISRIC - World Soil Information, Wageningen, the Netherlands. See Annex 4.
\.




--
-- TOC entry 5010 (class 0 OID 54924209)
-- Dependencies: 273
-- Data for Name: property_desc; Type: TABLE DATA; Schema: core; Owner: glosis
--
mappin2
COPY core.property_desc (property_desc_id, property_pretty_name, uri) FROM stdin;
MineralConcentrationsNature	Mineral Concentrations Nature	http://w3id.org/glosis/model/layerhorizon/mineralConcNatureProperty
Landuse	Landuse	http://w3id.org/glosis/model/siteplot/landUseClassProperty
poresAbundanceProperty	poresAbundanceProperty	http://w3id.org/glosis/model/layerhorizon/poresAbundanceProperty
CarbonateForms	Carbonate Forms	http://w3id.org/glosis/model/layerhorizon/carbonatesFormsProperty
soilDepthRootableClassProperty	soilDepthRootableClassProperty	http://w3id.org/glosis/model/common/soilDepthRootableClassProperty
Stickiness	Stickiness	http://w3id.org/glosis/model/layerhorizon/stickinessProperty
poresSizeProperty	poresSizeProperty	http://w3id.org/glosis/model/layerhorizon/poresSizeProperty
RockOutcropsCover	Rock Outcrops Cover	http://w3id.org/glosis/model/siteplot/rockOutcropsCoverProperty
CoatingsAbundance	Coatings Abundance	http://w3id.org/glosis/model/layerhorizon/coatingAbundanceProperty
KoeppenClass	Koeppen Class	http://w3id.org/glosis/model/siteplot/koeppenClassProperty
MineralConcentrationsHardness	Mineral Concentrations Hardness	http://w3id.org/glosis/model/layerhorizon/mineralConcHardnessProperty
MottlesBoundary	Mottles Boundary	http://w3id.org/glosis/model/layerhorizon/mottlesBoundaryClassificationProperty
DrainageClass	Drainage Class	\N
GypsumForms	Gypsum Forms	http://w3id.org/glosis/model/layerhorizon/gypsumFormsProperty
Cementation/compactionNature	Cementation/compaction Nature	http://w3id.org/glosis/model/layerhorizon/cementationNatureProperty
CoatingsNature	Coatings Nature	http://w3id.org/glosis/model/layerhorizon/coatingNatureProperty
FloodFrequency	Flood Frequency	http://w3id.org/glosis/model/siteplot/floodFrequencyProperty
parentTextureUnconsolidatedProperty	parentTextureUnconsolidatedProperty	http://w3id.org/glosis/model/siteplot/parentTextureUnconsolidatedProperty
mottlesPresenceProperty	mottlesPresenceProperty	http://w3id.org/glosis/model/layerhorizon/mottlesPresenceProperty
ArtefactKind	Artefact Kind	\N
ArtefactHardness	Artefact Hardness	http://w3id.org/glosis/model/layerhorizon/MineralConcHardness
HumanInfluence	Human Influence	http://w3id.org/glosis/model/siteplot/humanInfluenceClassProperty
RockShape	Rock Shape	http://w3id.org/glosis/model/common/rockShapeProperty
mineralContentProperty	mineralContentProperty	http://w3id.org/glosis/model/layerhorizon/mineralContentProperty
soilSuborderUSDA	USDA Suborder	http://w3id.org/glosis/model/profile/SoilClassificationUSDA
cationExchangeCapacityEffectiveProperty	cationExchangeCapacityEffectiveProperty	http://w3id.org/glosis/model/layerhorizon/cationExchangeCapacityEffectiveProperty
Lithology	Lithology	http://w3id.org/glosis/model/siteplot/geologyProperty
PeaDescomposition	Pea Descomposition	http://w3id.org/glosis/model/layerhorizon/peatDecompostionProperty
CoatingsForm	Coatings Form	http://w3id.org/glosis/model/layerhorizon/coatingFormProperty
RockNature	Rock Nature	http://w3id.org/glosis/model/siteplot/lithologyProperty
MottlesContrast	Mottles Contrast	http://w3id.org/glosis/model/layerhorizon/mottlesContrastProperty
PeatVolume	Peat Volume	http://w3id.org/glosis/model/layerhorizon/peatVolumeProperty
BiologicalAbundance	Biological Abundance	http://w3id.org/glosis/model/layerhorizon/biologicalAbundanceProperty
SurfaceAge	Surface Age	http://w3id.org/glosis/model/siteplot/surfaceAgeProperty
SoilOdour	Soil Odour	\N
PoreAbundance	Pore Abundance	http://w3id.org/glosis/model/layerhorizon/PoresAbundance
saltProperty	saltProperty	http://w3id.org/glosis/model/layerhorizon/saltProperty
RedoxPotential	Redox Potential	\N
SupplementaryQualifierWRB	WRB Supplementary Qualifier	http://w3id.org/glosis/model/profile/SoilClassificationWRB
OrganicMatter	Organic Matter Content	http://w3id.org/glosis/model/layerhorizon/OrganicMatterValue
ForestAbundance	Forest Abundance	http://w3id.org/glosis/model/siteplot/ForestAbundanceProperty
PeatDrainage	Peat Drainage	http://w3id.org/glosis/model/layerhorizon/peatDrainageProperty
GrassAbundance	Grass Abundance	http://w3id.org/glosis/model/siteplot/GrassAbundanceProperty
StructureSize	Structure Size	http://w3id.org/glosis/model/layerhorizon/structureSizeProperty
SaltContent	Salt Content	http://w3id.org/glosis/model/layerhorizon/saltContentProperty
ExternalDrainageClass	External Drainage Class	\N
textureLabClassProperty	textureLabClassProperty	http://w3id.org/glosis/model/layerhorizon/textureLabClassProperty
MottlesColour	Mottles Colour	http://w3id.org/glosis/model/layerhorizon/mottlesColourProperty
SoilTexture	Soil Texture	http://w3id.org/glosis/model/common/textureProperty
soilDepthSampledProperty	soilDepthSampledProperty	http://w3id.org/glosis/model/common/soilDepthSampledProperty
Cementation/compactionStructure	Cementation/compaction Structure	http://w3id.org/glosis/model/layerhorizon/cementationFabricProperty
MineralConcentrationsColour	Mineral Concentrations Colour	http://w3id.org/glosis/model/layerhorizon/mineralConcColourProperty
RockPrimary	Rock Primary	http://w3id.org/glosis/model/layerhorizon/mineralFragmentsProperty
BulkDensity	Bulk Density	http://w3id.org/glosis/model/layerhorizon/bulkDensityMineralProperty
solubleCationsTotalProperty	solubleCationsTotalProperty	http://w3id.org/glosis/model/layerhorizon/solubleCationsTotalProperty
gypsumWeightProperty	gypsumWeightProperty	http://w3id.org/glosis/model/layerhorizon/gypsumWeightProperty
SlopeOrientation	Slope Orientation	http://w3id.org/glosis/model/siteplot/slopeOrientationClassProperty
organicMatterClassProperty	organicMatterClassProperty	http://w3id.org/glosis/model/common/organicMatterClassProperty
BiologicalKind	Biological Kind	http://w3id.org/glosis/model/layerhorizon/biologicalFeaturesProperty
ComplexLandform	Complex Landform	http://w3id.org/glosis/model/siteplot/landformComplexProperty
Cementation/compactionDegree	Cementation/compaction Degree	http://w3id.org/glosis/model/layerhorizon/cementationDegreeProperty
infiltrationRateClassProperty	infiltrationRateClassProperty	http://w3id.org/glosis/model/common/infiltrationRateClassProperty
soilDepthBedrockProperty	soilDepthBedrockProperty	http://w3id.org/glosis/model/common/soilDepthBedrockProperty
PeatBulkDensity	Peat Bulk Density	http://w3id.org/glosis/model/layerhorizon/bulkDensityPeatProperty
SandfractionTexture	Sand fraction Texture	http://w3id.org/glosis/model/layerhorizon/sandyTextureProperty
SlopePathway	Slope Pathway	http://w3id.org/glosis/model/siteplot/slopePathwaysProperty
ConsistenceDry	Consistence Dry	http://w3id.org/glosis/model/layerhorizon/consistenceDryProperty
MineralConcentrationsShape	Mineral Concentrations Shape	http://w3id.org/glosis/model/layerhorizon/mineralConcShapeProperty
slopeGradientClassProperty	slopeGradientClassProperty	http://w3id.org/glosis/model/siteplot/slopeGradientClassProperty
EffectiveSoilDepth	Effective soil depth	http://w3id.org/glosis/model/common/SoilDepthRootableClass
MoistureRegime	Moisture Regime	\N
ErosionDegree	Erosion Degree	http://w3id.org/glosis/model/siteplot/erosionDegreeProperty
FloodDuration	Flood Duration	http://w3id.org/glosis/model/siteplot/floodDurationProperty
soilClassificationUSDAProperty	soilClassificationUSDAProperty	http://w3id.org/glosis/model/profile/soilClassificationUSDAProperty
PavedAbundance	Paved Abundance	http://w3id.org/glosis/model/siteplot/PavedAbundanceProperty
SlopeGradient	Slope Gradient	http://w3id.org/glosis/model/siteplot/slopeGradientProperty
formativeElementUSDA	USDA Formative Element	http://w3id.org/glosis/model/profile/SoilClassificationUSDA
soilClassificationWRB	WRB Soil Name	http://w3id.org/glosis/model/profile/SoilClassificationWRB
soilClassificationWRBProperty	soilClassificationWRBProperty	http://w3id.org/glosis/model/profile/soilClassificationWRBProperty
ErosionAreaAffected	Erosion Area Affected	http://w3id.org/glosis/model/siteplot/erosionAreaAffectedProperty
Cementation/compactionContinuity	Cementation/compaction Continuity	http://w3id.org/glosis/model/layerhorizon/cementationContinuityProperty
ColourDry	Colour Dry	http://w3id.org/glosis/model/common/colourDryProperty
GypsumContent	Gypsum Content	http://w3id.org/glosis/model/layerhorizon/gypsumContentProperty
TemperatureRegime	Temperature Regime	\N
Rocksize	Rock size	http://w3id.org/glosis/model/common/rockSizeProperty
MineralConcentrationsKind	Mineral Concentrations Kind	http://w3id.org/glosis/model/layerhorizon/mineralConcKindProperty
VoidsClassificationProperty	VoidsClassificationProperty	http://w3id.org/glosis/model/layerhorizon/voidsClassificationProperty
ArtefactWeathering	Artefact Weathering	http://w3id.org/glosis/model/common/weatheringFragmentsProperty
ErosionClass	Erosion Class	http://w3id.org/glosis/model/siteplot/erosionCategoryProperty
BoundaryTopography	Boundary Topography	http://w3id.org/glosis/model/layerhorizon/boundaryTopographyProperty
soilClassificationFAOProperty	soilClassificationFAOProperty	http://w3id.org/glosis/model/profile/soilClassificationFAOProperty
PastWeatherConditions	Past Weather Conditions	http://w3id.org/glosis/model/siteplot/weatherConditionsPastProperty
PorosityType	Porosity Type	http://w3id.org/glosis/model/layerhorizon/VoidsClassification
SoilSpecifierWRB	WRB Specifier	http://w3id.org/glosis/model/profile/SoilClassificationWRB
GroundwaterDepth	Groundwater Depth	http://w3id.org/glosis/model/siteplot/groundwaterDepthProperty
CracksDistance	Cracks Distance	http://w3id.org/glosis/model/common/cracksDistanceProperty
cationsSumProperty	cationsSumProperty	http://w3id.org/glosis/model/layerhorizon/cationsSumProperty
ArtefactAbundance	Artefact Abundance	http://w3id.org/glosis/model/common/rockAbundanceProperty
ReducingConditions	Reducing Conditions	\N
FragmentsCover	Fragments Cover	http://w3id.org/glosis/model/common/fragmentCoverProperty
dryConsistencyProperty	dryConsistencyProperty	http://w3id.org/glosis/model/layerhorizon/dryConsistencyProperty
wetPlasticityProperty	wetPlasticityProperty	http://w3id.org/glosis/model/layerhorizon/wetPlasticityProperty
CurrentWeatherConditions	Current Weather Conditions	http://w3id.org/glosis/model/siteplot/weatherConditionsCurrentProperty
RockOutcropsDistance	Rock Outcrops Distance	http://w3id.org/glosis/model/siteplot/rockOutcropsDistanceProperty
moistConsistencyProperty	moistConsistencyProperty	http://w3id.org/glosis/model/layerhorizon/moistConsistencyProperty
Croptype	Crop type	http://w3id.org/glosis/model/siteplot/cropClassProperty
ArtefactColour	Artefact Colour	http://w3id.org/glosis/model/layerhorizon/mineralConcColourProperty
AeromorphicForest	Aeromorphic Forest	\N
slopeOrientationProperty	slopeOrientationProperty	http://w3id.org/glosis/model/siteplot/slopeOrientationProperty
StructureType	Structure Type	\N
MoistureConditions	Moisture Conditions	\N
SaltThickness	Salt Thickness	http://w3id.org/glosis/model/surface/saltThicknessProperty
RootsAbundance	Roots Abundance	http://w3id.org/glosis/model/layerhorizon/rootsAbundanceProperty
FieldPH	Field pH	\N
saltPresenceProperty	saltPresenceProperty	http://w3id.org/glosis/model/surface/saltPresenceProperty
FieldTexture	Field Texture	http://w3id.org/glosis/model/layerhorizon/textureFieldClassProperty
soilDepthRootableProperty	soilDepthRootableProperty	http://w3id.org/glosis/model/common/soilDepthRootableProperty
MottlesSize	Mottles Size	http://w3id.org/glosis/model/layerhorizon/mottlesSizeProperty
AndicCharacteristics	Andic Characteristics	\N
soilGroupWRB	WRB Soil Group	http://w3id.org/glosis/model/profile/SoilClassificationWRB
oxalateExtractableOpticalDensityProperty	oxalateExtractableOpticalDensityProperty	http://w3id.org/glosis/model/layerhorizon/oxalateExtractableOpticalDensityProperty
ConsistenceMoist	Consistence Moist	http://w3id.org/glosis/model/layerhorizon/consistenceMoistProperty
soilOrderUSDA	USDA order	http://w3id.org/glosis/model/profile/SoilClassificationUSDA
BleachedSandCover	Bleached Sand Cover	http://w3id.org/glosis/model/common/bleachedSandProperty
SealingConsistence	Sealing Consistence	http://w3id.org/glosis/model/surface/sealingConsistenceProperty
Position	Position	http://w3id.org/glosis/model/siteplot/physiographyProperty
RootsSize	Roots Size	http://w3id.org/glosis/model/layerhorizon/rootsPresenceProperty
MajorLandForm	Major LandForm	http://w3id.org/glosis/model/siteplot/majorLandFormProperty
solubleAnionsTotalProperty	solubleAnionsTotalProperty	http://w3id.org/glosis/model/layerhorizon/solubleAnionsTotalProperty
SlopeForm	Slope Form	http://w3id.org/glosis/model/siteplot/slopeFormProperty
BoundaryDistinctness	Boundary Distinctness	http://w3id.org/glosis/model/layerhorizon/boundaryDistinctnessProperty
soilDepthProperty	soilDepthProperty	http://w3id.org/glosis/model/common/soilDepthProperty
ColourMoist	Colour Moist	http://w3id.org/glosis/model/common/colourWetProperty
BareSoilAbundance	Bare Soil Abundance	http://w3id.org/glosis/model/siteplot/bareCoverAbundanceProperty
infiltrationRateNumericProperty	infiltrationRateNumericProperty	http://w3id.org/glosis/model/common/infiltrationRateNumericProperty
Vegetation	Vegetation	http://w3id.org/glosis/model/siteplot/vegetationClassProperty
StructureGrade	Structure Grade	http://w3id.org/glosis/model/layerhorizon/structureGradeProperty
MineralConcentrationsAbundance	Mineral Concentrations Abundance	http://w3id.org/glosis/model/layerhorizon/mineralConcAbundanceProperty
mineralConcVolumeProperty	mineralConcVolumeProperty	http://w3id.org/glosis/model/layerhorizon/mineralConcVolumeProperty
CoatingsContrast	Coatings Contrast	http://w3id.org/glosis/model/layerhorizon/coatingContrastProperty
ArtefactSize	Artefact Size	http://w3id.org/glosis/model/common/rockSizeProperty
ParentMaterialClass	Parent Material Class	http://w3id.org/glosis/model/siteplot/lithologyProperty
SaltCover	Salt Cover	http://w3id.org/glosis/model/surface/saltCoverProperty
MineralConcentrationsSize	Mineral Concentrations Size	http://w3id.org/glosis/model/layerhorizon/mineralConcSizeProperty
descriptionStatus	Description Status	http://w3id.org/glosis/model/profile/profileDescriptionStatusProperty
PresenceOfWater	Presence Of Water	\N
cationExchangeCapacityProperty	cationExchangeCapacityProperty	http://w3id.org/glosis/model/layerhorizon/cationExchangeCapacityProperty
Plasticity	Plasticity	http://w3id.org/glosis/model/layerhorizon/plasticityProperty
PorositySize	Porosity Size	http://w3id.org/glosis/model/layerhorizon/PoresSize
Moisture	Moisture	http://w3id.org/glosis/model/layerhorizon/moistureContentProperty
SealingThickness	Sealing Thickness	http://w3id.org/glosis/model/surface/sealingThicknessProperty
TreeDensity	Tree Density	http://w3id.org/glosis/model/siteplot/treeDensityProperty
MottlesAbundance	Mottles Abundance	http://w3id.org/glosis/model/layerhorizon/mottlesAbundanceProperty
ParticleSizeFractionsSumProperty	ParticleSizeFractionsSumProperty	http://w3id.org/glosis/model/layerhorizon/particleSizeFractionsSumProperty
voidsDiameterProperty	voidsDiameterProperty	http://w3id.org/glosis/model/layerhorizon/voidsDiameterProperty
Rockweathering	Rock weathering	http://w3id.org/glosis/model/siteplot/weatheringRockProperty
CarbonateContent	Carbonate Content	http://w3id.org/glosis/model/layerhorizon/carbonatesContentProperty
erosionTotalAreaAffectedProperty	erosionTotalAreaAffectedProperty	http://w3id.org/glosis/model/siteplot/erosionTotalAreaAffectedProperty
SoilDepthtoBedrock	Soil Depth to Bedrock	http://w3id.org/glosis/model/common/SoilDepthBedrock
PorosityAbundance	Porosity Abundance	http://w3id.org/glosis/model/layerhorizon/porosityClassProperty
FragmentsSize	Fragments Size	http://w3id.org/glosis/model/common/fragmentSizeProperty
ShrubAbundace	Shrub Abundace	http://w3id.org/glosis/model/siteplot/ShrubsAbundanceProperty
GroundwaterQuality	Groundwater Quality	\N
soilPhase	Soil Phase	\N
CracksDepth	Cracks Depth	http://w3id.org/glosis/model/common/cracksDepthProperty
parentLithologyProperty	parentLithologyProperty	http://w3id.org/glosis/model/siteplot/parentLithologyProperty
CracksWidth	Cracks Width	http://w3id.org/glosis/model/common/cracksWidthProperty
Rockabundance	Rock abundance	http://w3id.org/glosis/model/common/rockAbundanceProperty
CoatingsLocation	Coatings Location	http://w3id.org/glosis/model/layerhorizon/coatingLocationProperty
ErosionActivityPeriod	Erosion Activity Period	http://w3id.org/glosis/model/siteplot/erosionActivityPeriodProperty
ParentDepositionProperty	ParentDepositionProperty	http://w3id.org/glosis/model/siteplot/parentDepositionProperty
ConsistenceWet	Consistence Wet	http://w3id.org/glosis/model/layerhorizon/consistenceMoistProperty
\.


--
-- TOC entry 4976 (class 0 OID 54922924)
-- Dependencies: 239
-- Data for Name: property_phys_chem; Type: TABLE DATA; Schema: core; Owner: glosis
--
mapping labdata
COPY core.property_phys_chem (property_phys_chem_id, uri) FROM stdin;
aluminiumProperty	http://w3id.org/glosis/model/layerhorizon/aluminiumProperty
Calcium (Ca++) - total	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Caltot
Carbon (C) - organic	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Carorg
Carbon (C) - total	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Cartot
Copper (Cu) - extractable	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Copext
Copper (Cu) - total	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Coptot
Hydrogen (H+) - exchangeable	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Hydexc
Iron (Fe) - extractable	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Iroext
Iron (Fe) - total	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Irotot
Magnesium (Mg++) - exchangeable	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Magexc
Magnesium (Mg) - extractable	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Magext
Magnesium (Mg) - total	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Magtot
Manganese (Mn) - extractable	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Manext
Manganese (Mn) - total	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Mantot
Nitrogen (N) - total	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Nittot
Phosphorus (P) - extractable	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Phoext
Phosphorus (P) - retention	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Phoret
Phosphorus (P) - total	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Photot
Potassium (K+) - exchangeable	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Potexc
Potassium (K) - extractable	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Potext
Potassium (K) - total	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Pottot
Sodium (Na) - extractable	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Sodext
Sodium (Na) - total	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Sodtot
Sulfur (S) - extractable	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Sulext
Sulfur (S) - total	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Sultot
Clay texture fraction	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Textclay
Sand texture fraction	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Textsand
Silt texture fraction	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Textsilt
Zinc (Zn) - extractable	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Zinext
pH - Hydrogen potential	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-pH
bulkDensityFineEarthProperty	http://w3id.org/glosis/model/layerhorizon/bulkDensityFineEarthProperty
bulkDensityWholeSoilProperty	http://w3id.org/glosis/model/layerhorizon/bulkDensityWholeSoilProperty
cadmiumProperty	http://w3id.org/glosis/model/layerhorizon/cadmiumProperty
carbonInorganicProperty	http://w3id.org/glosis/model/layerhorizon/carbonInorganicProperty
cationExchangeCapacitycSoilProperty	http://w3id.org/glosis/model/layerhorizon/cationExchangeCapacitycSoilProperty
coarseFragmentsProperty	http://w3id.org/glosis/model/layerhorizon/coarseFragmentsProperty
effectiveCecProperty	http://w3id.org/glosis/model/layerhorizon/effectiveCecProperty
electricalConductivityProperty	http://w3id.org/glosis/model/layerhorizon/electricalConductivityProperty
gypsumProperty	http://w3id.org/glosis/model/layerhorizon/gypsumProperty
hydraulicConductivityProperty	http://w3id.org/glosis/model/layerhorizon/hydraulicConductivityProperty
manganeseProperty	http://w3id.org/glosis/model/layerhorizon/manganeseProperty
molybdenumProperty	http://w3id.org/glosis/model/layerhorizon/molybdenumProperty
organicMatterProperty	http://w3id.org/glosis/model/layerhorizon/organicMatterProperty
pHProperty	http://w3id.org/glosis/model/layerhorizon/pHProperty
porosityProperty	http://w3id.org/glosis/model/layerhorizon/porosityProperty
solubleSaltsProperty	http://w3id.org/glosis/model/layerhorizon/solubleSaltsProperty
totalCarbonateEquivalentProperty	http://w3id.org/glosis/model/layerhorizon/totalCarbonateEquivalentProperty
zincProperty	http://w3id.org/glosis/model/layerhorizon/zincProperty
Acidity - exchangeable	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Aciexc
Boron (B) - total	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Bortot
Aluminium (Al+++) - exchangeable	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Aluexc
Available water capacity - volumetric (FC to WP)	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Avavol
Base saturation - calculated	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Bascal
Boron (B) - extractable	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Borext
Calcium (Ca++) - exchangeable	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Calexc
Calcium (Ca++) - extractable	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Calext
Sodium (Na+) - exchangeable	http://w3id.org/glosis/model/codelists/physioChemicalPropertyCode-Sodexp
\.

"""
SQL_DROP = f""" 
DROP VIEW IF EXISTS active_calcium_carbonate CASCADE;
DROP VIEW IF EXISTS antimony CASCADE;
DROP VIEW IF EXISTS arsenic CASCADE;
DROP VIEW IF EXISTS available_p_content CASCADE;
DROP VIEW IF EXISTS base_saturation_exchangeable_activity CASCADE;
DROP VIEW IF EXISTS base_saturation_soil_structure CASCADE;
DROP VIEW IF EXISTS bulk_density CASCADE;
DROP VIEW IF EXISTS cadmium CASCADE; 
DROP VIEW IF EXISTS calcium_carbonate CASCADE; 
DROP VIEW IF EXISTS cation_exchange_capacity CASCADE;
DROP VIEW IF EXISTS cec_clay_ratio CASCADE;
DROP VIEW IF EXISTS chromium CASCADE;
DROP VIEW IF EXISTS cobalt CASCADE;
DROP VIEW IF EXISTS copper CASCADE;
DROP VIEW IF EXISTS copper_relative_content CASCADE;
DROP VIEW IF EXISTS crust_cover CASCADE;
DROP VIEW IF EXISTS cryptogram_cover CASCADE;
DROP VIEW IF EXISTS c_n_ratio CASCADE;
DROP VIEW IF EXISTS effective_cation_exchange_capacity CASCADE;
DROP VIEW IF EXISTS electric_conductivity CASCADE;
DROP VIEW IF EXISTS exchangeable_calcium CASCADE;
DROP VIEW IF EXISTS exchangeable_magnesium CASCADE;
DROP VIEW IF EXISTS exchangeable_potassium CASCADE;
DROP VIEW IF EXISTS exchangeable_potassium_potential_impact CASCADE;
DROP VIEW IF EXISTS exchangeable_sodium CASCADE;
DROP VIEW IF EXISTS field_capacity CASCADE;
DROP VIEW IF EXISTS gravel CASCADE;
DROP VIEW IF EXISTS gypsum CASCADE;
DROP VIEW IF EXISTS hydraulic_conductivity_at_saturation CASCADE;
DROP VIEW IF EXISTS lead CASCADE;
DROP VIEW IF EXISTS lead_relative_content CASCADE;
DROP VIEW IF EXISTS litter_layer_cover CASCADE;
DROP VIEW IF EXISTS manganese CASCADE;
DROP VIEW IF EXISTS mercury CASCADE;
DROP VIEW IF EXISTS n_total CASCADE;
DROP VIEW IF EXISTS nh4 CASCADE;
DROP VIEW IF EXISTS nichel CASCADE;
DROP VIEW IF EXISTS no3 CASCADE;
DROP VIEW IF EXISTS organic_carbon CASCADE;
DROP VIEW IF EXISTS organic_matter CASCADE;
DROP VIEW IF EXISTS oxygen_availability_for_roots CASCADE;
DROP VIEW IF EXISTS p_p_threshold CASCADE;
DROP VIEW IF EXISTS packing_density CASCADE;
DROP VIEW IF EXISTS perennial_vegetation_cover CASCADE;
DROP VIEW IF EXISTS ph_h2o_bacterial_diversity CASCADE;
DROP VIEW IF EXISTS ph_h2o_fungal CASCADE;
DROP VIEW IF EXISTS ph_h2o_metal_toxicity CASCADE;
DROP VIEW IF EXISTS ph_h2o_microbial_carbon CASCADE;
DROP VIEW IF EXISTS ph_h2o_microbial_diversity CASCADE;
DROP VIEW IF EXISTS ph_h2o_organic_decomposition CASCADE;
DROP VIEW IF EXISTS ph_h2o_phosphorus CASCADE;
DROP VIEW IF EXISTS ph_h2o_plant_growth CASCADE;
DROP VIEW IF EXISTS ph_h2o_soil_salinity CASCADE;
DROP VIEW IF EXISTS ph_h2o_som_for_grassland CASCADE;
DROP VIEW IF EXISTS plant_available_water_capacity CASCADE;
DROP VIEW IF EXISTS relative_field_capacity CASCADE; 
DROP VIEW IF EXISTS slake_test CASCADE;
DROP VIEW IF EXISTS soc_stock CASCADE;
DROP VIEW IF EXISTS sodicity_salinity_ratio CASCADE;
DROP VIEW IF EXISTS sodium_adsorption_ratio_sodicity CASCADE;
DROP VIEW IF EXISTS sodium_adsorption_ratio_toxicity CASCADE;
DROP VIEW IF EXISTS sodium_exchangeable_percentage_sodicity CASCADE;
DROP VIEW IF EXISTS sodium_exchangeable_percentage_waterlogging CASCADE;                                                                   ;
DROP VIEW IF EXISTS soil_erodibility_by_water CASCADE;
DROP VIEW IF EXISTS soil_erodibility_by_wind CASCADE;
DROP VIEW IF EXISTS surface_compaction_risk CASCADE;
DROP VIEW IF EXISTS texture CASCADE;
DROP VIEW IF EXISTS total_iron CASCADE;
DROP VIEW IF EXISTS vanadium CASCADE;
DROP VIEW IF EXISTS wilting_point CASCADE;
DROP VIEW IF EXISTS zinc CASCADE;
DROP VIEW IF EXISTS zinc_relative_content CASCADE;                                                                                         

"""

### WARNING: Changes to tables will not be applied if they affect fields used in SQL views.
### It is recommended to verify the results of any new migrations generated with `makemigrations`.

class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0003_sqlview_sections'),
    ]

    operations = [
        migrations.RunSQL(
            sql=SQL_CREATE,
            reverse_sql=SQL_DROP,
        ),
    ]
    
