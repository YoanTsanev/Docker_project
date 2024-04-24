use db;

-- Create a table for hotels
CREATE TABLE Hotels (
    HotelID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Address VARCHAR(255),
    City VARCHAR(100),
    Rating DECIMAL(3, 1)
);

-- Create a table for rooms
CREATE TABLE Rooms (
    RoomID INT PRIMARY KEY,
    HotelID INT,
    RoomNumber VARCHAR(20),
    Type VARCHAR(50),
    Price DECIMAL(10, 2),
    FOREIGN KEY (HotelID) REFERENCES Hotels(HotelID)
);

-- Create a table for guests
CREATE TABLE Guests (
    GuestID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100),
    Phone VARCHAR(20)
);

-- Create a table for reservations
CREATE TABLE Reservations (
    ReservationID INT PRIMARY KEY,
    GuestID INT,
    RoomID INT,
    CheckInDate DATE,
    CheckOutDate DATE,
    FOREIGN KEY (GuestID) REFERENCES Guests(GuestID),
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID)
);

-- Create a table for employees
CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100),
    Phone VARCHAR(20),
    Position VARCHAR(50),
    HotelID INT,
    FOREIGN KEY (HotelID) REFERENCES Hotels(HotelID)
);

-- Insert sample data into the Hotels table
INSERT INTO Hotels (HotelID, Name, Address, City, Rating)
VALUES
    (1, 'Grand Hotel', 'tsar Osvoboditel 1', 'Sofia', 4.5),
    (2, 'Ocean View Resort', 'Vasil Levski 15', 'Varna', 4.2),
    (3, 'Mountain Lodge', 'Nezavisimost 4', 'Veliko Tarnovo', 4.7);

-- Insert sample data into the Rooms table
INSERT INTO Rooms (RoomID, HotelID, RoomNumber, Type, Price)
VALUES
    (101, 1, '101', 'Standard', 150.00),
    (102, 1, '102', 'Standard', 150.00),
    (201, 2, '201', 'Ocean View', 200.00),
    (202, 2, '202', 'Ocean View', 200.00),
    (301, 3, '301', 'Deluxe Suite', 300.00),
    (302, 3, '302', 'Deluxe Suite', 300.00);

-- Insert sample data into the Guests table
INSERT INTO Guests (GuestID, FirstName, LastName, Email, Phone)
VALUES
    (1, 'John', 'Doe', 'john.doe@example.com', '123-456-7890'),
    (2, 'Jane', 'Smith', 'jane.smith@example.com', '987-654-3210'),
    (3, 'Alice', 'Johnson', 'alice.johnson@example.com', '111-222-3333');

-- Insert sample data into the Reservations table
INSERT INTO Reservations (ReservationID, GuestID, RoomID, CheckInDate, CheckOutDate)
VALUES
    (1, 1, 101, '2024.04.15', '2024.04.18'),
    (2, 2, 201, '2024.05.01', '2024.05.05'),
    (3, 3, 302, '2024.06.10', '2024.06.15');

-- Insert sample data into the Employees table
INSERT INTO Employees (EmployeeID, FirstName, LastName, Email, Phone, Position, HotelID)
VALUES
    (1, 'Michael', 'Smith', 'michael.smith@grandhotel.com', '555-123-4567', 'Manager', 1),
    (2, 'Emily', 'Johnson', 'emily.johnson@oceanviewresort.com', '555-234-5678', 'Front Desk Clerk', 2),
    (3, 'David', 'Brown', 'david.brown@mountainlodge.com', '555-345-6789', 'Concierge', 3);
