SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER VIEW [dbo].[vw_Cleaned_Customer_Data] AS
SELECT 
    [ID],
    [Churn],
    [SeniorCitizen],
    [Partner],
    [Dependents],
    [Tenure],
    [Contract],
    [PaymentMethod],
    [PaperlessBilling],  
    [MonthlyCharges],    
    [TotalCharges],      
    [InternetService],
    [OnlineSecurity],
    [OnlineBackup],
    [DeviceProtection],
    [TechSupport]
FROM [dbo].[Predictive_Customer_Churn_DB];
GO