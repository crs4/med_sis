<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>edaf_unid_edaficas</Name>
    <UserStyle>
      <Name>edaf_unid_edaficas</Name>
      <Title>edaf_unid_edaficas</Title>
      <FeatureTypeStyle>
        <Rule>
          <Name>Albic Arenosols, Humic Cambisols, and Dystric Gleysols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Arenosoles álbicos, Cambisoles húmicos y Gleysoles dístricos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#36e786</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#36e786</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>              
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcic Cambisols with Calcaric Regosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Cambisoles cálcicos con Regosoles calcáreos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#c1d445</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#c1d445</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter> 
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcic Cambisols with Calcaric Regosols, Calcaric Fluvisols, and Calcic Luvisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Cambisoles cálcicos con Regosoles calcáreos, Fluvisoles calcáreos y Luvisoles Cálcicos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#15ccd2</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#15ccd2</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcic Cambisols and Calcaric Regosols with Leptic Leptosols, Calcaric Fluvisols, and Vertic Cambisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Cambisoles cálcicos y Regosoles calcáreos con Litosoles, Fluvisoles calcáreos y Cambisoles vérticos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#e0126e</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#e0126e</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Cambisoles cálcicos, Cambisoles gleicos y Regosoles calcáreos</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Cambisoles cálcicos, Cambisoles gleicos y Regosoles calcáreos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#dfbd4c</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#dfbd4c</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcic Cambisols, Calcic Luvisols, and Chromic Luvisols with Leptic Leptosols and Calcaric Fluvisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Cambisoles cálcicos, Luvisoles cálcicos y Luvisoles crómicos con Litosoles y Fluvisoles calcáreos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#70d5ba</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#70d5ba</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcic Cambisols, Calcic Luvisols, and Calcaric Regosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Cambisoles cálcicos, Luvisoles cálcicos y Regosoles calcáreos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#4e8be0</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#4e8be0</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcic Cambisols, Calcaric Regosols, and Leptic Leptosols with Rendzic Leptosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Cambisoles cálcicos, Regosoles calcáreos y Litosoles con Rendsinas</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#78e648</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#78e648</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Dystric Cambisols, Haplic Phaleozems, and Rankers with Humic Cambisols, Dystric Regosols, and Leptic Leptosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Cambisoles dístricos, Phaleozems háplicos y Rankers con Cambisoles húmicos, Regosoles dístricos y Litosoles</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#92ea3f</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#92ea3f</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Eutric Cambisols, Chromic Luvisols, and Calcic Cambisols with Eutric and Calcaric Regosols and Calcic Luvisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Cambisoles éutricos, Luvisoles crómicos y Cambisoles cálcicos con Regosoles éutricos y cálcareos y Luvisoles cálcicos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#cbc77b</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#cbc77b</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Eutric Cambisols, Chromic Luvisols, and Eutric Leptosols with Dystric Cambisols and Umbric Leptosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Cambisoles éutricos, Luvisoles crómicos y Litosoles con Cambisoles dístricos y Rankers</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#e2174d</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#e2174d</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Eutric Cambisols, Chromic Luvisols, and Orthic Luvisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Cambisoles éutricos, Luvisoles crómicos y Luvisoles órticos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#356eeb</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#356eeb</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Eutric Cambisols, Rankers, and Orthic Luvisols with Chromic Luvisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Cambisoles éutricos, Rankers y Luvisoles órticos con Luvisoles crómicos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#623fcd</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#623fcd</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Eutric Cambisols, Eutric Regosols, and Leptic Leptosols with Rankers</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Cambisoles éutricos, Regosoles éutricos y Litosoles con Rankers</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#5466d5</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#5466d5</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Eutric Cambisols, Eutric Regosols, and Chromic Luvisols with Leptic Leptosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Cambisoles éutricos, Regosoles éutricos y Luvisoles crómicos con Litosoles</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#e11dbd</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#e11dbd</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Eutric Cambisols, Rankers, and Orthic Luvisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Cambisoles éutricos,Rankers y Luvisoles órticos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#ef7186</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#ef7186</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Vertic Cambisols, Calcaric Regosols, and Chromic Vertisols with Calcic Cambisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Cambisoles vérticos, Regosoles calcáreos y Vertisoles crómicos con Cambisoles cálcicos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#43e75e</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#43e75e</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Vertic Cambisols, Chromic Vertisols, and Calcic Cambisols with Calcaric Regosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Cambisoles vérticos, Vertisoles crómicos y Cambisoles cálcicos con Regosoles calcáreos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#e6ed57</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#e6ed57</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcaric Fluvisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Fluvisoles calcáreos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#d9a779</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#d9a779</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcaric Fluvisols and Calcic Xerosols with Calcaric Regosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Fluvisoles calcáreos y Xerosoles cálcidos con Regosoles calcáreos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#d66535</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#d66535</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Eutric Fluvisols and Eutric Cambisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Fluvisoles éutricos y cambisoles éutricos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#bf19d1</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#bf19d1</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Eutric Histosols and Fluvisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Histosoles éutricos y Fluvisoles</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#4bd5e7</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#4bd5e7</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Leptic Leptosols and Dystric Regosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Litosoles y Regosoles  dítricos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#90d82b</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#90d82b</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Leptic Leptosols and Luvic Xerosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>litosoles y Xerosoles lúvicos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#e57fa2</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#e57fa2</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Leptic Leptosols, Calcic Cambisols, and Calcic Xerosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Litosoles, Cambisoles cálcicos y Xerosoles cálcicos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#afcb78</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#afcb78</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Leptic Leptosols, Chromic Luvisols, and Rendzic Leptosols with Calcic Cambisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Litosoles, Luvisoles crómicos y Rendsinas con Cambisoles cálcicos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#ac42d6</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#ac42d6</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Leptic Leptosols, Eutric Regosols, and Chromic Luvisols with Eutric Cambisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Litosoles, Regosoles éutricos y Luvisoles crómicos con Cambisoles éutricos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#e576b3</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#e576b3</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcic Luvisols, Calcic Cambisols, and Eutric Cambisols with Chromic Luvisols, Calcaric Regosols, and Leptic Leptosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Luvisoles cálcicos, Cambisoles cálcicos y Cambisoles éutricos con  Luvisoles crómicos, Regosoles calcáreos y Litosoles</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#ecb363</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#ecb363</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcic Luvisols, Calcic Cambisols, and Chromic Luvisols with Calcaric Regosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Luvisoles cálcicos, Cambisoles cálcicos y Luvisoles crómicos con Regosoles calcáreos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#e63f4a</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#e63f4a</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcic Luvisols, Chromic Luvisols, and Gleyic Luvisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Luvisoles cálcicos, Luvisoles crómicos y  Luvisoles gleicos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#2f13d1</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#2f13d1</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Chromic Luvisols, Calcic Cambisols, and Leptic Leptosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Luvisoles crómicos Cambisoles cálcicos y Litosoles</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#6defb4</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#6defb4</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Chromic Luvisols and Regosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Luvisoles crómicos y Regosoles</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#257fd8</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#257fd8</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Chromic Luvisols, Eutric Cambisols, and Leptic Leptosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Luvisoles crómicos, Cambisoles éutricos y Litosoles</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#de504d</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#de504d</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Chromic Luvisols, Leptic Leptosols, and Eutric Regosols with Dystric Nitosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Luvisoles crómicos, Litosoles y Regosoles  éutricos con Nitosoles dístricos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#ef361e</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#ef361e</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Chromic Luvisols, Eutric Regosols, and Leptic Leptosols with Phaleozems and Eutric Cambisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Luvisoles crómicos, Regosoles  éutricos y Litosoles con Phaleozems y Cambisoles éutricos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#69e394</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#69e394</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Gleyic Luvisols, Orthic Luvisols, and Eutric Cambisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Luvisoles gleicos, Luvisoles órticos y Cambisoles éutricos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#6ae817</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#6ae817</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Orthic Luvisols and Gleyic Luvisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Luvisoles órticos y Luvisoles gleicos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#3a9ee0</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#3a9ee0</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Orthic Luvisols, Gleyic Luvisols, and Eutric Cambisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Luvisoles órticos, Luvisoles gleicos y Cambisoles éutricos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#df5734</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#df5734</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Eutric Planosols, Gleyic Luvisols, and Plinthic Luvisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Planosoles éutricos, Luvisoles gleicos y Luvisoles Plínticos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#7accbd</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#7accbd</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Mollic Planosols, Pellitic Vertisols, Calcaric Phaeozems with Arenic Rankers</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Planosoles móllicos, Vertisoles pélicos, Phaleozems calcáreos con Rankers arenosos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#db600f</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#db600f</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcaric Regosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Regosoles calcáreos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#de1b96</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#de1b96</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcaric Regosols and Calcic Cambisols with Leptic Leptosols, Calcaric Fluvisols, and Rendzic Leptosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Regosoles Calcáreos y Cambisoles cálcicos con litosoles, Fluviosoles  calcáreos y Rendsinas</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#a9d028</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#a9d028</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcaric Regosols and Calcic Cambisols with Calcic Luvisols and Calcaric Fluvisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Regosoles Calcáreos y Cambisoles cálcicos con Luvisoles cálcicos y Fluvisoles calcáreos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#b65fcc</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#b65fcc</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcaric Regosols and Leptic Leptosols with Calcic Cambisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Regosoles calcáreos y Litosoles con Cambisoles cálcicos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#7f46ca</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#7f46ca</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcaric Regosols and Eutric Regosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Regosoles calcáreos y Regosoles éutricos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#e8ad37</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#e8ad37</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcaric Regosols and Calcic Xerosols with Leptic Leptosols and Calcaric Fluvisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Regosoles Calcáreos y Xerosoles cálcicos con Litosoles y Fluisoles cálcareos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#13c986</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#13c986</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Dystric Regosols and Arenosols (Dunes and Beaches)</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Regosoles dístricos y Arenosoles (Dunas y Playas)</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#11eedc</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#11eedc</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Eutric Regosols, Eutric Cambisols, and Orthic Luvisols with Leptic Leptosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Regosoles éutricos, Cambisoles éutricos y Luvisoles órticos con Litosoles</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#d5c560</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#d5c560</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Eutric Regosols, Leptic Leptosols, and Eutric Cambisols with Rankers, over metamorphic rocks</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Regosoles éutricos, Litosoles y cambisoles eútricos con Rankers, sobre materiales metamórficos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#8d88e4</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#8d88e4</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Eutric Regosols, Leptic Leptosols, and Eutric Cambisols with Rankers, over plutonic rocks</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Regosoles éutricos, Litosoles y cambisoles eútricos con Rankers, sobre materiales plutónicos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#58ea45</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#58ea45</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Eutric Regosols, Dystric Regosols, and Albic Arenosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Regosoles éutricos, Regosoles dístricos y Aerosoles álbicos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#cb69cd</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#cb69cd</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Eutric Regosols, Haplic Xerosols, and Leptic Leptosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Regosoles éutricos, Xerosoles hápilicos y Litosoles</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#e624b2</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#e624b2</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>no data</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Sin dato</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#a02ae9</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#a02ae9</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Takiric Solonchaks and Gleyic Solonchaks</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Solonchaks takírico y Solonchaks gleicos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#64db62</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#64db62</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Chromic Vertisols and Vertic Cambisols with Calcic Cambisols, Calcaric Regosols, and Pellitic Vertisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Vertisoles crómicos y Cambisoles vérticos con Cambisoles cálcicos, Regosoles calcáreos y Vertisoles pélicos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#58e47d</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#58e47d</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Pellitic Vertisols and Chromic Vertisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Vertisoles pélicos y Vertisoles crómicos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#5e63e9</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#5e63e9</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Pellitic Vertisols, Rendzic Leptosols, and Calcaric Regosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Vertisoles pélicos, Rendsinas y Regosoles calcáreos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#ed2cdd</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#ed2cdd</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcic Xerosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Xerosoles cálcicos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#48d525</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#48d525</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcic Xerosols and Calcaric Fluvisols with Calcaric Regosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Xerosoles cálcicos y Fluvisoles calcáreos con Regosoles calcáreos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#59ef66</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#59ef66</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcic Xerosols and Leptic Leptosols with Calcaric Fluvisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Xerosoles cálcicos y Litosoles con Fluvisoles calcáreos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#977dcd</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#977dcd</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcic Xerosols and Calcaric Regosols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Xerosoles cálcicos y Regosoles calcáreos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#3db9ee</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#3db9ee</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcic Xerosols and Calcaric Regosols with Calcaric Fluvisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Xerosoles cálcicos y Regosoles calcáreos con Fluvisoles calcáreos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#29aed3</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#29aed3</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Calcic Xerosols and Luvic Xerosols with Calcaric Regosols and Calcaric Fluvisols</Name>
          <Filter xmlns="http://www.opengis.net/ogc">
            <PropertyIsEqualTo>
              <PropertyName>unid_edaf</PropertyName>
              <Literal>Xerosoles cálcicos y Xerosoles Lúvicos con Regosoles calcáreos y Fluvisoles calcáreos</Literal>
            </PropertyIsEqualTo>
          </Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#9c4ae9</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#9c4ae9</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name></Name>
          <ElseFilter xmlns:se="http://www.opengis.net/se"/>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#ffffff</CssParameter>
            </Fill>
            <Stroke>
               <CssParameter name="stroke">#ffffff</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
               
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>

