CREATE TABLE Main(
    -- Document Object Identifier or the content that was registered at CrossRef. This field was obj_id.
    DOI                     VARCHAR(70),
    -- Unique ID of each event.
    event_id                VARCHAR(36) NOT NULL UNIQUE,
    Article_ID              INTEGER AUTO_INCREMENT UNIQUE,   
    Article_Title           VARCHAR(120),
    Journal_Name            VARCHAR(40),
    Article_Date            DATE,
    Article_URL             VARCHAR(100),
    PRIMARY KEY(DOI)
);
-- Journal Table has been removed and merged with Main Table
-- We can use Python to parse the JSON author lists into Given_Name and Family_Name over time'
-- Are ORCIDs worth considering?'
CREATE TABLE Author(
    -- Given by us, increments automatically
    Author_ID               INTEGER AUTO_INCREMENT, 
    Given_Name              VARCHAR(30),
    Family_Name             VARCHAR(30),
    PRIMARY KEY (Author_ID)
);

CREATE TABLE Article_to_Author(
    ArticleAuthorID         INTEGER,
    Article_ID              INTEGER,
    Author_ID               INTEGER,
    FOREIGN KEY (Article_ID) REFERENCES Main(Article_ID),
    FOREIGN KEY (Author_ID) REFERENCES Author(Author_ID)
);