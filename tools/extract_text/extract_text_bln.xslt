<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exsl="http://exslt.org/common"
  extension-element-prefixes="exsl"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

  <xsl:include href="extract_text_common.xslt"/>

  <xsl:template match="/">
    <xsl:apply-templates select="/BL_newspaper/BL_article" />
  </xsl:template>

  <xsl:template match="BL_newspaper/BL_article">
    <exsl:document method="text" href="{$output_path}.txt">
      <xsl:apply-templates select="image_metadata/articleImage/articleText/articleWord" />
     <xsl:text>&#xA;</xsl:text>
    </exsl:document>

    <exsl:document method="xml" href="{$output_path}_metadata.xml" indent="yes">
      <lwm>
        <process>
          <xsl:copy-of select="$lwm_tool" />
          <source_type>newspaper</source_type>
          <xml_flavour>bln</xml_flavour>
          <software><xsl:value-of select="article_metadata/additional_metadata/conversionCredit" /></software>
          <input_sub_path><xsl:value-of select="$input_sub_path" /></input_sub_path>
          <input_filename><xsl:value-of select="$input_filename" /></input_filename>
          <!-- namespaces -->
        </process>
        <publication>
          <xsl:attribute name="id"><xsl:value-of select="title_metadata/titleAbbreviation" /></xsl:attribute>
          <title><xsl:value-of select="title_metadata/title" /></title>
          <location><xsl:value-of select="title_metadata/placeOfPublication" /></location>
          <issue>
            <xsl:attribute name="id"><xsl:value-of select="issue_metadata/issueNumber" /></xsl:attribute>
            <date><xsl:value-of select="translate(issue_metadata/normalisedDate, '.', '-')" /></date>
            <item>
              <xsl:attribute name="id"><xsl:value-of select="image_metadata/pageImage/pageSequence" /></xsl:attribute>
              <plain_text_file><xsl:value-of select="$output_document_stub" />.txt</plain_text_file>
              <title><xsl:value-of select="article_metadata/dc_metadata/dc:Title" /></title>
              <!-- item_type -->
              <word_count><xsl:value-of select="format-number(count(image_metadata/articleImage/articleText/articleWord), '0')" /></word_count>
              <!-- ocr_quality stats -->
              <ocr_quality_summary><xsl:value-of select="issue_metadata/qualityRating" /></ocr_quality_summary>
            </item>
          </issue>
        </publication>
      </lwm>
    </exsl:document>
  </xsl:template>

  <xsl:template match="articleWord">
    <xsl:value-of select="." />
    <xsl:if test="position()!=last()">
      <xsl:choose>
        <xsl:when test="position() mod 10 = 0">
          <xsl:text>&#xA;</xsl:text>
        </xsl:when>
          <xsl:otherwise>
            <xsl:text> </xsl:text>
          </xsl:otherwise>
      </xsl:choose>
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>
