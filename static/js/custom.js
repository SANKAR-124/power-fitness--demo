$('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });


// Wait for the document to be fully loaded
$(document).ready(function() {

    // Listen for a click on our new button
    $('.get-quote-btn').on('click', function(e) {
        e.preventDefault(); // This stops the link from jumping to the top of the page

        // Show the pop-up modal
        $('#quoteModal').modal('show');

        // Fetch a random quote from our Flask API
        fetch(`/api/random-quote?t=${new Date().getTime()}`)
            .then(response => response.json())
            .then(data => {
                // Update the modal's text with the data we received
                $('#quote-text').text(data.text);
                $('#quote-author').text(data.author);
            });
    });

});