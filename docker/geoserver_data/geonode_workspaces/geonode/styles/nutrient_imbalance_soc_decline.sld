<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>C/N ratio</Name>
    <UserStyle>
      <Name>circle_square</Name>
      <Title>Example of different symbol</Title>
      <FeatureTypeStyle>
        <Rule>
          <Name>High SOC mineralization potential due to biological activity</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
             <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>use_type_fg</ogc:PropertyName>
              <ogc:Literal>false</ogc:Literal>
             </ogc:PropertyIsEqualTo>
	      
	         <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>value</ogc:PropertyName>
                <Literal>0</Literal>
             </ogc:PropertyIsGreaterThanOrEqualTo>
             <ogc:PropertyIsLessThan>
                <ogc:PropertyName>value</ogc:PropertyName>
                <Literal>8</Literal>
             </ogc:PropertyIsLessThan>
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
          <Name>Good biological activity potential</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	     <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>use_type_fg</ogc:PropertyName>
              <ogc:Literal>false</ogc:Literal>
             </ogc:PropertyIsEqualTo>
             
	     <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>value</ogc:PropertyName>
                <Literal>8</Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              
	      <ogc:PropertyIsLessThan>
                <ogc:PropertyName>value</ogc:PropertyName>
                <Literal>12</Literal>
              </ogc:PropertyIsLessThan>
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
          <Name>Beginning of nitrogen starvation for biological activity</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
             <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>use_type_fg</ogc:PropertyName>
              <ogc:Literal>false</ogc:Literal>
             </ogc:PropertyIsEqualTo>

	     <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>value</ogc:PropertyName>
                <Literal>12</Literal>
             </ogc:PropertyIsGreaterThanOrEqualTo>

             <ogc:PropertyIsLessThan>
                <ogc:PropertyName>value</ogc:PropertyName>
                <Literal>15</Literal>
             </ogc:PropertyIsLessThan>
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
          <Name>Low biological activity potential</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
             <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>use_type_fg</ogc:PropertyName>
              <ogc:Literal>false</ogc:Literal>
             </ogc:PropertyIsEqualTo>
  
	     <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>value</ogc:PropertyName>
                <Literal>15</Literal>
             </ogc:PropertyIsGreaterThanOrEqualTo>
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
          <Name>Higher microbial carbon accumulation activity</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	    <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>use_type_fg</ogc:PropertyName>
              <ogc:Literal>true</ogc:Literal>
             </ogc:PropertyIsEqualTo>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>value</ogc:PropertyName>
                <Literal>0</Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>value</ogc:PropertyName>
                <Literal>9.6</Literal>
              </ogc:PropertyIsLessThan>
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
          <Name>Lower microbial carbon accumulation activity</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
	   <And>
	    <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>use_type_fg</ogc:PropertyName>
              <ogc:Literal>true</ogc:Literal>
             </ogc:PropertyIsEqualTo>

             <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>value</ogc:PropertyName>
                <Literal>9.6</Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
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