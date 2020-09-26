-- ##########     WORK IN PROGRESS     ##########     


-- Incomplete: we will need to carefully go over the varchar lengths, what can and cannot be null, unique, etc.
-- NOTE: If we do it this way, maybe we can create 12 python scripts, one for each type of event.
        --That would allow us to break up the work more effectively.
CREATE DATABASE crossRefEventData;
USE crossRefEventData;


CREATE TABLE Main(
    -- Unique ID of each event
    UniqueEventID           VARCHAR(29) NOT NULL UNIQUE,
    Article_ID              INTEGER AUTO_INCREMENT,
    DOI                     VARCHAR(50),
    Article_Title           VARCHAR(120),
    Journal_Name            VARCHAR(40),
    Article_Date            DATE,
    Article_URL             VARCHAR(100),
    PRIMARY KEY(Article_ID)
);
--- Journal Table has been removed and merged with Main Table
--- We can use Python to parse the JSON author lists into Given_Name and Family_Name over time'
--- Are ORCIDs worth considering?'
CREATE TABLE Author(
    -- Given by us, increments automatically
    Author_ID               INTEGER AUTO_INCREMENT 
    Given_Name              VARCHAR(30),
    Family_Name             VARCHAR(30),
    PRIMARY KEY (Author_ID)
)

CREATE Article_to_Author(
    ArticleAuthorID         INTEGER,
    Article_ID              INTEGER,
    Author_ID               INTEGER,
    FOREIGN KEY (Article_ID)
    FOREIGN KEY (Author_ID)
)

--  Begin tables for 12 events -- 
CREATE TABLE Twitter_Event(
    -- Unique ID of each event
    UniqueEventID           VARCHAR(29) NOT NULL,
    -- Document Object Identifier, (obj_id) or the content
    DOI                     VARCHAR(50),
    -- Retweet author. If there isn't a retweet, this becomes the tweet author.
    twitterAuthor           VARCHAR(75),
    -- If not null, the tweet author is twitterAuthor 
    originalTweetAuthor     VARCHAR(40),
    -- 
    twitterIncrement        INTEGER AUTO_INCREMENT,
    timeOccured             TIMESTAMP,
    license                 VARCHAR(60),
    terms                   VARCHAR(50),
    -- URL to changes made to the data
    updated_reason          VARCHAR(100),
    updated                 VARCHAR(15),
    source_token            VARCHAR(29),
    evidence_record         VARCHAR(93),-- Hypothesis 105 chars
    actionByAgent           VARCHAR(10),
    --Captures retweet. If there is no retweet, captures tweet.
    subj_id                 VARCHAR(80),
    -- Captures retweet. If there is no retweet, captures tweet.
    pid                     VARCHAR(100),
    -- Original Tweet URL
    originalTweetURL        VARCHAR(100),
    -- Tweet #
    title                   VARCHAR(25),
    issued                  TIMESTAMP,
    -- Name of source that event came from
    source_id               VARCHAR(25),
    -- Same as DOI
    obj_pid                 VARCHAR(50),
    -- Same as DOI
    obj_url                 VARCHAR(50),
    -- Timestamp of when the Event was created
    eventCreationTime       TIMESTAMP,
    --  
    updated_date            DATETIME,
    -- Type of relation between subject and object
    relation_type_id        VARCHAR(10),
    
    PRIMARY KEY(UniqueEventID,twitterIncrement),
    FOREIGN KEY (UniqueEventID) REFERENCES Main(UniqueEventID)
    --FOREIGN KEY (DOI) REFERENCES DOI(DOI)
)

CREATE TABLE Wikipedia_Event(
    -- Unique ID of each event
    UniqueEventID           INTEGER NOT NULL,
    -- Document Object Identifier, (obj_id) or the content
    DOI                     VARCHAR(36),
    timeOccured             DATE,
    wikipediaAuthor         VARCHAR(36),
    wikipediaIncrement      INTEGER AUTO_INCREMENT,

    PRIMARY KEY (UniqueEventID),
    FOREIGN KEY (UniqueEventID) REFERENCES Main(UniqueEventID)
    --FOREIGN KEY (DOI) REFERENCES DOI(DOI)
)

CREATE TABLE Wordpress_Event(
    -- Unique ID of each event
    UniqueEventID           INTEGER NOT NULL,
    -- Document Object Identifier, (obj_id) or the content
    DOI VARCHAR(36),
    wordpressIncrement      INTEGER AUTO_INCREMENT,
    timeOccured             DATE,
    wordpressAuthor         VARCHAR(36),

    PRIMARY KEY (UniqueEventID),
    FOREIGN KEY (UniqueEventID) REFERENCES Event Main(UniqueEventID)
    --FOREIGN KEY (DOI) REFERENCES DOI(DOI)
)

CREATE TABLE StackExchange_Event(
    -- Unique ID of each event
    UniqueEventID           INTEGER NOT NULL,
    -- Document Object Identifier, (obj_id) or the content
    DOI                     VARCHAR(36),
    timeOccured             DATE,
    stackExchangeAuthor     VARCHAR(36),
    stackExchangeIncrement  INTEGER AUTO_INCREMENT,

    PRIMARY KEY (UniqueEventID),
    FOREIGN KEY (UniqueEventID) REFERENCES Event Main(UniqueEventID)
    --FOREIGN KEY (DOI) REFERENCES DOI(DOI)
)

CREATE TABLE RedditLinks_Event(
    -- Unique ID of each event
    UniqueEventID           INTEGER NOT NULL,
    -- Document Object Identifier, (obj_id) or the content
    DOI                     VARCHAR(36),
    timeOccured             DATE,
    redditLinksAuthor       VARCHAR(36),
    redditLinksIncrement    INTEGER AUTO_INCREMENT,

    PRIMARY KEY (UniqueEventID),
    FOREIGN KEY (UniqueEventID) REFERENCES Event Main(UniqueEventID)
    --FOREIGN KEY (DOI) REFERENCES DOI(DOI)
)

CREATE TABLE Reddit_Event(
    -- Unique ID of each event
    UniqueEventID           INTEGER NOT NULL,
    -- Document Object Identifier, (obj_id) or the content
    DOI                     VARCHAR(36),
    timeOccured             DATE,
    redditAuthor            VARCHAR(36),
    redditIncrement         INTEGER AUTO_INCREMENT,

    PRIMARY KEY (UniqueEventID),
    FOREIGN KEY (UniqueEventID) REFERENCES Event Main(UniqueEventID)
    --FOREIGN KEY (DOI) REFERENCES DOI(DOI)
)

CREATE TABLE Newsfeed_Event(
    -- Unique ID of each event
    UniqueEventID           INTEGER NOT NULL,
    -- Document Object Identifier, (obj_id) or the content
    DOI                     VARCHAR(36),
    timeOccured             DATE,
    NewsFeedAuthor          VARCHAR(36),
    newsfeedIncrement       INTEGER AUTO_INCREMENT,

    PRIMARY KEY (UniqueEventID),
    FOREIGN KEY (UniqueEventID) REFERENCES Event Main(UniqueEventID)
    --FOREIGN KEY (DOI) REFERENCES DOI(DOI)
)

CREATE TABLE theLens_Event(
    -- Unique ID of each event
    UniqueEventID           INTEGER NOT NULL,
    -- Document Object Identifier, (obj_id) or the content
    DOI                     VARCHAR(36),
    timeOccured             DATE,
    theLensAuthor           VARCHAR(36),
    theLensIncrement        INTEGER AUTO_INCREMENT,

    PRIMARY KEY (UniqueEventID),
    FOREIGN KEY (UniqueEventID) REFERENCES Event Main(UniqueEventID)
    --FOREIGN KEY (DOI) REFERENCES DOI(DOI)
)

CREATE TABLE Hypothesis_Event(
    -- Unique ID of each event
    UniqueEventID           INTEGER NOT NULL,
    -- Document Object Identifier, (obj_id) or the content
    DOI                     VARCHAR(36),
    timeOccured             DATE,
    HypothesisAuthor        VARCHAR(36),
    hypothesis              INTEGER AUTO_INCREMENT,

    PRIMARY KEY (UniqueEventID),
    FOREIGN KEY (UniqueEventID) REFERENCES Event Main(UniqueEventID)
    --FOREIGN KEY (DOI) REFERENCES DOI(DOI)
)

CREATE TABLE Cambria_Event(
    -- Unique ID of each event
    UniqueEventID           INTEGER NOT NULL,
    -- Document Object Identifier, (obj_id) or the content
    DOI                     VARCHAR(36),
    timeOccured             DATE,
    F1000                   VARCHAR(36),
    cambria                 INTEGER AUTO_INCREMENT,

    PRIMARY KEY (UniqueEventID),
    FOREIGN KEY (UniqueEventID) REFERENCES Event Main(UniqueEventID)
    --FOREIGN KEY (DOI) REFERENCES DOI(DOI)
)

CREATE TABLE DataCite_Event(
    -- Unique ID of each event
    UniqueEventID           INTEGER NOT NULL,
    -- Document Object Identifier, (obj_id) or the content
    DOI                     VARCHAR(36),
    timeOccured             DATE,
    dataCiteAuthor          VARCHAR(36),
    dataCiteIncrement       INTEGER AUTO_INCREMENT,

    PRIMARY KEY (UniqueEventID),
    FOREIGN KEY (UniqueEventID) REFERENCES Event Main(UniqueEventID)
    --FOREIGN KEY (DOI) REFERENCES DOI(DOI)
)

CREATE TABLE CrossrefMetadata_Event(
    -- Unique ID of each event
    UniqueEventID           INTEGER NOT NULL,
    -- Document Object Identifier, (obj_id) or the content
    DOI                     VARCHAR(36),
    timeOccured             DATE,
    crossrefMetadataAuthor VARCHAR(36),
    crossrefMetaDataIncrement INTEGER AUTO_INCREMENT,

    PRIMARY KEY (UniqueEventID),
    FOREIGN KEY (UniqueEventID) REFERENCES Event Main(UniqueEventID)
    --FOREIGN KEY (DOI) REFERENCES DOI(DOI)
)