import os
import re
import StringIO
#-------------------------------------------------- 
#Utility class to read engineData
#--------------------------------------------------   
#Reads a property
def readProp(stream):
    prop = ''
    while True:
        c = stream.read(1)
        if c == ' ' or c =='\n' or c=='\r' or c=='\t':
            break
        prop += c
    return prop
#--------------------------------------------------   
#Reads an "adobe string" (these are prefixed with two chars I called sigs)
def readText(stream):
    text = ''
    c = stream.read(1)
    #skip to start of string
    while c !='(':
       c = stream.read(1)
    
    sig1 = stream.read(1)
    sig2 = stream.read(1)
    
    if sig1 != '\xfe' or sig2 != '\xff':
        print("readText sig error")
    
    while True:
        c1 = stream.read(1)
        if c1 ==')':
            return text
        c2 = stream.read(1)
        if c2 =='\\':
            c2 = stream.read(1)
        if c2 =='13':
            text += '\n'
        else :
            
            val = ord(c1) << 8 | ord(c2)
            
            if val <= 255:
                text += chr(val)
            else:
                text += ('&#'+str(val)+';')
    return text
#--------------------------------------------------        
def readFontSize(stream):
    fontSize = ''
    while True:
        c = stream.read(1)
        if c ==' ' or c=='\n' or c=='\r' or c=='\t':
            break
        fontSize += c
    return fontSize

#--------------------------------------------------        
def readARGB(stream):
    argb = ''
    
    c = stream.read(1)
    #skip to start of string
    while c !='[':
       c = stream.read(1)
       
    while True:
        c = stream.read(1)
        if c ==']':
            break
        argb += c
    return argb    
    
def getFontAndColorDict(propDict, engineData):
    stream = StringIO.StringIO(engineData)
    
    while True:
        
        #if we reach the end
        if stream.pos == len(engineData):
            break
        
        c = stream.read(1)
        if c =='/':
            #found prop
            prop = readProp(stream)
            
            if prop == 'Text' and propDict['Text']=='':
                propDict['Text'] = readText(stream)

            if prop =='FontSet' and propDict['FontSet']=='':
                propDict['FontSet'] = readText(stream)
                            
            if prop =='FontSize' and propDict['FontSize']=='':
                propDict['FontSize'] = readFontSize(stream)
            
            if prop =='Values' and propDict['R']=='':
                argb = readARGB(stream)
                argb = argb.split()
                propDict['A'] = argb[0]
                propDict['R'] = argb[1]
                propDict['G'] = argb[2]
                propDict['B'] = argb[3]

    return propDict

def main(): 
    #test case
    propDict= {'FontSet':'','Text':'','FontSize':'','A':'','R':'','G':'','B':''}
    testData = '\n\n<<\n\t/EngineDict\n\t<<\n\t\t/Editor\n\t\t<<\n\t\t\t/Text (\xfe\xff\x00P\x00R\x00E\x00V\x00I\x00O\x00U\x00S\x00\r)\n\t\t>>\n\t\t/ParagraphRun\n\t\t<<\n\t\t\t/DefaultRunData\n\t\t\t<<\n\t\t\t\t/ParagraphSheet\n\t\t\t\t<<\n\t\t\t\t\t/DefaultStyleSheet 0\n\t\t\t\t\t/Properties\n\t\t\t\t\t<<\n\t\t\t\t\t>>\n\t\t\t\t>>\n\t\t\t\t/Adjustments\n\t\t\t\t<<\n\t\t\t\t\t/Axis [ 1.0 0.0 1.0 ]\n\t\t\t\t\t/XY [ 0.0 0.0 ]\n\t\t\t\t>>\n\t\t\t>>\n\t\t\t/RunArray [\n\t\t\t<<\n\t\t\t\t/ParagraphSheet\n\t\t\t\t<<\n\t\t\t\t\t/Name (\xfe\xff\x00B\x00a\x00s\x00i\x00c\x00 \x00P\x00a\x00r\x00a\x00g\x00r\x00a\x00p\x00h)\n\t\t\t\t\t/DefaultStyleSheet 0\n\t\t\t\t\t/Properties\n\t\t\t\t\t<<\n\t\t\t\t\t\t/Justification 0\n\t\t\t\t\t\t/FirstLineIndent 0.0\n\t\t\t\t\t\t/StartIndent 0.0\n\t\t\t\t\t\t/EndIndent 0.0\n\t\t\t\t\t\t/SpaceBefore 0.0\n\t\t\t\t\t\t/SpaceAfter 0.0\n\t\t\t\t\t\t/AutoHyphenate true\n\t\t\t\t\t\t/HyphenatedWordSize 6\n\t\t\t\t\t\t/PreHyphen 2\n\t\t\t\t\t\t/PostHyphen 2\n\t\t\t\t\t\t/ConsecutiveHyphens 8\n\t\t\t\t\t\t/Zone 36.0\n\t\t\t\t\t\t/WordSpacing [ .8 1.0 1.33 ]\n\t\t\t\t\t\t/LetterSpacing [ 0.0 0.0 0.0 ]\n\t\t\t\t\t\t/GlyphSpacing [ 1.0 1.0 1.0 ]\n\t\t\t\t\t\t/AutoLeading 1.2\n\t\t\t\t\t\t/LeadingType 0\n\t\t\t\t\t\t/Hanging false\n\t\t\t\t\t\t/Burasagari false\n\t\t\t\t\t\t/KinsokuOrder 0\n\t\t\t\t\t\t/EveryLineComposer false\n\t\t\t\t\t>>\n\t\t\t\t>>\n\t\t\t\t/Adjustments\n\t\t\t\t<<\n\t\t\t\t\t/Axis [ 1.0 0.0 1.0 ]\n\t\t\t\t\t/XY [ 0.0 0.0 ]\n\t\t\t\t>>\n\t\t\t>>\n\t\t\t]\n\t\t\t/RunLengthArray [ 9 ]\n\t\t\t/IsJoinable 1\n\t\t>>\n\t\t/StyleRun\n\t\t<<\n\t\t\t/DefaultRunData\n\t\t\t<<\n\t\t\t\t/StyleSheet\n\t\t\t\t<<\n\t\t\t\t\t/StyleSheetData\n\t\t\t\t\t<<\n\t\t\t\t\t>>\n\t\t\t\t>>\n\t\t\t>>\n\t\t\t/RunArray [\n\t\t\t<<\n\t\t\t\t/StyleSheet\n\t\t\t\t<<\n\t\t\t\t\t/StyleSheetData\n\t\t\t\t\t<<\n\t\t\t\t\t\t/Font 0\n\t\t\t\t\t\t/FontSize 18.0\n\t\t\t\t\t\t/AutoKerning false\n\t\t\t\t\t\t/Kerning 0\n\t\t\t\t\t\t/FillColor\n\t\t\t\t\t\t<<\n\t\t\t\t\t\t\t/Type 1\n\t\t\t\t\t\t\t/Values [ 1.0 .85489 .1059 .23923 ]\n\t\t\t\t\t\t>>\n\t\t\t\t\t\t/HindiNumbers false\n\t\t\t\t\t>>\n\t\t\t\t>>\n\t\t\t>>\n\t\t\t<<\n\t\t\t\t/StyleSheet\n\t\t\t\t<<\n\t\t\t\t\t/StyleSheetData\n\t\t\t\t\t<<\n\t\t\t\t\t\t/Font 0\n\t\t\t\t\t\t/FontSize 18.0\n\t\t\t\t\t\t/AutoKerning true\n\t\t\t\t\t\t/Kerning 0\n\t\t\t\t\t\t/FillColor\n\t\t\t\t\t\t<<\n\t\t\t\t\t\t\t/Type 1\n\t\t\t\t\t\t\t/Values [ 1.0 .85489 .1059 .23923 ]\n\t\t\t\t\t\t>>\n\t\t\t\t\t\t/HindiNumbers false\n\t\t\t\t\t>>\n\t\t\t\t>>\n\t\t\t>>\n\t\t\t]\n\t\t\t/RunLengthArray [ 1 8 ]\n\t\t\t/IsJoinable 2\n\t\t>>\n\t\t/GridInfo\n\t\t<<\n\t\t\t/GridIsOn false\n\t\t\t/ShowGrid false\n\t\t\t/GridSize 18.0\n\t\t\t/GridLeading 22.0\n\t\t\t/GridColor\n\t\t\t<<\n\t\t\t\t/Type 1\n\t\t\t\t/Values [ 0.0 0.0 0.0 1.0 ]\n\t\t\t>>\n\t\t\t/GridLeadingFillColor\n\t\t\t<<\n\t\t\t\t/Type 1\n\t\t\t\t/Values [ 0.0 0.0 0.0 1.0 ]\n\t\t\t>>\n\t\t\t/AlignLineHeightToGridFlags false\n\t\t>>\n\t\t/AntiAlias 4\n\t\t/UseFractionalGlyphWidths true\n\t\t/Rendered\n\t\t<<\n\t\t\t/Version 1\n\t\t\t/Shapes\n\t\t\t<<\n\t\t\t\t/WritingDirection 0\n\t\t\t\t/Children [\n\t\t\t\t<<\n\t\t\t\t\t/ShapeType 0\n\t\t\t\t\t/Procession 0\n\t\t\t\t\t/Lines\n\t\t\t\t\t<<\n\t\t\t\t\t\t/WritingDirection 0\n\t\t\t\t\t\t/Children [ ]\n\t\t\t\t\t>>\n\t\t\t\t\t/Cookie\n\t\t\t\t\t<<\n\t\t\t\t\t\t/Photoshop\n\t\t\t\t\t\t<<\n\t\t\t\t\t\t\t/ShapeType 0\n\t\t\t\t\t\t\t/PointBase [ 0.0 0.0 ]\n\t\t\t\t\t\t\t/Base\n\t\t\t\t\t\t\t<<\n\t\t\t\t\t\t\t\t/ShapeType 0\n\t\t\t\t\t\t\t\t/TransformPoint0 [ 1.0 0.0 ]\n\t\t\t\t\t\t\t\t/TransformPoint1 [ 0.0 1.0 ]\n\t\t\t\t\t\t\t\t/TransformPoint2 [ 0.0 0.0 ]\n\t\t\t\t\t\t\t>>\n\t\t\t\t\t\t>>\n\t\t\t\t\t>>\n\t\t\t\t>>\n\t\t\t\t]\n\t\t\t>>\n\t\t>>\n\t>>\n\t/ResourceDict\n\t<<\n\t\t/KinsokuSet [\n\t\t<<\n\t\t\t/Name (\xfe\xff\x00P\x00h\x00o\x00t\x00o\x00s\x00h\x00o\x00p\x00K\x00i\x00n\x00s\x00o\x00k\x00u\x00H\x00a\x00r\x00d)\n\t\t\t/NoStart (\xfe\xff0\x010\x02\xff\x0c\xff\x0e0\xfb\xff\x1a\xff\x1b\xff\x1f\xff\x010\xfc \x15 \x19 \x1d\xff\t0\x15\xff=\xff]0\t0\x0b0\r0\x0f0\x110\xfd0\xfe0\x9d0\x9e0\x050A0C0E0G0I0c0\x830\x850\x870\x8e0\xa10\xa30\xa50\xa70\xa90\xc30\xe30\xe50\xe70\xee0\xf50\xf60\x9b0\x9c\x00?\x00!\x00\\)\x00]\x00}\x00,\x00.\x00:\x00;!\x03!\t\x00\xa2\xff\x05 0)\n\t\t\t/NoEnd (\xfe\xff \x18 \x1c\xff\x080\x14\xff;\xff[0\x080\n0\x0c0\x0e0\x10\x00\\(\x00[\x00{\xff\xe5\xff\x04\x00\xa3\xff \x00\xa70\x12\xff\x03)\n\t\t\t/Keep (\xfe\xff \x15 %)\n\t\t\t/Hanging (\xfe\xff0\x010\x02\x00.\x00,)\n\t\t>>\n\t\t<<\n\t\t\t/Name (\xfe\xff\x00P\x00h\x00o\x00t\x00o\x00s\x00h\x00o\x00p\x00K\x00i\x00n\x00s\x00o\x00k\x00u\x00S\x00o\x00f\x00t)\n\t\t\t/NoStart (\xfe\xff0\x010\x02\xff\x0c\xff\x0e0\xfb\xff\x1a\xff\x1b\xff\x1f\xff\x01 \x19 \x1d\xff\t0\x15\xff=\xff]0\t0\x0b0\r0\x0f0\x110\xfd0\xfe0\x9d0\x9e0\x05)\n\t\t\t/NoEnd (\xfe\xff \x18 \x1c\xff\x080\x14\xff;\xff[0\x080\n0\x0c0\x0e0\x10)\n\t\t\t/Keep (\xfe\xff \x15 %)\n\t\t\t/Hanging (\xfe\xff0\x010\x02\x00.\x00,)\n\t\t>>\n\t\t]\n\t\t/MojiKumiSet [\n\t\t<<\n\t\t\t/InternalName (\xfe\xff\x00P\x00h\x00o\x00t\x00o\x00s\x00h\x00o\x00p\x006\x00M\x00o\x00j\x00i\x00K\x00u\x00m\x00i\x00S\x00e\x00t\x001)\n\t\t>>\n\t\t<<\n\t\t\t/InternalName (\xfe\xff\x00P\x00h\x00o\x00t\x00o\x00s\x00h\x00o\x00p\x006\x00M\x00o\x00j\x00i\x00K\x00u\x00m\x00i\x00S\x00e\x00t\x002)\n\t\t>>\n\t\t<<\n\t\t\t/InternalName (\xfe\xff\x00P\x00h\x00o\x00t\x00o\x00s\x00h\x00o\x00p\x006\x00M\x00o\x00j\x00i\x00K\x00u\x00m\x00i\x00S\x00e\x00t\x003)\n\t\t>>\n\t\t<<\n\t\t\t/InternalName (\xfe\xff\x00P\x00h\x00o\x00t\x00o\x00s\x00h\x00o\x00p\x006\x00M\x00o\x00j\x00i\x00K\x00u\x00m\x00i\x00S\x00e\x00t\x004)\n\t\t>>\n\t\t]\n\t\t/TheNormalStyleSheet 0\n\t\t/TheNormalParagraphSheet 0\n\t\t/ParagraphSheetSet [\n\t\t<<\n\t\t\t/Name (\xfe\xff\x00N\x00o\x00r\x00m\x00a\x00l\x00 \x00R\x00G\x00B)\n\t\t\t/DefaultStyleSheet 0\n\t\t\t/Properties\n\t\t\t<<\n\t\t\t\t/Justification 0\n\t\t\t\t/FirstLineIndent 0.0\n\t\t\t\t/StartIndent 0.0\n\t\t\t\t/EndIndent 0.0\n\t\t\t\t/SpaceBefore 0.0\n\t\t\t\t/SpaceAfter 0.0\n\t\t\t\t/AutoHyphenate true\n\t\t\t\t/HyphenatedWordSize 6\n\t\t\t\t/PreHyphen 2\n\t\t\t\t/PostHyphen 2\n\t\t\t\t/ConsecutiveHyphens 8\n\t\t\t\t/Zone 36.0\n\t\t\t\t/WordSpacing [ .8 1.0 1.33 ]\n\t\t\t\t/LetterSpacing [ 0.0 0.0 0.0 ]\n\t\t\t\t/GlyphSpacing [ 1.0 1.0 1.0 ]\n\t\t\t\t/AutoLeading 1.2\n\t\t\t\t/LeadingType 0\n\t\t\t\t/Hanging false\n\t\t\t\t/Burasagari false\n\t\t\t\t/KinsokuOrder 0\n\t\t\t\t/EveryLineComposer false\n\t\t\t>>\n\t\t>>\n\t\t]\n\t\t/StyleSheetSet [\n\t\t<<\n\t\t\t/Name (\xfe\xff\x00N\x00o\x00r\x00m\x00a\x00l\x00 \x00R\x00G\x00B)\n\t\t\t/StyleSheetData\n\t\t\t<<\n\t\t\t\t/Font 2\n\t\t\t\t/FontSize 12.0\n\t\t\t\t/FauxBold false\n\t\t\t\t/FauxItalic false\n\t\t\t\t/AutoLeading true\n\t\t\t\t/Leading 0.0\n\t\t\t\t/HorizontalScale 1.0\n\t\t\t\t/VerticalScale 1.0\n\t\t\t\t/Tracking 0\n\t\t\t\t/AutoKerning true\n\t\t\t\t/Kerning 0\n\t\t\t\t/BaselineShift 0.0\n\t\t\t\t/FontCaps 0\n\t\t\t\t/FontBaseline 0\n\t\t\t\t/Underline false\n\t\t\t\t/Strikethrough false\n\t\t\t\t/Ligatures true\n\t\t\t\t/DLigatures false\n\t\t\t\t/BaselineDirection 2\n\t\t\t\t/Tsume 0.0\n\t\t\t\t/StyleRunAlignment 2\n\t\t\t\t/Language 0\n\t\t\t\t/NoBreak false\n\t\t\t\t/FillColor\n\t\t\t\t<<\n\t\t\t\t\t/Type 1\n\t\t\t\t\t/Values [ 1.0 0.0 0.0 0.0 ]\n\t\t\t\t>>\n\t\t\t\t/StrokeColor\n\t\t\t\t<<\n\t\t\t\t\t/Type 1\n\t\t\t\t\t/Values [ 1.0 0.0 0.0 0.0 ]\n\t\t\t\t>>\n\t\t\t\t/FillFlag true\n\t\t\t\t/StrokeFlag false\n\t\t\t\t/FillFirst true\n\t\t\t\t/YUnderline 1\n\t\t\t\t/OutlineWidth 1.0\n\t\t\t\t/CharacterDirection 0\n\t\t\t\t/HindiNumbers false\n\t\t\t\t/Kashida 1\n\t\t\t\t/DiacriticPos 2\n\t\t\t>>\n\t\t>>\n\t\t]\n\t\t/FontSet [\n\t\t<<\n\t\t\t/Name (\xfe\xff\x00F\x00u\x00t\x00u\x00r\x00a\x00-\x00C\x00o\x00n\x00d\x00e\x00n\x00s\x00e\x00d\x00M\x00e\x00d\x00i\x00u\x00m)\n\t\t\t/Script 0\n\t\t\t/FontType 1\n\t\t\t/Synthetic 0\n\t\t>>\n\t\t<<\n\t\t\t/Name (\xfe\xff\x00A\x00d\x00o\x00b\x00e\x00I\x00n\x00v\x00i\x00s\x00F\x00o\x00n\x00t)\n\t\t\t/Script 0\n\t\t\t/FontType 0\n\t\t\t/Synthetic 0\n\t\t>>\n\t\t<<\n\t\t\t/Name (\xfe\xff\x00M\x00y\x00r\x00i\x00a\x00d\x00P\x00r\x00o\x00-\x00R\x00e\x00g\x00u\x00l\x00a\x00r)\n\t\t\t/Script 0\n\t\t\t/FontType 0\n\t\t\t/Synthetic 0\n\t\t>>\n\t\t]\n\t\t/SuperscriptSize .583\n\t\t/SuperscriptPosition .333\n\t\t/SubscriptSize .583\n\t\t/SubscriptPosition .333\n\t\t/SmallCapSize .7\n\t>>\n\t/DocumentResources\n\t<<\n\t\t/KinsokuSet [\n\t\t<<\n\t\t\t/Name (\xfe\xff\x00P\x00h\x00o\x00t\x00o\x00s\x00h\x00o\x00p\x00K\x00i\x00n\x00s\x00o\x00k\x00u\x00H\x00a\x00r\x00d)\n\t\t\t/NoStart (\xfe\xff0\x010\x02\xff\x0c\xff\x0e0\xfb\xff\x1a\xff\x1b\xff\x1f\xff\x010\xfc \x15 \x19 \x1d\xff\t0\x15\xff=\xff]0\t0\x0b0\r0\x0f0\x110\xfd0\xfe0\x9d0\x9e0\x050A0C0E0G0I0c0\x830\x850\x870\x8e0\xa10\xa30\xa50\xa70\xa90\xc30\xe30\xe50\xe70\xee0\xf50\xf60\x9b0\x9c\x00?\x00!\x00\\)\x00]\x00}\x00,\x00.\x00:\x00;!\x03!\t\x00\xa2\xff\x05 0)\n\t\t\t/NoEnd (\xfe\xff \x18 \x1c\xff\x080\x14\xff;\xff[0\x080\n0\x0c0\x0e0\x10\x00\\(\x00[\x00{\xff\xe5\xff\x04\x00\xa3\xff \x00\xa70\x12\xff\x03)\n\t\t\t/Keep (\xfe\xff \x15 %)\n\t\t\t/Hanging (\xfe\xff0\x010\x02\x00.\x00,)\n\t\t>>\n\t\t<<\n\t\t\t/Name (\xfe\xff\x00P\x00h\x00o\x00t\x00o\x00s\x00h\x00o\x00p\x00K\x00i\x00n\x00s\x00o\x00k\x00u\x00S\x00o\x00f\x00t)\n\t\t\t/NoStart (\xfe\xff0\x010\x02\xff\x0c\xff\x0e0\xfb\xff\x1a\xff\x1b\xff\x1f\xff\x01 \x19 \x1d\xff\t0\x15\xff=\xff]0\t0\x0b0\r0\x0f0\x110\xfd0\xfe0\x9d0\x9e0\x05)\n\t\t\t/NoEnd (\xfe\xff \x18 \x1c\xff\x080\x14\xff;\xff[0\x080\n0\x0c0\x0e0\x10)\n\t\t\t/Keep (\xfe\xff \x15 %)\n\t\t\t/Hanging (\xfe\xff0\x010\x02\x00.\x00,)\n\t\t>>\n\t\t]\n\t\t/MojiKumiSet [\n\t\t<<\n\t\t\t/InternalName (\xfe\xff\x00P\x00h\x00o\x00t\x00o\x00s\x00h\x00o\x00p\x006\x00M\x00o\x00j\x00i\x00K\x00u\x00m\x00i\x00S\x00e\x00t\x001)\n\t\t>>\n\t\t<<\n\t\t\t/InternalName (\xfe\xff\x00P\x00h\x00o\x00t\x00o\x00s\x00h\x00o\x00p\x006\x00M\x00o\x00j\x00i\x00K\x00u\x00m\x00i\x00S\x00e\x00t\x002)\n\t\t>>\n\t\t<<\n\t\t\t/InternalName (\xfe\xff\x00P\x00h\x00o\x00t\x00o\x00s\x00h\x00o\x00p\x006\x00M\x00o\x00j\x00i\x00K\x00u\x00m\x00i\x00S\x00e\x00t\x003)\n\t\t>>\n\t\t<<\n\t\t\t/InternalName (\xfe\xff\x00P\x00h\x00o\x00t\x00o\x00s\x00h\x00o\x00p\x006\x00M\x00o\x00j\x00i\x00K\x00u\x00m\x00i\x00S\x00e\x00t\x004)\n\t\t>>\n\t\t]\n\t\t/TheNormalStyleSheet 0\n\t\t/TheNormalParagraphSheet 0\n\t\t/ParagraphSheetSet [\n\t\t<<\n\t\t\t/Name (\xfe\xff\x00N\x00o\x00r\x00m\x00a\x00l\x00 \x00R\x00G\x00B)\n\t\t\t/DefaultStyleSheet 0\n\t\t\t/Properties\n\t\t\t<<\n\t\t\t\t/Justification 0\n\t\t\t\t/FirstLineIndent 0.0\n\t\t\t\t/StartIndent 0.0\n\t\t\t\t/EndIndent 0.0\n\t\t\t\t/SpaceBefore 0.0\n\t\t\t\t/SpaceAfter 0.0\n\t\t\t\t/AutoHyphenate true\n\t\t\t\t/HyphenatedWordSize 6\n\t\t\t\t/PreHyphen 2\n\t\t\t\t/PostHyphen 2\n\t\t\t\t/ConsecutiveHyphens 8\n\t\t\t\t/Zone 36.0\n\t\t\t\t/WordSpacing [ .8 1.0 1.33 ]\n\t\t\t\t/LetterSpacing [ 0.0 0.0 0.0 ]\n\t\t\t\t/GlyphSpacing [ 1.0 1.0 1.0 ]\n\t\t\t\t/AutoLeading 1.2\n\t\t\t\t/LeadingType 0\n\t\t\t\t/Hanging false\n\t\t\t\t/Burasagari false\n\t\t\t\t/KinsokuOrder 0\n\t\t\t\t/EveryLineComposer false\n\t\t\t>>\n\t\t>>\n\t\t]\n\t\t/StyleSheetSet [\n\t\t<<\n\t\t\t/Name (\xfe\xff\x00N\x00o\x00r\x00m\x00a\x00l\x00 \x00R\x00G\x00B)\n\t\t\t/StyleSheetData\n\t\t\t<<\n\t\t\t\t/Font 2\n\t\t\t\t/FontSize 12.0\n\t\t\t\t/FauxBold false\n\t\t\t\t/FauxItalic false\n\t\t\t\t/AutoLeading true\n\t\t\t\t/Leading 0.0\n\t\t\t\t/HorizontalScale 1.0\n\t\t\t\t/VerticalScale 1.0\n\t\t\t\t/Tracking 0\n\t\t\t\t/AutoKerning true\n\t\t\t\t/Kerning 0\n\t\t\t\t/BaselineShift 0.0\n\t\t\t\t/FontCaps 0\n\t\t\t\t/FontBaseline 0\n\t\t\t\t/Underline false\n\t\t\t\t/Strikethrough false\n\t\t\t\t/Ligatures true\n\t\t\t\t/DLigatures false\n\t\t\t\t/BaselineDirection 2\n\t\t\t\t/Tsume 0.0\n\t\t\t\t/StyleRunAlignment 2\n\t\t\t\t/Language 0\n\t\t\t\t/NoBreak false\n\t\t\t\t/FillColor\n\t\t\t\t<<\n\t\t\t\t\t/Type 1\n\t\t\t\t\t/Values [ 1.0 0.0 0.0 0.0 ]\n\t\t\t\t>>\n\t\t\t\t/StrokeColor\n\t\t\t\t<<\n\t\t\t\t\t/Type 1\n\t\t\t\t\t/Values [ 1.0 0.0 0.0 0.0 ]\n\t\t\t\t>>\n\t\t\t\t/FillFlag true\n\t\t\t\t/StrokeFlag false\n\t\t\t\t/FillFirst true\n\t\t\t\t/YUnderline 1\n\t\t\t\t/OutlineWidth 1.0\n\t\t\t\t/CharacterDirection 0\n\t\t\t\t/HindiNumbers false\n\t\t\t\t/Kashida 1\n\t\t\t\t/DiacriticPos 2\n\t\t\t>>\n\t\t>>\n\t\t]\n\t\t/FontSet [\n\t\t<<\n\t\t\t/Name (\xfe\xff\x00F\x00u\x00t\x00u\x00r\x00a\x00-\x00C\x00o\x00n\x00d\x00e\x00n\x00s\x00e\x00d\x00M\x00e\x00d\x00i\x00u\x00m)\n\t\t\t/Script 0\n\t\t\t/FontType 1\n\t\t\t/Synthetic 0\n\t\t>>\n\t\t<<\n\t\t\t/Name (\xfe\xff\x00A\x00d\x00o\x00b\x00e\x00I\x00n\x00v\x00i\x00s\x00F\x00o\x00n\x00t)\n\t\t\t/Script 0\n\t\t\t/FontType 0\n\t\t\t/Synthetic 0\n\t\t>>\n\t\t<<\n\t\t\t/Name (\xfe\xff\x00M\x00y\x00r\x00i\x00a\x00d\x00P\x00r\x00o\x00-\x00R\x00e\x00g\x00u\x00l\x00a\x00r)\n\t\t\t/Script 0\n\t\t\t/FontType 0\n\t\t\t/Synthetic 0\n\t\t>>\n\t\t]\n\t\t/SuperscriptSize .583\n\t\t/SuperscriptPosition .333\n\t\t/SubscriptSize .583\n\t\t/SubscriptPosition .333\n\t\t/SmallCapSize .7\n\t>>\n>>'
    getFontAndColorDict(propDict,testData)
    print(propDict)

if __name__ == "__main__":
    main()