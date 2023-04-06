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

  #print('dfTemp')
  print('dfTemp:' + dftemp)
  #Manipulate the dataframe
  
  
  
 









