<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0" 
    xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
    xmlns="http://www.opengis.net/sld" 
    xmlns:ogc="http://www.opengis.net/ogc" 
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>Soil Map - Fierotti original SLD </Name>
    <UserStyle>
      <Name>Soil Map - Fierotti original SLD</Name>
      <FeatureTypeStyle>
        <Rule>
          <Name>Corpo Idrico</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Corpo Idrico</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#6aa8e2</CssParameter>
            </Fill>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Dune litoranee</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Dune litoranee</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#ebc735</CssParameter>
            </Fill>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Litosuoli - Roccia affiorante - Protorendzina</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Litosuoli - Roccia affiorante - Protorendzina</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#e434d8</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Litosuoli - Roccia affiorante - Suoli bruni</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Litosuoli - Roccia affiorante - Suoli bruni</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#e437bf</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Litosuoli - Roccia affiorante - Suoli bruni andici</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Litosuoli - Roccia affiorante - Suoli bruni andici</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#4975c8</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Litosuoli - Roccia affiorante - Terra rossa</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Litosuoli - Roccia affiorante - Terra rossa</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#4b39d4</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Litosuoli - Suoli bruni acidi - Roccia affiorante</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Litosuoli - Suoli bruni acidi - Roccia affiorante</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#952be1</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Litosuoli - Suoli bruni lisciviati - Suoli bruni</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Litosuoli - Suoli bruni lisciviati - Suoli bruni</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#74e0c0</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Regosuoli - Litosuoli - Suoli bruni andici</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Regosuoli - Litosuoli - Suoli bruni andici</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#d13196</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Regosuoli - Litosuoli - Suoli bruni e/o Suoli bruni vertici</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Regosuoli - Litosuoli - Suoli bruni e/o Suoli bruni vertici</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#a5ef73</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Regosuoli - Suoli alluvionali e/o Vertisuoli</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Regosuoli - Suoli alluvionali e/o Vertisuoli</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#bd6bd8</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Regosuoli - Suoli bruni - Suoli bruni leggermente lisciviati</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Regosuoli - Suoli bruni - Suoli bruni leggermente lisciviati</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#d27967</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Regosuoli - Suoli bruni andici - Suoli bruni lisciviati</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Regosuoli - Suoli bruni andici - Suoli bruni lisciviati</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#6bd562</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Regosuoli - Suoli bruni e/o Suoli bruni vertici</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Regosuoli - Suoli bruni e/o Suoli bruni vertici</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#80c868</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Regosuoli - Suoli bruni e/o Suoli bruni vertici - Suoli alluvionali e/o Vertisuoli</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Regosuoli - Suoli bruni e/o Suoli bruni vertici - Suoli alluvionali e/o Vertisuoli</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#272fd2</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Roccia affiorante - Litosuoli</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Roccia affiorante - Litosuoli</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#0e39e8</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Roccia affiorante - Litosuoli - Terra rossa</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Roccia affiorante - Litosuoli - Terra rossa</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#e03d89</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Roccia affiorante - Terra rossa - Suoli bruni e/o Suoli bruni calcarei</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Roccia affiorante - Terra rossa - Suoli bruni e/o Suoli bruni calcarei</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#eb1156</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Saline</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Saline</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#dfda42</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Suoli alluvionali</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Suoli alluvionali</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#92d23f</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Suoli alluvionali - Vertisuoli</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Suoli alluvionali - Vertisuoli</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#cb1934</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Suoli bruni - Suoli alluvionali</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Suoli bruni - Suoli alluvionali</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#f04a4a</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Suoli bruni - Suoli bruni calcarei - Litosuoli</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Suoli bruni - Suoli bruni calcarei - Litosuoli</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#46d3be</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Suoli bruni - Suoli bruni calcarei - Rendzina</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Suoli bruni - Suoli bruni calcarei - Rendzina</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#6d27c8</CssParameter>
            </Fill>


          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Suoli bruni - Suoli bruni lisciviati - Regosuoli e/o Litosuoli</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Suoli bruni - Suoli bruni lisciviati - Regosuoli e/o Litosuoli</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#1fd565</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Suoli bruni - Suoli bruni vertici - Vertisuoli</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Suoli bruni - Suoli bruni vertici - Vertisuoli</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#3cca5d</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Suoli bruni acidi - Litosuoli - Roccia affiorante</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Suoli bruni acidi - Litosuoli - Roccia affiorante</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#9171ea</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Suoli bruni andici - Litosuoli</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Suoli bruni andici - Litosuoli</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#6ce274</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Suoli bruni calcarei - Litosuoli - Regosuoli</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Suoli bruni calcarei - Litosuoli - Regosuoli</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#c151ce</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Suoli bruni leggermente acidi - Suoli bruni - Suoli bruni lisciviati</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Suoli bruni leggermente acidi - Suoli bruni - Suoli bruni lisciviati</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#de9a1d</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Suoli bruni lisciviati - Terra rossa</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Suoli bruni lisciviati - Terra rossa</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#b2d55a</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Suoli idromorfi</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Suoli idromorfi</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#3ac6e2</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Terra rossa - Litosuoli</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Terra rossa - Litosuoli</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#efa380</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Terra rossa - Suoli bruni calcarei - Litosuoli</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Terra rossa - Suoli bruni calcarei - Litosuoli</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#f0c090</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Variante 17</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Variante 17</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#49b0e4</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Vertisuoli</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Vertisuoli</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#c3d062</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>Zona Urbana</Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>desc</ogc:PropertyName>
              <ogc:Literal>Zona Urbana</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#4ee7a0</CssParameter>
            </Fill>

          </PolygonSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
