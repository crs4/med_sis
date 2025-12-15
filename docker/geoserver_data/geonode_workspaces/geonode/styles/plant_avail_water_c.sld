<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
<<<<<<< HEAD
    <Name>Plant Available Water Capacity (%)</Name>
    <UserStyle>
      <Name>Plant Available Water Capacity (%)</Name>
      <Title>Plant Available Water Capacity (%)</Title>
=======
    <Name>plant_avail_water_c</Name>
    <UserStyle>
      <Name>circle_point</Name>
      <Title>Point Red Symbol Border</Title>
>>>>>>> 58dcde557d1da9070628851a32775b2507519611
      <FeatureTypeStyle>
        <Rule>
          <Name>Ideal water storage capacity</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>pawc</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>pawc</PropertyName>
                <Literal>10</Literal>
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
          <Name>Good water storage capacity</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>pawc</PropertyName>
                <Literal>10</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>pawc</PropertyName>
                <Literal>15</Literal>
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

<<<<<<< HEAD
        <Rule>
=======
 <Rule>
>>>>>>> 58dcde557d1da9070628851a32775b2507519611
          <Name>Limited water storage capacity</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>pawc</PropertyName>
                <Literal>15</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>pawc</PropertyName>
                <Literal>20</Literal>
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
          <Name>Poor water storage capacity</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
             <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>pawc</PropertyName>
                <Literal>20</Literal>
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
<<<<<<< HEAD
=======
       
>>>>>>> 58dcde557d1da9070628851a32775b2507519611
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>