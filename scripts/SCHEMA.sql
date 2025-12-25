USE OracleOfDelphi

CREATE TABLE transactions(
	TransactionID INT IDENTITY(1,1) PRIMARY KEY,
	InvoiceNo VARCHAR(50),
	StockCode VARCHAR(50),
	Description VARCHAR(300),
	InvoiceDate DATETIME,
	Quantity INT,
	UnitPrice INT,
	Revenue INT,
	CustomerID VARCHAR(50),
	Country VARCHAR(50),
	SalesChannel VARCHAR(50),
	UNIQUE (InvoiceNo, Description)
);
