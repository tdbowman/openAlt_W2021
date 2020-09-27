--   ##########     WORK IN PROGRESS     ##########     


--  Incomplete: we will need to carefully go over the varchar lengths, what can and cannot be null, unique, etc.
--  NOTE: If we do it this way, maybe we can create 12 python scripts, one for each type of event.
        -- That would allow us to break up the work more effectively.
CREATE DATABASE crossRefEventData;
USE crossRefEventData;



CREATE TABLE Main(
    -- Document Object Identifier or the content that was registered at CrossRef. This field was obj_id.
    DOI                     VARCHAR(70),
    -- Unique ID of each event.
    UniqueEventID           VARCHAR(36) NOT NULL UNIQUE,
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

CREATE TABLE CrossRefEvent
(

    -- Auto increment for easy primary keys
    crossRefIncrement INTEGER AUTO_INCREMENT PRIMARY KEY,

    --  Foreign key to reference the doi
    FOREIGN KEY (eventID) REFERENCES Main(UniqueEventID),

    --  --  -############################--  --  -COLUMNS--  ###############################--  --  -
    
    --  Author
    DOIAuthor VARCHAR(36),

    --  License provided by each service (CrossRef, DataCite, etc). Could be null(?)
    crossrefLicense VARCHAR(60),

    --  Link to the scholarly writing
    objectID VARCHAR(100),

    --  The source token identifies the Agent that processed the data to produce an Event
    sourceToken VARCHAR(36),

    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601
    occurredAt TIMESTAMP,

    --  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event
    subjectID VARCHAR(100),

    --  Every event is assigned a unique ID. Used for reference.
    eventID VARCHAR(36),

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    crossrefTermsOfUse VARCHAR(45),

    --  The status of the message containing a list of events (message created, updated, deleted, etc.)
    messageAction VARCHAR(15),

    --  The original source of the input data. Source could be any of the 12 sources listed in CrossRef's guide.
    sourceID VARCHAR (20),

    --  Timestamp shortly after the event was observed, CONFORMS TO ISO8601
    timeObserved TIMESTAMP,

    --  Type of relationship between the subject and the object. String (varchar)
    relationType VARCHAR (20)

);

CREATE TABLE IF NOT EXISTS RedditEvent(   

    --  Auto increment for easy primary keys
    redditIncrement INTEGER AUTO_INCREMENT PRIMARY KEY,

    --  Foreign key to reference the doi
    FOREIGN KEY (eventID) REFERENCES Main(UniqueEventID),

    --  --  -############################--  --  -COLUMNS--  ###############################--  --  -
    --  Author
    DOIAuthor VARCHAR(36),

    --  License provided by service
    license VARCHAR(70),

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    termsOfUse VARCHAR (45),

    --  Reason for updating an event. Optional, may point to an announcement page explaining the edit
    updatedReason VARCHAR (100),

    --  Updated (Kind of boolean) states whether the event was edited or deleted 
    updated VARCHAR(10),

    --  Updated date
    updatedDate TIMESTAMP,

    --  ID of the scholarly writing
    objectID VARCHAR(100),

    --  URL of the scholarly writing
    objectURL VARCHAR (100),

    --  The source token identifies the Agent that processed the data to produce an Event
    sourceToken VARCHAR(36),

    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601
    occurredAt TIMESTAMP,

    --  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event
    subjectID VARCHAR(100),

    --  Every event is assigned a unique ID. Used for reference.
    eventID VARCHAR(36) NOT NULL,

    --  Evidence record contains all of the information used to create an event.
    evidenceRecord VARCHAR(100),

    --  Action is the nature of the event, such as adding a comment, in which case the action is "add"
    eventAction VARCHAR(15),

     --  The original source of the input data. Source could be any of the 12 sources listed in CrossRef's guide.
    sourceID VARCHAR (20),

    --  The ID of the entity mentioning the DOI
    subjectPID VARCHAR (80),

    --  The title of the subject
    subjectTitle VARCHAR(60),

    --  Date the subject issued the mention
    subjectIssuedDate TIMESTAMP,

    --  Author of the event
    subjectAuthorURL VARCHAR(50),

    --  Original tweet (if retweeted)
    subjectOriginalTweetURL VARCHAR (80),

    --  Author of the original tweet (if retweeted)
    subjectOriginalTweetAuthor VARCHAR(50),

    --  ID of the original tweet (if retweeted)
    alternativeID VARCHAR(20),

    --  Timestamp shortly after the event was observed, CONFORMS TO ISO8601
    timeObserved TIMESTAMP,

    --  Type of relationship between the subject and the object. String (varchar)
    relationType VARCHAR (20)
    
    );



    CREATE TABLE IF NOT EXISTS StackexchangeEvent(

    --  Auto increment for easy primary keys
    stackExchangeIncrement INTEGER AUTO_INCREMENT PRIMARY KEY,

    --  Foreign key to reference the doi
    FOREIGN KEY (eventID) REFERENCES Main(UniqueEventID),



    --  --  -############################--  --  -COLUMNS--  ###############################--  --  -
    
    --  Author
    DOIAuthor VARCHAR(36),

    --  License provided by each service (CrossRef, DataCite, etc). Could be null(?)
    license VARCHAR(60),

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    termsOfUse VARCHAR (45),

    --  Link to the scholarly writing
    objectID VARCHAR(100),

    --  The source token identifies the Agent that processed the data to produce an Event
    sourceToken VARCHAR(36),

    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601
    occurredAt TIMESTAMP,

    --  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event
    subjectID VARCHAR(100),

    --  Every event is assigned a unique ID. Used for reference.
    eventID VARCHAR(36) NOT NULL,

    --  Evidence record contains all of the information used to create an event.
    evidenceRecord VARCHAR(150),

    --  The ID of the entity mentioning the DOI
    subjectPID VARCHAR (80),

    --  The title of the subject
    subjectTitle VARCHAR(60),

    --  Date the subject issued the mention
    subjectIssuedDate TIMESTAMP,

    --  Type of the subject (post, comment, etc.)
    subjectType VARCHAR(20),

    --  Subject author's URL
    subjectAuthorURL VARCHAR(50),

    --  Subject author's name
    subjectAuthorName VARCHAR(30),

    --  Subject author's ID
    subjectAuthorID INTEGER (10),

    --  The original source of the input data. Source could be any of the 12 sources listed in CrossRef's guide.
    sourceID VARCHAR (20),

    --  PID of the object (DOI being discussed)
    objectPID VARCHAR(80),

    --  URL of the doi being discussed
    objectURL VARCHAR(80),

    --  Timestamp shortly after the event was spotted
    timeObserved TIMESTAMP,

    --  Nature of the discussion on the doi (discusses, mentions, etc.)
    relationType VARCHAR(20)

    );

    CREATE TABLE IF NOT EXISTS WikipediaEvent(

    --  Auto increment for easy primary keys
    wikipediaIncrement INTEGER AUTO_INCREMENT PRIMARY KEY,

    --  Foreign key to reference the doi
    FOREIGN KEY (eventID) REFERENCES Main(UniqueEventID),

    --  --  -############################--  --  -COLUMNS--  ###############################--  --  -
    
    --  Author
    DOIAuthor VARCHAR(36),

    --  License provided by each service (CrossRef, DataCite, etc). Could be null(?)
    license VARCHAR(60),

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    termsOfUse VARCHAR (45),

    --  Updated date
    updatedDate TIMESTAMP,

    --  Reason for updating an event. Optional, may point to an announcement page explaining the edit
    updatedReason VARCHAR (100),

    --  Link to the scholarly writing
    objectID VARCHAR(100),

    --  The source token identifies the Agent that processed the data to produce an Event
    sourceToken VARCHAR(36),

    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601
    occurredAt TIMESTAMP,

    --  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event
    subjectID VARCHAR(100),

    --  Every event is assigned a unique ID. Used for reference.
    eventID VARCHAR(36) NOT NULL,

    --  Evidence record contains all of the information used to create an event.
    evidenceRecord VARCHAR(150),

    --  Action is the nature of the event, such as adding a comment, in which case the action is "add"
    eventAction VARCHAR(15),

    --  The ID of the entity mentioning the DOI
    subjectPID VARCHAR (80),

    --  The title of the subject
    subjectTitle VARCHAR(60),

    --  Author of the event
    subjectURL VARCHAR(100),

    --  Type of the subject (post, comment, etc.)
    subjectAPIURL VARCHAR(70),

    --  The original source of the input data. Source could be any of the 12 sources listed in CrossRef's guide.
    sourceID VARCHAR (20),

    --  PID of the object (DOI being discussed)
    objectPID VARCHAR(80),

    --  URL of the doi being discussed
    objectURL VARCHAR(80),

    --  Timestamp shortly after the event was spotted
    timeObserved TIMESTAMP,

    --  Nature of the discussion on the doi (discusses, mentions, etc.)
    relationType VARCHAR(20)

    );

    CREATE TABLE IF NOT EXISTS WordPressEvent(

    --  Auto increment for easy primary keys
    wordPressIncrement INTEGER AUTO_INCREMENT PRIMARY KEY,

    --  Foreign key to reference the doi
    FOREIGN KEY (eventID) REFERENCES Main(UniqueEventID),

    --  --  -############################--  --  -COLUMNS--  ###############################--  --  -
    
    --  Author
    DOIAuthor VARCHAR(36),

    --  License provided by each service (CrossRef, DataCite, etc). Could be null(?)
    license VARCHAR(60),

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    termsOfUse VARCHAR (45),

    --  Updated date
    updatedDate TIMESTAMP,

    --  Reason for updating an event. Optional, may point to an announcement page explaining the edit
    updatedReason VARCHAR (100),

    --  Link to the scholarly writing
    objectID VARCHAR(100),

    --  The source token identifies the Agent that processed the data to produce an Event
    sourceToken VARCHAR(36),

    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601
    occurredAt TIMESTAMP,

    --  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event
    subjectID VARCHAR(100),

    --  Every event is assigned a unique ID. Used for reference.
    eventID VARCHAR(36) NOT NULL,

    --  Evidence record contains all of the information used to create an event.
    evidenceRecord VARCHAR(150),

    --  Action is the nature of the event, such as adding a comment, in which case the action is "add"
    eventAction VARCHAR(15),

    --  The ID of the entity mentioning the DOI
    subjectPID VARCHAR (80),

    --  The title of the subject
    subjectTitle VARCHAR(60),

    --  Author of the event
    subjectType VARCHAR(100),

    --  The original source of the input data. Source could be any of the 12 sources listed in CrossRef's guide.
    sourceID VARCHAR (20),

    --  PID of the object (DOI being discussed)
    objectPID VARCHAR(80),

    --  URL of the doi being discussed
    objectURL VARCHAR(80),

    --  Timestamp shortly after the event was spotted
    timeObserved TIMESTAMP,

    --  Nature of the discussion on the doi (discusses, mentions, etc.)
    relationType VARCHAR(20)

    );

    CREATE TABLE IF NOT EXISTS DataCiteEvent(

    --   Auto increment for easy primary keys
    dataCiteIncrement INTEGER AUTO_INCREMENT PRIMARY KEY,

    --   Foreign key to reference the doi
    FOREIGN KEY (eventID) REFERENCES Main(UniqueEventID),

    --  --  -############################--  --  -COLUMNS--  ###############################--  --  -
    
    --  Author
    DOIAuthor VARCHAR(36),

    --  License provided by each service (CrossRef, DataCite, etc). Could be null(?)
    license VARCHAR(60),

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    termsOfUse VARCHAR (45),

    --  Link to the scholarly writing
    objectID VARCHAR(100),

    --  The source token identifies the Agent that processed the data to produce an Event
    sourceToken VARCHAR(36),

    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601
    occurredAt TIMESTAMP,

    --  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event
    subjectID VARCHAR(100),

    --  Every event is assigned a unique ID. Used for reference.
    eventID VARCHAR(36) NOT NULL,

    --  Timestamp shortly after the event was spotted
    timeObserved TIMESTAMP,

    --  Nature of the discussion on the doi (discusses, mentions, etc.)
    relationType VARCHAR(20),

    --  The original source of the input data. Source could be any of the 12 sources listed in CrossRef's guide.
    sourceID VARCHAR (20)

    );