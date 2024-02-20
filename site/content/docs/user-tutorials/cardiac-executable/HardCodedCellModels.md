---
title: "Hardcoded cell model options"
draft: false
layout: "single"
images: []
---

The hardcoded cell models are listed in the schema (.xsd) file, which should be present in any folder containing an xml parameters file.

In `ChasteParameters_2_0.xsd`, onwards the hardcoded cell models are

```

#!xml
<xs:enumeration value="DifrancescoNoble"/>
<xs:enumeration value="FaberRudy2000"/>
<xs:enumeration value="FaberRudy2000Optimised"/>
<xs:enumeration value="Fox2002BackwardEuler"/>
<xs:enumeration value="HodgkinHuxley"/>
<xs:enumeration value="LuoRudyI"/>
<xs:enumeration value="LuoRudyIBackwardEuler"/>
<xs:enumeration value="MahajanShiferaw"/>
<xs:enumeration value="Maleckar"/>
<xs:enumeration value="tenTusscher2006"/>

```


In `ChasteParameters_3_1.xsd`, onwards the hardcoded cell models are

```

#!xml
<xs:enumeration value="DifrancescoNoble"/>
<xs:enumeration value="FaberRudy2000"/>
<xs:enumeration value="FaberRudy2000Optimised"/>
<xs:enumeration value="Fox2002"/>
<xs:enumeration value="Fox2002BackwardEuler"/>
<xs:enumeration value="HodgkinHuxley"/>
<xs:enumeration value="LuoRudyI"/>
<xs:enumeration value="LuoRudyIBackwardEuler"/>
<xs:enumeration value="MahajanShiferaw"/>
<xs:enumeration value="MahajanShiferawBackwardEuler"/>
<xs:enumeration value="Maleckar"/>
<xs:enumeration value="tenTusscher2006"/>
<xs:enumeration value="tenTusscher2006BackwardEuler"/>

```

