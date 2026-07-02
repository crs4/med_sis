<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>Rupture resistance cemented soil</Name>
    <UserStyle>
      <Name>Rupture resistance cemented soil</Name>
      <Title>Rupture resistance cemented soil</Title>
      <FeatureTypeStyle>
	  <Rule>
          <Name>Not cemented (NOC) - Potentially sensitive to wind erosion</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            
              <PropertyIsEqualTo>
                <PropertyName>cement_cls_id</PropertyName>
                <Literal>CEMENTATION_CLASSES:NOC</Literal>
              </PropertyIsEqualTo>
	      
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
        <Name>Extremely weakly, very weakly and weakly cemented (EWC, VWC and WEC) - Moderate potential for wind erosion</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <Or>
              <PropertyIsEqualTo>
                <PropertyName>cement_cls_id</PropertyName>
                <Literal>CEMENTATION_CLASSES:EWC</Literal>
              </PropertyIsEqualTo>
	      <PropertyIsEqualTo>
                <PropertyName>cement_cls_id</PropertyName>
                <Literal>CEMENTATION_CLASSES:VWC</Literal>
              </PropertyIsEqualTo>
              <PropertyIsEqualTo>
                <PropertyName>cement_cls</PropertyName>
                <Literal>CEMENTATION_CLASSES:WEC</Literal>
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
        <Name>Moderately cemented and Strongly cemented (MOC and STC) - Low potential for wind erosion</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <Or>
              <PropertyIsEqualTo>
                <PropertyName>cement_cls_id</PropertyName>
                <Literal>CEMENTATION_CLASSES:MOC</Literal>
              </PropertyIsEqualTo>
	      <PropertyIsEqualTo>
                <PropertyName>cement_cls_id</PropertyName>
                <Literal>CEMENTATION_CLASSES:STC</Literal>
              </PropertyIsEqualTo>
	                    
            </Or>
          </Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>circle</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#2649F7</CssParameter>
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
        <Name>Very strongly cemented (VSC) and Extremely strongly cemented (EXC) - Very low potential for wind erosion</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <Or>
              <PropertyIsEqualTo>
                <PropertyName>cement_cls_id</PropertyName>
                <Literal>CEMENTATION_CLASSES:VSC</Literal>
              </PropertyIsEqualTo>
	      <PropertyIsEqualTo>
                <PropertyName>cement_cls_id</PropertyName>
                <Literal>CEMENTATION_CLASSES:EXC</Literal>
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