
# Import date class from datetime module
from datetime import datetime
from ReadConfig2 import getSQLCONFIG
import pyodbc
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine


configFilePath = r'C:\Users\akdmille\Documents\Python Files\configDEV72.ini'
flagNoIndex = False
flagHeap = False
global flagTableChanges
flagNoTableSpecs = False
IndexCount = 0
IndexString = ''
ColumnDescripList = []
IndexTypeList = []
IndexNameList = []
global dfColumnDetails
global dfTableSpecs 
global dfIndexDetail
global dfTableChange
global dfIndexDetailsCollapsed 


currentTableName = 'ProviderVendor_DentaQuestDental_ChangesOnly_Archive'
currentSchemaName = 'dbo'
currentDBName = 'NRTCUSTOMDB'
params = ("DRIVER={SQL Server};SERVER=dev_72.sql.caresource.corp\dev_72;DATABASE=ChangeTracking;Trusted_Connection=yes")
currentPageTitle = currentSchemaName + '.' + currentTableName

dfColumnDetailParamString = "EXEC [dbo].[usp_WBTableDetails] @DatabaseName = N'" + currentDBName + "', @TableName = N'" + currentTableName + "', @Schema = N'" + currentSchemaName + "'"
#dfTableSpecsParamString = "EXEC [dbo].[usp_WBTableSpecs] @DBName = N'" + currentDBName + "',  @TableName = N'" + currentTableName + "', @SchemaName = N'" + currentSchemaName + "'"
#dfIndexDetailParamString = "EXEC [dbo].[usp_WBIndexDetails] @DatabaseName = N'" + currentDBName + "',  @TableName = N'" + currentTableName + "', @Schema = N'" + currentSchemaName + "'"
#dfTableChangeParamString = "EXEC [dbo].[usp_WBTableChanges] @DatabaseName = N'" + currentDBName + "',  @TableName = N'" + currentTableName + "', @Schema = N'" + currentSchemaName + "'"
    


c = getSQLCONFIG(configFilePath)


def flagType(value):
    if value == 'nvarchar':
        return 0
    if value == 'uniqueidentifier':
        return 1
    #elif 25000 <= value < 40000:
    #    return "average"
    #elif 40000 <= value < 50000:
    #    return "better"
    else:
        return 2


       

def ModifyColumnDetails():
    global dfColumnDetails

    dfColumnDetails['IdentityColumn'] = dfColumnDetails['IdentityColumn'].fillna(0)
    dfColumnDetails['CHARACTER_MAXIMUM_LENGTH'] = dfColumnDetails['CHARACTER_MAXIMUM_LENGTH'].fillna(0)
    dfColumnDetails['CHARACTER_MAXIMUM_LENGTH'] = dfColumnDetails['CHARACTER_MAXIMUM_LENGTH'].astype(int)
    dfColumnDetails['IndexType'] = dfColumnDetails['IndexType'].fillna(0)
    dfColumnDetails = dfColumnDetails.sort_values(by=['ORDINAL_POSITION'])
    #print(len(dfColumnDetails))
    dfColumnDetails.sort_values(by='ORDINAL_POSITION', inplace=True)
    dfColumnDetails['flagType'] = dfColumnDetails['DATA_TYPE'].map(flagType)
    print(dfColumnDetails[['COLUMN_NAME', 'DATA_TYPE', 'flagType']])
    
   

try:
      engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params) 
      with engine.begin() as conn:
        print('Connected to database')
        dfColumnDetails = pd.DataFrame(conn.execute(dfColumnDetailParamString))
       
        


except SQLAlchemyError as e:
       error = str(e.__dict__['orig'])
       print('database error ', e.args)
       print('Database connection error')  
       engine.dispose   

    
if not dfColumnDetails.empty:    
   ModifyColumnDetails()     
   print(dfColumnDetails[['COLUMN_NAME', 'DATA_TYPE']])



 
#dfColumnDetails['flagType'] = dfColumnDetails['DATA_TYPE'].map(flagType)
#print(dfColumnDetails[['COLUMN_NAME', 'DATA_TYPE', 'flagType']])
