''' Runing the application
spark-submit --packages com.databricks:spark-xml_2.11:0.5.0 dataframes_alto.py
'''

from pyspark import SparkContext  # pylint: disable=import-error
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.functions import  explode

import sys
reload(sys)
sys.setdefaultencoding('utf8')

context = SparkContext(appName="text")
sqlContext = SQLContext(context)
spark = SparkSession.builder.getOrCreate()

######## Metadata file ########
print("----> Loading the metadata.xml file\n")
metadata_info=spark.read.format("com.databricks.spark.xml").options(rowTag='xmlData').load('/Users/rosafilgueira/EPCC/ATI-SE/000051983_0_1-92pgs__568584_dat/000051983_metadata.xml')
metadata_info= metadata_info.select("MODS:mods.MODS:originInfo.*")
metadata_info.show()
metadata_info.printSchema()
publisher=metadata_info.select("MODS:publisher").collect()

########### Option 1 ############ Different Columns for different sections of text

print(" ---> Loading the alto element and subelements. Each section of text is stored in different columns\n")
print("\n")
print("\n")
ALTO_XPATH=spark.read.format("com.databricks.spark.xml").options(rowTag='alto').load('/Users/rosafilgueira/EPCC/ATI-SE/000051983_0_1-92pgs__568584_dat/ALTO/')
PAGE_XPATH=ALTO_XPATH.select("Layout.Page.*")
print("PAGE SCHEMA:\n")
PAGE_XPATH.printSchema()
print("PAGE DATAFRAME:\n")
PAGE_XPATH.show()

Page_info=PAGE_XPATH.select("PrintSpace.TextBlock.TextLine","_WIDTH", "_HEIGHT","TopMargin.TextBlock.TextLine.String._CONTENT", "_ID")
Page_info=Page_info.withColumnRenamed("_CONTENT", "PAGE_TopMargin_Text").withColumnRenamed("_WIDTH", "PAGE_WIDTH").withColumnRenamed("_HEIGHT", "PAGE_HEIGHT").withColumnRenamed("_ID", "PAGE_ID")
Page_info=Page_info.withColumn('TextLine',explode('TextLine')).withColumn('TextLine',explode('TextLine'))
Page_info = Page_info.select("TextLine.String._CONTENT", "PAGE_WIDTH", "PAGE_HEIGHT", "PAGE_TopMargin_Text", "PAGE_ID")
Page_info=Page_info.withColumnRenamed("_CONTENT", "PAGE_TextLine")
Page_info.printSchema()
print("NEW PAGE DATAFRAME- WITH ONLY THE INFO NECESARY ")
Page_info.show()

width=Page_info.select("PAGE_WIDTH").collect()
height=Page_info.select("PAGE_HEIGHT").collect()
topMargin=Page_info.select("PAGE_TopMargin_Text").collect()

for element in width:
   print element[0]

######### Option 2  ########## ALL the String._CONTENT in the same column
print(" ---> Loading the String element and subelements. All sections of text are stored in the same columns\n")
print("\n")
print("\n")
ALTO_XPATH=spark.read.format("com.databricks.spark.xml").options(rowTag='alto').load('/Users/rosafilgueira/EPCC/ATI-SE/000051983_0_1-92pgs__568584_dat/ALTO/')
STRINGS_XPATH= spark.read.format("com.databricks.spark.xml").options(rowTag='String').load('/Users/rosafilgueira/EPCC/ATI-SE/000051983_0_1-92pgs__568584_dat/ALTO/')
STIRNGS_XPATH=STRINGS_XPATH.withColumnRenamed("_CONTENT", "Total_Page_Text")
WORDS_XPATH=STIRNGS_XPATH.select("Total_Page_Text").collect()
page_words=''
for wd in WORDS_XPATH:
    page_words= page_words+ ' '+ wd[0]

print(" ---->Words in a Page %s" % page_words)


