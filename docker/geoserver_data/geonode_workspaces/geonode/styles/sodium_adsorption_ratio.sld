<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
<<<<<<< HEAD
    <Name>Sodium Adsorption Ratio - sodicity</Name>
=======
    <Name>sodium_adsorption_ratio</Name>
>>>>>>> 58dcde557d1da9070628851a32775b2507519611
    <UserStyle>
      <Name>circle_point</Name>
      <Title>Point Red Symbol Border</Title>
      <FeatureTypeStyle>
        <Rule>
          <Name>Non sodium impacted soil</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
              <PropertyIsGreaterThanOrEqualTo>
<<<<<<< HEAD
                <PropertyName>value</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>13</Literal>
=======
                <PropertyName>sar</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>sar</PropertyName>
                <Literal>8</Literal>
>>>>>>> 58dcde557d1da9070628851a32775b2507519611
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
<<<<<<< HEAD
          <Name>Sodium impacted soil</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
             <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
=======
          <Name>Potential particle clay dispersion and pore blocking</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>sar</PropertyName>
                <Literal>8</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>sar</PropertyName>
                <Literal>13</Literal>
              </PropertyIsLessThan>
            </And>
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
          <Name>Sodium impacted soil</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
             <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>sar</PropertyName>
>>>>>>> 58dcde557d1da9070628851a32775b2507519611
                <Literal>13</Literal>
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