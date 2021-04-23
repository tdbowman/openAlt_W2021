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
CREATE DATABASE opencitations;
USE opencitations;

CREATE TABLE IF NOT EXISTS ref
(
	-- To uniquely identify each row. Autoincrements for an easy primary key.
	id					BIGINT AUTO_INCREMENT,
    
    -- the Open Citation Identifier (OCI) of the citation in consideration;
    oci 				varchar(255),
    
    -- the DOI of the citing entity;
    citing 				varchar(255),
    
    -- the DOI of the cited entity;
    cited 				varchar(255),
    
    -- the creation date of the citation
    creation 			datetime,
    
    -- the interval between the publication date of the cited entity and the publication date of the citing entity
    timespan 			varchar(255),
    
    -- it records whether the citation is a journal self-citations
    journal_sc 			varchar(255),
    
    --  it records whether the citation is an author self-citation
	author_sc 			varchar(255),
	
    PRIMARY KEY(id)
);


CREATE TABLE IF NOT EXISTS citations
(
	-- To uniquely identify each row. Autoincrements for an easy primary key.
	id					BIGINT AUTO_INCREMENT,
    
    -- the Open Citation Identifier (OCI) of the citation in consideration;
    oci 				varchar(255),
    
    -- the DOI of the citing entity;
    citing 				varchar(255),
    
    -- the DOI of the cited entity;
    cited 				varchar(255),
    
    -- the creation date of the citation
    creation 			datetime,
    
    -- the interval between the publication date of the cited entity and the publication date of the citing entity
    timespan 			varchar(255),
    
    -- it records whether the citation is a journal self-citations
    journal_sc 			varchar(255),
    
    --  it records whether the citation is an author self-citation
	author_sc 			varchar(255),
	
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS citation
(
	-- To uniquely identify each row. Autoincrements for an easy primary key.
	id				BIGINT AUTO_INCREMENT,
    
    -- the Open Citation Identifier (OCI) of the citation in consideration;
    oci 				varchar(255),
    
    -- the DOI of the citing entity;
    citing 				varchar(255),
    
    -- the DOI of the cited entity;
    cited 				varchar(255),
    
    -- the creation date of the citation
    creation 			datetime,
    
    -- the interval between the publication date of the cited entity and the publication date of the citing entity
    timespan 			varchar(255),
    
    -- it records whether the citation is a journal self-citations
    journal_sc 			varchar(255),
    
    --  it records whether the citation is an author self-citation
	author_sc 			varchar(255),
	
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS metadata
(
	-- To uniquely identify each row. Autoincrements for an easy primary key.
	id						BIGINT AUTO_INCREMENT,
    
    -- the semicolon-separated list of authors of the bibliographic entity;
    author 					varchar(255),
    
    -- the year of publication of the bibliographic entity;
    year 					year,
    
    --  the title of the bibliographic entity;
    title 					varchar(255),
    
    -- the title of the venue where the bibliographic entity has been published;
    source_title 			varchar(255),
    
    -- the semicolon-separated list of identifiers referring to the source where the bibliographic entity has been published;
    source_id 				varchar(255),
    
    -- the number of the volume in which the bibliographic entity has been published;
    volume					bigint,
    
    --  the number of the issue in which the bibliographic entity has been published;
	issue 					bigint,
    
    -- the starting and ending pages of the bibliographic entity in the context of the venue where it has been published;
    page					varchar(255),
    
    -- the DOI of the bibliographic entity;
    doi						varchar(255),
    
    -- the semicolon-separated DOIs of all the entities cited by the bibliographic entity;
    reference				varchar(255),
    
    -- the semicolon-separated DOIs of all the entities that cite the bibliographic entity;
    citation				varchar(255),
    
    -- the number of citations received by the bibliographic entity;
    citation_count			bigint,
    
    -- the link to the Open Access version of the bibliographic entity, if available.
    oa_link					varchar(255),
	
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS citation_count
(
	-- To uniquely identify each row. Autoincrements for an easy primary key.
	id				BIGINT AUTO_INCREMENT,
    
    -- digital object identifier
    doi			varchar(255),
    
    -- the number of incoming citations to the input bibliographic entity.
    count			bigint,
	
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS reference_count
(
	-- To uniquely identify each row. Autoincrements for an easy primary key.
	id				BIGINT AUTO_INCREMENT,
    
    -- digital object identifier
    doi			varchar(255),
    
    -- the number of incoming citations to the input bibliographic entity.
    count			bigint,
	
    PRIMARY KEY(id)
);











    