// Only run this function when the document has fully loaded.
$(document).ready(function () {

    // Grab the elements in bold then the last bold element within the class ".pagination-page-info". 
    let $paginationBoldText = $(".pagination-page-info").children("b");
    let $lastPaginationBoldText = $paginationBoldText.last();

    // If the total records are less than 11, hide the "Per Page" Form.
    if (parseInt($lastPaginationBoldText.text(), 10) < 11) {
        $(".perPages").hide();
    }

    // Change positioning of X-axis label. Will look into Bootstrap 4.0+ for row padding/margin manipulation to give more room for the X-axis label.
    $(".c3-axis-x-label").attr("dy", "36");

    // Create jQuery variables to reference the text box and the submit button
    let $yearInput = $("#yearBox");
    let $submitButton = $("input[type='submit']");

    // Creates in instance of the currentTime and grabs the year from it.
    let currentTime = new Date();
    let year = currentTime.getFullYear();

    // Grab the publication year and slice it to remove the month portion.
    // The array articleDates is initialized near the bottom of this document(line 234).
    let oldestPubYear = articleDates[0];

    // Iterate through the list of dates and find the oldest date for the author.
    for (let i = 0; i < articleDates.length; i++) {
        if (oldestPubYear > articleDates[i]) {
            oldestPubYear = articleDates[i];
        }
    }

    // Grabs all elements (g) from the class ".c3-axis-y" and stores them as objects in $yAxis.
    let $yAxis = $(".c3-axis-y");

    // Grabs all the children elements (g) of class ".tick" and stores them as objects in $yAxisTicks. 
    let $yAxisTicks = $yAxis.children(".tick");

    // Grabs all the elements (g) of class ".c3-legend-item" and stores them as objects in $legendItems.
    let $legendItems = $(".c3-legend-item");

    // When you click on any of the platforms within the legend.
    $legendItems.click(function () {

        //  setTimeout(function,x) executes a function after x milliseconds.
        setTimeout(function () {
            // Grabs the tick elements after the page loads with the new chart data.
            $yAxis = $(".c3-axis-y");
            $yAxisTicks = $yAxis.children(".tick");
            // Loop through each tick object..
            $yAxisTicks.each(function () {
                // Store the label text of the tick into $tickText. 
                let $tickText = $(this).children("text").text();

                // If the label text is an empty string, remove the line associated with it.
                if ($tickText === '') {
                    $(this).children("line").remove();
                }
            });
        }, 500);

    });

    // When the user clicks on the submit button..
    $submitButton.click(function () {
        // If the year text box is empty, send an alert and don't allow the user to submit the form.
        if (document.forms['YearRange'].year.value == "") {
            alert("Please enter a year.");
            return false;
        }
        // If the year input is greater than the current year, send an alert and don't allow the user to submit the form.
        else if (document.forms['YearRange'].year.value > String(year)) {
            alert("Please enter a year before " + year + ".");
            return false;
        }
        // If the year input is less than the oldest publication year, send an alert and don't allow the user to submit the form.
        else if (document.forms['YearRange'].year.value < oldestPubYear) {
            alert("Please enter a year after " + oldestPubYear + ".");
            return false;
        }
    });

    // When the focus is inside the year text box...
    $yearInput.keydown(function (event) {
        // Allow numbers from the top row of the keyboard and numpad.
        if (event.keyCode >= 48 && event.keyCode <= 57 || event.keyCode >= 96 && event.keyCode <= 105) {
            return true;
        }
        // Allow backspace, tab or enter button.
        else if (event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 13) {
            return true;
        }
        // Disable shift key to stop special characters from entering text box.
        else if (event.shiftKey == true) {
            return false;
        }
        else {
            return false;
        }
    });
});