<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<!-- This variable holds the table name and is modified by converter script -->
<xsl:variable name="table">TABLE</xsl:variable>
<xsl:template match="RESULTS">
  <!-- dataset is the root element -->
  <xsl:element name="dataset">
    <xsl:text>&#10;</xsl:text>

    <!-- one table row per line -->
    <xsl:for-each select="ROW">
      <xsl:element name="{$table}">
        <xsl:for-each select="COLUMN">
           <xsl:attribute name="{@NAME}">
             <xsl:value-of select="."/>
           </xsl:attribute>
        </xsl:for-each>
      </xsl:element>
      <xsl:text>&#10;</xsl:text>
    </xsl:for-each>

  </xsl:element>
</xsl:template>
</xsl:stylesheet>
