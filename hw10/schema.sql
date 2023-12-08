-- Create the Request Table
CREATE TABLE request (
  request_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
  country VARCHAR(255), 
  client_ip VARCHAR(255), 
  gender ENUM('Male', 'Female'), 
  age ENUM(
    '0-16', '17-25', '26-35', '36-45', 
    '46-55', '56-65', '66-75', '76+'
  ), 
  income ENUM(
    '0-10k', '10k-20k', '20k-40k', '40k-60k', 
    '60k-100k', '100k-150k', '150k-250k', 
    '250k+'
  ), 
  is_banned BOOLEAN, 
  time_of_request TIMESTAMP, 
  requested_file VARCHAR(255)
);
-- Create the Failed Request Table
CREATE TABLE failed_request (
  failed_request_id INT AUTO_INCREMENT PRIMARY KEY, 
  time_of_request TIMESTAMP, 
  requested_file VARCHAR(255), 
  error_code INT
);
