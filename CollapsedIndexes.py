def BuildIndexDescriptions(incomingDB, incomingSchema,incomingTable):
    
  # Import date class from datetime module
  from datetime import datetime
  from ReadConfig2 import getSQLCONFIG
  import pandas as pd
  from sqlalchemy.exc import SQLAlchemyError
  from sqlalchemy import create_engine


  configFilePath = r'C:\Users\akdmille\Documents\Python Files\configDEV72.ini'
  
  currentTableName = incomingTable
  currentSchemaName = incomingSchema
  currentDBName = incomingDB

  c = getSQLCONFIG(configFilePath)

  dfCollapsedIndexesParamString = "EXEC [dbo].[usp_WBIndexDetails] @DatabaseName = N'" + currentDBName + "',  @TableName = N'" + currentTableName + "', @Schema = N'" + currentSchemaName + "'"
  params = ("DRIVER={SQL Server};SERVER=dev_72.sql.caresource.corp\dev_72;DATABASE=ChangeTracking;Trusted_Connection=yes")

  try:
      engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params) 
      with engine.begin() as conn:
        print('Connected to database')
        result = conn.execute(dfCollapsedIndexesParamString)
        dftemp = pd.DataFrame(result)
        conn.close
        engine.dispose

  except SQLAlchemyError as e:
    error = str(e.__dict__['orig'])
    print('database error ', e.args)
    print('Database connection error')  

  engine.dispose

  print('dfTemp')
  print('dfTemp:' + dftemp)
  #Manipulate the dataframe
  
  
  
 
  if not dftemp.empty:
    
    IndexCount = dftemp['IndexID'].max()
    indexString = ''
    #Create a DataFrame object
    dfIndexDetails = pd.DataFrame()
    dfIndexDetails_cols = ['IndexName', 'IndexColumns', 'IndexType']


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

    dfIndexDetails.columns =['IndexName', 'IndexColumns', 'IndexType']
  
  if dftemp.empty:
    
    
    dfIndexDetails = pd.DataFrame()
    indexType = 0
    indexString = 'None'
    indexName = 'None'
    
    s1 = pd.Series(indexName)
    s2 = pd.Series(indexString)
    s3 = pd.Series(indexType) 
    appended_series = pd.concat([s1,s2,s3],axis=1)  
    dfIndexDetails = dfIndexDetails.append(appended_series, ignore_index=True)
    dfIndexDetails.columns =['IndexName', 'IndexColumns', 'IndexType']
  
  return(dfIndexDetails)    








