/* 
This script generates the stacked bar charts using c3 and d3.

Reassign these with Python - position in array corresponds to column
Like: [column1, column2, column3, column4, column5]
All 12 of these combine to make 5 bars, which are each 12 blocks high

PYTHON CHANGES THESE OR PUTS THEM AS PARAMS */
const cambiaevent = [10,30,10,80,70];
const crossrefevent = [0,4,10,20,40];
const dataciteevent = [10,0,10,10,10];
const hypothesisevent = [10,10,10,70,10];
const newsfeedevent = [10,30,10,80,10];
const redditevent = [10,10,10,10,10];
const redditlinksevent = [10,10,20,10,10];
const stackexchangeevent = [10,30,10,10,10];
const twitterevent = [30,10,30,10,10];
const webevent = [10,60,10,30,20];
const wikipediaevent = [60,60,30,10,10];
const wordpressevent = [70,90,30,10,10];
const year0 = 2016;
const year1 = 2017;
const year2 = 2018;
const year3 = 2019;
const year4 = 2020;

/* CHANGE COLORS HERE */
const cambiaColor = '#002f99';
const crossrefColor = '#F4AE22';
const dataciteColor = '#F4AE22';
const hypothesisColor = '#D22C7F';
const newsfeedColor = '#452fa3';
const redditColor = '#FF4500';
const redditLinksColor = '#FF1100';
const stackExchangeColor = '#f68749';
const twitterColor = '#1DA1F2';
const webColor = '#257E22';
const wikipediaColor = '#D7D8D9';
const wordpressColor = '#904860';

/*
Now we can prepend the column names since these are constant. 
Names need to be at [0]
*/
cambiaevent.unshift('Cambia');
crossrefevent.unshift("Crossref");
dataciteevent.unshift("DataCite");
hypothesisevent.unshift("Hypothesis");
newsfeedevent.unshift("Newsfeed");
redditevent.unshift("Reddit");
redditlinksevent.unshift("Reddit-Links");
stackexchangeevent.unshift("Stack Exchange");
twitterevent.unshift("Twitter");
webevent.unshift("Web");
wikipediaevent.unshift("Wikipedia");
wordpressevent.unshift("Wordpress");

/*
----------- No changes below this line ------------------------------------
*/
var chart = c3.generate({
  bindto: '#chart',
  data: {
        columns: [
          cambiaevent,
          crossrefevent,
          dataciteevent,
          hypothesisevent,
          newsfeedevent,
          redditevent,
          redditlinksevent,
          stackexchangeevent,
          twitterevent,
          webevent,
          wikipediaevent,
          wordpressevent
        ],
        colors: {
          [cambiaevent[0]]: cambiaColor,
          [crossrefevent[0]]: crossrefColor,
          [dataciteevent[0]]: dataciteColor,
          [hypothesisevent[0]]: hypothesisColor,
          [newsfeedevent[0]]: newsfeedColor,
          [redditevent[0]]: redditColor,
          [redditlinksevent[0]]: redditLinksColor,
          [stackexchangeevent[0]]: stackExchangeColor,
          [twitterevent[0]]: twitterColor,
          [webevent[0]]: webColor,
          [wikipediaevent[0]]: wikipediaColor,
          [wordpressevent[0]]: wordpressColor,
        },
        legend: {
          position: 'right'
        },
        type: 'bar',
        /* 
        This is confusing, but these need to be the items at position [0] in
        each list. It won't work if you put cambiaevent or 'cambiaevent'.
        It must be the cambiaevent[0]

        If you want to change their displayed names, change them in the 
        unshift section above.
        */
        groups: [
          [ cambiaevent[0], 
            crossrefevent[0], 
            dataciteevent[0], 
            hypothesisevent[0],
            newsfeedevent[0],
            redditevent[0],
            redditlinksevent[0],
            stackexchangeevent[0],
            twitterevent[0],
            webevent[0],
            wikipediaevent[0],
            wordpressevent[0]
        ]]
  },
  grid: {
      y: {
         lines: [{value:0}]
      }
  },
  axis: {
    x: {
      label: {
        text: '',
        position: 'outer-center'
      },
      type: 'category',
      categories: [year0, year1, year2, year3, year4]        
    },
    y: {
      label: {
        text: 'Total Events',
        position: 'outer-middle'
      }
    }
  },
  /*
  size: {
    height: 600
  }
  */
});