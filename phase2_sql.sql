CREATE TABLE IF NOT  EXISTS User
	(Username	VARCHAR(50)	NOT NULL,
	 Password	VARCHAR(50)	NOT NULL,
	 Firstname	VARCHAR(50)	NOT NULL,
	 Lastname	VARCHAR(50)	NOT NULL,
	 Status		VARCHAR(20)	NOT NULL,
	 PRIMARY KEY (Username));
-- Note: we assume the validation of email and password occurs in the front-end application instead of here.

CREATE TABLE IF NOT  EXISTS Employee
(EmployeeID     VARCHAR(50)           NOT NULL,
 Phone               CHAR(10)                  NOT NULL,
 Address            VARCHAR(50)           NOT NULL,
 City                   VARCHAR(20)           NOT NULL,
 State                 CHAR(2)                    NOT NULL,
 Zipcode             CHAR(5)                   NOT NULL,
 Username	  VARCHAR(50)	 NOT NULL,
 EmployeeType  VARCHAR(20)          NOT NULL,
 PRIMARY KEY (EmployeeID),
 UNIQUE (Phone),
 FOREIGN KEY (Username) 
REFERENCES User(Username)
ON DELETE CASCADE
ON UPDATE CASCADE);

CREATE TABLE IF NOT  EXISTS Site
	(Site_Name            VARCHAR(50)              NOT NULL,
 EmployeeID          VARCHAR(50)              NOT NULL,
	 Address                VARCHAR(50),              
	 Zipcode                CHAR(5)                       NOT NULL,
 OpenEveryDay     BOOLEAN                    NOT NULL,
 PRIMARY KEY (Site_Name),
 FOREIGN KEY (EmployeeID) 
REFERENCES Employee(EmployeeID)
ON DELETE RESTRICT
ON UPDATE CASCADE);

CREATE TABLE IF NOT  EXISTS Event
	(Event_Name	VARCHAR(50)	NOT NULL,
	 Site_Name	VARCHAR(50)	NOT NULL,
	 StartDate	DATE			NOT NULL,
	 EndDate	DATE			NOT NULL,
	 Price		INT			NOT NULL,
	 Capacity	INT			NOT NULL,
	 Description	VARCHAR(500)	NOT NULL,
 MinStaffReq	INT	NOT NULL,
PRIMARY KEY (Event_Name, Site_Name, StartDate),
FOREIGN KEY (Site_Name) 
REFERENCES Site(Site_Name)
ON DELETE CASCADE
ON UPDATE CASCADE);	 

CREATE TABLE IF NOT  EXISTS Email
	(Username	VARCHAR(50)	NOT NULL,
	 Email		VARCHAR(50)	NOT NULL,
	 PRIMARY KEY (Username),
	 UNIQUE(Email),
	 FOREIGN KEY (Username) 
REFERENCES User(Username)
ON DELETE CASCADE
ON UPDATE CASCADE);


CREATE TABLE IF NOT  EXISTS Assign_To
	(EmployeeID	VARCHAR(50)	NOT NULL,
	 Event_Name	VARCHAR(50)	NOT NULL,
 	 StartDate	DATE			NOT NULL,
	Site_Name	VARCHAR(50)	NOT NULL,
PRIMARY KEY (EmployeeID, Event_Name, StartDate, Site_Name),
FOREIGN KEY (EmployeeID) 
REFERENCES Employee(EmployeeID)
ON DELETE CASCADE
ON UPDATE CASCADE,
 FOREIGN KEY (Event_Name,  Site_Name,StartDate) 
REFERENCES  Event(Event_Name, Site_Name,StartDate)
ON DELETE CASCADE
ON UPDATE CASCADE);
-- NOTE: even if we remove the staff, we would want to know the event happened in the past (for visitors’ event history, etc.) Also, staff is not a component of primary key. Therefore, we would want to set null for foreign key EmployeeID.


CREATE TABLE IF NOT  EXISTS Visit_Event 
	(Date                     DATE                  	         NOT NULL,
	 Site_Name            VARCHAR(50)              NOT NULL,
 StartDate	       DATE	                     NOT NULL,
 Username	VARCHAR(50)	NOT NULL,
 Event_Name	       VARCHAR(50)	         NOT NULL,
	 PRIMARY KEY (Date, Event_Name, Username, Site_Name, StartDate),
FOREIGN KEY (Event_Name,  Site_Name,StartDate) 
REFERENCES  Event(Event_Name, Site_Name,StartDate)
ON DELETE CASCADE
ON UPDATE CASCADE,
 FOREIGN KEY (Username) 
REFERENCES User(Username)
ON DELETE CASCADE
ON UPDATE CASCADE);


CREATE TABLE IF NOT  EXISTS Visit_Site
	(Date               DATE			NOT NULL,
	 Site_Name	VARCHAR(50)	NOT NULL,
	 Username	VARCHAR(50)	NOT NULL,
	 PRIMARY KEY (Date, Site_Name, Username),
 FOREIGN KEY (Site_Name) 
REFERENCES Site(Site_Name)
ON DELETE CASCADE
ON UPDATE CASCADE,
 FOREIGN KEY (Username) 
REFERENCES User(Username)
ON DELETE CASCADE
ON UPDATE CASCADE);


CREATE TABLE IF NOT  EXISTS Transit
	(Type		VARCHAR(10)	NOT NULL,
	 Route		VARCHAR(10)	NOT NULL,
	 Price		INT			NOT NULL,
	 PRIMARY KEY (Type, Route));


CREATE TABLE IF NOT  EXISTS Connect
(Type		VARCHAR(10)	NOT NULL,
 Route		VARCHAR(10)	NOT NULL,
 Site_Name      VARCHAR(50)           NOT NULL,   
 PRIMARY KEY (Type, Route, Site_Name), 
 FOREIGN KEY (Type, Route) 
REFERENCES Transit (Type, Route)
ON DELETE CASCADE
ON UPDATE CASCADE,
 FOREIGN KEY (Site_Name) 
REFERENCES Site (Site_Name)
ON DELETE CASCADE
ON UPDATE CASCADE);        

CREATE TABLE IF NOT  EXISTS Take	
	(Date		DATE			NOT NULL,
	 Type		VARCHAR(10)	NOT NULL,
	 Route		VARCHAR(10)	NOT NULL,
	 Username	VARCHAR(10)	NOT NULL,
 PRIMARY KEY (Date, Type, Route, Username),
	 FOREIGN KEY (Type, Route) 
REFERENCES Transit (Type, Route)
ON DELETE CASCADE
ON UPDATE CASCADE,
 FOREIGN KEY (Username) 
REFERENCES User(Username)
ON DELETE CASCADE
ON UPDATE CASCADE);