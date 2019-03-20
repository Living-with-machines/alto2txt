<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:exsl="http://exslt.org/common"
xmlns:str="http://exslt.org/strings"
xmlns:math="http://exslt.org/math"
extension-element-prefixes="exsl str"
exclude-result-prefixes="str"
xmlns:dc="http://purl.org/dc/elements/1.1/"
xmlns:mets="http://www.loc.gov/METS/"
xmlns:mods="http://www.loc.gov/mods/v3"
xmlns:xlink="http://www.w3.org/1999/xlink"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<xsl:output method="text" />
<xsl:param name="input_path" />
<xsl:param name="input_sub_path" />
<xsl:param name="input_filename" />
<xsl:param name="output_document_stub" />

<xsl:template match="/">
  <xsl:apply-templates select="/mets:mets" />
  <xsl:apply-templates select="/BL_newspaper/BL_article" />
</xsl:template>

<xsl:template match="/mets:mets">
  <xsl:for-each select="mets:structMap[@TYPE='LOGICAL']/mets:div">
    <xsl:variable name="issue_DMDID"><xsl:value-of select="@DMDID"/></xsl:variable>
    <xsl:for-each select="mets:div">
      <xsl:variable name="item_ID"><xsl:value-of select="@ID"/></xsl:variable>
      <xsl:variable name="item_ID_hash">#<xsl:value-of select="$item_ID"/></xsl:variable>
      <xsl:variable name="item_DMDID"><xsl:value-of select="@DMDID"/></xsl:variable>
      <xsl:variable name="first_alto"><xsl:value-of select="$input_path" />/<xsl:value-of select="/mets:mets/mets:fileSec//mets:fileGrp[@USE='Fulltext']/mets:file[@MIMETYPE='text/xml']/mets:FLocat/@xlink:href" /></xsl:variable>

      <xsl:variable name="item_page_areas">
      <xsl:for-each select="/mets:mets/mets:structLink/mets:smLinkGrp/mets:smLocatorLink[@xlink:href=$item_ID_hash]/../mets:smArcLink">
        <xsl:variable name="link"><xsl:value-of select="@xlink:to" /></xsl:variable>
        <xsl:variable name="pagearea"><xsl:value-of select="../mets:smLocatorLink[@xlink:label=$link]/@xlink:href" /></xsl:variable>
        <xsl:variable name="pagearea_unhash"><xsl:value-of select="substring($pagearea, 2)" /></xsl:variable>
        <xsl:for-each select="/mets:mets/mets:structMap[@TYPE='PHYSICAL']//mets:div[@ID=$pagearea_unhash][@TYPE='pagearea']|/mets:mets/mets:structMap[@TYPE='PHYSICAL']//mets:div[@ID=$pagearea_unhash]//mets:div[@TYPE='pagearea']">
          <xsl:variable name="pagearea_sub"><xsl:value-of select="@ID" /></xsl:variable>
          <xsl:variable name="fileid"><xsl:value-of select="mets:fptr/mets:area[@BETYPE='IDREF']/@FILEID" /></xsl:variable>
          <!-- LABEL="Illustration" has no IDFEF -->
          <xsl:if test="$fileid != ''">
            <xsl:variable name ="fileref"><xsl:value-of select="/mets:mets/mets:fileSec//mets:file[@ID=$fileid]/mets:FLocat/@xlink:href" /></xsl:variable>
            <!--
            <xsl:variable name="filename">
              <xsl:value-of select="str:replace($fileref, 'file://./', '')" />
            </xsl:variable>
            -->
            <xsl:variable name="filename"><xsl:value-of select="$fileref" /></xsl:variable>
            <xsl:variable name="fileloc"><xsl:value-of select="$input_path" />/<xsl:value-of select="$filename" /></xsl:variable>
            <xsl:copy-of select="document($fileloc)/alto/Layout//*[@ID=$pagearea_sub]" />
          </xsl:if>
        </xsl:for-each>
      </xsl:for-each>
      </xsl:variable>

      <exsl:document method="text" href="{$output_document_stub}_{$item_ID}.txt">
        <xsl:for-each select="exsl:node-set($item_page_areas)//TextBlock">
          <xsl:apply-templates select="TextLine" />
          <xsl:if test="position()!=last()">
            <xsl:text>
</xsl:text>
          </xsl:if>
        </xsl:for-each>
      </exsl:document>

      <xsl:variable name="item_word_confidences">
        <xsl:for-each select="exsl:node-set($item_page_areas)//String/@WC">
          <wc><xsl:value-of select="." /></wc>
        </xsl:for-each>
      </xsl:variable>

      <xsl:variable name="word_count"><xsl:value-of select="count(exsl:node-set($item_word_confidences)/wc)" /></xsl:variable>
      <xsl:variable name="ocr_quality_sum"><xsl:value-of select="sum(exsl:node-set($item_word_confidences)/wc)" /></xsl:variable>
      <xsl:variable name="ocr_quality_mean"><xsl:value-of select="$ocr_quality_sum div $word_count" /></xsl:variable>

      <xsl:variable name="sub_mean_and_square">
        <xsl:for-each select="exsl:node-set($item_word_confidences)/wc">
          <wc><xsl:value-of select="math:power(. - $ocr_quality_mean, 2)" /></wc>
        </xsl:for-each>
      </xsl:variable>

      <xsl:variable name="standard_deviation">
        <xsl:value-of select="math:sqrt((sum(exsl:node-set($sub_mean_and_square)/wc)) div $word_count)"/>
      </xsl:variable>

      <exsl:document method="xml" href="{$output_document_stub}_{$item_ID}_metadata.xml" indent="yes">
        <lwm>
          <process>
            <lwm_tool>
              <name>extract_text</name>
              <version>0.1</version>
              <source>https://github.com/alan-turing-institute/Living-with-Machines-code</source>
            </lwm_tool>
            <source_type>newspaper</source_type>
            <xml_flavour>alto</xml_flavour>
            <input_sub_path><xsl:value-of select="$input_sub_path" /></input_sub_path>
            <input_filename><xsl:value-of select="$input_filename" /></input_filename>
            <mets_namespace><xsl:value-of select="/mets:mets/@xsi:schemaLocation" /></mets_namespace>
            <alto_namespace><xsl:value-of select="document($first_alto)/alto/@xsi:noNamespaceSchemaLocation" /></alto_namespace>
          </process>
          <publication>
            <xsl:attribute name="id"><xsl:value-of select="/mets:mets/mets:dmdSec[@ID=$issue_DMDID]//mods:mods/mods:relatedItem/mods:identifier" /></xsl:attribute>
            <title><xsl:value-of select="/mets:mets/mets:dmdSec[@ID=$issue_DMDID]//mods:title" /></title>
            <location><xsl:value-of select="/mets:mets/mets:dmdSec[@ID=$issue_DMDID]//mods:placeTerm" /></location>
            <issue>
              <xsl:attribute name="id"><xsl:value-of select="/mets:mets/mets:dmdSec[@ID=$issue_DMDID]//mods:mods/mods:part//mods:number" /></xsl:attribute>
              <date><xsl:value-of select="/mets:mets/mets:dmdSec[@ID=$issue_DMDID]//mods:dateIssued" /></date>
              <item>
                <xsl:attribute name="id"><xsl:value-of select="$item_ID" /></xsl:attribute>
                <plain_text_file><xsl:value-of select="$output_document_stub" />_<xsl:value-of select="$item_ID" />.txt</plain_text_file>
                <title><xsl:value-of select="/mets:mets/mets:dmdSec[@ID=$item_DMDID]//mods:title" /></title>
                <item_type><xsl:value-of select="@TYPE" /></item_type>
                <word_count><xsl:value-of select="format-number(($word_count), '0')" /></word_count>
                <ocr_quality_mean><xsl:value-of select="format-number($ocr_quality_mean, '0.0000')" /></ocr_quality_mean>
                <ocr_quality_sd><xsl:value-of select="format-number($standard_deviation, '0.0000')" /></ocr_quality_sd>
              </item>
            </issue>
          </publication>
        </lwm>
      </exsl:document>

    </xsl:for-each>
  </xsl:for-each>
</xsl:template>

<xsl:template match="TextLine">
  <xsl:for-each select="String|HYP">
    <xsl:value-of select="@CONTENT" />
    <xsl:if test="following-sibling::SP">
      <xsl:if test="position()!=last()">
        <xsl:text> </xsl:text>
      </xsl:if>
    </xsl:if>
  </xsl:for-each>
  <xsl:text>
</xsl:text>
</xsl:template>

<xsl:template match="BL_newspaper/BL_article">
  <exsl:document method="text" href="{$output_document_stub}.txt">
    <xsl:apply-templates select="image_metadata/articleImage/articleText/articleWord" />
    <xsl:text>
</xsl:text>
  </exsl:document>


  <exsl:document method="xml" href="{$output_document_stub}_metadata.xml" indent="yes">
    <lwm>
      <process>
        <lwm_tool>
          <name>extract_text</name>
          <version>0.1</version>
          <source>https://github.com/alan-turing-institute/Living-with-Machines-code</source>
        </lwm_tool>
        <source_type>newspaper</source_type>
        <xml_flavour>bln</xml_flavour>
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
      <xsl:when test="position() mod 10 = 0 ">
        <xsl:text>
</xsl:text>
      </xsl:when>
        <xsl:otherwise>
          <xsl:text> </xsl:text>
        </xsl:otherwise>
    </xsl:choose>
  </xsl:if>
</xsl:template>

</xsl:stylesheet>
