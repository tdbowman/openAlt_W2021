// Python sets these, sends them to jinja, then JS picks them up
//const publishedPerYear = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
//const publishedPerYear = publishedPerYear
//const journalName = "Nature"
// These should not change - for now. Need to set dynamically in the future
const years = [1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
const strLabel = "Articles published in " + journalName + " per year";

// Have to prepend the column label
publishedPerYr.unshift(strLabel);

// Setup the X axis, prepend the column label
const xAxis = years;
xAxis.unshift('x');

var chart = c3.generate({
    data: {
        x: 'x',
        columns: [
            xAxis,
            publishedPerYr
        ]
    },
    axis: {
        x: {
          tick: {
            culling: true
          }
        },
        y: {
          label: {
            min: 0,
            text: 'Number of Articles',
            position: 'outer-middle',

          }
        }
      },
      legend: {
        hide: true
        //or hide: 'data1'
        //or hide: ['data1', 'data2']
      },
    interaction: {
    enabled: false
    },
    size: {
      width: 670
    }
});

// These two lines force the C3 chart back into its column. 
var loader = document.getElementById("changeAfterChart");
loader.className = "col-sm-7";