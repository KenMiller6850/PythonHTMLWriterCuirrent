from airium import Airium
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
flagTableChanges = False
flagNoTableSpecs = False
IndexCount = 0
IndexString = ''
ColumnDescripList = []
IndexTypeList = []
IndexNameList = []

c = getSQLCONFIG(configFilePath)


# datetime object containing current date and time
now = datetime.now()
 
# dd/mm/YY H:M:S
#dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
dt_string = now.strftime("%B %d %Y %H:%M:%S")
#print("date and time =", dt_string)

currentTableName = 'ProviderVendor_ASH_Acupunture'
currentSchemaName = 'dbo'
currentDBName = 'NRTCUSTOMDB'



dfColumnDetailParamString = "EXEC [dbo].[usp_WBTableDetails] @DatabaseName = N'" + currentDBName + "', @TableName = N'" + currentTableName + "', @Schema = N'" + currentSchemaName + "'"
dfTableSpecsParamString = "EXEC [dbo].[usp_WBTableSpecs] @DBName = N'" + currentDBName + "',  @TableName = N'" + currentTableName + "', @SchemaName = N'" + currentSchemaName + "'"
dfIndexDetailParamString = "EXEC [dbo].[usp_WBIndexDetails] @DatabaseName = N'" + currentDBName + "',  @TableName = N'" + currentTableName + "', @Schema = N'" + currentSchemaName + "'"
dfTableChangeParamString = "EXEC [dbo].[usp_WBTableChanges] @DatabaseName = N'" + currentDBName + "',  @TableName = N'" + currentTableName + "', @Schema = N'" + currentSchemaName + "'"

params = ("DRIVER={SQL Server};SERVER=dev_72.sql.caresource.corp\dev_72;DATABASE=ChangeTracking;Trusted_Connection=yes")


try:
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params) 
    with engine.begin() as conn:
      print('Connected to database')

      #Build the four dataframes

      dfColumnDetails = pd.DataFrame(conn.execute(dfColumnDetailParamString))
      dfTableSpecs = pd.DataFrame(conn.execute(dfTableSpecsParamString))
      dfIndexDetail = pd.DataFrame(conn.execute(dfIndexDetailParamString))
      dfTableChange = pd.DataFrame(conn.execute(dfTableChangeParamString))

      print(dfTableChange)

      if dfTableChange.empty:
          flagTableChanges = False
          print('No Changes')
      else:
         flagTableChanges = True
         dfTableChange = dfTableChange.sort_values(by=['ORDINAL_POSITION'])
         dfTableChange['CHARACTER_MAXIMUM_LENGTH'] = dfTableChange['CHARACTER_MAXIMUM_LENGTH'].fillna(0)
         dfTableChange['CHARACTER_MAXIMUM_LENGTH'] = dfTableChange['CHARACTER_MAXIMUM_LENGTH'].astype(int)         
         print('Changes Found')

      if dfColumnDetails.empty:
         print('ColumnDetails DataFrame is empty!')
      else:   
        dfColumnDetails['IdentityColumn'] = dfColumnDetails['IdentityColumn'].fillna(0)
        dfColumnDetails['CHARACTER_MAXIMUM_LENGTH'] = dfColumnDetails['CHARACTER_MAXIMUM_LENGTH'].fillna(0)
        dfColumnDetails['CHARACTER_MAXIMUM_LENGTH'] = dfColumnDetails['CHARACTER_MAXIMUM_LENGTH'].astype(int)
        dfColumnDetails['IndexType'] = dfColumnDetails['IndexType'].fillna(0)
        dfColumnDetails = dfColumnDetails.sort_values(by=['ORDINAL_POSITION'])
        #print(len(dfColumnDetails))
        
        dfColumnDetails.sort_values(by='ORDINAL_POSITION', inplace=True)

      
      
      
      if dfIndexDetail.empty:
         print('IndexDetail DataFrame is empty!')
         flagHeap = True
         print(dfIndexDetail)
      else:  
         
      
        IndexCount = len(pd.unique(dfIndexDetail['IndexID']))
        print('Index Count: ' + str(IndexCount))
        #print(dfIndexDetail)
        #print(dfIndexDetail['IndexID'].unique())




      if dfTableSpecs.empty:
          print('TableSpec DataFrame is empty!')
          flagHeap = True
          flagNoTableSpecs = True
          print('flagNoTableSpecs = ' + str(flagNoTableSpecs))
      else:     
          print(dfTableSpecs) 







except SQLAlchemyError as e:
         error = str(e.__dict__['orig'])
         print('database error ', e.args)
         print('Database connection error')  
         engine.dispose


#
print(flagHeap)
if not flagHeap:
   dfIndexDetailsCollapsed = pd.DataFrame(columns=['IndexColumnData','IndexType'])


   i = 1

   while i <= IndexCount:

     newdf = dfIndexDetail.query('IndexID == ' + str(i))
     #indexName = newdf.iloc[i, newdf.columns.get_loc('IndexName')] 
     #print(newdf)

     indexName = newdf.iloc[0,2]
     indexType = newdf.iloc[0,5]
     print('Index Type: ' + str(indexType))
     #df2 = newdf.iloc[:, 1]
  
     df2 = newdf.iloc[: ,1].copy()
     s= df2.str.cat(sep=',')
  
     #print(indexName + ': ' + s)

     #abc_series = pd.Series(s)

     ColumnDescripList.append(s)
     IndexTypeList.append(indexType)
     IndexNameList.append(indexName)

     #dfIndexDetailsCollapsed  = pd.DataFrame([indexName + ': ' + s, indexType], columns=['IndexColumnData', 'IndexType'])
       
     i += 1

print(IndexTypeList)

dfIndexDetailsCollapsed = pd.DataFrame(
    {'IndexColumns': ColumnDescripList,
     'IndexType': IndexTypeList,
     'IndexName' : IndexNameList
    })




def addChangedRow(i):
    with a.tr(klass='changed'):

        with a.td():   
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('ORDINAL_POSITION')])
                             
        with a.td():

               if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IndexType')] is None:
                 a.div(_t='<i class="fas fa-project-diagram text-info"></i>')    

               if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IndexType')] == 1:
                 a.div(_t='<i class="fas fa-key text-danger"></i>')

                 #titleString = df.iloc[i, df.columns.get_loc('IndexName')] + ' clustered'
                 #a.img(alt='Clustered Index', klass='cluster', src='../../../Images/cluster.png', title= titleString)
        
               if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IndexType')] > 1:
                 a.div(_t='<i class="fas fa-project-diagram text-info"></i>')

             
                 #titleString = df.iloc[i, df.columns.get_loc('IndexName')] + ' non-clustered'
                 #a.img(a.img(alt='Non-Clustered Index', klass='Index', src='../../../Images/Index.png', title= titleString))

        with a.td():   
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('COLUMN_NAME')])

        with a.td():      
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('DATA_TYPE')])

        with a.td():     
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('CHARACTER_MAXIMUM_LENGTH')])

        with a.td():   
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IS_NULLABLE')])

        with a.td():     
           if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('COLUMN_DEFAULT')] == -999:
                a.div()

        with a.td():     
            if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IdentityColumn')] == 1:
                 a.div(_t='<i class="fas fa-flag text-success"></i>')
                 #titleString = df.iloc[i, df.columns.get_loc('IndexName')] + ' clustered'
                 #a.img(alt='Clustered Index', klass='cluster', src='../../../Images/cluster.png', title= titleString)


def addNormalRow(i):
    with a.tr():
                                 

        with a.td():   
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('ORDINAL_POSITION')])

        with a.td():
               #a.div(_t=df.iloc[i, df.columns.get_loc('IndexName')])
               if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IndexType')] == 1:
                 a.div(_t='<i class="fas fa-key  text-danger"></i>')
                 #titleString = df.iloc[i, df.columns.get_loc('IndexName')] + ' clustered'
                 #a.img(alt='Clustered Index', klass='cluster', src='../../../Images/cluster.png', title= titleString)
        
               if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IndexType')] > 1:
                 a.div(_t='<i class="fas fa-project-diagram text-info"></i>')
                 
               if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IndexType')] == -999:
                 a.div()


        with a.td():   
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('COLUMN_NAME')])

        with a.td():      
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('DATA_TYPE')])

        with a.td():     
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('CHARACTER_MAXIMUM_LENGTH')])

        with a.td():   
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IS_NULLABLE')])

        with a.td():     
            #a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('COLUMN_DEFAULT')])
            #a.div()
            #a.div(_t=df.iloc[i, df.columns.get_loc('IndexName')])
            
            if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('COLUMN_DEFAULT')] == -999:
                 a.div()
            #     #titleString = df.iloc[i, df.columns.get_loc('IndexName')] + ' clustered'
            #     #a.img(alt='Clustered Index', klass='cluster', src='../../../Images/cluster.png', title= titleString)
        
            if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('COLUMN_DEFAULT')] != -999:
                 a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('COLUMN_DEFAULT')])
                 


        with a.td():     
            if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IdentityColumn')] == -999:
                 a.div()
            #     #titleString = df.iloc[i, df.columns.get_loc('IndexName')] + ' clustered'
            #     #a.img(alt='Clustered Index', klass='cluster', src='../../../Images/cluster.png', title= titleString)
        
            if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IdentityColumn')] != -999:
                 a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IdentityColumn')])
                 
            #a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IdentityColumn')])       


def addClusteredIndexRow(i):
    with a.tr(klass='clustered'):
        with a.td():   
            #a.div(_t=dfIndexDetails.iloc[i, dfIndexDetails.columns.get_loc('IndexType')])
            a.div(_t='Clustered')
        
        with a.td():   
           if dfIndexDetailsCollapsed.iloc[i, dfIndexDetailsCollapsed.columns.get_loc('IndexName')] != '-999':
                 a.div(_t=dfIndexDetailsCollapsed.iloc[i, dfIndexDetailsCollapsed.columns.get_loc('IndexName')])
           else:
             a.div()

        with a.td():                    
           if dfIndexDetailsCollapsed.iloc[i, dfIndexDetailsCollapsed.columns.get_loc('IndexColumns')] != '-999':
                 a.div(_t=dfIndexDetailsCollapsed.iloc[i, dfIndexDetailsCollapsed.columns.get_loc('IndexColumns')])
           else:
              a.div()



def addNCIndexRow(i):
    with a.tr():
        with a.td():   
            #a.div(_t='Non-Clustered')
            a.div(_t= '-') 

        with a.td():   
           if dfIndexDetailsCollapsed.iloc[i, dfIndexDetailsCollapsed.columns.get_loc('IndexName')] != '-999':
                 a.div(_t=dfIndexDetailsCollapsed.iloc[i, dfIndexDetailsCollapsed.columns.get_loc('IndexName')])
           else:
             a.div()

        with a.td():                    
           if dfIndexDetailsCollapsed.iloc[i, dfIndexDetailsCollapsed.columns.get_loc('IndexColumns')] != '-999':
                 a.div(_t=dfIndexDetailsCollapsed.iloc[i, dfIndexDetailsCollapsed.columns.get_loc('IndexColumns')])
           else:
              a.div()


def addColumnChangeRow(i):
    with a.tr():
                                 

        with a.td():   
            a.div(_t=dfTableChange.iloc[i, dfTableChange.columns.get_loc('ORDINAL_POSITION')])

        with a.td():   
            a.div()

        with a.td():   
            a.div(_t=dfTableChange.iloc[i, dfTableChange.columns.get_loc('COLUMN_NAME')])


        with a.td():      
            a.div(_t=dfTableChange.iloc[i, dfTableChange.columns.get_loc('DATA_TYPE')])

        with a.td():     
            a.div(_t=dfTableChange.iloc[i, dfTableChange.columns.get_loc('CHARACTER_MAXIMUM_LENGTH')])

        with a.td():   
            a.div(_t=dfTableChange.iloc[i, dfTableChange.columns.get_loc('IS_NULLABLE')])            

    """with a.td():
               #a.div(_t=df.iloc[i, df.columns.get_loc('IndexName')])
               if dfTableChange.iloc[i, dfTableChange.columns.get_loc('IndexType')] == 1:
                 a.div(_t='<i class="fas fa-key  text-danger"></i>')
                 #titleString = df.iloc[i, df.columns.get_loc('IndexName')] + ' clustered'
                 #a.img(alt='Clustered Index', klass='cluster', src='../../../Images/cluster.png', title= titleString)
        
            if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IndexType')] > 1:
                 a.div(_t='<i class="fas fa-project-diagram text-info"></i>')
                 
               if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IndexType')] == -999:
                 a.div()


        with a.td():   
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('COLUMN_NAME')])

        with a.td():      
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('DATA_TYPE')])

        with a.td():     
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('CHARACTER_MAXIMUM_LENGTH')])

        with a.td():   
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IS_NULLABLE')])

        with a.td():     
            #a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('COLUMN_DEFAULT')])
            #a.div()
            #a.div(_t=df.iloc[i, df.columns.get_loc('IndexName')])
            
            if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('COLUMN_DEFAULT')] == -999:
                 a.div()
            #     #titleString = df.iloc[i, df.columns.get_loc('IndexName')] + ' clustered'
            #     #a.img(alt='Clustered Index', klass='cluster', src='../../../Images/cluster.png', title= titleString)
        
            if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('COLUMN_DEFAULT')] != -999:
                 a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('COLUMN_DEFAULT')])
                 


        with a.td():     
            if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IdentityColumn')] == -999:
                 a.div()
            #     #titleString = df.iloc[i, df.columns.get_loc('IndexName')] + ' clustered'
            #     #a.img(alt='Clustered Index', klass='cluster', src='../../../Images/cluster.png', title= titleString)
        
            if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IdentityColumn')] != -999:
                 a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IdentityColumn')])
                 
            #a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IdentityColumn')])        """


def StatError(StatRows,TrueRows):
     
    # Returns flag based on stat row vs true row count mismatch
    if StatRows != TrueRows:
      return True
    else:
      return False  


def ZeroRows(StatRows,TrueRows):
     
    # Returns flag based on stat row vs true row count mismatch
    if (StatRows == 0 and TrueRows == 0):
      return True
    else:
      return False  
    
def RowMatch(StatRows,TrueRows):
     
    # Returns flag based on stat row vs true row count mismatch
    if (StatRows == TrueRows):
      return True
    else:
      return False  
    
if flagNoTableSpecs != True:
   tableCreatedDate = dfTableSpecs.iloc[0, dfTableSpecs.columns.get_loc('CreatedDate')].strftime("%Y-%m-%d %H:%M:%S")
   tableModifiedDate = dfTableSpecs.iloc[0, dfTableSpecs.columns.get_loc('ModifiedDate')].strftime("%Y-%m-%d %H:%M:%S")
   StatRowCount  = 0
   TrueRowCount = 0
   StatRowCount = dfTableSpecs.iloc[0, dfTableSpecs.columns.get_loc('StatRowCount')]
   TrueRowCount = dfTableSpecs.iloc[0, dfTableSpecs.columns.get_loc('TrueRowCount')]
      


a = Airium()

a('<!DOCTYPE html>')
with a.html(id="index"):
    with a.head():
        a.meta(charset="utf-8")
        a.title(_t="dbo.PaymentSettlementClaims")
        a.link(href='https://cdn.metroui.org.ua/v4/css/metro-all.min.css', rel='stylesheet')
        a.link(href='../../../Style/Master.css', rel='stylesheet', type='text/css')
        a.link(href='../../../vendor/fontawesome/all.min.css', rel='stylesheet', type='text/css' )
        
        a.script(src='../../../Scripts/jquery-1.9.1.js', type='text/javascript')
        a.script(src='../../../Scripts/sections.js', type='text/javascript')
        a.script(src='../../../Scripts/sortable.min.js', type='text/javascript')


        
    
    with a.body():
        with a.div(id='wrap'):
            with a.div(id='container'):
                with a.div(id='top-header', klass='image-text'):
                       
                       #a.img(alt='expanded', src='../../../Images/tableCS.png', style='')

                       with a.div(klass='flex-container'):
                           with a.div(klass='flex-item-cap-title'):
                              a.i(klass='fas fa-table')
                           with a.div(klass='flex-item-button-title'):
                              a(currentTableName)                              
                       #a('<h1 style="color:black; background-color: #ddbbff;border-radius: 6px;width: 1200px">' + currentTableName +'</h1>')

                #with a.div(id='pageTitle'):
                    
                    
                if flagNoTableSpecs == False:    
                   

                   with a.div(klass='panel panel-default', style='background-color: #444a77'):
                       with a.div(klass='panel-heading'):
                           with a.div():
                            #a.img(alt='collapsed', klass='collapsed', src='../../../Images/collapsed.png', style='display:none;', title='collapsed')
                            #a.img(alt='expanded', klass='expanded', src='../../../Images/expanded.png', style='', title='expanded')
                               a.a(name='properties', _t='Table Details')
                       with a.div(klass='panel-body'):

                        with a.div(klass='flex-container'):
                           


                           with a.div(klass='flex-item-cap'):
                              a.i(klass='fas fa-calendar-alt')

                           with a.div(klass='flex-item'):
                              a('Created: ' + str(tableCreatedDate))
                       
                           
                           if StatError(StatRowCount,TrueRowCount):
                              with a.div(klass='flex-item-cap-warning'):
                                  a.i(klass='fas fa-align-justify fa-spin')
                              with a.div(klass='flex-item-button-warning'):
                                  a('Stats: ' +"{:,}".format(StatRowCount)
                                    + '     Actual: '+"{:,}".format(TrueRowCount))
                                 
                           elif ZeroRows(StatRowCount,TrueRowCount):
                              with a.div(klass='flex-item-cap-zero'):
                                   a.i(klass='fas fa-align-justify')
                              with a.div(klass='flex-item-button-zero'):
                                   a('Zero Row Count')

                           elif RowMatch(StatRowCount,TrueRowCount):
                               with a.div(klass='flex-item-cap-match'):
                                    a.i(klass='fas fa-align-justify')
                               with a.div(klass='flex-item-button-match'):
                                    a('Stats: ' +"{:,}".format(StatRowCount)
                                      + '     Actual: '+"{:,}".format(TrueRowCount))

                           else:
                               with a.div(klass='flex-item-cap-rows'):
                                    a('Rows')
                               with a.div(klass='flex-item-button'):
                                    a('Stats: ' +str(StatRowCount) 
                                      + '     Actual: '+"{:,}".format(TrueRowCount))  
                                    


                            
                           if flagTableChanges:
                              with a.div(klass='flex-item-cap-notify'):
                                a.i(klass='fas fa-table fa-spin')
                              with a.div(klass='flex-item-button-notify'):
                                 a('Column Changes Detected')


                        with a.div(klass='flex-container'):
                           
                           with a.div(klass='flex-item-cap'):
                              a.i(klass='fas fa-calendar-alt')

                           with a.div(klass='flex-item'):
                              a('Last Modified: ' + str(tableModifiedDate))
                        	
                           if flagHeap:
                              with a.div(klass='flex-item-cap-warning'):
                                 a.i(klass='fas fa-table fa-spin')
                              with a.div(klass='flex-item-button-warning'):
                                 a('HEAP')

                           #with a.div(klass='flex-item-cap'):
                           #   a('&nbsp;')
                           #with a.div(klass='flex-item', style='color: black'):
                           #   a.i(klass='fas fa-calendar-alt')
                           #   a('Different Data') 

                           #with a.div(klass='flex-item-cap'):
                           #   a('&nbsp;')
                           #with a.div(klass='flex-item', style='color: black'):
                           #   a.i(klass='fas fa-calendar-alt')
                           #   a('Different Data') 




                with a.div(klass='panel panel-default'):
                    with a.div(klass='panel-heading'):
                        with a.div():
                            #a.img(alt='collapsed', klass='collapsed', src='../../../Images/collapsed.png', style='display:none;', title='collapsed')
                            #a.img(alt='expanded', klass='expanded', src='../../../Images/expanded.png', style='', title='expanded')
                            a.a(name='columns', _t='Column Specifications')
                    with a.div(klass='panel-body'):
                        with a.table(border='0', cellspacing='1', klass='sortable', id="columnsTable"):
                          with a.thead():
                            with a.tbody():
                                with a.div():
                                  with a.tr():
                                    a.th(_t='#')
                                    a.th(_t='Key')
                                    a.th(_t='Name')
                                    a.th(_t='Data Type')
                                    a.th(_t='Max Length (Bytes)')
                                    with a.th():
                                        with a.div():
                                            a('Null Allowed')
                                            with a.a(href='#', title='Find information on the NULL option here.'):
                                                a.img(_t='<i class="fa fa-question-circle fa-lg"></i>')
                                    a.th(_t='Default Value')
                                    a.th(_t='Identity Column')
                                    

                                    
                            i = 0
                            while i < len(dfColumnDetails.index):
                                if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('DATA_TYPE')] == 'int':
                                   addChangedRow(i)
                                    #print(i)
                                else:  
                                   addNormalRow(i)
                                   #print(i)
                                i += 1 





                if flagTableChanges:  
                  with a.div(klass='panel panel-default'):
                    with a.div(klass='panel-heading'):
                        with a.div():
                            #a.img(alt='collapsed', klass='collapsed', src='../../../Images/collapsed.png', style='display:none;', title='collapsed')
                            #a.img(alt='expanded', klass='expanded', src='../../../Images/expanded.png', style='', title='expanded')
                            a.a(name='columns', _t='Column Changes')
                    with a.div(klass='panel-body'):
                        with a.table(border='0', cellspacing='1', klass='sortable2', id="columnsChangedTable"):
                          with a.thead():
                            with a.tbody():
                                with a.div():
                                  with a.tr():
                                    a.th(_t='#')
                                    a.th(_t='Key')
                                    a.th(_t='Name')
                                    a.th(_t='Data Type')
                                    a.th(_t='Max Length (Bytes)')
                                    with a.th():
                                        with a.div():
                                            a('Null Allowed')
                                            #with a.a(href='#', title='Find information on the NULL option here.'):
                                            #    a.img(_t='<i class="fa fa-question-circle fa-lg"></i>')
                                    a.th(_t='Default Value')
                                    a.th(_t='Identity Column')


 
                            i = 0
                            while i < len(dfTableChange.index):
                                addColumnChangeRow(i)
                                i += 1                              





                with a.div(klass='panel panel-default panel-collapsible'):
                    with a.div(klass='panel-heading'):
                        with a.div(klass='expandCollapse'):
                            #a.img(alt='collapsed', klass='collapsed', src='../../../Images/collapsed.png', style='display:none;', title='collapsed')
                            #a.img(alt='expanded', klass='expanded', src='../../../Images/expanded.png', style='', title='expanded')
                            a.a(name='indexes', _t='Index Details')
                    with a.div(klass='panel-body'):
                        with a.table(border='0', cellspacing='1', klass='dataTable table-hover'):
                            with a.tbody():
                                with a.tr():
                                    a.th(_t='Type')
                                    a.th(_t='Name')
                                    a.th(_t='Key Columns')
 
                            i = 0
                            while i < len(dfIndexDetailsCollapsed.index):
                                if dfIndexDetailsCollapsed.iloc[i, dfIndexDetailsCollapsed.columns.get_loc('IndexType')] == 1:
                                   addClusteredIndexRow(i)
                                    #print(i)
                                else:  
                                   addNCIndexRow(i)
                                   #print(i)
                                i += 1 












"""                                          if df.iloc[i, df.columns.get_loc('DATA_TYPE')] == 'int':
                                            addChangedRow(i)
                                    else:
                                         if df.iloc[i, df.columns.get_loc('DATA_TYPE')] == 'int':
                                             addNormalRow(i)
                                             
                                         print(i)
                                         i += 1  """
                                         
                                       #print(df.iloc[i, df.columns.get_loc('COLUMN_NAME')])    
"""                                          with a.tr(klass='changed'):
                                          
                                         #a.td()
                                          with a.td():
                                            a.div()

                                          with a.td():   
                                            a.div(_t=df.iloc[i, df.columns.get_loc('COLUMN_NAME')])

                                          with a.td():      
                                            a.div(_t=df.iloc[i, df.columns.get_loc('DATA_TYPE')])

                                          with a.td():     
                                            a.div(_t=df.iloc[i, df.columns.get_loc('CHARACTER_MAXIMUM_LENGTH')])

                                          with a.td():   
                                            a.div(_t=df.iloc[i, df.columns.get_loc('IS_NULLABLE')])

                                          with a.td():     
                                            a.div(_t=df.iloc[i, df.columns.get_loc('COLUMN_DEFAULT')])

                                          with a.td():     
                                            a.div() 
                                         """


with a.div(klass='panel panel-default panel-collapsible'):
                    with a.div(klass='panel-heading'):
                        with a.div(klass='expandCollapse'):
                            #a.img(alt='collapsed', klass='collapsed', src='./CARESOURCE_jmmcabe.OLE DB Destination_files/collapsed.png', style='display:none;', title='collapsed')
                            #a.img(alt='expanded', klass='expanded', src='./CARESOURCE_jmmcabe.OLE DB Destination_files/expanded.png', style='', title='expanded')
                            a.a(name='uses', _t='Uses')
                    with a.div(klass='panel-body'):
                        with a.ul(klass='DependencyList'):
                            with a.li():
                                with a.a(href='https://caresource.sharepoint.com/sites/SQLAssistance/DataDictionary/DEV72Docs/User_databases/NRTCUSTOMDB/Security/Schemas/CARESOURCE_jmmcabe_CARESOURCE_jmmcabe.aspx'):
                                    a('CARESOURCE\\jmmcabe')
with a.div(id='footer'):
            with a.div(klass='row'):
                with a.div(klass='col-sm-4', id='customtext'):
                    a.div(id='projectauthor', _t='CareSource Database Engineering')
                a.div(klass='col-sm-4', id='copyright', _t='Part of the Data Dictionary Project')
                a.div(klass='col-sm-4', id='date', _t='Created: ' + dt_string )









html = str(a) # casting to string extracts the value

#print(html)

with open('C:\\Users\\akdmille\\Documents\\My Database Documentation\\FileTesting3\\User_databases\\NRTCUSTOMDB\\Tables\\' + currentTableName + '.html', 'wb') as f:
    f.write(bytes(html, encoding="utf-8"))

with open('C:\\Users\\akdmille\\Documents\\My Database Documentation\\FileTesting3\\User_databases\\NRTCUSTOMDB\\Tables\\' + currentTableName + '.aspx', 'wb') as f:
    f.write(bytes(html, encoding="utf-8"))    
