-- Create tables if they don't exist
CREATE TABLE IF NOT EXISTS `registration` (
  `Sr_No.` INT PRIMARY KEY,
  `First_Name` VARCHAR(100),
  `Last_Name` VARCHAR(100),
  `Email` VARCHAR(255),
  `Contact_No` VARCHAR(50),
  `Gender` VARCHAR(10),
  `Photo` LONGBLOB
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `attendance` (
  `srno` INT,
  `number` INT,
  `time` DATETIME
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
