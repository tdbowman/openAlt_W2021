/* 
This script generates the stacked bar charts using c3 and d3.

Reassign these with Python - position in array corresponds to column
Like: [column1, column2, column3, column4, column5]
All 12 of these combine to make 5 bars, which are each 12 blocks high.

Years(columns) will be generated within each dashboard function in app.py.

Bar Chart Legend Colors for each platform. */

const cambiaColor = '#002f99';
const crossrefColor = '#F4AE22';
const dataciteColor = '#15d4cf';
const hypothesisColor = '#D22C7F';
const newsfeedColor = '#a89ae5';
const redditColor = '#FF4500';
const redditLinksColor = '#983333';
const stackExchangeColor = '#ee874e';
const twitterColor = '#1DA1F2';
const webColor = '#257E22';
const wikipediaColor = '#D7D8D9';
const wordpressColor = '#e3b9c7';
const f1000Color = '#D7ffD9';

// Platforms set to true, these variables will be used when hiding the platform bars in the chart and the events in the events section of the article dashboard webpage.
let cambiaBool = true;
let crossrefBool = true;
let dataciteBool = true;
let hypothesisBool = true;
let newsfeedBool = true;
let redditBool = true;
let redditLinksBool = true;
let stackExchangeBool = true;
let twitterBool = true;
let webBool = true;
let wikipediaBool = true;
let wordpressBool = true;
let f1000bool = true;

/*
Now we can prepend the column names since these are constant. 
Names need to be at [0].
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
f1000event.unshift("F1000");

// We need to set all these to "initial" now, so we can hide and reset them later on.
let elements = document.getElementsByClassName("eventItem");
for (var i = 0; i < elements.length; i++) {
	elements[i].style.display = "initial";
}


/*
----------- C3 Chart ------------------------------------
*/
var chart = c3.generate({
	bindto: '#chart',
	data: {
		columns: [
			cambiaevent,
			crossrefevent,
			dataciteevent,
			f1000event,
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
		type: 'bar',
		groups: [
			[cambiaevent[0],
			crossrefevent[0],
			dataciteevent[0],
			f1000event[0],
			hypothesisevent[0],
			newsfeedevent[0],
			redditevent[0],
			redditlinksevent[0],
			stackexchangeevent[0],
			twitterevent[0],
			webevent[0],
			wikipediaevent[0],
			wordpressevent[0]
			]],
		colors: {
			[cambiaevent[0]]: cambiaColor,
			[crossrefevent[0]]: crossrefColor,
			[dataciteevent[0]]: dataciteColor,
			[f1000event[0]]: f1000Color,
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
	},

	/* 
	This is confusing, but these need to be the items at position [0] in
	each list. It won't work if you put cambiaevent or 'cambiaevent'.
	It must be the cambiaevent[0]
  
	If you want to change their displayed names, change them in the 
	unshift section above.
	*/
	legend: {
		position: 'right',
		item: {
			// When you click on one of the platforms, this event handler determines which <div> to hide in the events section of article dashboard.
			onclick: function (id) {

				// Switching on the column names - determine what is clicked in the legend.
				switch (id) {

					case cambiaevent[0]:
						if (cambiaBool) {
							chart.hide(id);
							cambiaBool = false;
						} else {
							chart.show(id);
							cambiaBool = true;
						}
						hideElements(elements);
						break;

					case crossrefevent[0]:
						if (crossrefBool) {
							chart.hide(id);
							crossrefBool = false;
						} else {
							chart.show(id);
							crossrefBool = true;
						}
						hideElements(elements);
						break;

					case dataciteevent[0]:
						if (dataciteBool) {
							chart.hide(id);
							dataciteBool = false;
						} else {
							chart.show(id);
							dataciteBool = true;
						}
						hideElements(elements);
						break;

					case f1000event[0]:
						if (wordpressBool) {
							chart.hide(id);
							wordpressBool = false;
						} else {
							chart.show(id);
							wordpressBool = true;
						}
						hideElements(elements);
						break;

					case hypothesisevent[0]:
						if (hypothesisBool) {
							chart.hide(id);
							hypothesisBool = false;
						} else {
							chart.show(id);
							hypothesisBool = true;
						}
						hideElements(elements);
						break;

					case newsfeedevent[0]:
						if (newsfeedBool) {
							chart.hide(id);
							newsfeedBool = false;
						} else {
							chart.show(id);
							newsfeedBool = true;
						}
						hideElements(elements);
						break;

					case redditevent[0]:
						if (redditBool) {
							chart.hide(id);
							redditBool = false;
						} else {
							chart.show(id);
							redditBool = true;
						}
						hideElements(elements);
						break;

					case redditlinksevent[0]:
						if (redditLinksBool) {
							chart.hide(id);
							redditLinksBool = false;
						} else {
							chart.show(id);
							redditLinksBool = true;
						}
						hideElements(elements);
						break;

					case stackexchangeevent[0]:
						if (stackExchangeBool) {
							chart.hide(id);
							stackExchangeBool = false;
						} else {
							chart.show(id);
							stackExchangeBool = true;
						}
						hideElements(elements);
						break;

					case twitterevent[0]:
						if (twitterBool) {
							chart.hide(id);
							twitterBool = false;
						} else {
							chart.show(id);
							twitterBool = true;
						}
						hideElements(elements);
						break;

					case webevent[0]:
						if (stackExchangeBool) {
							chart.hide(id);
							stackExchangeBool = false;
						} else {
							chart.show(id);
							stackExchangeBool = true;
						}
						hideElements(elements);
						break;

					case wikipediaevent[0]:
						if (wikipediaBool) {
							chart.hide(id);
							wikipediaBool = false;
							console.log(wikipediaBool);
						} else {
							chart.show(id);
							wikipediaBool = true;
						}
						hideElements(elements);
						break;

					case wordpressevent[0]:
						if (wordpressBool) {
							chart.hide(id);
							wordpressBool = false;
						} else {
							chart.show(id);
							wordpressBool = true;
						}
						hideElements(elements);
						break;
				}
			}
		},
	},
	grid: {
		y: {
			show: false
		}
	},
	axis: {
		x: {
			label: {
				text: '',
				position: 'outer-center'
			},
			type: 'category',
			categories: [years_list[0], years_list[1], years_list[2], years_list[3], years_list[4]]
		},
		y: {
			label: {
				text: 'Total Events',
				position: 'outer-middle',
			},
			tick: {
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
		},
		rotated: false
	},
	size: {
		width: 670
	}
});


// This function hides the bar chart items the user clicks, both in the chart and in the events section below.
function hideElements(elements) {
	//elements = document.getElementsByClassName("eventItem");
	for (var i = 0; i < elements.length; i++) {
		// If the element ID is twitter, and the twitterBool is false, hide twitter.
		// False booleans mean we want to hide them.

		// WARNING - THIS TOOK FOREVER TO FIGURE OUT - CHANGE IT AT YOUR OWN RISK.
		// YOU ABSOLUTELY MUST USE  .style.display = "none" or .style.display = "initial".
		if (elements[i].id === "twitter" && twitterBool === false) {
			elements[i].style.display = "none";
		}
		else if (elements[i].id === "wikipedia" && wikipediaBool === false) {
			elements[i].style.display = "none";
		}
		else if (elements[i].id === "reddit" && redditBool === false) {
			elements[i].style.display = "none";
		}
		else if (elements[i].id === "hypothesis" && hypothesisBool === false) {
			elements[i].style.display = "none";
		}
		else if (elements[i].id === "newsfeed" && newsfeedBool === false) {
			elements[i].style.display = "none";
		}
		else if (elements[i].id === "redditlinks" && redditLinksBool === false) {
			elements[i].style.display = "none";
		}
		else if (elements[i].id === "stackexchange" && stackExchangeBool === false) {
			elements[i].style.display = "none";
		}
		else if (elements[i].id === "cambia" && cambiaBool === false) {
			elements[i].style.display = "none";
		}
		else if (elements[i].id === "web" && webBool === false) {
			elements[i].style.display = "none";
		}
		else if (elements[i].id === "wordpressdotcom" && wordpressBool === false) {
			elements[i].style.display = "none";
		}
		else {
			elements[i].style.display = "initial";
		}
	}
}

// Without this, the chart would extend beyond its column and obstruct other divs within the row.
// These two lines force the C3 chart back into its column. 
var loader = document.getElementById("changeAfterChart");
loader.className = "col-sm-7";