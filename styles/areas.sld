<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0" 
                       xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
                       xmlns="http://www.opengis.net/sld" 
                       xmlns:ogc="http://www.opengis.net/ogc" 
                       xmlns:xlink="http://www.w3.org/1999/xlink" 
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>areas</Name>
    <UserStyle>
      <Title>generic polygon style</Title>
      <FeatureTypeStyle>
        <Rule>
          <Name>Area</Name>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#fff955</CssParameter>
              <CssParameter name="fill-opacity">0.26</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#ffaa00</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
              <CssParameter name="stroke-linejoin">bevel</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>