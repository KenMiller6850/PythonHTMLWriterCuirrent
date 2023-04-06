from airium import Airium
# Import date class from datetime module
from datetime import datetime
from ReadConfig2 import getSQLCONFIG
import pyodbc
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine


configFilePath = r'C:\Users\akdmille\Documents\Python Files\configDEV72.ini'


c = getSQLCONFIG(configFilePath)

#conn = pyodbc.connect('Driver={SQL Server};'
#                      'Server='+c[1]+';'
#                      'Database='+c[0]+';'
#                      'Trusted_Connection=yes;')


params = ("DRIVER={SQL Server};SERVER=dev_72.sql.caresource.corp\dev_72;DATABASE=ChangeTracking;Trusted_Connection=yes")

try:
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params) 
    with engine.begin() as conn:
      print('Connected to database')
      #result = conn.execute("EXEC [dbo].[usp_WBIndexDetails] @DatabaseName = N'NRTCUSTOMDB', @TableName = N'Network_Ops_Provider_Network_Prefix_Info', @Schema = N'dbo'")
      #result = conn.execute("EXEC [dbo].[usp_WBIndexDetails] @DatabaseName = N'NRTCUSTOMDB', @TableName = N'CLAIMS_ADJ_CORR', @Schema = N'dbo'")
      result = conn.execute("EXEC [dbo].[usp_WBIndexDetails] @DatabaseName = N'NRTCUSTOMDB', @TableName = N'ProviderVendor_DentaQuestDental_ChangesOnly', @Schema = N'dbo'")
      dftemp = pd.DataFrame(result)

      

      #for row in result:
      #  print((row['COLUMN_NAME'], row['ORDINAL_POSITION']))
      
      conn.close
      engine.dispose

except SQLAlchemyError as e:
  error = str(e.__dict__['orig'])
  print('database error ', e.args)
  print('Database connection error')  


engine.dispose


#Manipulate the dataframe

if not dftemp.empty:
  print(dftemp)
  IndexCount = dftemp['IndexID'].max()
  indexString = ''

  #Create a DataFrame object
  dfIndexDetails_cols = ['IndexName', 'IndexColumns', 'IndexType']
  dfIndexDetails = pd.DataFrame()

  i = 1

  while i <= IndexCount:
      z = 0
    
      newdf = dftemp.query('IndexID == ' + str(i))

      while z < len(newdf.index):
        indexType = newdf.iloc[z, newdf.columns.get_loc('IndexType')] 
        indexString += newdf.iloc[z, newdf.columns.get_loc('COLUMN_NAME')] + ',' 
        indexName = newdf.iloc[z, newdf.columns.get_loc('IndexName')] 
        s1 = pd.Series([indexName])
        s2 = pd.Series([indexString])
        s3 = pd.Series([indexType])
        z += 1 
   
      indexString = ''
      appended_series = pd.concat([s1,s2,s3],axis=1)  
      dfIndexDetails = dfIndexDetails.append(appended_series, ignore_index=True)
      i += 1 
      print(dfIndexDetails)


if dftemp.empty:
  dfIndexDetails_cols = ['IndexName', 'IndexColumns', 'IndexType']
  dfIndexDetails = pd.DataFrame()
  indexType = -999 
  indexString = 'None'
  indexName = 'None'
  s1 = pd.Series([indexName])
  s2 = pd.Series([indexString])
  s3 = pd.Series([indexType])
  appended_series = pd.concat([s1,s2,s3],axis=1)  
  dfIndexDetails = dfIndexDetails.append(appended_series, ignore_index=True)
  print(dfIndexDetails)




