USE OracleOfDelphi

CREATE TABLE transactions(
	transactionid INT IDENTITY(1,1) PRIMARY KEY,
	invoiceno VARCHAR(50),
	stockcode VARCHAR(50),
	description VARCHAR(300),
	invoicedate DATETIME,
	quantity INT,
	unitprice INT,
	revenue INT,
	customerid VARCHAR(50),
	country VARCHAR(50),
	saleschannel VARCHAR(50),
	UNIQUE (invoiceno, description)
);
