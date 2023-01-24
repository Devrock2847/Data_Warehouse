import pandas as pd
import pyodbc

from ODS_Star_Schema import ODS


class ParseSQL:
    def __init__(self):
        self.conn = pyodbc.connect(
                    'Driver={SQL Server};'
                    'Server=sql2016.fse.network;'
                    'Database=db_2126677_AssignmentData;'
                    'UID=user_db_2126677_AssignmentData;'
                    'PWD=Password123;')
        self.cursor = self.conn.cursor()

    def ParseSQL(self):
        print("Parsing from SQL database begun")
        self.ParseCustomer()
        self.ParseProduct()
        self.ParseSupplier()
        self.ParseInternetSaleItem()
        self.ParseFactSales()
        print("Parsing from SQL database finished")

    def ParseCustomer(self):
        customer_df = pd.read_sql_query('SELECT * FROM Customer', self.conn)
        ODS.Dim_Customer_df = ODS.Dim_Customer_df.append(customer_df)
        #print(ODS.Dim_Customer_df.to_string())

    def ParseProduct(self):
        product_df = pd.read_sql_query('SELECT * FROM Product', self.conn)
        ODS.Dim_Product_df = ODS.Dim_Product_df.append(product_df)
        #print(ODS.Dim_Product_df.to_string())

    def ParseSupplier(self):
        supplier_df = pd.read_sql_query('SELECT SupplierID, SupplierAddress, SupplierCity, SupplierStateProvince, SupplierCountry, SupplierPhone, SupplierPostCode FROM Supplier', self.conn)
        ODS.Dim_Supplier_df = ODS.Dim_Supplier_df.append(supplier_df)
        #print(ODS.Dim_Supplier_df.to_string())

    def ParseInternetSaleItem(self):
        internetSaleItem_df = pd.read_sql_query('SELECT SaleID, Quantity, DateShipped, ShippingType FROM InternetSaleItem', self.conn)
        ODS.Dim_InternetSaleItem_df = ODS.Dim_InternetSaleItem_df.append(internetSaleItem_df)
        # UniqueID
        ODS.Dim_InternetSaleItem_df['tempCol2'] = range(0, len(ODS.Dim_InternetSaleItem_df.index))
        ODS.Dim_InternetSaleItem_df['tempCol1'] = ODS.Dim_InternetSaleItem_df['DateShipped'].astype(str) + "-" + ODS.Dim_InternetSaleItem_df['SaleID'].str[0] + ODS.Dim_InternetSaleItem_df['SaleID'].str[1] + "-"
        ODS.Dim_InternetSaleItem_df['UniqueID'] = ODS.Dim_InternetSaleItem_df['tempCol1'] + ODS.Dim_InternetSaleItem_df['tempCol2'].astype(str)
        ODS.Dim_InternetSaleItem_df = ODS.Dim_InternetSaleItem_df.drop(columns=['tempCol1', 'tempCol2'])
        #print(ODS.Dim_InternetSaleItem_df.to_string())

    def ParseFactSales(self):
        internetSale_df = pd.read_sql_query('SELECT * FROM InternetSale', self.conn)
        internetSaleItem_df = pd.read_sql_query('SELECT SaleID, ProductID, DateShipped FROM InternetSaleItem', self.conn)

        # UniqueID
        internetSaleItem_df['tempCol2'] = range(0, len(internetSaleItem_df.index))
        internetSaleItem_df['tempCol1'] = internetSaleItem_df['DateShipped'].astype(str) + "-" + internetSaleItem_df['SaleID'].str[0] + internetSaleItem_df['SaleID'].str[1] + "-"
        internetSaleItem_df['UniqueID'] = internetSaleItem_df['tempCol1'] + internetSaleItem_df['tempCol2'].astype(str)
        internetSaleItem_df = internetSaleItem_df.drop(columns=['tempCol1', 'tempCol2', 'DateShipped'])

        # SaleID
        internetSaleItem_df.drop_duplicates(subset='SaleID', keep='first', inplace=True)
        internetSale_df = pd.merge(internetSale_df, internetSaleItem_df[['SaleID', 'ProductID', 'UniqueID']], left_on='SaleID', right_on='SaleID', how='left')

        ODS.FACT_Sales_df = ODS.FACT_Sales_df.append(internetSale_df)

        #print(ODS.FACT_Sales_df.to_string())
