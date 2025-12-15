<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
<<<<<<< HEAD
    <Name>Sodium Exchangeable Percentage - Sodicity</Name>
    <UserStyle>
      <Name>Sodium Exchangeable Percentage - Sodicity</Name>
      <Title>Sodium Exchangeable Percentage - Sodicity</Title>
=======
    <Name>sodium_exchangeable_percentage</Name>
    <UserStyle>
      <Name>circle_point</Name>
      <Title>Point Red Symbol Border</Title>
>>>>>>> 58dcde557d1da9070628851a32775b2507519611
      <FeatureTypeStyle>
        <Rule>
          <Name>Non sodic soil</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
              <PropertyIsGreaterThanOrEqualTo>
<<<<<<< HEAD
                <PropertyName>value</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
=======
                <PropertyName>esp</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>esp</PropertyName>
>>>>>>> 58dcde557d1da9070628851a32775b2507519611
                <Literal>0.15</Literal>
              </PropertyIsLessThan>
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
          <Name>Sodic soil</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
             <PropertyIsGreaterThanOrEqualTo>
<<<<<<< HEAD
                <PropertyName>value</PropertyName>
=======
                <PropertyName>esp</PropertyName>
>>>>>>> 58dcde557d1da9070628851a32775b2507519611
                <Literal>0.15</Literal>
              </PropertyIsGreaterThanOrEqualTo>
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
       
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>