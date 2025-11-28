<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0" 
    xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
    xmlns="http://www.opengis.net/sld" 
    xmlns:ogc="http://www.opengis.net/ogc" 
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>WRB - Reference Soil Groups (Dominant)</Name>
    <UserStyle>
      <Title>WRB - Reference Soil Groups (Dominant) </Title>
      <FeatureTypeStyle>
        <Rule>
            <Name>Acrisol (AC)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>AC</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#F79804</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Alisol (AL)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>AL</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#FFFFBE</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Andosol (AN)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>AN</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#FE0000</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Anthrosol (AT)
            </Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>AT</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#CF9804</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Arenosol (AR)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>AR</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#F5D4A1</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Calcisol (CL)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>CL</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#FEF400</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Cambisol (CM)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>CM</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#FEBE00</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Chernozem (CH)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>CH</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#914D35</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Cryosol (CR)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>CR</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#4B3DAC</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Durisol (DU)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>DU</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#EFE4BE</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Ferralsol (FR)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>FR</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#FF8721</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Fluvisol (FL)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>FL</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#00FEFD</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Gleysol (GL)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>GL</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#8083D9</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Gypsisol (GY)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>GY</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#FEF6A4</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Histosol (HS)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>HS</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#706B66</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Kastanozem (KS)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>KS</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#CA937F</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Leptosol (LP)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>LP</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#D1D1D1</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Lixisol (LX)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>LX</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#FFBEBE</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Luvisol (LV)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>LV</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#FA8484</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Nitisol (NT)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>NT</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#FFA77F</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Phaeozem (PH)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>PH</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#BD6446</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Planosol (PL)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>PL</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#F77D3A</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Plinthosol (PT)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>PT</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#730000</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Podzol (PZ)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>PZ</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#0CD900</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Regosol (RG)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>RG</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#FEE3A4</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Retisol (RT)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>RT</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#FEC2C2</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Solonchak (SC)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>SC</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#FE00FA</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Solonetz (SN)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>SN</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#F9C2FE</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Stagnosol (ST)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>ST</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#40C0E9</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Technosol (TC)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>TC</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#91009D</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Umbrisol (UM)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>UM</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#738E7F</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Name>Vertisol (VR)</Name>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>wrb</ogc:PropertyName>
                    <ogc:Literal>VR</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            <PolygonSymbolizer>
                <Fill>
                    <CssParameter name="fill">#C500FF</CssParameter>
                </Fill>
            </PolygonSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
