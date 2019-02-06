''' Runing the application
spark-submit --packages com.databricks:spark-xml_2.11:0.5.0 dataframes_issues.py
'''
from pyspark import SparkContext  # pylint: disable=import-error
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.functions import  explode

context = SparkContext(appName="text")
sqlContext = SQLContext(context)
spark = SparkSession.builder.getOrCreate()

####### Option 1 ##### 
print(" ----> Option 1- Loading article element and subelement. Article_Text and Titlte_Text in two different columns\n")
print("\n")
print("\n")
df_article = spark.read.format("com.databricks.spark.xml").options(rowTag='article').load('/Users/rosafilgueira/EPCC/ATI-SE/LwM/test.xml')
df_article.printSchema()
df_text=df_article.select("text.*")
df_text=df_text.withColumnRenamed("text.cr", "cr").withColumnRenamed("text.title", "title")
df_text=df_text.select("cr", "title.p.wd._VALUE")
df_text=df_text.withColumnRenamed("_VALUE", "Title_Text")
df_text=df_text.withColumn('cr',explode('cr'))
df_text=df_text.select("cr.p.wd", "Title_Text")
df_text=df_text.withColumn('wd',explode('wd'))
df_text=df_text.select("wd._VALUE", "Title_Text")
df_text=df_text.withColumnRenamed('_VALUE',"Article_Text")
df_text.show()
df_text.printSchema()

#### Option 2 ####### 
print(" -----> Option 2- Loading text element and subelements. Article_Text and Title_Tex in two different columns \n")
print("\n")
print("\n")
df_text = spark.read.format("com.databricks.spark.xml").options(rowTag='text').load('/Users/rosafilgueira/EPCC/ATI-SE/LwM/test.xml')
df_text.printSchema()
df_text=df_text.withColumnRenamed("text.cr", "cr").withColumnRenamed("text.title", "title")
df_text=df_text.select("cr", "title.p.wd._VALUE")
df_text=df_text.withColumnRenamed("_VALUE", "Title_Text")
df_text=df_text.withColumn('cr',explode('cr'))
df_text=df_text.select("cr.p.wd", "Title_Text")
df_text=df_text.withColumn('wd',explode('wd'))
df_text=df_text.select("wd._VALUE", "Title_Text")
df_text=df_text.withColumnRenamed('_VALUE',"Article_Text")
df_text.show()
df_text.printSchema()
df_text.registerTempTable("XMLtable")
sqlContext.sql("select * from XMLtable").show()

##### Option 3 ######### Text from Title and Paragraph are mixed
print(" ----> Option 3- Loading p element and subelements. Article_Text and Title_Tex in the same column as Total_Article_Text \n")
print("\n")
print("\n")
df_paragraph = spark.read.format("com.databricks.spark.xml").options(rowTag='p').load('/Users/rosafilgueira/EPCC/ATI-SE/LwM/test.xml')
df_paragraph.printSchema()
df_paragraph=df_paragraph.select('wd._VALUE')
df_paragraph=df_paragraph.withColumnRenamed('_VALUE',"Total_Article_Text")
df_paragraph.show()
df_paragraph.printSchema()
