<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" version="1.0.0" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" xmlns:sld="http://www.opengis.net/sld">
  <UserLayer>
    <sld:LayerFeatureConstraints>
      <sld:FeatureTypeConstraint/>
    </sld:LayerFeatureConstraints>
    <sld:UserStyle>
      <sld:Name>mappa_dei_suoli_europa_clip_sicilia</sld:Name>
      <sld:FeatureTypeStyle>
        <sld:Rule>
          <sld:RasterSymbolizer>
            <sld:ChannelSelection>
              <sld:GrayChannel>
                <sld:SourceChannelName>1</sld:SourceChannelName>
              </sld:GrayChannel>
            </sld:ChannelSelection>
            <sld:ColorMap type="values">
              <sld:ColorMapEntry quantity="1" label="1" color="#3feaea"/>
              <sld:ColorMapEntry quantity="3" label="3" color="#85e16e"/>
              <sld:ColorMapEntry quantity="9" label="9" color="#c233e6"/>
              <sld:ColorMapEntry quantity="13" label="13" color="#de8d13"/>
              <sld:ColorMapEntry quantity="15" label="15" color="#c93d91"/>
              <sld:ColorMapEntry quantity="20" label="20" color="#44ce7b"/>
              <sld:ColorMapEntry quantity="21" label="21" color="#dc1010"/>
              <sld:ColorMapEntry quantity="25" label="25" color="#6045ca"/>
              <sld:ColorMapEntry quantity="29" label="29" color="#649cef"/>
              <sld:ColorMapEntry quantity="30" label="30" color="#cfef4d"/>
            </sld:ColorMap>
          </sld:RasterSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </UserLayer>
</StyledLayerDescriptor>
