<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exsl="http://exslt.org/common"
  extension-element-prefixes="exsl"
  xmlns:ukp="http://tempuri.org/ncbpissue"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

  <xsl:include href="extract_text_common.xslt"/>

  <xsl:template match="/">
    <xsl:apply-templates select="/ukp:UKP/ukp:Periodical/ukp:issue" />
  </xsl:template>

  <xsl:template match="/ukp:UKP/ukp:Periodical/ukp:issue" >
    <xsl:apply-templates select="ukp:page/ukp:article" >
      <xsl:with-param name="issue_id"><xsl:value-of select="ukp:id" /></xsl:with-param>
      <xsl:with-param name="issue_number"><xsl:value-of select="ukp:is" /></xsl:with-param>
      <xsl:with-param name="issue_volume"><xsl:value-of select="ukp:volNum" /></xsl:with-param>
      <xsl:with-param name="issue_date"><xsl:value-of select="ukp:pf" /></xsl:with-param>
    </xsl:apply-templates>
  </xsl:template>

  <xsl:template match="ukp:page/ukp:article">
    <xsl:param name="issue_id" />
    <xsl:param name="issue_number" />
    <xsl:param name="issue_volume" />
    <xsl:param name="issue_date" />
    <xsl:variable name="article_id"><xsl:value-of select="ukp:id" /></xsl:variable>
    <exsl:document method="text" href="{$output_path}-{$article_id}.txt">
      <xsl:apply-templates select="ukp:text/ukp:text.title/ukp:p/ukp:wd" />
      <xsl:text>&#xA;</xsl:text>
      <xsl:apply-templates select="ukp:text/ukp:text.preamble/ukp:p/ukp:wd" />
      <xsl:text>&#xA;</xsl:text>
      <xsl:apply-templates select="ukp:text/ukp:text.cr/ukp:p/ukp:wd" />
      <xsl:text>&#xA;</xsl:text>
    </exsl:document>
    <exsl:document method="xml" href="{$output_path}-{$article_id}_metadata.xml" indent="yes">
      <lwm>
        <process>
          <xsl:copy-of select="$lwm_tool" />
          <source_type>newspaper</source_type>
          <xml_flavour>ukp</xml_flavour>
          <input_sub_path><xsl:value-of select="$input_sub_path" /></input_sub_path>
          <input_filename><xsl:value-of select="$input_filename" /></input_filename>
        </process>
       <publication>
          <xsl:attribute name="id"></xsl:attribute>
          <title/>
          <location/>
          <issue>
            <xsl:attribute name="id"><xsl:value-of select="$issue_id" /></xsl:attribute>
            <number><xsl:value-of select="$issue_number" /></number>
            <volume><xsl:value-of select="$issue_volume" /></volume>
            <!-- Convert YYYYMMDD to YYYY-MM-DD -->
            <date><xsl:value-of select="concat(substring($issue_date, 1, 4), '-', substring($issue_date, 5, 2), '-', substring($issue_date, 7, 2))"/></date>
            <item>
              <xsl:attribute name="id"><xsl:value-of select="ukp:id" /></xsl:attribute>
              <plain_text_file><xsl:value-of select="$output_document_stub" />-<xsl:value-of select="$article_id" />.txt</plain_text_file>
              <title><xsl:value-of select="ukp:ti" /></title>
              <word_count><xsl:value-of select="format-number(count(ukp:text//ukp:wd), '0')" /></word_count>
              <ocr_quality><xsl:value-of select="ukp:ocr" /></ocr_quality>
            </item>
          </issue>
       </publication>
      </lwm>
    </exsl:document>
  </xsl:template>

  <xsl:template match="ukp:wd">
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
