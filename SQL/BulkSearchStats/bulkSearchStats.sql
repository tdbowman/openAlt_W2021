CREATE DATABASE bulkSearchStats;
USE bulkSearchStats;

CREATE TABLE IF NOT EXISTS bulkSearch
(
	-- To uniquely identify each record
    id					BIGINT AUTO_INCREMENT,
    
	-- To identify the user by their provided email.
	email				varchar(255),
    
    -- Type of bulksearch (DOI, Author, Uni);
    type 				varchar(10),
    
    -- Timestamp to check how many times they have used in x amount of time
    time 			datetime default current_timestamp,
    
    -- UNIX time stamp
    timestamp 		timestamp default current_timestamp,
    
    
    
    PRIMARY KEY(id)
);
