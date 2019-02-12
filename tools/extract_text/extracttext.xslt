<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:exsl="http://exslt.org/common" extension-element-prefixes="exsl"
xmlns:dc="http://purl.org/dc/elements/1.1/">
<xsl:output method="text" omit-xml-declaration="yes" indent="no" />
<xsl:param name="pagefilename" />

<xsl:template match="/">
  <xsl:apply-templates select="/alto" />
  <xsl:apply-templates select="/BL_newspaper/BL_article" />
</xsl:template>

<xsl:template match="alto">
  <xsl:for-each select="//TextBlock">
    <exsl:document method="text" href="{$pagefilename}_{@ID}.txt">
      <xsl:apply-templates select=".//String" />
    </exsl:document>
  </xsl:for-each>
<xsl:text>type: alto
</xsl:text>
</xsl:template>

<xsl:template match="String">
  <xsl:value-of select="@CONTENT" /><xsl:text> </xsl:text>
</xsl:template>

<xsl:template match="BL_newspaper/BL_article">
  <exsl:document method="text" href="{$pagefilename}.txt">
    <xsl:apply-templates select=".//articleWord" />
  </exsl:document>
<xsl:text>type: BL_newspaper
</xsl:text>
<xsl:text>title: </xsl:text><xsl:value-of select="//normalisedTitle/text()" /><xsl:text>
</xsl:text>
<xsl:text>date: </xsl:text><xsl:value-of select="//normalisedDate/text()" /><xsl:text>
</xsl:text>
<xsl:text>article_title: </xsl:text><xsl:value-of select="//dc:Title/text()" /><xsl:text>
</xsl:text>
</xsl:template>

<xsl:template match="articleWord">
  <xsl:value-of select="text()" /><xsl:text> </xsl:text>
</xsl:template>

</xsl:stylesheet>
