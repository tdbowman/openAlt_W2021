// Author: Rihat Rahman
// Lines 1 - 78
// This script generates citation bar graph
//-------------------------------------------------------------------------------------------
const citationColor = '#FF4500';

let citationBool = true;

citationEvent.unshift('Citation');

let citationElements = document.getElementsByClassName("citationItem");


for (var i = 0; i < citationElements.length; i++) {
	citationElements[i].style.display = "initial";
}

var citationChart = c3.generate({
    bindto: '#citationChart',
    data: {
        columns: [
            citationEvent
        ],

        type: 'bar',
        groups: [[citationEvent[0]]],
        colors: {
            [citationEvent[0]]: citationColor
        },
    },

    legend: {
        position: 'right',
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
			categories: [citation_years_list[0], citation_years_list[1], citation_years_list[2], citation_years_list[3], citation_years_list[4]]
		},
		y: {
			label: {
				text: 'Total Citations',
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

var loader = document.getElementById("changeAfterChart");
loader.className = "col-sm-7";
//-------------------------------------------------------------------------------------------