<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>Soil erodibility by water (K)</Name>
    <UserStyle>
      <Name>Soil erodibility by water</Name>
      <Title>Soil erodibility by water</Title>
      <FeatureTypeStyle>
        <Rule>
          <Name>Slight</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
	   <Or>
            <And>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>0.35</Literal>
              </PropertyIsLessThan>

	      <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>max_gradient</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>max_gradient</PropertyName>
                <Literal>15</Literal>
              </PropertyIsLessThan>   
            </And>

	    <And>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0.35</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              
	      <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>max_gradient</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThanOrEqualTo>
                <PropertyName>max_gradient</PropertyName>
                <Literal>9</Literal>
              </PropertyIsLessThanOrEqualTo>   
            </And>
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
          <Name>Moderate</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
           <Or>
            <And>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>0.35</Literal>
              </PropertyIsLessThan>

	      <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>max_gradient</PropertyName>
                <Literal>15</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>max_gradient</PropertyName>
                <Literal>36</Literal>
              </PropertyIsLessThan>   
            </And>

	    <And>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0.35</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              
	      <PropertyIsGreaterThan>
                <PropertyName>max_gradient</PropertyName>
                <Literal>9</Literal>
              </PropertyIsGreaterThan>
              <PropertyIsLessThanOrEqualTo>
                <PropertyName>max_gradient</PropertyName>
                <Literal>25</Literal>
              </PropertyIsLessThanOrEqualTo>   
            </And>
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
          <Name>Severe</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
           <Or>
            <And>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>0.35</Literal>
              </PropertyIsLessThan>

	      <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>max_gradient</PropertyName>
                <Literal>36</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThanOrEqualTo>
                <PropertyName>max_gradient</PropertyName>
                <Literal>50</Literal>
              </PropertyIsLessThanOrEqualTo>   
            </And>

	    <And>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0.35</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              
	      <PropertyIsGreaterThan>
                <PropertyName>max_gradient</PropertyName>
                <Literal>25</Literal>
              </PropertyIsGreaterThan>
              <PropertyIsLessThanOrEqualTo>
                <PropertyName>max_gradient</PropertyName>
                <Literal>40</Literal>
              </PropertyIsLessThanOrEqualTo>   
            </And>
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
          <Name>Very severe</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <Or>
            <And>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>0.35</Literal>
              </PropertyIsLessThan>

	      <PropertyIsGreaterThan>
                <PropertyName>max_gradient</PropertyName>
                <Literal>50</Literal>
              </PropertyIsGreaterThan>
            </And>

	    <And>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0.35</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              
	      <PropertyIsGreaterThan>
                <PropertyName>max_gradient</PropertyName>
                <Literal>40</Literal>
              </PropertyIsGreaterThan>
            </And>
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
       
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>