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

CREATE DATABASE crossrefeventdatamain;
USE crossrefeventdatamain;

CREATE TABLE IF NOT EXISTS main
(
	-- To uniquely identify each row. Autoincrements for an easy primary key.
	increment				BIGINT AUTO_INCREMENT,
    
    -- A link that contains the Document Object Identifier(DOI) or the scholarly content that was registered at CrossRef.
    objectID 				VARCHAR(100) UNIQUE,
    
    -- Total number of events of all the event tables in the database
    totalEvents 			BIGINT,
    
    -- Total number of Cambia events 
    totalCambiaEvents 		INT,
    
    -- First Cambia datetime inserted into the database
    firstCambiaEvent 		datetime,
    
    -- Last Cambia datetime inserted into the database
    lastCambiaEvent 		datetime,
    
    -- Total number of Crossref events
    totalCrossrefEvents 	INT,
    
    -- First Crossref datetime inserted into the database
	firstCrossrefEvent 		datetime,
    
    -- Last Crossref datetime inserted into the database
    lastCrossrefEvent 		datetime,
    
    
    -- Total number of Datacite events
    totalDataciteEvents 	INT,
    
    -- First Datacite datetime inserted into the database
    firstDataciteEvent 		datetime,
    
    -- Last Datacite datetime inserted into the database
    lastDataciteEvent 		datetime,
    
    -- Total number of F1000 events
    totalF1000Events        INT,

    -- First F1000 datetime inserted into the database
    firstF1000Event         datetime,

    -- Last F1000 datetime inserted into the database
    lastF1000Event          datetime,
    
    -- Total number of Hypothesis events
    totalHypothesisEvents 	INT,
    
    -- First Hypothesis datetime inserted into the database
    firstHypothesisEvent 	datetime,
    
    -- Last Hypothesis datetime inserted into the database
    lastHypothesisEvent 	datetime,
    
    
    -- Total number of Newsfeed events
    totalNewsfeedEvents 	INT,
    
    -- First Newsfeed datetime inserted into the database
    firstNewsfeedEvent 		datetime,
    
    -- Last Newsfeed datetime inserted into the database
    lastNewsfeedEvent 		datetime,
    
    
    -- Total number of Reddit events
    totalRedditEvents 		INT,
    
    -- First Reddit datetime inserted into the database
    firstRedditEvent 		datetime,
    
    -- Last Reddit datetime inserted into the database
    lastRedditEvent 		datetime,
    
    
	-- Total number of RedditLinks events
    totalRedditLinksEvents 	INT,
    
    -- First RedditLinks datetime inserted into the database
    firstRedditLinksEvent 	datetime,
    
    -- Last RedditLinks datetime inserted into the database
    lastRedditLinksEvent 	datetime,
    
    
    -- Total number of Stackexchange events
    totalStackExchangeEvents INT,
    
    -- First Stackexchange datetime inserted into the database
    firstStackExchangeEvent datetime,
    
    -- Last Stackexchange datetime inserted into the database
    lastStackExchangeEvent 	datetime,
    
    
    -- Total number of Twitter events
    totalTwitterEvents 		INT,
    
    -- First Twitter datetime inserted into the database
    firstTwitterEvent 		datetime,
    
    -- Last Twitter datetime inserted into the database
    lastTwitterEvent 		datetime,
    
    
    -- Total number of Web events
    totalWebEvents 			INT,
    
    -- First Web datetime inserted into the database
    firstWebEvent 			datetime,
    
    -- Last Web datetime inserted into the database
    lastWebEvent 			datetime,
    
    
    -- Total number of Wikipedia events
    totalWikipediaEvents 	INT,
    
    -- First Wikipedia datetime inserted into the database
    firstWikipediaEvent 	datetime,
    
    -- Last Wikipedia datetime inserted into the database
    lastWikipediaEvent		datetime,
    
    
    -- Total number of Wordpress events
    totalWordpressEvents 	INT,
    
    -- First Wordpress datetime inserted into the database
    firstWordpressEvent 	datetime,
    
    -- Last Wordpress datetime inserted into the database
    lastWordPressEvent 		datetime,
	
    PRIMARY KEY(increment)
);



CREATE TABLE IF NOT EXISTS cambiaevent(

    -- To uniquely identify each row.
    cambiaIncrement         INTEGER AUTO_INCREMENT  PRIMARY KEY,

	-- Name of source that event came from.
    sourceID                VARCHAR(100),
    
    -- A link that contains the Document Object Identifier(DOI) or the scholarly content that was registered at CrossRef.
    objectID                VARCHAR(100),
    
    -- Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event. As for the type of URL, it's usually the Canonical URL of a webpage, if one is available. If not, then it's a URL of a webpage.
    subjectID               VARCHAR(200),
    
    -- Unique ID of each event.
    eventID                 VARCHAR(50),
    
    -- datetime of when the Event was reported to have occurred.
    occurredAt              datetime,
    
    -- datetime of when the Event was created.
    timeObserved            datetime,
    
    -- Nature of the discussion on the doi (discusses, mentions, etc.).
    relationType            VARCHAR(50),
    
    -- An id that identifies the Agent that made the Event.
    sourceToken             VARCHAR(50),

    -- A license under which the Event is made available.
    license                 VARCHAR(55),
    
    -- Terms of using the API at the point that you acquire the Event.
    termsOfUse              VARCHAR(100),

    -- Link to URL to changes made to the data.
    updatedReason           VARCHAR(100),

    -- If an Event is updated, it will have the value of deleted or edited.
    updated                 VARCHAR(50),

    -- Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction             VARCHAR(50),

    -- Type of patent.
    workSubtypeID           VARCHAR(50),

    -- 'patent'.
    workTypeID              VARCHAR(50),

    -- The title of the subject.
    subjectTitle            VARCHAR(140),

    -- The ID of the entity mentioning the DOI.
    subjectPID              VARCHAR(100),

    -- Patent groups distributing patents.
    jurisdiction            VARCHAR(50),

    -- Updated date.
    updatedDate             datetime,
    
    --  Foreign key to reference the doi
	FOREIGN KEY (objectID) REFERENCES main(objectID) ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS crossrefevent
(

    -- Auto increment for easy primary keys
    crossRefIncrement       INTEGER AUTO_INCREMENT PRIMARY KEY,
    
	--  The original source of the input data. Source could be any of the 13 sources listed in CrossRef's guide.
    sourceID                VARCHAR(100),
    
	--  Link to the scholarly writing.
    objectID                VARCHAR(100),
    
	--  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event.
    subjectID               VARCHAR(100),
    
	--  Every event is assigned a unique ID. Used for reference.
    eventID                 VARCHAR(50),
    
    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601.
    occurredAt              datetime,
    
	--  datetime shortly after the event was observed, CONFORMS TO ISO8601.
    timeObserved            datetime,
    
    --  Type of relationship between the subject and the object. String (varchar).
    relationType            VARCHAR(100),
    
    --  The source token identifies the Agent that processed the data to produce an Event.
    sourceToken             VARCHAR(50),
    
    --  License provided by each service (CrossRef, DataCite, etc). Could be null(?)
    license         		VARCHAR(100), 

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    crossrefTermsOfUse      VARCHAR(50),

    --  The status of the message containing a list of events (message created, updated, deleted, etc.).
    messageAction           VARCHAR(50),

	--  Foreign key to reference the doi
	FOREIGN KEY (objectID) REFERENCES main(objectID) ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS dataciteevent(

    --   Auto increment for easy primary keys.
    dataCiteIncrement       INTEGER AUTO_INCREMENT PRIMARY KEY,

	--  The original source of the input data. Source could be any of the 13 sources listed in CrossRef's guide.
    sourceID                VARCHAR (20),
    
    --  Link to the scholarly writing.
    objectID                VARCHAR(100),
    
    --  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event.
    subjectID               VARCHAR(100),
    
    --  Every event is assigned a unique ID. Used for reference.
    eventID                 VARCHAR(50),
    
    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601.
    occurredAt              datetime,
    
    --  datetime shortly after the event was spotted.
    timeObserved            datetime,
    
    --  Nature of the discussion on the doi (discusses, mentions, etc.).
    relationType            VARCHAR(100),
    
    --  License provided by each service (CrossRef, DataCite, etc). Could be null(?)
    license                 VARCHAR(100),

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    termsOfUse              VARCHAR (45),

    --  The status of the message containing a list of events (message created, updated, deleted, etc.).
    messageAction           VARCHAR(50),

	--  Foreign key to reference the doi
	FOREIGN KEY (objectID) REFERENCES main(objectID) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS f1000event(

    -- To uniquely identify each row.
    f1000Increment  		INTEGER AUTO_INCREMENT  PRIMARY KEY,

    -- Name of source that event came from.
    sourceID       	 		VARCHAR(100),

    --  Link to the scholarly writing.
    objectID        		VARCHAR(100),

    --  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event.
    subjectID       		VARCHAR(100),

    --  Every event is assigned a unique ID. Used for reference.
    eventID         		VARCHAR(100),

    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601.
    occurredAt      		datetime,

    --  datetime shortly after the event was spotted.
    timeObserved    		datetime,

    --  Nature of the discussion on the doi (discusses, mentions, etc.).
    relationType    		VARCHAR(100),

    -- An id that identifies the Agent that made the Event.
    sourceToken     		VARCHAR(100),

    -- A license under which the Event is made available.
    license         		VARCHAR(100),

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    termsOfUse      		VARCHAR(100),

    -- Includes a link to an Evidence Record for this Event. This is used to generate an Event and contains all of the information used to create the Event.
    evidenceRecord  		VARCHAR(100),

    -- Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction     		VARCHAR(100),

    -- The ID of the entity mentioning the DOI.
    subjectPID      		VARCHAR(100),

    -- Author of the event.
    subjectURL      		VARCHAR(100),


    alternativeID   		VARCHAR(100),


    workTypeID      		VARCHAR(100),

    -- Persistent Identifer(PID) of the object (DOI being discussed).
    objectPID       		VARCHAR(100),

    -- URL of the doi being discussed.
    objectURL       		VARCHAR(100),

    --  Foreign key to reference the doi
    FOREIGN KEY (objectID) REFERENCES main(objectID) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS hypothesisevent(

    -- To uniquely identify each row.
    hypothesisIncrement     INTEGER AUTO_INCREMENT  PRIMARY KEY,
    
	-- Name of source that event came from.
    sourceID                VARCHAR(100),

	-- A link that contains the Document Object Identifier(DOI) or the scholarly content that was registered at CrossRef.
    objectID                VARCHAR(100),
    
    -- Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event. As for the type of URL, it's usually the Canonical URL of a webpage, if one is available. If not, then it's a URL of a webpage.
    subjectID               VARCHAR(200),
    
    -- Unique ID of each event.
    eventID                 VARCHAR(50),

    -- datetime of when the Event was reported to have occurred.
    occurredAt              datetime,
    
    -- datetime of when the Event was created.
    timeObserved            datetime,
    
    -- Nature of the discussion on the doi (discusses, mentions, etc.).
    relationType            VARCHAR(50),
    
    -- An id that identifies the Agent that made the Event.
    sourceToken           	VARCHAR(50),

    -- A license under which the Event is made available.
    license                 VARCHAR(100),
    
    -- Terms of using the API at the point that you acquire the Event.
    termsOfUse              VARCHAR(100),

    -- Includes a link to an Evidence Record for this Event. This is used to generate an Event and contains all of the information used to create the Event.
    evidenceRecord          VARCHAR(120),

    -- Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction             VARCHAR(50),

    -- The ID of the entity mentioning the DOI.
    subjectPID              VARCHAR(100),

    -- URL link of the JSON.
    subj_json_url           VARCHAR(100),

    -- Author of the event.
    subjectURL              VARCHAR(200),

    --  Type of the subject (post, comment, etc.).
    subjectType             VARCHAR(50),

    -- The title of the subject. Can be NULL/empty string.
    subjectTitle            VARCHAR(1030),

    -- Date the subject issued the mention.
    subjectIssued           datetime,

    -- Persistent Identifer(PID) of the object (DOI being discussed).
    objectPID               VARCHAR(100),

    -- URL of the doi being discussed.
    objectURL               VARCHAR(100),
    
    --  Foreign key to reference the doi
	FOREIGN KEY (objectID) REFERENCES main(objectID) ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS newsfeedevent(

    -- To uniquely identify each row.
    newsfeedIncrement       INTEGER AUTO_INCREMENT  PRIMARY KEY,

	-- Name of source that event came from.
    sourceID                VARCHAR(100),
    
    -- A link that contains the Document Object Identifier(DOI) or the scholarly content that was registered at CrossRef.
    objectID                VARCHAR(100),
    
    -- Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event. As for the type of URL, it's usually the Canonical URL of a webpage, if one is available. If not, then it's a URL of a webpage.
    subjectID               VARCHAR(200),
    
    -- Unique ID of each event.
    eventID                 VARCHAR(50),

    -- datetime of when the Event was reported to have occurred.
    occurredAt              datetime,
    
    -- datetime of when the Event was created.
    timeObserved            datetime,
    
    -- Nature of the discussion on the doi (discusses, mentions, etc.).
    relationType            VARCHAR(50),
    
    -- An id that identifies the Agent that made the Event.
    sourceToken             VARCHAR(50),

    -- A license under which the Event is made available.
    license                 VARCHAR(100),

    -- Terms of using the API at the point that you acquire the Event.
    termsOfUse              VARCHAR(100),

    -- Link to URL to changes made to the data.
    updatedReason           VARCHAR(100),

    -- If an Event is updated, it will have the value of deleted or edited.
    updated                 VARCHAR(50),

    -- Includes a link to an Evidence Record for this Event. This is used to generate an Event and contains all of the information used to create the Event.
    evidenceRecord          VARCHAR(150),

    -- Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction             VARCHAR(50),

    -- The ID of the entity mentioning the DOI.
    subjectPID              VARCHAR(200),

    --  Type of the subject (post, comment, etc.).
    subjectType             VARCHAR(50),

    -- The title of the subject.
    subjectTitle            VARCHAR(125),

    -- Author of the event.
    subjectURL              VARCHAR(200),

    -- Persistent Identifer(PID) of the object (DOI being discussed).
    objectPID               VARCHAR(100),

    -- URL of the doi being discussed.
    objectURL               VARCHAR(200),

    -- Updated date.
    updatedDate             datetime,
    
    --  Foreign key to reference the doi
	FOREIGN KEY (objectID) REFERENCES main(objectID) ON DELETE CASCADE

);



CREATE TABLE IF NOT EXISTS redditevent(   

    --  Auto increment for easy primary keys.
    redditIncrement         INTEGER AUTO_INCREMENT PRIMARY KEY,
    
    --  The original source of the input data. Source could be any of the 13 sources listed in CrossRef's guide.
    sourceID                VARCHAR(100),
    
	--  ID of the scholarly writing.
    objectID                VARCHAR(100),
    
    --  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event
    subjectID               VARCHAR(100),
    
    --  Every event is assigned a unique ID. Used for reference.
    eventID                 VARCHAR(50),
    
    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601.
    occurredAt              datetime,
    
    --  datetime shortly after the event was observed, CONFORMS TO ISO8601.
    timeObserved            datetime,
    
    --  Type of relationship between the subject and the object. String (varchar).
    relationType            VARCHAR(100),
    
    --  The source token identifies the Agent that processed the data to produce an Event.
    sourceToken             VARCHAR(50),
    
    --  License provided by service.
    license                 VARCHAR(100),

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    termsOfUse              VARCHAR(100),

    --  Reason for updating an event. Optional, may point to an announcement page explaining the edit
    updatedReason           VARCHAR(100),

    --  Updated (Kind of boolean) states whether the event was edited or deleted. 
    updated                 VARCHAR(50),

    --  Updated date.
    updatedDate             datetime,

    --  PID of the object (DOI being discussed).
    objectPID               VARCHAR(200),

    --  URL of the scholarly writing.
    objectURL               VARCHAR(200),

    --  Evidence record contains all of the information used to create an event.
    evidenceRecord          VARCHAR(100),

    --  Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction             VARCHAR(50),

    --  The ID of the entity mentioning the DOI.
    subjectPID              VARCHAR(100),

    -- Type of discussion about DOI
    subjectType             VARCHAR(50),

    --  The title of the subject.
    subjectTitle            VARCHAR(200),

    --  Date the subject issued the mention.
    subjectIssuedDate       datetime,
    
    --  Foreign key to reference the doi
	FOREIGN KEY (objectID) REFERENCES main(objectID) ON DELETE CASCADE
    );



CREATE TABLE IF NOT EXISTS redditlinksevent(

    -- To uniquely identify each row.
    redditLinksIncrement    INTEGER AUTO_INCREMENT  PRIMARY KEY,
    
    -- Name of source that event came from.
    sourceID                VARCHAR(100),
    
    -- A link that contains the Document Object Identifier(DOI) or the scholary content that was registered at CrossRef.
    objectID                VARCHAR(100),
    
    -- Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event. As for the type of URL, it's usually the Canonical URL of a webpage, if one is available. If not, then it's a URL of a webpage.
    subjectID               VARCHAR(200),

    -- Unique ID of each event.
    eventID                 VARCHAR(50),

    -- datetime of when the Event was reported to have occurred.
    occurredAt              datetime,
    
    -- datetime of when the Event was created.
    timeObserved            datetime,
    
    -- Type of relation between subject and object.
    relationType            VARCHAR(50),
    
    -- An id that identifies the Agent that made the Event.
    sourceToken             VARCHAR(50),

    -- A license under which the Event is made available.
    license                 VARCHAR(100),

    -- Terms of using the API at the point that you acquire the Event.
    termsOfUse              VARCHAR(100),

    -- Link to URL to changes made to the data.
    updatedReason           VARCHAR(100),

    -- If an Event is updated, it will have the value of deleted or edited.
    updated                 VARCHAR(50),

    -- Includes a link to an Evidence Record for this Event. This is used to generate an Event and contains all of the information used to create the Event.
    evidenceRecord          VARCHAR(150),

    -- Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction             VARCHAR(50),

    -- The ID of the entity mentioning the DOI.
    subjectPID              VARCHAR(200),

    --  Author of the event.
    subjectURL              VARCHAR(200),

    -- Persistent Identifer(PID) of the object (DOI being discussed).
    objectPID               VARCHAR(100),

    -- URL of the doi being discussed.
    objectURL               VARCHAR(120),

    -- Updated date.
    updatedDate             datetime,
    
    --  Foreign key to reference the doi
	FOREIGN KEY (objectID) REFERENCES main(objectID) ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS stackexchangeevent(

    --  Auto increment for easy primary keys.
    stackExchangeIncrement  INTEGER AUTO_INCREMENT PRIMARY KEY,

	--  The original source of the input data. Source could be any of the 13 sources listed in CrossRef's guide.
    sourceID                VARCHAR(100),
    
	--  Link to the scholarly writing.
    objectID                VARCHAR(100),
    
    --  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event.
    subjectID               VARCHAR(100),
    
    --  Every event is assigned a unique ID. Used for reference.
    eventID                 VARCHAR(50),
    
    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601.
    occurredAt              datetime,
    
    --  datetime shortly after the event was spotted.
    timeObserved            datetime,
    
    --  Nature of the discussion on the doi (discusses, mentions, etc.).
    relationType            VARCHAR(100),
    
    --  The source token identifies the Agent that processed the data to produce an Event.
    sourceToken             VARCHAR(50),
    
    --  License provided by each service (CrossRef, DataCite, etc). Could be null(?)
    license                 VARCHAR(100),

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    termsOfUse              VARCHAR(50),

    --  Evidence record contains all of the information used to create an event.
    evidenceRecord          VARCHAR(150),

    --  The ID of the entity mentioning the DOI.
    subjectPID              VARCHAR(100),

    --  The title of the subject.
    subjectTitle            VARCHAR(100),

    --  Date the subject issued the mention.
    subjectIssuedDate       datetime,

    --  Type of the subject (post, comment, etc.).
    subjectType             VARCHAR(100),

    --  Subject author's URL.
    subjectAuthorURL        VARCHAR(100),

    --  Subject author's name.
    subjectAuthorName       VARCHAR(50),

    --  Subject author's ID.
    subjectAuthorID         INT,

    --  PID of the object (DOI being discussed).
    objectPID               VARCHAR(100),

    --  URL of the doi being discussed.
    objectURL               VARCHAR(100),
    
    --  Foreign key to reference the doi
	FOREIGN KEY (objectID) REFERENCES main(objectID) ON DELETE CASCADE

);


CREATE TABLE IF NOT EXISTS twitterevent(

    -- Uniquely identify each row.
    twitterIncrement 		INTEGER AUTO_INCREMENT PRIMARY KEY,

	-- Name of source that event came from.
    sourceID                VARCHAR(50),
    
    -- Captures URL of retweet. If there is no retweet, captures URL of tweet. If value is just 'http://twitter.com', everything within subject is NULL.
    subjectID               VARCHAR(100),
    
    -- A link that contains the Document Object Identifier(DOI) or the scholarly content that was registered at CrossRef.
    objectID                VARCHAR(100),
    
    -- Unique ID of each event.
    eventID                 VARCHAR(50),
    
    -- datetime of when the Event was reported to have occurred.
    occurredAt              datetime,
    
    -- datetime of when the Event was created. This field was originally called datetime.
    timeObserved            datetime,
    
    -- Type of relation between subject and object.
    relationType            VARCHAR(50),
    
    -- An id that identifies the Agent that made the Event.
    sourceToken             VARCHAR(50),
    
    -- A license under which the Event is made available.
    license                 VARCHAR(100),
    
    -- Terms of using the API at the point that you acquire the Event.
    termsOfUse              VARCHAR(100),

    -- Retweet author. If there isn't a retweet, this becomes the tweet author. Can be null.
    tweetAuthor             VARCHAR(75),

    -- If not null, the tweet author is tweetAuthor. Can be null.
    originalTweetAuthor     VARCHAR(75),

    -- Link to URL to changes made to the data.
    updatedReason           VARCHAR(100),

    -- If an Event is updated, it will have the value of deleted or edited.
    updated                 VARCHAR(50),

    -- Includes a link to an Evidence Record for this Event. This is used to generate an Event and contains all of the information used to create the Event. 
    evidenceRecord          VARCHAR(100),

    -- Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction             VARCHAR(50),

    -- Same value as subjectID. If no tweet or retweet exists, turns into NULL. Can be NULL. This field is within subject.
    subjectPID              VARCHAR(100),

    -- Original Tweet URL. If tweet doesn't exist but retweet does, stores retweet URL.  Can be NULL. This field is within subject.
    originalTweetURL        VARCHAR(100),

    -- id given to each tweet or retweet by Twitter. Can be NULL. This field is within subject.
    alternativeID           VARCHAR(100),

    -- Contains the value "tweet" and an alternative_id. Can be NULL. This field is within subject. 
    title                   VARCHAR(50),

    -- Same value as time_occurred. Can be NULL. This field is within subject.
    issued                  datetime,

    -- Same value as the DOI.
    objectPID               VARCHAR(100),

    -- URL of the doi being discussed.
    objectURL               VARCHAR(100),

    -- Date and time of when the Event was updated. **DATE AND TIME different from updated_reason for some reason?**
    updatedDate             DATETIME,
    
    --  Foreign key to reference the doi
	FOREIGN KEY (objectID) REFERENCES main(objectID) ON DELETE CASCADE

);



CREATE TABLE IF NOT EXISTS webevent(

    -- To uniquely identify each row.
    webIncrement            INTEGER AUTO_INCREMENT  PRIMARY KEY,
    
    -- Name of source that event came from.
    sourceID                VARCHAR(100),
    
    -- A link that contains the Document Object Identifier(DOI) or the scholarly content that was registered at CrossRef.
    objectID                VARCHAR(100),
    
    -- Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event. As for the type of URL, it's usually the Canonical URL of a webpage, if one is available. If not, then it's a URL of a webpage.
    subjectID               VARCHAR(200),

    -- Unique ID of each event.
    eventID                 VARCHAR(50),

    -- datetime of when the Event was reported to have occurred.
    occurredAt              datetime,
    
    -- datetime of when the Event was created.
    timeObserved            datetime,
    
    -- Nature of the discussion on the doi (discusses, mentions, etc.).
    relationType            VARCHAR(50),

    -- Terms of using the API at the point that you acquire the Event.
    termsOfUse              VARCHAR(100),

    -- Link to URL to changes made to the data.
    updatedReason           VARCHAR(100),

    -- If an Event is updated, it will have the value of deleted or edited.
    updated                 VARCHAR(50),

    -- An id that identifies the Agent that made the Event.
    sourceToken             VARCHAR(50),

    -- Includes a link to an Evidence Record for this Event. This is used to generate an Event and contains all of the information used to create the Event.
    evidenceRecord          VARCHAR(150),

    -- Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction             VARCHAR(50),

    -- The ID of the entity mentioning the DOI.
    subjectPID              VARCHAR(100),

    -- Author of the event.
    subjectURL              VARCHAR(200),

    -- Persistent Identifer(PID) of the object (DOI being discussed).
    objectPID               VARCHAR(100),

    -- URL of the doi being discussed.
    objectURL               VARCHAR(100),

    -- Updated date.
    updatedDate             datetime,
    
    --  Foreign key to reference the doi
	FOREIGN KEY (objectID) REFERENCES main(objectID) ON DELETE CASCADE
);



    CREATE TABLE IF NOT EXISTS wikipediaevent(
    
    --  Auto increment for easy primary keys
    wikipediaIncrement      INTEGER AUTO_INCREMENT PRIMARY KEY,

	--  The original source of the input data. Source could be any of the 13 sources listed in CrossRef's guide.
    sourceID                VARCHAR(100),
    
    --  Link to the scholarly writing.
    objectID                VARCHAR(100),
    
    --  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event.
    subjectID               VARCHAR(100),
    
    --  Every event is assigned a unique ID. Used for reference.
    eventID                 VARCHAR(50),
    
    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601.
    occurredAt              datetime,
    
    --  datetime shortly after the event was spotted.
    timeObserved            datetime,
    
    --  Nature of the discussion on the doi (discusses, mentions, etc.).
    relationType            VARCHAR(100),
    
    --  The source token identifies the Agent that processed the data to produce an Event.
    sourceToken             VARCHAR(50),
    
    --  License provided by each service (CrossRef, DataCite, etc). Could be null(?)
    license                 VARCHAR(100),

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    termsOfUse              VARCHAR(50),

    --  Updated date.
    updatedDate             datetime,

    --  Reason for updating an event. Optional, may point to an announcement page explaining the edit.
    updatedReason           VARCHAR(100),

    --  Evidence record contains all of the information used to create an event.
    evidenceRecord          VARCHAR(150),

    --  Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction             VARCHAR(50),

    --  The ID of the entity mentioning the DOI.
    subjectPID              VARCHAR (80),

    --  The title of the subject.
    subjectTitle            VARCHAR(100),

    --  Author of the event.
    subjectURL              VARCHAR(100),

    --  Type of the subject (post, comment, etc.).
    subjectAPIURL           VARCHAR(100),

    --  PID of the object (DOI being discussed).
    objectPID               VARCHAR(100),

    --  URL of the doi being discussed.
    objectURL               VARCHAR(100),

	--  Foreign key to reference the doi
	FOREIGN KEY (objectID) REFERENCES main(objectID) ON DELETE CASCADE
    );



    CREATE TABLE IF NOT EXISTS wordpressevent(

    --  Auto increment for easy primary keys.
    wordPressIncrement      INTEGER AUTO_INCREMENT PRIMARY KEY,
    
    --  The original source of the input data. Source could be any of the 13 sources listed in CrossRef's guide.
    sourceID                VARCHAR(100),
    
	--  Link to the scholarly writing.
    objectID                VARCHAR(100),
    
    --  Subject ID is similar to the object ID, since most events have a URL as a subject ID and the DOI as object ID. The agent that processes the data decides on each event.
    subjectID               VARCHAR(200),
    
    --  Every event is assigned a unique ID. Used for reference.
    eventID                 VARCHAR(50),
    
    --  The date and time the event was "REPORTED" to have been published by users. CONFORMS TO ISO8601.
    occurredAt              datetime,
    
    --  datetime shortly after the event was spotted.
    timeObserved            datetime,
    
    --  Nature of the discussion on the doi (discusses, mentions, etc.).
    relationType            VARCHAR(100),
    
    --  The source token identifies the Agent that processed the data to produce an Event.
    sourceToken             VARCHAR(50),
    
    --  License provided by each service (CrossRef, DataCite, etc). Could be null(?)
    license                 VARCHAR(100),

    --  Terms of use for the CROSSREF EVENT DATA QUERY API.
    termsOfUse              VARCHAR (45),

    --  Evidence record contains all of the information used to create an event.
    evidenceRecord          VARCHAR(150),

    --  Action is the nature of the event, such as adding a comment, in which case the action is "add".
    eventAction             VARCHAR(50),

    --  The ID of the entity mentioning the DOI.
    subjectPID              VARCHAR(200),

    --  The title of the subject.
    subjectTitle            VARCHAR(200),

    --  Author of the event.
    subjectType             VARCHAR(100),

    --  PID of the object (DOI being discussed).
    objectPID               VARCHAR(100),

    --  URL of the doi being discussed.
    objectURL               VARCHAR(100),

	--  Foreign key to reference the doi
	FOREIGN KEY (objectID) REFERENCES main(objectID) ON DELETE CASCADE
    );
    