<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0" 
 xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
 xmlns="http://www.opengis.net/sld" 
 xmlns:ogc="http://www.opengis.net/ogc" 
 xmlns:xlink="http://www.w3.org/1999/xlink" 
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>point_soil_data</Name>
    <UserStyle>
      <Title>Point Soil Data</Title>
      <FeatureTypeStyle>
        <Rule>
          <Title>Point</Title>
            <PointSymbolizer>
              <Graphic>
               <Mark>
                <WellKnownName>circle</WellKnownName>
                 <Fill>
                  <CssParameter name="fill">#FFAA00</CssParameter>
                 </Fill>
                 <Stroke>
                  <CssParameter name="stroke">#990000</CssParameter>
                  <CssParameter name="stroke-width">2</CssParameter>
                 </Stroke>
              </Mark>
              <Size>8</Size>
            </Graphic>
          </PointSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>