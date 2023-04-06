import HTMLFileWriterFunction4 as fw
from ReadConfig2 import getSQLCONFIG
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
import pandas as pd


currentDBName = 'NRTCUSTOMDB'
DBCaptureID = 27

configFilePath = r'C:\Users\akdmille\Documents\Python Files\configDEV72.ini'
params = ("DRIVER={SQL Server};SERVER=dev_72.sql.caresource.corp\dev_72;DATABASE=ChangeTracking;Trusted_Connection=yes")
dfExtractedTableslParamString = "EXEC [dbo].[usp_WBGetExtractedTables] @DatabaseName = N'" + currentDBName + "', @DBCaptureID = " + str(DBCaptureID) 

#print (dfExtractedTableslParamString)

try:
   engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params) 
   with engine.begin() as conn:
      print('Connected to database')
      dfExtractedTables = pd.DataFrame(conn.execute(dfExtractedTableslParamString))   

except SQLAlchemyError as e:
  error = str(e.__dict__['orig'])
  print('database error ', e.args)
  print('Database connection error')  
  engine.dispose   

#print(dfExtractedTables)

#Exclude non-standard schemas

dfNonStandard = dfExtractedTables[dfExtractedTables['TABLE_SCHEMA'].str.contains('CARESOURCE')]

dfFinal = pd.concat([dfNonStandard, dfExtractedTables]).drop_duplicates(keep=False)


                                
i = 0
while i < len(dfFinal.index):
    DBName = dfFinal.iloc[i, dfFinal.columns.get_loc('TABLE_CATALOG')]
    SchemaName = dfFinal.iloc[i, dfFinal.columns.get_loc('TABLE_SCHEMA')]
    TableName = dfFinal.iloc[i, dfFinal.columns.get_loc('TABLE_NAME')]
    
    print(SchemaName + '.' + TableName)
    
    fw.CreateHTMLPage(DBName,SchemaName,TableName)
    i += 1 
 
                                    
                                    


#fw.CreateHTMLPage('NRTCUSTOMDB','Provider','EXT_PRAD_ADDRESS')

