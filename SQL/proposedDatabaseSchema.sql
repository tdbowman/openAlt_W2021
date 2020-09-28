--   ##########     WORK IN PROGRESS     ##########     
CREATE DATABASE crossRefEventData;
USE crossRefEventData;


CREATE TABLE Main(
    -- A link that contains the Document Object Identifier(DOI) or the scholary content that was registered at CrossRef.
    objectID               VARCHAR(70),
    -- Unique ID of each event.
    uniqueEventID          VARCHAR(36) NOT NULL UNIQUE,
    articleID              INTEGER AUTO_INCREMENT UNIQUE,   
    articleTitle           VARCHAR(120),
    journalName            VARCHAR(40),
    articleDate            DATE,
    articleURL             VARCHAR(100),
    PRIMARY KEY(objectID)
);
-- Journal Table has been removed and merged with Main Table
-- We can use Python to parse the JSON author lists into Given_Name and Family_Name over time'
-- Are ORCIDs worth considering?'
CREATE TABLE Author(
    -- Given by us, increments automatically
    authorID               INTEGER AUTO_INCREMENT, 
    givenName              VARCHAR(30),
    familyName             VARCHAR(30),
    PRIMARY KEY (authorID)
);

CREATE TABLE Article_to_Author(
    articleAuthorID        INTEGER AUTO_INCREMENT,
    articleID              INTEGER,
    authorID               INTEGER,
    PRIMARY KEY(articleAuthorID),
    FOREIGN KEY (articleID) REFERENCES Main(articleID),
    FOREIGN KEY (authorID) REFERENCES Author(authorID)
);

CREATE TABLE CrossRefEvent
(

    -- Auto increment for easy primary keys
    crossRefIncrement       INTEGER AUTO_INCREMENT PRIMARY KEY,

    --  Foreign key to reference the doi
    FOREIGN KEY (eventID) REFERENCES Main(uniqueEventID),

    --  --  -############################--  --  -COLUMNS--  ###############################--  --  -
    
    --  Author
    DOIAuthor               VARCHAR(36),

    --  License provided by each service (CrossRef, DataCite, etc). Could be null(?)
    crossrefLicense         VARCHAR(60),

    --  Link to the scholarly writing.
    objectID                VARCHAR(100),

    --  The source token identifies the Agent that processed the data to produce an Event.
    sourceToken             VARCHAR(36),

    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601.
    occurredAt              TIMESTAMP,

    --  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event.
    subjectID               VARCHAR(100),

    --  Every event is assigned a unique ID. Used for reference.
    eventID                 VARCHAR(36),

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    crossrefTermsOfUse      VARCHAR(45),

    --  The status of the message containing a list of events (message created, updated, deleted, etc.).
    messageAction           VARCHAR(15),

    --  The original source of the input data. Source could be any of the 12 sources listed in CrossRef's guide.
    sourceID                VARCHAR(20),

    --  Timestamp shortly after the event was observed, CONFORMS TO ISO8601.
    timeObserved            TIMESTAMP,

    --  Type of relationship between the subject and the object. String (varchar).
    relationType            VARCHAR (20)

);

CREATE TABLE IF NOT EXISTS RedditEvent(   

    --  Auto increment for easy primary keys.
    redditIncrement         INTEGER AUTO_INCREMENT PRIMARY KEY,

    --  Foreign key to reference the doi.
    FOREIGN KEY (eventID) REFERENCES Main(uniqueEventID),

    --  --  -############################--  --  -COLUMNS--  ###############################--  --  -
    --  Author
    DOIAuthor               VARCHAR(36),

    --  License provided by service.
    license                 VARCHAR(70),

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    termsOfUse              VARCHAR (45),

    --  Reason for updating an event. Optional, may point to an announcement page explaining the edit
    updatedReason           VARCHAR (100),

    --  Updated (Kind of boolean) states whether the event was edited or deleted. 
    updated                 VARCHAR(10),

    --  Updated date.
    updatedDate             TIMESTAMP,

    --  ID of the scholarly writing.
    objectID                VARCHAR(100),

    --  URL of the scholarly writing.
    objectURL               VARCHAR (100),

    --  The source token identifies the Agent that processed the data to produce an Event.
    sourceToken             VARCHAR(36),

    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601.
    occurredAt              TIMESTAMP,

    --  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event
    subjectID               VARCHAR(100),

    --  Every event is assigned a unique ID. Used for reference.
    eventID                 VARCHAR(36) NOT NULL,

    --  Evidence record contains all of the information used to create an event.
    evidenceRecord          VARCHAR(100),

    --  Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction             VARCHAR(15),

     --  The original source of the input data. Source could be any of the 12 sources listed in CrossRef's guide.
    sourceID                VARCHAR(20),

    --  The ID of the entity mentioning the DOI.
    subjectPID              VARCHAR(80),

    --  The title of the subject.
    subjectTitle            VARCHAR(60),

    --  Date the subject issued the mention.
    subjectIssuedDate       TIMESTAMP,

    --  Author of the event.
    subjectAuthorURL        VARCHAR(50),

    --  Original tweet (if retweeted).
    subjectOriginalTweetURL VARCHAR(80),

    --  Author of the original tweet (if retweeted).
    subjectOriginalTweetAuthor VARCHAR(50),

    --  ID of the original tweet (if retweeted).
    alternativeID           VARCHAR(20),

    --  Timestamp shortly after the event was observed, CONFORMS TO ISO8601.
    timeObserved            TIMESTAMP,

    --  Type of relationship between the subject and the object. String (varchar).
    relationType            VARCHAR (20)
    
    );



    CREATE TABLE IF NOT EXISTS StackexchangeEvent(

    --  Auto increment for easy primary keys.
    stackExchangeIncrement  INTEGER AUTO_INCREMENT PRIMARY KEY,

    --  Foreign key to reference the doi.
    FOREIGN KEY (eventID) REFERENCES Main(uniqueEventID),



    --  --  -############################--  --  -COLUMNS--  ###############################--  --  -
    
    --  Author
    DOIAuthor               VARCHAR(36),

    --  License provided by each service (CrossRef, DataCite, etc). Could be null(?)
    license                 VARCHAR(60),

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    termsOfUse              VARCHAR (45),

    --  Link to the scholarly writing.
    objectID                VARCHAR(100),

    --  The source token identifies the Agent that processed the data to produce an Event.
    sourceToken             VARCHAR(36),

    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601.
    occurredAt              TIMESTAMP,

    --  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event.
    subjectID               VARCHAR(100),

    --  Every event is assigned a unique ID. Used for reference.
    eventID                 VARCHAR(36) NOT NULL,

    --  Evidence record contains all of the information used to create an event.
    evidenceRecord          VARCHAR(150),

    --  The ID of the entity mentioning the DOI.
    subjectPID              VARCHAR (80),

    --  The title of the subject.
    subjectTitle            VARCHAR(60),

    --  Date the subject issued the mention.
    subjectIssuedDate       TIMESTAMP,

    --  Type of the subject (post, comment, etc.).
    subjectType             VARCHAR(20),

    --  Subject author's URL.
    subjectAuthorURL        VARCHAR(50),

    --  Subject author's name.
    subjectAuthorName       VARCHAR(30),

    --  Subject author's ID.
    subjectAuthorID         INTEGER,

    --  The original source of the input data. Source could be any of the 12 sources listed in CrossRef's guide.
    sourceID                VARCHAR (20),

    --  PID of the object (DOI being discussed).
    objectPID               VARCHAR(80),

    --  URL of the doi being discussed.
    objectURL               VARCHAR(80),

    --  Timestamp shortly after the event was spotted.
    timeObserved            TIMESTAMP,

    --  Nature of the discussion on the doi (discusses, mentions, etc.).
    relationType            VARCHAR(20)

    );

    CREATE TABLE IF NOT EXISTS WikipediaEvent(

    --  Auto increment for easy primary keys
    wikipediaIncrement      INTEGER AUTO_INCREMENT PRIMARY KEY,

    --  Foreign key to reference the doi
    FOREIGN KEY (eventID) REFERENCES Main(uniqueEventID),

    --  --  -############################--  --  -COLUMNS--  ###############################--  --  -
    
    --  Author.
    DOIAuthor               VARCHAR(36),

    --  License provided by each service (CrossRef, DataCite, etc). Could be null(?)
    license                 VARCHAR(60),

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    termsOfUse              VARCHAR(45),

    --  Updated date.
    updatedDate             TIMESTAMP,

    --  Reason for updating an event. Optional, may point to an announcement page explaining the edit.
    updatedReason           VARCHAR(100),

    --  Link to the scholarly writing.
    objectID                VARCHAR(100),

    --  The source token identifies the Agent that processed the data to produce an Event.
    sourceToken             VARCHAR(36),

    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601.
    occurredAt              TIMESTAMP,

    --  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event.
    subjectID               VARCHAR(100),

    --  Every event is assigned a unique ID. Used for reference.
    eventID                 VARCHAR(36) NOT NULL,

    --  Evidence record contains all of the information used to create an event.
    evidenceRecord          VARCHAR(150),

    --  Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction             VARCHAR(15),

    --  The ID of the entity mentioning the DOI.
    subjectPID              VARCHAR (80),

    --  The title of the subject.
    subjectTitle            VARCHAR(60),

    --  Author of the event.
    subjectURL              VARCHAR(100),

    --  Type of the subject (post, comment, etc.).
    subjectAPIURL           VARCHAR(70),

    --  The original source of the input data. Source could be any of the 12 sources listed in CrossRef's guide.
    sourceID                VARCHAR(20),

    --  PID of the object (DOI being discussed).
    objectPID               VARCHAR(80),

    --  URL of the doi being discussed.
    objectURL               VARCHAR(80),

    --  Timestamp shortly after the event was spotted.
    timeObserved            TIMESTAMP,

    --  Nature of the discussion on the doi (discusses, mentions, etc.).
    relationType            VARCHAR(20)

    );

    CREATE TABLE IF NOT EXISTS WordPressEvent(

    --  Auto increment for easy primary keys.
    wordPressIncrement      INTEGER AUTO_INCREMENT PRIMARY KEY,

    --  Foreign key to reference the doi.
    FOREIGN KEY (eventID) REFERENCES Main(uniqueEventID),

    --  --  -############################--  --  -COLUMNS--  ###############################--  --  -
    
    --  Author.
    DOIAuthor               VARCHAR(36),

    --  License provided by each service (CrossRef, DataCite, etc). Could be null(?)
    license                 VARCHAR(60),

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    termsOfUse              VARCHAR (45),

    --  Updated date.
    updatedDate             TIMESTAMP,

    --  Reason for updating an event. Optional, may point to an announcement page explaining the edit.
    updatedReason           VARCHAR(100),

    --  Link to the scholarly writing.
    objectID                VARCHAR(100),

    --  The source token identifies the Agent that processed the data to produce an Event.
    sourceToken             VARCHAR(36),

    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601.
    occurredAt              TIMESTAMP,

    --  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event.
    subjectID               VARCHAR(100),

    --  Every event is assigned a unique ID. Used for reference.
    eventID                 VARCHAR(36) NOT NULL,

    --  Evidence record contains all of the information used to create an event.
    evidenceRecord          VARCHAR(150),

    --  Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction             VARCHAR(15),

    --  The ID of the entity mentioning the DOI.
    subjectPID              VARCHAR(80),

    --  The title of the subject.
    subjectTitle            VARCHAR(60),

    --  Author of the event.
    subjectType             VARCHAR(100),

    --  The original source of the input data. Source could be any of the 12 sources listed in CrossRef's guide.
    sourceID                VARCHAR(20),

    --  PID of the object (DOI being discussed).
    objectPID               VARCHAR(80),

    --  URL of the doi being discussed.
    objectURL               VARCHAR(80),

    --  Timestamp shortly after the event was spotted.
    timeObserved            TIMESTAMP,

    --  Nature of the discussion on the doi (discusses, mentions, etc.).
    relationType            VARCHAR(20)

    );

    CREATE TABLE IF NOT EXISTS DataCiteEvent(

    --   Auto increment for easy primary keys.
    dataCiteIncrement       INTEGER AUTO_INCREMENT PRIMARY KEY,

    --   Foreign key to reference the doi.
    FOREIGN KEY (eventID) REFERENCES Main(uniqueEventID),

    --  --  -############################--  --  -COLUMNS--  ###############################--  --  -
    
    --  Author.
    DOIAuthor               VARCHAR(36),

    --  License provided by each service (CrossRef, DataCite, etc). Could be null(?)
    license                 VARCHAR(60),

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    termsOfUse              VARCHAR (45),

    --  Link to the scholarly writing.
    objectID                VARCHAR(100),

    --  The source token identifies the Agent that processed the data to produce an Event.
    sourceToken             VARCHAR(36),

    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601.
    occurredAt              TIMESTAMP,

    --  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event.
    subjectID               VARCHAR(100),

    --  Every event is assigned a unique ID. Used for reference.
    eventID                 VARCHAR(36) NOT NULL,

    --  Timestamp shortly after the event was spotted.
    timeObserved            TIMESTAMP,

    --  Nature of the discussion on the doi (discusses, mentions, etc.).
    relationType            VARCHAR(20),

    --  The original source of the input data. Source could be any of the 12 sources listed in CrossRef's guide.
    sourceID                VARCHAR (20)

    );

CREATE TABLE Twitter_Event(
    -- Uniquely identify each row.
    twitterIncrement        INTEGER AUTO_INCREMENT,

    -- Unique ID of each event.
    eventID                 VARCHAR(36) NOT NULL UNIQUE,

    -- A link that contains the Document Object Identifier(DOI) or the scholarly content that was registered at CrossRef.
    objectID                VARCHAR(50),

    -- Author of the DOI.
    DOIAuthor               VARCHAR(36),

    -- Retweet author. If there isn't a retweet, this becomes the tweet author. Can be null.
    tweetAuthor             VARCHAR(75),

    -- If not null, the tweet author is tweetAuthor. Can be null.
    originalTweetAuthor     VARCHAR(75),

    -- Timestamp of when the Event was reported to have occurred.
    occurredAt              TIMESTAMP NOT NULL,

    -- A license under which the Event is made available.
    license                 VARCHAR(70) NOT NULL,

    -- Terms of using the API at the point that you acquire the Event.
    terms                   VARCHAR(70) NOT NULL,

    -- Link to URL to changes made to the data.
    updatedReason           VARCHAR(100) NOT NULL,

    -- If an Event is updated, it will have the value of deleted or edited.
    updated                 VARCHAR(10) NOT NULL,

    -- An id that identifies the Agent that made the Event.
    sourceToken             VARCHAR(40) NOT NULL,

    -- Includes a link to an Evidence Record for this Event. This is used to generate an Event and contains all of the information used to create the Event. 
    evidenceRecord          VARCHAR(100) NOT NULL,

    -- Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction             VARCHAR(10) NOT NULL,

    -- Captures URL of retweet. If there is no retweet, captures URL of tweet. If value is just 'http://twitter.com', everything within subject is NULL.
    subjectID               VARCHAR(80) NOT NULL,

    -- Same value as subjectID. If no tweet or retweet exists, turns into NULL. Can be NULL. This field is within subject.
    subjectPID              VARCHAR(80),

    -- Original Tweet URL. If tweet doesn't exist but retweet does, stores retweet URL.  Can be NULL. This field is within subject.
    originalTweetURL        VARCHAR(80),

    -- id given to each tweet or retweet by Twitter. Can be NULL. This field is within subject.
    alternativeID           VARCHAR(20),

    -- Contains the value "tweet" and an alternative_id. Can be NULL. This field is within subject. 
    title                   VARCHAR(25),

    -- Same value as time_occurred. Can be NULL. This field is within subject.
    issued                  TIMESTAMP,

    -- Name of source that event came from.
    sourceID                VARCHAR(25) NOT NULL,

    -- Same value as the DOI.
    objectPID               VARCHAR(50) NOT NULL,

    -- URL of the doi being discussed.
    objectURL               VARCHAR(50) NOT NULL,

    -- Timestamp of when the Event was created. This field was originally called timestamp.
    timeObserved            TIMESTAMP NOT NULL,

    -- Date and time of when the Event was updated. **DATE AND TIME different from updated_reason for some reason?**
    updatedDate             DATETIME NOT NULL,

    -- Type of relation between subject and object.
    relationType            VARCHAR(10) NOT NULL,

    PRIMARY KEY(twitterIncrement),
    FOREIGN KEY (eventID) REFERENCES Main(uniqueEventID) ON DELETE CASCADE,
    FOREIGN KEY (objectID) REFERENCES Main(objectID) ON DELETE CASCADE
);

CREATE TABLE RedditLinks_Event(
    -- To uniquely identify each row.
    redditLinksIncrement    INTEGER AUTO_INCREMENT,

    -- Unique ID of each event.
    eventID                 VARCHAR(36) NOT NULL UNIQUE,

    -- A link that contains the Document Object Identifier(DOI) or the scholary content that was registered at CrossRef.
    objectID                VARCHAR(50),

    -- Author of the DOI.
    DOIAuthor               VARCHAR(36),

    -- Timestamp of when the Event was reported to have occurred.
    occurredAt              TIMESTAMP NOT NULL,

    -- A license under which the Event is made available.
    license                 VARCHAR(60) NOT NULL,

    -- Terms of using the API at the point that you acquire the Event.
    terms                   VARCHAR(50) NOT NULL,

    -- Link to URL to changes made to the data.
    updatedReason           VARCHAR(100) NOT NULL,

    -- If an Event is updated, it will have the value of deleted or edited.
    updated                 VARCHAR(10) NOT NULL,

    -- An id that identifies the Agent that made the Event.
    sourceToken             VARCHAR(40) NOT NULL,

    -- Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event. As for the type of URL, it's usually the Canonical URL of a webpage, if one is available. If not, then it's a URL of a webpage.
    subjectID               VARCHAR(200) NOT NULL,

    -- Includes a link to an Evidence Record for this Event. This is used to generate an Event and contains all of the information used to create the Event.
    evidenceRecord          VARCHAR(110) NOT NULL,

    -- Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction             VARCHAR(10) NOT NULL,

    -- The ID of the entity mentioning the DOI.
    subjectPID              VARCHAR(200) NOT NULL,

    --  Author of the event.
    subjectURL              VARCHAR(200) NOT NULL,

    -- Name of source that event came from.
    sourceID                VARCHAR(20) NOT NULL,

    -- Persistent Identifer(PID) of the object (DOI being discussed).
    objectPID               VARCHAR(70) NOT NULL,

    -- URL of the doi being discussed.
    objectURL               VARCHAR(120) NOT NULL,

    -- Timestamp of when the Event was created.
    timeObserved            TIMESTAMP NOT NULL,

    -- Updated date.
    updatedDate             TIMESTAMP NOT NULL,

    -- Type of relation between subject and object.
    relationType            VARCHAR(15) NOT NULL,


    PRIMARY KEY (redditLinksIncrement),
    FOREIGN KEY (eventID) REFERENCES Main(uniqueEventID) ON DELETE CASCADE,
    FOREIGN KEY (objectID) REFERENCES Main(objectID) ON DELETE CASCADE
);



CREATE TABLE Newsfeed_Event(
    -- To uniquely identify each row.
    newsfeedIncrement       INTEGER AUTO_INCREMENT,

    -- Unique ID of each event.
    eventID                 VARCHAR(36) NOT NULL UNIQUE,

    -- A link that contains the Document Object Identifier(DOI) or the scholarly content that was registered at CrossRef.
    objectID                VARCHAR(50),

    -- Author of the DOI.
    DOIAuthor               VARCHAR(36),

    -- Timestamp of when the Event was reported to have occurred.
    occurredAt              TIMESTAMP NOT NULL,

    -- A license under which the Event is made available.
    license                 VARCHAR(60) NOT NULL,

    -- Terms of using the API at the point that you acquire the Event.
    terms                   VARCHAR(50) NOT NULL,

    -- Link to URL to changes made to the data.
    updatedReason           VARCHAR(100) NOT NULL,

    -- If an Event is updated, it will have the value of deleted or edited.
    updated                 VARCHAR(10) NOT NULL,

    -- An id that identifies the Agent that made the Event.
    sourceToken             VARCHAR(40) NOT NULL,

    -- Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event. As for the type of URL, it's usually the Canonical URL of a webpage, if one is available. If not, then it's a URL of a webpage.
    subjectID               VARCHAR(200) NOT NULL,

    -- Includes a link to an Evidence Record for this Event. This is used to generate an Event and contains all of the information used to create the Event.
    evidenceRecord          VARCHAR(110) NOT NULL,

    -- Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction             VARCHAR(10) NOT NULL,

    -- The ID of the entity mentioning the DOI.
    subjectPID              VARCHAR(200) NOT NULL,

    --  Type of the subject (post, comment, etc.).
    subjectType             VARCHAR(12) NOT NULL,

    -- The title of the subject.
    subjectTitle            VARCHAR(125) NOT NULL,

    -- Author of the event.
    subjectURL              VARCHAR(200) NOT NULL,

    -- Name of source that event came from.
    sourceID                VARCHAR(20) NOT NULL,

    -- Persistent Identifer(PID) of the object (DOI being discussed).
    objectPID               VARCHAR(70) NOT NULL,

    -- URL of the doi being discussed.
    objectURL               VARCHAR(200) NOT NULL,

    -- Timestamp of when the Event was created.
    timeObserved            TIMESTAMP NOT NULL,

    -- Updated date.
    updatedDate             TIMESTAMP NOT NULL,

    -- Nature of the discussion on the doi (discusses, mentions, etc.).
    relationType            VARCHAR(10) NOT NULL,

    PRIMARY KEY (newsfeedIncrement),
    FOREIGN KEY (eventID) REFERENCES Main(uniqueEventID),
    FOREIGN KEY (objectID) REFERENCES Main(objectID)
);


CREATE TABLE Hypothesis_Event(
    -- To uniquely identify each row.
    hypothesisIncrement     INTEGER AUTO_INCREMENT,

    -- Unique ID of each event.
    eventID                 VARCHAR(36) NOT NULL UNIQUE,

    -- A link that contains the Document Object Identifier(DOI) or the scholarly content that was registered at CrossRef.
    objectID                VARCHAR(50),

    -- Author of the DOI.
    DOIAuthor               VARCHAR(36),

    -- Timestamp of when the Event was reported to have occurred.
    occurredAt              TIMESTAMP NOT NULL,

    -- A license under which the Event is made available.
    license                 VARCHAR(60) NOT NULL,

    -- An id that identifies the Agent that made the Event.
    sourceToken            VARCHAR(40) NOT NULL,

    -- Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event. As for the type of URL, it's usually the Canonical URL of a webpage, if one is available. If not, then it's a URL of a webpage.
    subjectID               VARCHAR(200) NOT NULL,

    -- Includes a link to an Evidence Record for this Event. This is used to generate an Event and contains all of the information used to create the Event.
    evidenceRecord          VARCHAR(120) NOT NULL,

    -- Terms of using the API at the point that you acquire the Event.
    terms                   VARCHAR(50) NOT NULL,

    -- Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction             VARCHAR(10) NOT NULL,

    -- The ID of the entity mentioning the DOI.
    subjectPID              VARCHAR(50) NOT NULL,

    -- URL link of the JSON.
    subj_json_url           VARCHAR(70) NOT NULL,

    -- Author of the event.
    subjectURL              VARCHAR(200) NOT NULL,

    --  Type of the subject (post, comment, etc.).
    subjectType             VARCHAR(12) NOT NULL,

    -- The title of the subject. Can be NULL/empty string.
    subjectTitle            VARCHAR(1030),

    -- Date the subject issued the mention.
    subjectIssued           TIMESTAMP NOT NULL,

    -- Name of source that event came from.
    sourceID                VARCHAR(20) NOT NULL,

    -- Persistent Identifer(PID) of the object (DOI being discussed).
    objectPID               VARCHAR(70) NOT NULL,

    -- URL of the doi being discussed.
    objectURL               VARCHAR(100) NOT NULL,

    -- Timestamp of when the Event was created.
    timeObserved            TIMESTAMP NOT NULL,

    -- Nature of the discussion on the doi (discusses, mentions, etc.).
    relationType            VARCHAR(10) NOT NULL,

    PRIMARY KEY (hypothesisIncrement),
    FOREIGN KEY (eventID) REFERENCES Main(uniqueEventID) ON DELETE CASCADE,
    FOREIGN KEY (objectID) REFERENCES Main(objectID) ON DELETE CASCADE
);


CREATE TABLE Cambia_Event(
    -- To uniquely identify each row.
    cambiaIncrement         INTEGER AUTO_INCREMENT,

    -- Unique ID of each event.
    eventID                 VARCHAR(36) NOT NULL UNIQUE,

    -- A link that contains the Document Object Identifier(DOI) or the scholarly content that was registered at CrossRef.
    objectID                VARCHAR(50),

    -- Author of the DOI.
    DOIAuthor               VARCHAR(36),

    -- A license under which the Event is made available.
    license                 VARCHAR(55) NOT NULL,

    -- Link to URL to changes made to the data.
    updatedReason           VARCHAR(100) NOT NULL,

    -- If an Event is updated, it will have the value of deleted or edited.
    updated                 VARCHAR(10) NOT NULL,

    -- An id that identifies the Agent that made the Event.
    sourceToken             VARCHAR(40) NOT NULL,

    -- Timestamp of when the Event was reported to have occurred.
    occurredAt              TIMESTAMP NOT NULL,

    -- Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event. As for the type of URL, it's usually the Canonical URL of a webpage, if one is available. If not, then it's a URL of a webpage.
    subjectID               VARCHAR(200) NOT NULL,

    -- Terms of using the API at the point that you acquire the Event.
    terms                   VARCHAR(50) NOT NULL,

    -- Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction             VARCHAR(10) NOT NULL,

    -- Type of patent.
    workSubtypeID           VARCHAR(25) NOT NULL,

    -- 'patent'.
    workTypeID              VARCHAR(10) NOT NULL,

    -- The title of the subject.
    subjectTitle            VARCHAR(140) NOT NULL,

    -- The ID of the entity mentioning the DOI.
    subjectPID              VARCHAR(50) NOT NULL,

    -- Patent groups distributing patents.
    jurisdiction            VARCHAR(5) NOT NULL,

    -- Name of source that event came from.
    sourceID                VARCHAR(20) NOT NULL,

    -- Timestamp of when the Event was created.
    timeObserved            TIMESTAMP NOT NULL,

    -- Updated date.
    updatedDate             TIMESTAMP NOT NULL,

    -- Nature of the discussion on the doi (discusses, mentions, etc.).
    relationType            VARCHAR(10) NOT NULL,

    PRIMARY KEY (cambiaIncrement),
    FOREIGN KEY (eventID) REFERENCES Main(uniqueEventID) ON DELETE CASCADE,
    FOREIGN KEY (objectID) REFERENCES Main(objectID) ON DELETE CASCADE
);


CREATE TABLE Web_Event(
    -- To uniquely identify each row.
    webIncrement            INTEGER AUTO_INCREMENT,

    -- Unique ID of each event.
    eventID                 VARCHAR(36) NOT NULL UNIQUE,

    -- A link that contains the Document Object Identifier(DOI) or the scholarly content that was registered at CrossRef.
    objectID                VARCHAR(50),

    -- Author of the DOI.
    DOIAuthor               VARCHAR(36),

    -- Timestamp of when the Event was reported to have occurred.
    occurredAt              TIMESTAMP NOT NULL,

    -- Terms of using the API at the point that you acquire the Event.
    Terms                   VARCHAR(50) NOT NULL,

    -- Link to URL to changes made to the data.
    updatedReason           VARCHAR(100) NOT NULL,

    -- If an Event is updated, it will have the value of deleted or edited.
    updated                 VARCHAR(10) NOT NULL,

    -- An id that identifies the Agent that made the Event.
    sourceToken             VARCHAR(40) NOT NULL,

    -- Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event. As for the type of URL, it's usually the Canonical URL of a webpage, if one is available. If not, then it's a URL of a webpage.
    subjectID               VARCHAR(200) NOT NULL,

    -- Includes a link to an Evidence Record for this Event. This is used to generate an Event and contains all of the information used to create the Event.
    evidenceRecord          VARCHAR(110) NOT NULL,

    -- Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction             VARCHAR(10) NOT NULL,

    -- The ID of the entity mentioning the DOI.
    subjectPID              VARCHAR(50) NOT NULL,

    -- Author of the event.
    subjectURL              VARCHAR(200) NOT NULL,

    -- Name of source that event came from.
    sourceID                VARCHAR(20) NOT NULL,

    -- Persistent Identifer(PID) of the object (DOI being discussed).
    objectPID               VARCHAR(70) NOT NULL,

    -- URL of the doi being discussed.
    objectURL               VARCHAR(60) NOT NULL,

    -- Timestamp of when the Event was created.
    timeObserved            TIMESTAMP NOT NULL,

    -- Updated date.
    updatedDate             TIMESTAMP NOT NULL,

    -- Nature of the discussion on the doi (discusses, mentions, etc.).
    relationType            VARCHAR(10) NOT NULL,

    PRIMARY KEY (webIncrement),
    FOREIGN KEY (eventID) REFERENCES Main(uniqueEventID) ON DELETE CASCADE,
    FOREIGN KEY (objectID) REFERENCES Main(objectID) ON DELETE CASCADE
);