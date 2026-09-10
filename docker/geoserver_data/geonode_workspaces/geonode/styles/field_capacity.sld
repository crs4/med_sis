<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>Volumetric water content at field capacity (%)</Name>
    <UserStyle>
      <Name>Volumetric water content at field capacity (%)</Name>
      <Title>Volumetric water content at field capacity (%)</Title>
      <FeatureTypeStyle>
        
	<Rule>
          <Name>Low (depends of the soil texture for irrigated cropland)</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
          
	     <Or>
    
    		<!-- Primo blocco AND -->
    		<And>  
		     <ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>S</Literal>
              	     </ogc:PropertyIsEqualTo>
              		
		     <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>0</Literal>
              			</PropertyIsGreaterThanOrEqualTo>
             		      <PropertyIsLessThan>
                		        <PropertyName>value</PropertyName>
                			<Literal>10</Literal>
             		      </PropertyIsLessThan>
		</And>


	<!-- Secondo blocco AND -->
    		<And>  
		     
			<ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>LS</Literal>
              		</ogc:PropertyIsEqualTo>
              		
		     <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>0</Literal>
              			</PropertyIsGreaterThanOrEqualTo>
             		      <PropertyIsLessThan>
                		        <PropertyName>value</PropertyName>
                			<Literal>16</Literal>
             		      </PropertyIsLessThan>
		</And>



	<!-- Terzo blocco AND -->
    		<And>  
		     
			<ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>SL</Literal>
              		</ogc:PropertyIsEqualTo>
              		
		     <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>0</Literal>
              			</PropertyIsGreaterThanOrEqualTo>
             		      <PropertyIsLessThan>
                		        <PropertyName>value</PropertyName>
                			<Literal>21</Literal>
             		      </PropertyIsLessThan>
		</And>



	<!-- Quarto blocco AND -->
    		<And>  
		    <ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>L</Literal>
              		</ogc:PropertyIsEqualTo>
              	    <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>0</Literal>
              		    </PropertyIsGreaterThanOrEqualTo>
             		    <PropertyIsLessThan>
                		        <PropertyName>value</PropertyName>
                			<Literal>27</Literal>
             		    </PropertyIsLessThan>
		</And>


	<!-- Quinto blocco AND -->
    		<And>  
		     
			<ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>SiL</Literal>
              		</ogc:PropertyIsEqualTo>
              		
		     <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>0</Literal>
              			</PropertyIsGreaterThanOrEqualTo>
             		      <PropertyIsLessThan>
                		        <PropertyName>value</PropertyName>
                			<Literal>30</Literal>
             		      </PropertyIsLessThan>
		</And>


	<!-- Sesto blocco AND -->
    		<And>  
			<ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>SCL</Literal>
              		</ogc:PropertyIsEqualTo>
              		
		     <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>0</Literal>
              			</PropertyIsGreaterThanOrEqualTo>
             		      <PropertyIsLessThan>
                		        <PropertyName>value</PropertyName>
                			<Literal>36</Literal>
             		      </PropertyIsLessThan>
		</And>

	<!-- Settimo blocco AND -->
    		<And>  
		    <ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>SC</Literal>
              		</ogc:PropertyIsEqualTo>
              	    <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>0</Literal>
              		    </PropertyIsGreaterThanOrEqualTo>
             		    <PropertyIsLessThan>
                		        <PropertyName>value</PropertyName>
                			<Literal>32</Literal>
             		    </PropertyIsLessThan>
		</And>


	<!-- Ottavo blocco AND -->
    		<And>  
		    <ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>CL</Literal>
              		</ogc:PropertyIsEqualTo>
              	    <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>0</Literal>
              		    </PropertyIsGreaterThanOrEqualTo>
             		    <PropertyIsLessThan>
                		        <PropertyName>value</PropertyName>
                			<Literal>29</Literal>
             		    </PropertyIsLessThan>
		</And>


<!-- Nono blocco AND -->
    		<And>  
		    <ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>SiCL</Literal>
              		</ogc:PropertyIsEqualTo>
              	    <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>0</Literal>
              		    </PropertyIsGreaterThanOrEqualTo>
             		    <PropertyIsLessThan>
                		        <PropertyName>value</PropertyName>
                			<Literal>28</Literal>
             		    </PropertyIsLessThan>
		</And>


<!-- Decimo blocco AND -->
    		<And>  
		    <ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>SiC</Literal>
              		</ogc:PropertyIsEqualTo>
              	    <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>0</Literal>
              		    </PropertyIsGreaterThanOrEqualTo>
             		    <PropertyIsLessThan>
                		        <PropertyName>value</PropertyName>
                			<Literal>40</Literal>
             		    </PropertyIsLessThan>
		</And>


<!-- Undicesimo blocco AND -->
    		<And>  
		    <ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>C</Literal>
              		</ogc:PropertyIsEqualTo>
              	    <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>0</Literal>
              		    </PropertyIsGreaterThanOrEqualTo>
             		    <PropertyIsLessThan>
                		        <PropertyName>value</PropertyName>
                			<Literal>40</Literal>
             		    </PropertyIsLessThan>
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

	
	<Rule>
          <Name>High (depends of the soil texture for irrigated cropland)</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
          
	     <Or>
    
    		<!-- Primo blocco AND_2 -->
    		<And>  
		     <ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>S</Literal>
              	     </ogc:PropertyIsEqualTo>
              		
		     <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>10</Literal>
              			</PropertyIsGreaterThanOrEqualTo>
             		      
		</And>


	<!-- Secondo blocco AND_2 -->
    		<And>  
		     
			<ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>LS</Literal>
              		</ogc:PropertyIsEqualTo>
              		
		     <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>16</Literal>
              			</PropertyIsGreaterThanOrEqualTo>
             		      
		</And>



	<!-- Terzo blocco AND_2 -->
    		<And>  
		     
			<ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>SL</Literal>
              		</ogc:PropertyIsEqualTo>
              		
		     <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>21</Literal>
              			</PropertyIsGreaterThanOrEqualTo>
             		      
		</And>



	<!-- Quarto blocco AND_2 -->
    		<And>  
		    <ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>L</Literal>
              		</ogc:PropertyIsEqualTo>
              	    <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>27</Literal>
              		    </PropertyIsGreaterThanOrEqualTo>
             		    
		</And>


	<!-- Quinto blocco AND_2 -->
    		<And>  
		     
			<ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>SiL</Literal>
              		</ogc:PropertyIsEqualTo>
              		
		     <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>30</Literal>
              			</PropertyIsGreaterThanOrEqualTo>
             		      
		</And>


	<!-- Sesto blocco AND_2 -->
    		<And>  
			<ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>SCL</Literal>
              		</ogc:PropertyIsEqualTo>
              		
		     <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>36</Literal>
              			</PropertyIsGreaterThanOrEqualTo>
             		      
		</And>

	<!-- Settimo blocco AND_2 -->
    		<And>  
		    <ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>SC</Literal>
              		</ogc:PropertyIsEqualTo>
              	    <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>32</Literal>
              		    </PropertyIsGreaterThanOrEqualTo>
             		    
		</And>


	<!-- Ottavo blocco AND_2 -->
    		<And>  
		    <ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>CL</Literal>
              		</ogc:PropertyIsEqualTo>
              	    <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>29</Literal>
              		    </PropertyIsGreaterThanOrEqualTo>
             		    
		</And>


<!-- Nono blocco AND_2 -->
    		<And>  
		    <ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>SiCL</Literal>
              		</ogc:PropertyIsEqualTo>
              	    <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>28</Literal>
              		    </PropertyIsGreaterThanOrEqualTo>
             		    
		</And>


<!-- Decimo blocco AND_2 -->
    		<And>  
		    <ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>SiC</Literal>
              		</ogc:PropertyIsEqualTo>
              	    <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>40</Literal>
              		    </PropertyIsGreaterThanOrEqualTo>
             		    
		</And>


<!-- Undicesimo blocco AND_2 -->
    		<And>  
		    <ogc:PropertyIsEqualTo>
                	<ogc:PropertyName>texture</ogc:PropertyName>
                	<Literal>C</Literal>
              		</ogc:PropertyIsEqualTo>
              	    <PropertyIsGreaterThanOrEqualTo>
                			<PropertyName>value</PropertyName>
                			<Literal>40</Literal>
              		    </PropertyIsGreaterThanOrEqualTo>
             		   
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

	
       
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>