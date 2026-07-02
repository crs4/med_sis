<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>texture</Name>
    <UserStyle>
      <Title>Texture (unitless)</Title>
      <FeatureTypeStyle>
   		<Rule>
          <Name>Clay and Silty clay - Very slow infiltration rate</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <Or>
              <PropertyIsEqualTo>
                <PropertyName>texture</PropertyName>
                <Literal>TEXTURE_CLASSES:C</Literal>
              </PropertyIsEqualTo>
	      	  <PropertyIsEqualTo>
                <PropertyName>texture</PropertyName>
                <Literal>TEXTURE_CLASSES:SiC</Literal>
              </PropertyIsEqualTo>              
            </Or>
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
        <Name>Sandy clay loam and sandy clay - Slow infiltration rate</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <Or>
              <PropertyIsEqualTo>
                <PropertyName>texture</PropertyName>
                <Literal>TEXTURE_CLASSES:SCL</Literal>
              </PropertyIsEqualTo>
	      <PropertyIsEqualTo>
                <PropertyName>texture</PropertyName>
                <Literal>TEXTURE_CLASSES:SC</Literal>
              </PropertyIsEqualTo>
              
            </Or>
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
        <Name>Sandy loam, loam, silt loam, clay loam, silty clay loam, silt - Moderate infiltration rate</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <Or>
              <PropertyIsEqualTo>
                <PropertyName>texture</PropertyName>
                <Literal>TEXTURE_CLASSES:SL</Literal>
              </PropertyIsEqualTo>
	      <PropertyIsEqualTo>
                <PropertyName>texture</PropertyName>
                <Literal>TEXTURE_CLASSES:L</Literal>
              </PropertyIsEqualTo>
	      <PropertyIsEqualTo>
                <PropertyName>texture</PropertyName>
                <Literal>TEXTURE_CLASSES:SiL</Literal>
              </PropertyIsEqualTo>
	      <PropertyIsEqualTo>
                <PropertyName>texture</PropertyName>
                <Literal>TEXTURE_CLASSES:CL</Literal>
              </PropertyIsEqualTo>
              <PropertyIsEqualTo>
                <PropertyName>texture</PropertyName>
                <Literal>TEXTURE_CLASSES:SiCL</Literal>
              </PropertyIsEqualTo>
	      <PropertyIsEqualTo>
                <PropertyName>texture</PropertyName>
                <Literal>TEXTURE_CLASSES:Si</Literal>
              </PropertyIsEqualTo>              
            </Or>
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
        <Name>Sand and loamy sand - High infiltration rate</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <Or>
              <PropertyIsEqualTo>
                <PropertyName>texture</PropertyName>
                <Literal>TEXTURE_CLASSES:S</Literal>
              </PropertyIsEqualTo>
	      <PropertyIsEqualTo>
                <PropertyName>texture</PropertyName>
                <Literal>TEXTURE_CLASSES:LS</Literal>
              </PropertyIsEqualTo>
	         
            </Or>
          </Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>circle</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#919399</CssParameter>
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