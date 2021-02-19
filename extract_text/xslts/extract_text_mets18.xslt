<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exsl="http://exslt.org/common"
  xmlns:math="http://exslt.org/math"
  extension-element-prefixes="exsl"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:mets="http://www.loc.gov/METS/"
  xmlns:mods="http://www.loc.gov/mods/v3"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

  <xsl:include href="extract_text_common.xslt"/>

  <xsl:template match="/">
    <xsl:apply-templates select="/mets:mets" />
  </xsl:template>

  <xsl:key name="page_doc_area" match="/doc/alto/Layout//ComposedBlock|doc/alto/Layout//TextBlock" use="@ID" />
  <xsl:key name="smLocatorLink_href" match="/mets:mets/mets:structLink/mets:smLinkGrp/mets:smLocatorLink" use="@xlink:href" />
  <xsl:key name="smLocatorLink_label" match="/mets:mets/mets:structLink/mets:smLinkGrp/mets:smLocatorLink" use="@xlink:label" />
  <xsl:key name="structMap" match="/mets:mets/mets:structMap[@TYPE='PHYSICAL']//mets:div" use="@ID" />

  <xsl:template match="/mets:mets">
    <xsl:variable name="page_docs_rt">
      <xsl:for-each select="mets:fileSec//mets:fileGrp[@USE='Fulltext']/mets:file">
        <doc>
          <xsl:attribute name="ID"><xsl:value-of select="@ID" /></xsl:attribute>
          <xsl:variable name="fileloc2"><xsl:value-of select="$input_path" />/<xsl:value-of select="mets:FLocat/@xlink:href" /></xsl:variable>
          <xsl:copy-of select="document($fileloc2)" />
        </doc>
      </xsl:for-each>
    </xsl:variable>

    <xsl:variable name="page_docs" select="exsl:node-set($page_docs_rt)" />

    <xsl:for-each select="mets:structMap[@TYPE='LOGICAL']/mets:div">
      <xsl:variable name="issue_DMDID" select="@DMDID" />
      <xsl:for-each select="mets:div">
        <xsl:variable name="item_ID" select="@ID" />
        <xsl:variable name="item_ID_hash">#<xsl:value-of select="$item_ID" /></xsl:variable>
        <xsl:variable name="item_DMDID" select="@DMDID" />

        <xsl:variable name="item_page_areas_rt">
          <xsl:for-each select="key('smLocatorLink_href', $item_ID_hash)/../mets:smArcLink/@xlink:to">
            <xsl:variable name="pagearea" select="key('smLocatorLink_label', .)/@xlink:href" />
            <xsl:variable name="pagearea_unhash" select="substring($pagearea, 2)" />
            <xsl:variable name="key_out" select="key('structMap', $pagearea_unhash)" />
            <xsl:for-each select="$key_out[@TYPE='pagearea']|$key_out/mets:div[@TYPE='pagearea']">
              <xsl:if test="mets:fptr/mets:area[@BETYPE='IDREF']">
                <xsl:variable name="pagearea_sub" select="@ID" />
                <xsl:for-each select="$page_docs">
                  <xsl:copy-of select="key('page_doc_area', $pagearea_sub)" />
                </xsl:for-each>
              </xsl:if>
            </xsl:for-each>
          </xsl:for-each>
        </xsl:variable>

        <xsl:variable name="item_page_areas" select="exsl:node-set($item_page_areas_rt)" />

        <exsl:document method="text" href="{$output_path}_{$item_ID}.txt">
          <xsl:choose>
            <xsl:when test="$item_page_areas//String|$item_page_areas//HYP">
              <xsl:for-each select="$item_page_areas//TextBlock">
                <xsl:apply-templates select="TextLine" />
                <xsl:if test="position()!=last()">
                  <xsl:text>&#xA;</xsl:text>
                </xsl:if>
              </xsl:for-each>
            </xsl:when>
            <xsl:otherwise>
              <xsl:text>&#xA;</xsl:text>
            </xsl:otherwise>
          </xsl:choose>
        </exsl:document>

        <xsl:variable name="item_word_confidences_rt">
          <xsl:for-each select="$item_page_areas//String/@WC">
            <w><xsl:value-of select="." /></w>
          </xsl:for-each>
        </xsl:variable>

        <xsl:variable name="item_word_confidences" select="exsl:node-set($item_word_confidences_rt)" />

        <xsl:variable name="word_count" select="count($item_word_confidences/w)" />
        <xsl:variable name="ocr_quality_sum" select="sum($item_word_confidences/w)" />
        <xsl:variable name="ocr_quality_mean" select="$ocr_quality_sum div $word_count" />

        <xsl:variable name="standard_deviation_square_and_mean_rt">
          <xsl:for-each select="$item_word_confidences/w">
            <w><xsl:value-of select="math:power(. - $ocr_quality_mean, 2)" /></w>
          </xsl:for-each>
        </xsl:variable>

        <xsl:variable name="standard_deviation_square_and_mean" select="exsl:node-set($standard_deviation_square_and_mean_rt)" />

        <xsl:variable name="standard_deviation" select="math:sqrt(sum($standard_deviation_square_and_mean/w) div $word_count)" />

        <exsl:document method="xml" href="{$output_path}_{$item_ID}_metadata.xml" indent="yes">
          <lwm>
            <process>
              <xsl:copy-of select="$lwm_tool" />
              <source_type>newspaper</source_type>
              <xml_flavour>alto</xml_flavour>
              <software><xsl:value-of select="/mets:mets/mets:metsHdr/mets:agent[@OTHERTYPE='SOFTWARE']/mets:name" /></software>
              <input_sub_path><xsl:value-of select="$input_sub_path" /></input_sub_path>
              <input_filename><xsl:value-of select="$input_filename" /></input_filename>
              <mets_namespace><xsl:value-of select="/mets:mets/@xsi:schemaLocation" /></mets_namespace>
              <alto_namespace><xsl:value-of select="$page_docs/doc[1]/alto/@xsi:noNamespaceSchemaLocation" /></alto_namespace>
            </process>
            <publication>
              <xsl:attribute name="id"><xsl:value-of select="/mets:mets/mets:dmdSec[@ID=$issue_DMDID]//mods:mods/mods:relatedItem/mods:identifier" /></xsl:attribute>
              <source><xsl:value-of select="/mets:mets/mets:dmdSec[@ID=$issue_DMDID]//mods:note" /></source>
              <title><xsl:value-of select="/mets:mets/mets:dmdSec[@ID=$issue_DMDID]//mods:title" /></title>
              <location><xsl:value-of select="/mets:mets/mets:dmdSec[@ID=$issue_DMDID]//mods:placeTerm" /></location>
              <issue>
                <xsl:choose>
                  <xsl:when test="/mets:mets/mets:dmdSec[@ID=$issue_DMDID]//mods:mods/mods:part//mods:number != ''" >
                    <xsl:attribute name="id"><xsl:value-of select="/mets:mets/mets:dmdSec[@ID=$issue_DMDID]//mods:mods/mods:part//mods:number" /></xsl:attribute>
                  </xsl:when>
                  <xsl:otherwise>
                    <!-- If missing then use date as issue ID -->
                    <xsl:attribute name="id"><xsl:value-of select="/mets:mets/mets:dmdSec[@ID=$issue_DMDID]//mods:dateIssued" /></xsl:attribute>
                  </xsl:otherwise>
     	        </xsl:choose>
                <date><xsl:value-of select="/mets:mets/mets:dmdSec[@ID=$issue_DMDID]//mods:dateIssued" /></date>
                <item>
                  <xsl:attribute name="id"><xsl:value-of select="$item_ID" /></xsl:attribute>
                  <plain_text_file><xsl:value-of select="$output_document_stub" />_<xsl:value-of select="$item_ID" />.txt</plain_text_file>
                  <title><xsl:value-of select="/mets:mets/mets:dmdSec[@ID=$item_DMDID]//mods:title" /></title>
                  <item_type><xsl:value-of select="@TYPE" /></item_type>
                  <word_count><xsl:value-of select="format-number(($word_count), '0')" /></word_count>
                  <!-- ocr_quality summary -->
                  <ocr_quality_mean>
                    <xsl:if test="number($ocr_quality_mean) = number($ocr_quality_mean)">
                      <xsl:value-of select="format-number($ocr_quality_mean, '0.0000')" />
                    </xsl:if>
                  </ocr_quality_mean>
                  <ocr_quality_sd>
                    <xsl:if test="number($standard_deviation) = number($standard_deviation)">
                      <xsl:value-of select="format-number($standard_deviation, '0.0000')" />
                    </xsl:if>
                  </ocr_quality_sd>
                </item>
              </issue>
            </publication>
          </lwm>
        </exsl:document>

      </xsl:for-each>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="TextLine">
    <xsl:apply-templates select="String|HYP|SP" />
    <xsl:text>&#xA;</xsl:text>
  </xsl:template>

  <xsl:template match="String|HYP">
    <xsl:value-of select="@CONTENT" />
  </xsl:template>

  <xsl:template match="SP">
    <xsl:if test="position()!=last()">
      <xsl:text> </xsl:text>
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>
