<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exsl="http://exslt.org/common"
  extension-element-prefixes="exsl"
  xmlns:ukp="http://tempuri.org/ncbpissue"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

  <!-- Metadata about plaintext extraction code -->
  <xsl:param name="name">alto2txt</xsl:param>
  <xsl:param name="version">0.3.4</xsl:param>
  <xsl:param name="source">https://github.com/Living-with-machines/alto2txt</xsl:param>
  <xsl:variable name="lwm_tool">
    <lwm_tool>
      <name><xsl:value-of select="$name" /></name>
      <version><xsl:value-of select="$version" /></version>
      <source><xsl:value-of select="$source" /></source>
    </lwm_tool>
  </xsl:variable>

  <!-- Input parameters to be set by caller -->
  <xsl:param name="input_path" />
  <xsl:param name="input_sub_path" />
  <xsl:param name="input_filename" />
  <xsl:param name="output_document_stub" />
  <xsl:param name="output_path" />

  <xsl:output method="text" />

</xsl:stylesheet>
