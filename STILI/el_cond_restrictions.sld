<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>Electric conductivity (dS/m) and SAR</Name>
    <UserStyle>
      <Name>el_cond_restrictions</Name>
      <Title>Electric conductivity (dS/m) and SAR</Title>
      <FeatureTypeStyle>
        <Rule>
          <Name>Excessive restriction on irrigation (SAR between 0 and 3 )</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>sar</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
	            <PropertyIsLessThan>
                <PropertyName>sar</PropertyName>
                <Literal>3</Literal>
              </PropertyIsLessThan>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>0.2</Literal>
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
          <Name>Restriction on irrigation (SAR between 0 and 3 )</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>sar</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
	            <PropertyIsLessThan>
                <PropertyName>sar</PropertyName>
                <Literal>3</Literal>
              </PropertyIsLessThan>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0.2</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>0.7</Literal>
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
          <Name>No restriction on irrigation (SAR between 0 and 3 )</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>sar</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
	            <PropertyIsLessThan>
                <PropertyName>sar</PropertyName>
                <Literal>3</Literal>
              </PropertyIsLessThan>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0.7</Literal>
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
          <Name>Excessive restriction on irrigation (SAR between 3 and 6 )</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>sar</PropertyName>
                <Literal>3</Literal>
              </PropertyIsGreaterThanOrEqualTo>
	            <PropertyIsLessThan>
                <PropertyName>sar</PropertyName>
                <Literal>6</Literal>
              </PropertyIsLessThan>
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
                <WellKnownName>square</WellKnownName>
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
          <Name>Restriction on irrigation (SAR between 3 and 6 )</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>sar</PropertyName>
                <Literal>3</Literal>
              </PropertyIsGreaterThanOrEqualTo>
	            <PropertyIsLessThan>
                <PropertyName>sar</PropertyName>
                <Literal>6</Literal>
              </PropertyIsLessThan>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0.3</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>1.2</Literal>
              </PropertyIsLessThan>
            </And>
          </Filter>
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
          <Name>No restriction on irrigation (SAR between 3 and 6 )</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>sar</PropertyName>
                <Literal>3</Literal>
              </PropertyIsGreaterThanOrEqualTo>
	            <PropertyIsLessThan>
                <PropertyName>sar</PropertyName>
                <Literal>6</Literal>
              </PropertyIsLessThan>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>1.2</Literal>
              </PropertyIsGreaterThanOrEqualTo>
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
          <Name>Excessive restriction on irrigation (SAR between 6 and 12 )</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>sar</PropertyName>
                <Literal>6</Literal>
              </PropertyIsGreaterThanOrEqualTo>
	            <PropertyIsLessThan>
                <PropertyName>sar</PropertyName>
                <Literal>12</Literal>
              </PropertyIsLessThan>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>0.5</Literal>
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
          <Name>Restriction on irrigation (SAR between 6 and 12 )</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>sar</PropertyName>
                <Literal>6</Literal>
              </PropertyIsGreaterThanOrEqualTo>
	            <PropertyIsLessThan>
                <PropertyName>sar</PropertyName>
                <Literal>12</Literal>
              </PropertyIsLessThan>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0.5</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>1.9</Literal>
              </PropertyIsLessThan>
            </And>
          </Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>triangle</WellKnownName>
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
          <Name>No restriction on irrigation (SAR between 6 and 12 )</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>sar</PropertyName>
                <Literal>6</Literal>
              </PropertyIsGreaterThanOrEqualTo>
	            <PropertyIsLessThan>
                <PropertyName>sar</PropertyName>
                <Literal>12</Literal>
              </PropertyIsLessThan>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>1.9</Literal>
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
        <Rule>
          <Name>Excessive restriction on irrigation (SAR between 12 and 20 )</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>sar</PropertyName>
                <Literal>12</Literal>
              </PropertyIsGreaterThanOrEqualTo>
	            <PropertyIsLessThan>
                <PropertyName>sar</PropertyName>
                <Literal>20</Literal>
              </PropertyIsLessThan>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>1.3</Literal>
              </PropertyIsLessThan>
            </And>
          </Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>star</WellKnownName>
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
          <Name>Restriction on irrigation (SAR between 12 and 20 )</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>sar</PropertyName>
                <Literal>12</Literal>
              </PropertyIsGreaterThanOrEqualTo>
	            <PropertyIsLessThan>
                <PropertyName>sar</PropertyName>
                <Literal>20</Literal>
              </PropertyIsLessThan>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>1.3</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>2.9</Literal>
              </PropertyIsLessThan>
            </And>
          </Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>star</WellKnownName>
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
          <Name>No restriction on irrigation (SAR between 12 and 20 )</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>sar</PropertyName>
                <Literal>12</Literal>
              </PropertyIsGreaterThanOrEqualTo>
	            <PropertyIsLessThan>
                <PropertyName>sar</PropertyName>
                <Literal>20</Literal>
              </PropertyIsLessThan>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>2.9</Literal>
              </PropertyIsGreaterThanOrEqualTo>
            </And>
          </Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>star</WellKnownName>
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
          <Name>Excessive restriction on irrigation (SAR between 20 and 40 )</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>sar</PropertyName>
                <Literal>20</Literal>
              </PropertyIsGreaterThanOrEqualTo>
	            <PropertyIsLessThan>
                <PropertyName>sar</PropertyName>
                <Literal>40</Literal>
              </PropertyIsLessThan>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>0</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>2.9</Literal>
              </PropertyIsLessThan>
            </And>
          </Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>cross</WellKnownName>
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
          <Name>Restriction on irrigation (SAR between 20 and 40 )</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>sar</PropertyName>
                <Literal>20</Literal>
              </PropertyIsGreaterThanOrEqualTo>
	            <PropertyIsLessThan>
                <PropertyName>sar</PropertyName>
                <Literal>40</Literal>
              </PropertyIsLessThan>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>2.9</Literal>
              </PropertyIsGreaterThanOrEqualTo>
              <PropertyIsLessThan>
                <PropertyName>value</PropertyName>
                <Literal>5</Literal>
              </PropertyIsLessThan>
            </And>
          </Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>cross</WellKnownName>
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
          <Name>No restriction on irrigation (SAR between 20 and 40 )</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <And>
	            <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>sar</PropertyName>
                <Literal>20</Literal>
              </PropertyIsGreaterThanOrEqualTo>
	            <PropertyIsLessThan>
                <PropertyName>sar</PropertyName>
                <Literal>40</Literal>
              </PropertyIsLessThan>
              <PropertyIsGreaterThanOrEqualTo>
                <PropertyName>value</PropertyName>
                <Literal>5</Literal>
              </PropertyIsGreaterThanOrEqualTo>
            </And>
          </Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>cross</WellKnownName>
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