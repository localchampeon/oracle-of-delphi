use OracleOfDelphi

CREATE TABLE sales_hybrid (
    invoiceid INT IDENTITY(1,1) PRIMARY KEY,
    invoiceno VARCHAR(20) NULL,
    invoicedate DATETIME NULL,
    stockcode VARCHAR(20),
    description VARCHAR(255),
    quantity INT NULL,
    unitprice DECIMAL(10,2) NULL,
    revenue DECIMAL(18,2) NULL,
    customerid VARCHAR(20),
    country VARCHAR(50),
    saleschannel VARCHAR(10) CHECK (saleschannel IN ('online', 'offline')),
    UNIQUE (invoiceno, description),
    
    -- Indexes
    INDEX idx_invoice_date (invoicedate),
    INDEX idx_customer (customerid)
);
