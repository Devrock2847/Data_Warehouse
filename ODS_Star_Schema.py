import pandas as pd


class ODS:
	tables = [
			'Dim_InternetSaleItem',
			'Dim_Supplier',
			'Dim_Product',
			'Dim_Customer',
			'FACT_Sales'
	]
	Dim_Supplier_df = pd.DataFrame(columns=['SupplierID', 'SupplierAddress', 'SupplierCity', 'SupplierStateProvince', 'SupplierCountry', 'SupplierPhone', 'SupplierPostCode'])
	Dim_InternetSaleItem_df = pd.DataFrame(columns=['UniqueID', 'SaleID', 'Quantity', 'DateShipped', 'ShippingType'])
	Dim_Product_df = pd.DataFrame(columns=['ProductID', 'SupplierID', 'ProductDescription', 'CategoryID', 'SupplierPrice', 'ProductPrice', 'SafetyStockLevel', 'ReorderPoint'])
	Dim_Customer_df = pd.DataFrame(columns=['CustomerID', 'CustomerEmail', 'FirstName', 'SecondName', 'CustomerType', 'City', 'StateProvince', 'Country', 'PostalCode'])
	FACT_Sales_df = pd.DataFrame(columns=['SaleID', 'UniqueID', 'ProductID', 'CustomerID', 'DateOfSale', 'SaleAmount', 'SalesTax', 'SaleTotal'])
