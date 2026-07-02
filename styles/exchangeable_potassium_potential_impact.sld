<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>exchangeable_potassium_potential_impact</Name>
    <UserStyle>
      <Title>Exchangeable Potassium - K+ (cmol/Kg)</Title>
      <FeatureTypeStyle> 
       <Rule>
          <Name>Potential positive impact on productivity following potassium fertilizers in sandy soils</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
               <Or>
				 <ogc:PropertyIsEqualTo>
                	  <ogc:PropertyName>texture</ogc:PropertyName>
                	  <Literal>TEXTURE_CLASSES:S</Literal>
              	 </ogc:PropertyIsEqualTo>
		         <ogc:PropertyIsEqualTo>
                	  <ogc:PropertyName>texture</ogc:PropertyName>
                	  <Literal>TEXTURE_CLASSES:LS</Literal>
              	 </ogc:PropertyIsEqualTo>
                 <ogc:PropertyIsEqualTo>
                	  <ogc:PropertyName>texture</ogc:PropertyName>
                	  <Literal>TEXTURE_CLASSES:SL</Literal>
              	 </ogc:PropertyIsEqualTo>
               </Or>
			   <PropertyIsGreaterThanOrEqualTo>
			   		<PropertyName>value</PropertyName>
                	<Literal>0</Literal>
              	</PropertyIsGreaterThanOrEqualTo>
             	<PropertyIsLessThan>
                	<PropertyName>value</PropertyName>
                	<Literal>0.3</Literal>
             	</PropertyIsLessThan>
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
          <Name>Potential non positive impact on productivity following potassium fertilizers in sandy soils</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
          <And>
               <Or>
			<ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>TEXTURE_CLASSES:S</Literal>
              		</ogc:PropertyIsEqualTo>
		         <ogc:PropertyIsEqualTo>
                	  <ogc:PropertyName>texture</ogc:PropertyName>
                	  <Literal>TEXTURE_CLASSES:LS</Literal>
              		  </ogc:PropertyIsEqualTo>
                          <ogc:PropertyIsEqualTo>
                	  <ogc:PropertyName>texture</ogc:PropertyName>
                	  <Literal>TEXTURE_CLASSES:SL</Literal>
              		  </ogc:PropertyIsEqualTo>
                  </Or>
            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0.3</Literal>
              </PropertyIsGreaterThanOrEqualTo>
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
          <Name>Potential positive impact on productivity following potassium fertilizers in clayey soils</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
               <Or>
			<ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>TEXTURE_CLASSES:C</Literal>
              		</ogc:PropertyIsEqualTo>
		         <ogc:PropertyIsEqualTo>
                	  <ogc:PropertyName>texture</ogc:PropertyName>
                	  <Literal>TEXTURE_CLASSES:SiC</Literal>
              		  </ogc:PropertyIsEqualTo>
                          <ogc:PropertyIsEqualTo>
                	  <ogc:PropertyName>texture</ogc:PropertyName>
                	  <Literal>TEXTURE_CLASSES:SC</Literal>
              		  </ogc:PropertyIsEqualTo>
                  </Or>

			  <PropertyIsGreaterThanOrEqualTo>
			  <PropertyName>value</PropertyName>
                	  <Literal>0</Literal>
              		  </PropertyIsGreaterThanOrEqualTo>
             		  <PropertyIsLessThan>
                	  <PropertyName>value</PropertyName>
                	  <Literal>0.75</Literal>
             		  </PropertyIsLessThan>

            </And>
          </Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>triangle</WellKnownName>
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
          <Name>Potential non positive impact on productivity following potassium fertilizers in clayey soils</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
          <And>
               <Or>
				<ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>TEXTURE_CLASSES:C</Literal>
              	</ogc:PropertyIsEqualTo>
		        <ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                		<Literal>TEXTURE_CLASSES:SiC</Literal>
              		</ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                	  <ogc:PropertyName>texture</ogc:PropertyName>
                	  <Literal>TEXTURE_CLASSES:SC</Literal>
              		</ogc:PropertyIsEqualTo>
                  </Or>
            	  <PropertyIsGreaterThanOrEqualTo>
                	<PropertyName>value</PropertyName>
                	<Literal>0.75</Literal>
              	  </PropertyIsGreaterThanOrEqualTo>
            	</And>
            </Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>triangle</WellKnownName>
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
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>