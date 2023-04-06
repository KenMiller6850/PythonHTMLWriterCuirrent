import CollapsedIndexes5 as CI
from ReadConfig2 import getSQLCONFIG
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
import pandas as pd

          
                                    

df = CI.BuildIndexDescriptions('NRTCUSTOMDB','dbo','Facets_ProviderSetupQualityCheck_Audit_Stg')

#df = CI.BuildIndexDescriptions('NRTCUSTOMDB','dbo','Network_Ops_Provider_Network_Prefix_Info')



#df = CI.BuildIndexDescriptions('NRTCUSTOMDB','dbo','ProviderVendor_DentaQuestDental_ChangesOnly')
        #result = conn.execute("EXEC [dbo].[usp_WBIndexDetails] @DatabaseName = N'NRTCUSTOMDB', @TableName = N'Network_Ops_Provider_Network_Prefix_Info', @Schema = N'dbo'")
        #result = conn.execute("EXEC [dbo].[usp_WBIndexDetails] @DatabaseName = N'NRTCUSTOMDB', @TableName = N'CLAIMS_ADJ_CORR', @Schema = N'dbo'")
        #result = conn.execute("EXEC [dbo].[usp_WBIndexDetails] @DatabaseName = N'NRTCUSTOMDB', @TableName = N'ProviderVendor_DentaQuestDental_ChangesOnly', @Schema = N'dbo'")


print(df)



