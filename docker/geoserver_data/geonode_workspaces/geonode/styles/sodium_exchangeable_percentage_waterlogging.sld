<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>Sodium Exchangeable Percentage (ESP)- Waterlogging</Name>
    <UserStyle>
      <Name>sodium_exchangeable_percentage_waterlogging</Name>
      <Title>Sodium Exchangeable Percentage (ESP)- Waterlogging</Title>
      <FeatureTypeStyle>
        <Rule>
          <Name>Lower waterlogging potential risk due to soil sodicity (CEC/Clay ≥ 0.24)</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>cec_clay_ratio</PropertyName>
                <Literal>0.24</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>6</Literal>
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
          <Name>Higher waterlogging potential for soil with high charge density clay (CEC/Clay ≥ 0.24)</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>cec_clay_ratio</PropertyName>
                <Literal>0.24</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>6</Literal>
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
          <Name>Higher waterlogging  potential risk due to soil sodicity (CEC/Clay ≥ 0.24)</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>cec_clay_ratio</PropertyName>
                <Literal>0.24</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>15</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>100</Literal>
              </PropertyIsLessThanOrEqualTo>
            </And>
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
        <Rule>
          <Name>Lower waterlogging potential risk due to soil sodicity (CEC/Clay less than 0.24)</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsLessThan>
                <PropertyName>cec_clay_ratio</PropertyName>
                <Literal>0.24</Literal>
              </PropertyIsLessThan>
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
        <Rule>
          <Name>Higher waterlogging  potential risk due to soil sodicity (CEC/Clay less than 0.24)</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsLessThan>
                <PropertyName>cec_clay_ratio</PropertyName>
                <Literal>0.24</Literal>
              </PropertyIsLessThan>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>15</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>100</Literal>
              </PropertyIsLessThanOrEqualTo>
            </And>
          </Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>square</WellKnownName>
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