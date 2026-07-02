<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>c_n_ratio</Name>
    <UserStyle>
      <Title>C/N ratio</Title>
      <FeatureTypeStyle>      
	  <Rule>
          <Name>High SOC mineralization potential (Cropland and first layer only)</Name>
          <ogc:Filter>
            <ogc:And>
	           <ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <ogc:Literal>C</ogc:Literal>
               </ogc:PropertyIsEqualTo>
               <ogc:PropertyIsGreaterThanOrEqualTo>
                  <ogc:PropertyName>value</ogc:PropertyName>
                  <ogc:Literal>0</ogc:Literal>
               </ogc:PropertyIsGreaterThanOrEqualTo>
               <ogc:PropertyIsLessThan>
                  <ogc:PropertyName>value</ogc:PropertyName>
                  <ogc:Literal>8</ogc:Literal>
               </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
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
          <Name>Moderate SOC mineralization potential (Cropland and first layer only)</Name>
          <ogc:Filter>
            <ogc:And>
	           <ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <ogc:Literal>C</ogc:Literal>
               </ogc:PropertyIsEqualTo>
               <ogc:PropertyIsGreaterThanOrEqualTo>
                  <ogc:PropertyName>value</ogc:PropertyName>
                  <ogc:Literal>8</ogc:Literal>
               </ogc:PropertyIsGreaterThanOrEqualTo>
               <ogc:PropertyIsLessThan>
                  <ogc:PropertyName>value</ogc:PropertyName>
                  <ogc:Literal>12</ogc:Literal>
               </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
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
          <Name>Low SOC mineralization potential (Cropland and first layer only)</Name>
          <ogc:Filter>
            <ogc:And>
	      		<ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <ogc:Literal>C</ogc:Literal>
                </ogc:PropertyIsEqualTo>
                <ogc:PropertyIsGreaterThanOrEqualTo>
                  <ogc:PropertyName>value</ogc:PropertyName>
                  <ogc:Literal>12</ogc:Literal>
                </ogc:PropertyIsGreaterThanOrEqualTo>
            </ogc:And>
          </ogc:Filter>
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
          <Name>High SOC mineralization potential and high microbial carbon accumulation activity (Grassland and forest with C/N less than 9.6 and 1st layer only)</Name>
          <ogc:Filter>
            <ogc:And>
	      		<ogc:Or>
	        		<ogc:PropertyIsEqualTo>
                  		<ogc:PropertyName>lu_type</ogc:PropertyName>
                  		<ogc:Literal>G</ogc:Literal>
                	</ogc:PropertyIsEqualTo>
	        		<ogc:PropertyIsEqualTo>
                  		<ogc:PropertyName>lu_type</ogc:PropertyName>
                  		<ogc:Literal>F</ogc:Literal>
                	</ogc:PropertyIsEqualTo>
                </ogc:Or>
                <ogc:PropertyIsGreaterThanOrEqualTo>
                	<ogc:PropertyName>value</ogc:PropertyName>
                	<ogc:Literal>0</ogc:Literal>
              	</ogc:PropertyIsGreaterThanOrEqualTo>
              	<ogc:PropertyIsLessThan>
                	<ogc:PropertyName>value</ogc:PropertyName>
                	<ogc:Literal>8</ogc:Literal>
              	</ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>square</WellKnownName>
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
          <Name>Moderate SOC mineralization potential and HIGH microbial carbon accumulation activity (Grassland and forest with C/N less than 9.6 and 1st layer only)</Name>
          <ogc:Filter>
            <ogc:And>
	      <ogc:Or>
	        <ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <ogc:Literal>G</ogc:Literal>
                </ogc:PropertyIsEqualTo>
	        <ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <ogc:Literal>F</ogc:Literal>
                </ogc:PropertyIsEqualTo>
              </ogc:Or>

              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>value</ogc:PropertyName>
                <ogc:Literal>8</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>value</ogc:PropertyName>
                <ogc:Literal>9.6</ogc:Literal>
              </ogc:PropertyIsLessThan>

            </ogc:And>
          </ogc:Filter>
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
          <Name>Moderate SOC mineralization potential and LOW microbial carbon accumulation activity (Grassland and forest with C/N is greater than or equal to 9.6 and 1st layer only)</Name>
          <ogc:Filter>
            <ogc:And>
	      <ogc:Or>
	        <ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <ogc:Literal>G</ogc:Literal>
                </ogc:PropertyIsEqualTo>
	        <ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <ogc:Literal>F</ogc:Literal>
                </ogc:PropertyIsEqualTo>
              </ogc:Or>

              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>value</ogc:PropertyName>
                <ogc:Literal>9.6</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>value</ogc:PropertyName>
                <ogc:Literal>12</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>square</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#194012</CssParameter>
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
          <Name>Low SOC mineralization potential and low microbial carbon accumulation activity (Grassland and forest with C/N is greater than or equal to 9.6 and 1st layer only)</Name>
          <ogc:Filter>
            <ogc:And>
	      <ogc:Or>
	        <ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <ogc:Literal>G</ogc:Literal>
                </ogc:PropertyIsEqualTo>
	        <ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>lu_type</ogc:PropertyName>
                  <ogc:Literal>F</ogc:Literal>
                </ogc:PropertyIsEqualTo>
              </ogc:Or>

              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>value</ogc:PropertyName>
                <ogc:Literal>12</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              
            </ogc:And>
          </ogc:Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>square</WellKnownName>
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

	
       
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>