-- Author: Darpan (whole file)
/*
MIT License

Copyright (c) 2020 tdbowman-CompSci-F2020

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
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
     
        
    PRIMARY KEY(id)
);
