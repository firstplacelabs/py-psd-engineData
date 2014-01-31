py-psd-engineData
=================

Reads the text, font type, font size and color from a photoshop psd file

To first obtain the engineData you will need to install psd-tools, then you can parse the engineData with the following:

#HOW TO
from psd_tools import PSDImage
from engineData import getFontAndColorDict

#open the psd
fname = 'myPsdName.psd'
psd = PSDImage.load(fname)


for layer in reversed(psd.layers):
  #get the raw engine data
  rawData = layer._tagged_blocks['TySh'][-1][-1][-1][-1]
  rawDataValue = rawData.value
  propDict= {'FontSet':'','Text':'','FontSize':'','A':'','R':'','G':'','B':''}
  getFontAndColorDict(propDict,engineDataValue)
  
  #gettin the text from the dict is as normal now
  
  myText = propDict['Text']
  myFont = propDict['FontSet']
  
  etc..
  
  *note A R G B are percentages so to get the actual value multiply by 255
  
  rNumeric = propDict['R'] * 255

