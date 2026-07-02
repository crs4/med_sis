<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>soc_stock</Name>
    <UserStyle>
      <Title>SOC stock ('mg.ha^-1')</Title>
      <FeatureTypeStyle>    
		<Rule>
          <Name>Degraded equivalence (for grassland and cropland)</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	      <Or>
	        <ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <Literal>C</Literal>
                </ogc:PropertyIsEqualTo>
	        <ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <Literal>G</Literal>
                </ogc:PropertyIsEqualTo>
              </Or>

              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>15</Literal>
              </PropertyIsLessThan>
            </And>
          </Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>circle</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#F72626</CssParameter>
                  <CssParameter name="fill-opacity">1</CssParameter>
                </Fill>
                <Stroke>
                  <CssParameter name="stroke">#777777</CssParameter>
                  <CssParameter name="stroke-width">2</CssParameter>
                  <CssParameter name="stroke-opacity">1</CssParameter>
                </Stroke>
              </Mark>
              <Size>14</Size>
            </Graphic>
          </PointSymbolizer>
        </Rule>
		<Rule>
          <Name>Strong pressure equivalence (for grassland and cropland)</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	      <Or>
	        <ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <Literal>C</Literal>
                </ogc:PropertyIsEqualTo>
	        <ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <Literal>G</Literal>
                </ogc:PropertyIsEqualTo>
              </Or>

              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>15</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>35</Literal>
              </PropertyIsLessThan>
            </And>
          </Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>circle</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#F37844</CssParameter>
                  <CssParameter name="fill-opacity">1</CssParameter>
                </Fill>
                <Stroke>
                  <CssParameter name="stroke">#777777</CssParameter>
                  <CssParameter name="stroke-width">2</CssParameter>
                  <CssParameter name="stroke-opacity">1</CssParameter>
                </Stroke>
              </Mark>
              <Size>14</Size>
            </Graphic>
          </PointSymbolizer>
        </Rule>
		<Rule>
          <Name>Weak to moderate pressure equivalence (for grassland and cropland)</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	      <Or>
	        <ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <Literal>C</Literal>
                </ogc:PropertyIsEqualTo>
	        <ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <Literal>G</Literal>
                </ogc:PropertyIsEqualTo>
              </Or>

              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>35</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>75</Literal>
              </PropertyIsLessThan>
            </And>
          </Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>circle</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#7551e0</CssParameter>
                  <CssParameter name="fill-opacity">1</CssParameter>
                </Fill>
                <Stroke>
                  <CssParameter name="stroke">#777777</CssParameter>
                  <CssParameter name="stroke-width">2</CssParameter>
                  <CssParameter name="stroke-opacity">1</CssParameter>
                </Stroke>
              </Mark>
              <Size>14</Size>
            </Graphic>
          </PointSymbolizer>
        </Rule>
		<Rule>
          <Name>Very weak to no pressure equivalence (for grassland and cropland)</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	      <Or>
	        <ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <Literal>C</Literal>
                </ogc:PropertyIsEqualTo>
	        <ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <Literal>G</Literal>
                </ogc:PropertyIsEqualTo>
              </Or>

              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>75</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              
            </And>
          </Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>circle</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#41ED31</CssParameter>
                  <CssParameter name="fill-opacity">1</CssParameter>
                </Fill>
                <Stroke>
                  <CssParameter name="stroke">#777777</CssParameter>
                  <CssParameter name="stroke-width">2</CssParameter>
                  <CssParameter name="stroke-opacity">1</CssParameter>
                </Stroke>
              </Mark>
              <Size>14</Size>
            </Graphic>
          </PointSymbolizer>
        </Rule>
		<Rule>
          <Name>Low dense forests stands (only for forest)</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	      
	        <ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <Literal>F</Literal>
                </ogc:PropertyIsEqualTo>
	       

              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>45</Literal>
              </PropertyIsLessThan>
            </And>
          </Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>square</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#F72626</CssParameter>
                  <CssParameter name="fill-opacity">1</CssParameter>
                </Fill>
                <Stroke>
                  <CssParameter name="stroke">#777777</CssParameter>
                  <CssParameter name="stroke-width">2</CssParameter>
                  <CssParameter name="stroke-opacity">1</CssParameter>
                </Stroke>
              </Mark>
              <Size>14</Size>
            </Graphic>
          </PointSymbolizer>
        </Rule>
		<Rule>
          <Name>Moderately dense to dense forests stands equivalent (Only for forest)</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>	      
	        	<ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <Literal>F</Literal>
                </ogc:PropertyIsEqualTo>
                <PropertyIsGreaterThanOrEqualTo>
                	<PropertyName>value</PropertyName>
                	<Literal>45</Literal>
              	</PropertyIsGreaterThanOrEqualTo>              
            </And>
          </Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>square</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#41ED31</CssParameter>
                  <CssParameter name="fill-opacity">1</CssParameter>
                </Fill>
                <Stroke>
                  <CssParameter name="stroke">#777777</CssParameter>
                  <CssParameter name="stroke-width">2</CssParameter>
                  <CssParameter name="stroke-opacity">1</CssParameter>
                </Stroke>
              </Mark>
              <Size>14</Size>
            </Graphic>
          </PointSymbolizer>
        </Rule>       
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>