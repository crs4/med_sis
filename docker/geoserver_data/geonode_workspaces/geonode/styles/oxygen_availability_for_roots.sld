<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>oxygen_availability_for_roots</Name>
    <UserStyle>
      <Title>Oxygen availability for roots (D/D0)</Title>
      <FeatureTypeStyle>   
	    <Rule>
          <Name>Low (soil easily aerated optimal for most of plant growth) - for cropland and grassland - only in topsoils</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
	       <And>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>0.005</Literal>
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
          <Name>Medium (potential beginning of O2 turnover depletion and nitrate reduction rate potentially increase facilitating potentially root growth) - for cropland and grassland - only in topsoils</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
	   <And>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0.005</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>0.02</Literal>
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
          <Name>Good (very low O2 turnover)  - for cropland and grassland - only in topsoils</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
	    <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0.02</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              
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
       
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>