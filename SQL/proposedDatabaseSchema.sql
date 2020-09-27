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
    
<<<<<<< Updated upstream
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
=======
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
    subjectAuthorID INTEGER,

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

    --  Begin tables for 12 events -- 
-- Research documentation for comments on some fields
CREATE TABLE Twitter_Event(
    -- Uniquely identify each row.
    twitter_increment        INTEGER AUTO_INCREMENT,
    -- Unique ID of each event.
    event_id                VARCHAR(36) NOT NULL UNIQUE,
    -- Document Object Identifier or the content that was registered at CrossRef. This field was obj_id.
    DOI                     VARCHAR(50),
    -- Retweet author. If there isn't a retweet, this becomes the tweet author. Can be null.
    twitter_author          VARCHAR(75),
    -- If not null, the tweet author is twitterAuthor. Can be null.
    original_tweet_author   VARCHAR(75),
    -- Timestamp of when the Event was reported to have occurred. This field was 'occurred_at'.
    time_occurred           TIMESTAMP NOT NULL,
    -- A license under which the Event is made available.
    license                 VARCHAR(70) NOT NULL,
    -- Terms of using the API at the point that you acquire the Event.
    terms                   VARCHAR(70) NOT NULL,
    -- Link to URL to changes made to the data.
    updated_reason          VARCHAR(100) NOT NULL,
    -- If an Event is updated, it will have the value of deleted or edited.
    updated                 VARCHAR(10) NOT NULL,
    -- An id that identifies the Agent that made the Event.
    source_token            VARCHAR(40) NOT NULL,
    -- Includes a link to an Evidence Record for this Event. This is used to generate an Event and contains all of the information used to create the Event. 
    evidence_record         VARCHAR(100) NOT NULL,
    -- An action performed by the Agent.
    action_by_agent           VARCHAR(10) NOT NULL,
    -- Captures retweet. If there is no retweet, captures tweet. If value is just 'http://twitter.com', everything within subject is NULL.
    subj_id                 VARCHAR(80) NOT NULL,
    -- Same value as subj_id.If no tweet or retweet exists, turns into NULL. Can be NULL. This field is within subject.
    subj_pid                VARCHAR(80),
    -- Original Tweet URL. If tweet doesn't exist but retweet does, stores retweet URL.  Can be NULL. This field is within subject.
    originalTweetURL        VARCHAR(80),
    -- id given to each tweet or retweet by Twitter. Can be NULL. This field is within subject.
    alternative_id          VARCHAR(20),
    -- Contains the value "tweet" and an alternative_id. Can be NULL. This field originally was title field. This field is within subject. 
    tweet_label             VARCHAR(25),
    -- Same value as time_occurred. Can be NULL. This field is within subject.
    issued                  TIMESTAMP,
    -- Name of source that event came from.
    source_id               VARCHAR(25) NOT NULL,
    -- Same value as the DOI.
    obj_pid                 VARCHAR(50) NOT NULL,
    -- Same as the DOI.
    obj_url                 VARCHAR(50) NOT NULL,
    -- Timestamp of when the Event was created. This field was originally called timestamp.
    event_creation_time     TIMESTAMP NOT NULL,
    -- Date and time of when the Event was updated. **DATE AND TIME different from updated_reason for some reason?**
    updated_date            DATETIME NOT NULL,
    -- Type of relation between subject and object.
    relation_type_id        VARCHAR(10) NOT NULL,
    PRIMARY KEY(twitter_increment),
    FOREIGN KEY (event_id) REFERENCES Main(UniqueEventID) ON DELETE CASCADE,
    FOREIGN KEY (DOI) REFERENCES Main(DOI) ON DELETE CASCADE
);

-- Research documentation for comments on some fields
CREATE TABLE RedditLinks_Event(
    -- To uniquely identify each row.
    reddit_links_increment  INTEGER AUTO_INCREMENT,
    -- Unique ID of each event.
    event_id                VARCHAR(36) NOT NULL UNIQUE,
    -- Document Object Identifier or the content that was registered at CrossRef. This field was obj_id.
    DOI                     VARCHAR(70),
    -- Timestamp of when the Event was reported to have occurred. This field was 'occurred_at'.
    time_occurred           TIMESTAMP NOT NULL,
    -- A license under which the Event is made available.
    license                 VARCHAR(60) NOT NULL,
    -- Terms of using the API at the point that you acquire the Event.
    terms                   VARCHAR(50) NOT NULL,
    -- Link to URL to changes made to the data.
    updated_reason          VARCHAR(90) NOT NULL,
    -- If an Event is updated, it will have the value of deleted or edited.
    updated                 VARCHAR(10) NOT NULL,
    -- An id that identifies the Agent that made the Event.
    source_token            VARCHAR(40) NOT NULL,
    -- The Canonical URL of a webpage, if one is available. If not, then it's a URL of a webpage.
    subj_id                 VARCHAR(200) NOT NULL,
    -- Includes a link to an Evidence Record for this Event. This is used to generate an Event and contains all of the information used to create the Event.
    evidence_record         VARCHAR(110) NOT NULL,
    -- An action performed by the Agent.
    action_by_agent         VARCHAR(10) NOT NULL,
    -- Same as subj_id
    subj_pid                VARCHAR(200) NOT NULL,
    -- Sometimes the same as subj_id, sometimes not...
    subj_url                VARCHAR(200) NOT NULL,
    -- Name of source that event came from.
    source_id               VARCHAR(20) NOT NULL,
    -- Same as obj_id
    obj_pid                 VARCHAR(70) NOT NULL,
    -- Sometimes the same as subj_id, sometimes not...
    obj_url                 VARCHAR(120) NOT NULL,
    -- Timestamp of when the Event was created. This field was originally called timestamp.
    event_creation_time     TIMESTAMP NOT NULL,
    -- **TIMESTAMP OR DATETIME**
    updated_date            DATETIME NOT NULL,
    -- Type of relation between subject and object.
    relation_type_id        VARCHAR(15) NOT NULL,
    -- redditLinksAuthor     VARCHAR(36),

    PRIMARY KEY (reddit_links_increment),
    FOREIGN KEY (event_id) REFERENCES Main(UniqueEventID) ON DELETE CASCADE,
    FOREIGN KEY (DOI) REFERENCES Main(DOI) ON DELETE CASCADE
);



CREATE TABLE Newsfeed_Event(
    -- To uniquely identify each row.
    newsfeed_increment      INTEGER AUTO_INCREMENT,
    -- Unique ID of each event.
    event_id                VARCHAR(36) UNIQUE NOT NULL,
    -- Document Object Identifier or the content that was registered at CrossRef. This field was obj_id.
    DOI                     VARCHAR(70),
    -- Timestamp of when the Event was reported to have occurred. This field was 'occurred_at'.
    time_occurred           TIMESTAMP NOT NULL,
    -- A license under which the Event is made available.
    license                 VARCHAR(60) NOT NULL,
    -- Terms of using the API at the point that you acquire the Event.
    terms                   VARCHAR(50) NOT NULL,
    -- Link to URL to changes made to the data.Can be NULL.
    updated_reason          VARCHAR(90),
    -- If an Event is updated, it will have the value of deleted or edited.
    updated                 VARCHAR(10) NOT NULL,
    -- An id that identifies the Agent that made the Event.
    source_token            VARCHAR(40) NOT NULL,
    subj_id                 VARCHAR(200),
    -- Includes a link to an Evidence Record for this Event. This is used to generate an Event and contains all of the information used to create the Event.
    evidence_record         VARCHAR(110) NOT NULL,
    -- An action performed by the Agent.
    action_by_agent         VARCHAR(10) NOT NULL,
    -- Same value as subj_id.
    subj_pid                VARCHAR(200) NOT NULL,
    subj_type               VARCHAR(12) NOT NULL,
    subj_title              VARCHAR(125) NOT NULL,
    -- Same value as subj_id.
    subj_url                VARCHAR(200) NOT NULL,
    -- Name of source that event came from.
    source_id               VARCHAR(10) NOT NULL,
    -- Same as DOI.
    obj_pid                 VARCHAR(70) NOT NULL,
    -- Sometimes same as DOI.
    obj_url                 VARCHAR(200) NOT NULL,
    -- Timestamp of when the Event was created. This field was originally called timestamp.
    event_creation_time     TIMESTAMP NOT NULL,
    -- Can be null.
    updated_date            DATETIME,
    -- Type of relation between subject and object.
    relation_type_id        VARCHAR(10) NOT NULL,

    -- NewsFeedAuthor        VARCHAR(36),
    PRIMARY KEY (newsfeed_increment),
    FOREIGN KEY (event_id) REFERENCES Main(UniqueEventID),
    FOREIGN KEY (DOI) REFERENCES Main(DOI)
);


-- Research documentation for comments on some fields
CREATE TABLE Hypothesis_Event(
    -- To uniquely identify each row.
    hypothesis_increment    INTEGER AUTO_INCREMENT,
    -- Unique ID of each event.
    event_id                VARCHAR(36) UNIQUE NOT NULL,
    -- Document Object Identifier or the content that was registered at CrossRef. This field was obj_id.
    DOI                     VARCHAR(60),
    -- Timestamp of when the Event was reported to have occurred. This field was 'occurred_at'.
    time_occurred           TIMESTAMP NOT NULL,
    -- A license under which the Event is made available.
    license                 VARCHAR(60) NOT NULL,
    -- An id that identifies the Agent that made the Event.
    source_token            VARCHAR(40) NOT NULL,
    -- The Canonical URL of a webpage, if one is available. If not, then it's a URL of a webpage.
    subj_id                 VARCHAR(50) NOT NULL,
    -- Includes a link to an Evidence Record for this Event. This is used to generate an Event and contains all of the information used to create the Event.
    evidence_record         VARCHAR(120) NOT NULL,
    -- Terms of using the API at the point that you acquire the Event.
    terms                   VARCHAR(50) NOT NULL,
    -- An action performed by the Agent.
    action_by_agent         VARCHAR(10) NOT NULL,
    -- Same value as subj_id
    subj_pid                VARCHAR(50) NOT NULL,
    subj_json_url           VARCHAR(70) NOT NULL,
    subj_url                VARCHAR(150) NOT NULL,
    subj_type               VARCHAR(15) NOT NULL,
    -- Can be NULL/empty string.
    subj_title              VARCHAR(1030),
    subj_issued             TIMESTAMP NOT NULL,
    -- Name of source that event came from.
    source_id               VARCHAR(15) NOT NULL,
    -- Same value as obj_id
    obj_pid                 VARCHAR(60) NOT NULL,
    obj_url                 VARCHAR(100) NOT NULL,
    -- Timestamp of when the Event was created. This field was originally called timestamp.
    event_creation_time     TIMESTAMP NOT NULL,
    -- Type of relation between subject and object.
    relation_type_id        VARCHAR(15) NOT NULL,
    -- HypothesisAuthor      VARCHAR(36),
    PRIMARY KEY (hypothesis_increment),
    FOREIGN KEY (event_id) REFERENCES Main(UniqueEventID) ON DELETE CASCADE,
    FOREIGN KEY (DOI) REFERENCES Main(DOI) ON DELETE CASCADE
);
-- Research documentation for comments on some fields
CREATE TABLE Cambia_Event(
    -- To uniquely identify each row.
    cambia_increment        INTEGER AUTO_INCREMENT,
    -- Unique ID of each event.
    event_id                VARCHAR(36) UNIQUE NOT NULL,
    -- Document Object Identifier or the content that was registered at CrossRef. This field was obj_id.
    DOI                     VARCHAR(60) NOT NULL,
    -- A license under which the Event is made available.
    license                 VARCHAR(55) NOT NULL,
    -- Link to URL to changes made to the data.
    updated_reason          VARCHAR(100) NOT NULL,
    -- If an Event is updated, it will have the value of deleted or edited.
    updated                 VARCHAR(10) NOT NULL,
    -- An id that identifies the Agent that made the Event.
    source_token            VARCHAR(40) NOT NULL,
    -- Timestamp of when the Event was reported to have occurred. This field was 'occurred_at'.
    time_occurred           TIMESTAMP NOT NULL,
    -- The Canonical URL of a webpage, if one is available. If not, then it's a URL of a webpage.
    subj_id                 VARCHAR(40) NOT NULL,
    -- Terms of using the API at the point that you acquire the Event.
    terms                   VARCHAR(50) NOT NULL,
    -- An action performed by the Agent.
    action_by_agent         VARCHAR(10) NOT NULL,
    work_subtype_id         VARCHAR(25) NOT NULL,
    work_type_id            VARCHAR(10) NOT NULL,
    subj_title              VARCHAR(140) NOT NULL,
    -- Same value as subj_id.
    subj_pid                VARCHAR(40) NOT NULL,
    jurisdiction            VARCHAR(5) NOT NULL,
    -- Name of source that event came from.
    source_id               VARCHAR(15) NOT NULL,
    -- Timestamp of when the Event was created. This field was originally called timestamp.
    event_creation_time     TIMESTAMP NOT NULL,
    updated_date            TIMESTAMP NOT NULL,
    -- Type of relation between subject and object.
    relation_type_id        VARCHAR(10) NOT NULL,        
    -- cambiaAuthor          VARCHAR(36),
    PRIMARY KEY (cambia_increment),
    FOREIGN KEY (event_id) REFERENCES Main(UniqueEventID) ON DELETE CASCADE,
    FOREIGN KEY (DOI) REFERENCES Main(DOI) ON DELETE CASCADE
);

-- Research documentation for comments on some fields
CREATE TABLE Web_Event(
    -- To uniquely identify each row.
    web_increment           INTEGER AUTO_INCREMENT,
    -- Unique ID of each event.
    event_id                VARCHAR(36) UNIQUE NOT NULL,
    -- Document Object Identifier or the content that was registered at CrossRef. This field was obj_id.
    DOI                     VARCHAR(60) NOT NULL,
    -- Timestamp of when the Event was reported to have occurred. This field was 'occurred_at'.
    time_occurred           TIMESTAMP NOT NULL,
    -- Terms of using the API at the point that you acquire the Event.
    terms                   VARCHAR(50) NOT NULL,
    -- Link to URL to changes made to the data.
    updated_reason          VARCHAR(100) NOT NULL,
    -- If an Event is updated, it will have the value of deleted or edited.
    updated                 VARCHAR(10) NOT NULL,
    -- An id that identifies the Agent that made the Event.
    source_token            VARCHAR(40) NOT NULL,
    -- The Canonical URL of a webpage, if one is available. If not, then it's a URL of a webpage.
    subj_id                 VARCHAR(50) NOT NULL,
    -- Includes a link to an Evidence Record for this Event. This is used to generate an Event and contains all of the information used to create the Event.
    evidence_record         VARCHAR(100) NOT NULL,
    -- An action performed by the Agent.
    action_by_agent         VARCHAR(10) NOT NULL,
    -- Same value as subj_id
    subj_pid                VARCHAR(50) NOT NULL,
    -- Same value as subj_id
    subj_url                VARCHAR(50) NOT NULL,
    -- Name of source that event came from.
    source_id               VARCHAR(10) NOT NULL,
    -- Same value as DOI
    obj_pid                 VARCHAR(60) NOT NULL,
    -- Same value as DOI
    obj_url                 VARCHAR(60) NOT NULL,
    -- Timestamp of when the Event was created. This field was originally called timestamp.
    event_creation_time     TIMESTAMP NOT NULL,
    updated_date            DATETIME NOT NULL,
    -- Type of relation between subject and object.
    relation_type_id        VARCHAR(10) NOT NULL,
    -- web_author            VARCHAR(36),
    PRIMARY KEY (web_increment),
    FOREIGN KEY (event_id) REFERENCES Main(UniqueEventID) ON DELETE CASCADE,
    FOREIGN KEY (DOI) REFERENCES Main(DOI) ON DELETE CASCADE
);
>>>>>>> Stashed changes
