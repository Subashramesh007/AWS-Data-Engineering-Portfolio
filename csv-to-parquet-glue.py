IAM -> Create role -> Glue service -> AWSGlueServiceRole -> Glue-role-demo
S3-> Create csv source folder(actions-query s3 select), create parquet target folder
Glue Data catalog -> Create database glue_db_demo -> location - source S3 URI
Tables -> custom crawler glue_demo9583-> Config.S3 source path -> IAM role-Glue-demo -> Target db- Glue_db_demo -> on-demand schedule -> create & run - check in Glue_db_demo
glue studio -> blank canvas -> Source- data catalog -db& table -> Transform-apply mapping -> Target-parquet,uncom,target folder-> script-> job name&iam role -> run
target folder -> file with S3 query select - viewing format csv

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as SqlFuncs

def sparkAggregate(glueContext, parentFrame, groups, aggs, transformation_ctx) -> DynamicFrame:
    aggsFuncs = []
    for column, func in aggs:
        aggsFuncs.append(getattr(SqlFuncs, func)(column))
    result = parentFrame.toDF().groupBy(*groups).agg(*aggsFuncs) if len(groups) > 0 else parentFrame.toDF().agg(*aggsFuncs)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1750678632487 = glueContext.create_dynamic_frame.from_catalog(database="glue_db_demo", table_name="annual_enterprise_survey_2023_financial_year_provisional_csv", transformation_ctx="AWSGlueDataCatalog_node1750678632487")

# Script generated for node Aggregate
Aggregate_node1750680500411 = sparkAggregate(glueContext, parentFrame = AWSGlueDataCatalog_node1750678632487, groups = ["year"], aggs = [["value", "max"]], transformation_ctx = "Aggregate_node1750680500411")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=Aggregate_node1750680500411, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1750678596555", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1750679856310 = glueContext.write_dynamic_frame.from_options(frame=Aggregate_node1750680500411, connection_type="s3", format="glueparquet", connection_options={"path": "s3://glue-files9583/target-files/", "partitionKeys": []}, format_options={"compression": "uncompressed"}, transformation_ctx="AmazonS3_node1750679856310")

job.commit()