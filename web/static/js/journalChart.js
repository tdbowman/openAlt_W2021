// These should not change - for now. Need to set dynamically in the future
const xAxis = [1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]

// 'x' needs to be in the [0] position, because it is the title of our array, and C3 demands the title be at [0].
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
          label: {
            text: '',
            position: 'outer-center'
          },
          tick: {
            culling: true
          }
        },
        y: {
          label: {
            text: 'Papers Published',
            position: 'outer-middle',
          },
          tick: {
            // Hide the automatically generated tick marks if they are not natural numbers or < 0.
            format: function (d) { 
              if (d < 0) {
                  return null
              }
              else if (d % 1 > 0) {
                  return null
              }
              else {
                return d;  
              }
            }
          }
        }
      },
      legend: {
        hide: true
      },
    // Disable clicking, hovering tooltips.
    interaction: {
    enabled: false
    },
});

// These two lines force the C3 chart back into its column. 
var loader = document.getElementById("changeAfterChart");
loader.className = "col-sm-12";

// This line sets the x-axis label a little lower on the page to accomodate the larger font size.
$(".c3-axis-x-label").attr("dy", 50);