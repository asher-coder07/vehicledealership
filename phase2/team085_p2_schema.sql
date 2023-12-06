CREATE TABLE if not exists AdminUser (
  username varchar(250) NOT NULL,
  password varchar(250) NOT NULL,
  first_name varchar(250) NOT NULL,
  last_name varchar(250) NOT NULL,
  PRIMARY KEY (username)
);

CREATE TABLE if not exists Manager (
  username varchar(250) NOT NULL,
  password varchar(250) NOT NULL,
  first_name varchar(250) NOT NULL,
  last_name varchar(250) NOT NULL,
  PRIMARY KEY (username)
);

CREATE TABLE if not exists SalesPeople (
  username varchar(250) NOT NULL,
  password varchar(250) NOT NULL,
  first_name varchar(250) NOT NULL,
  last_name varchar(250) NOT NULL,
  PRIMARY KEY (username)
);

CREATE TABLE if not exists InventoryClerk (
  username varchar(250) NOT NULL,
  password varchar(250) NOT NULL,
  first_name varchar(250) NOT NULL,
  last_name varchar(250) NOT NULL,
  PRIMARY KEY (username)
);

CREATE TABLE if not exists Vehicle (
  vin varchar(250) NOT NULL,
  vehicle_type varchar(250) NOT NULL,
  manufacturer_name varchar(250) NOT NULL,
  fuel_type varchar(250) NOT NULL,
  model_name varchar(250) NOT NULL,
  model_year numeric(4,0) NOT NULL,
  description varchar(2000) DEFAULT NULL, 
  mileage int4 NOT NULL,
  PRIMARY KEY (vin)
);

CREATE TABLE if not exists VehicleType (
  vehicle_type varchar(250) NOT NULL,
  PRIMARY KEY (vehicle_type)
);

CREATE TABLE if not exists VehicleManufacturer (
  manufacturer_name varchar(250) NOT NULL,
  PRIMARY KEY (manufacturer_name)
);

CREATE TABLE if not exists VehicleColor (
  color varchar(250) NOT NULL,
  vin varchar(250) NOT NULL,
  PRIMARY KEY (color,vin)
);

CREATE TABLE if not exists Customer (
  customer_id  uuid NOT NULL,
  street varchar(250) NOT NULL,
  city varchar(250) NOT NULL,
  state varchar(250) NOT NULL,
  postal_code varchar(250) NOT NULL,
  phone_number varchar(250) NOT NULL,
  PRIMARY KEY(customer_id)  
);

CREATE TABLE if not exists CustomerIndividual (
  drivers_license_number varchar(250) NOT NULL,
  customer_id uuid NOT NULL,
  first_name varchar(250) NOT NULL,
  last_name varchar(250) NOT NULL,
  PRIMARY KEY(drivers_license_number)
);

CREATE TABLE if not exists CustomerBusiness (
  tax_id_number varchar(250) NOT NULL,
  customer_id uuid NOT NULL,
  contact_name varchar(250) NOT NULL,
  title varchar(250) NOT NULL,
  PRIMARY KEY(tax_id_number)
);

CREATE TABLE if not exists Buy (
  customer_id uuid NOT NULL,
  vin varchar(250) NOT NULL,
  username varchar(250) NOT NULL,
  sale_date date NOT NULL,
  PRIMARY KEY(customer_id,vin,username)
);

CREATE TABLE if not exists Sell (
  customer_id uuid NOT NULL,
  vin varchar(250) NOT NULL,
  username varchar(250) NOT NULL,
  purchase_price integer NOT NULL,
  purchase_date date NOT NULL,
  vehicle_condition varchar(250) NOT NULL,
  PRIMARY KEY(customer_id,vin,username)
);

CREATE TABLE if not exists PartOrder (
  purchase_order_number varchar(250) UNIQUE NOT NULL,
  vin varchar(250) NOT NULL,
  part_vendor_name varchar(250) NOT NULL,
  username varchar(250) NOT NULL,
  total_cost integer NOT NULL,
  PRIMARY KEY(purchase_order_number,vin)
);

CREATE TABLE if not exists PartVendor(
  name varchar(250) NOT NULL,
  phone_number varchar(250) NOT NULL,
  street varchar(250) NOT NULL,
  city varchar(250) NOT NULL,
  state varchar(250) NOT NULL,
  postal_code varchar(250) NOT NULL,
  PRIMARY KEY(name)
);

CREATE TABLE if not exists Part (
  part_number varchar(250) NOT NULL,
  purchase_order_number varchar(250) NOT NULL,
  description varchar(250) DEFAULT NULL,
  status varchar(250) NOT NULL,
  cost integer NOT NULL,
  quantity integer NOT NULL,
  PRIMARY KEY(part_number)
);

ALTER TABLE Part
  ADD CONSTRAINT fk_Part_purchaseOrderNumber_PartOrder_purchaseOrderNumber FOREIGN KEY (purchase_order_number) REFERENCES PartOrder(purchase_order_number);
  
ALTER TABLE PartOrder
  ADD CONSTRAINT fk_PartOrder_partVendorName_PartVendor_name FOREIGN KEY (part_vendor_name) REFERENCES PartVendor(name),
  ADD CONSTRAINT fk_PartOrder_username_InventoryClerk_username FOREIGN KEY(username) REFERENCES InventoryClerk(username),
  ADD CONSTRAINT fk_PartOrder_vin_Vehicle_vin FOREIGN KEY (vin) REFERENCES Vehicle(vin);
  
ALTER TABLE Sell
  ADD CONSTRAINT fk_Sell_customerId_Customer_customerId FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
  ADD CONSTRAINT fk_Sell_vin_Vehicle_vin FOREIGN KEY (vin) REFERENCES Vehicle(vin),
  ADD CONSTRAINT fk_Sell_username_InventoryClerk_username FOREIGN KEY (username) REFERENCES InventoryClerk(username);
  
ALTER TABLE Buy
  ADD CONSTRAINT fk_Buy_customerId_Customer_customerId FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
  ADD CONSTRAINT fk_Buy_vin_Vehicle_vin FOREIGN KEY (vin) REFERENCES Vehicle(vin),
  ADD CONSTRAINT fk_Buy_username_SalesPeople_username FOREIGN KEY (username) REFERENCES SalesPeople (username);
  
ALTER TABLE CustomerBusiness
  ADD CONSTRAINT fk_CustomerBusiness_customerId_Customer_customerId FOREIGN KEY (customer_id) REFERENCES Customer(customer_id);
  
ALTER TABLE CustomerIndividual
  ADD CONSTRAINT fk_CustomerIndividual_customerId_Customer_customerId FOREIGN KEY (customer_id) REFERENCES Customer(customer_id);
  
ALTER TABLE VehicleColor
  ADD CONSTRAINT fk_VehicleColor_vin_Vehicle_vin FOREIGN KEY (vin) REFERENCES Vehicle(vin);
  
ALTER TABLE Vehicle
  ADD CONSTRAINT fk_Vehicle_vehicleType_VehicleType_vehicleType FOREIGN KEY (vehicle_type) REFERENCES VehicleType(vehicle_type),
  ADD CONSTRAINT fk_Vehicle_manufacturerName_VehicleManufacturer_manufacturerName FOREIGN KEY (manufacturer_name) REFERENCES VehicleManufacturer(manufacturer_name);

ALTER TABLE Sell
  ADD CONSTRAINT ck_Sell_vehicleCondition CHECK (vehicle_condition in ('Excellent', 'Very Good', 'Good', 'Fair'));

ALTER TABLE Vehicle
  ADD CONSTRAINT ck_Vehicle_modelYear_fourDigits CHECK (model_year <= date_part('year', current_date)::numeric::int + 1);
  
ALTER TABLE Part
  ADD CONSTRAINT ck_Part_status CHECK (status in ('Ordered', 'Received', 'Installed'));
  