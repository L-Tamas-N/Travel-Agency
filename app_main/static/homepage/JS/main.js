document.addEventListener("DOMContentLoaded", function () {
    // Tab functionality
    const tabTitles = document.querySelectorAll('.tab-titles li');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabTitles.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.getAttribute('data-tab');

            tabTitles.forEach(tab => tab.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));

            tab.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });

    // View More for reviews
    const reviewMessages = document.querySelectorAll('.review-message');
    
    reviewMessages.forEach(function(reviewMessage) {

        const words = reviewMessage.textContent.split(' ');
        
        const first10Words = words.slice(0, 7).join(' ') + '...';
        
        reviewMessage.textContent = first10Words;

                // Save the full text for later use
        const fullText = words.join(' ');

        // Update the review message text with only the first 10 words
        reviewMessage.textContent = first10Words;

        // Find the "View More" link
        const viewMoreButton = reviewMessage.nextElementSibling;
        
        // Add functionality to the "View More" link
        viewMoreButton.addEventListener('click', function() {
            // Toggle between showing full or partial text
            if (viewMoreButton.textContent === 'View More') {
                // Show full message
                reviewMessage.textContent = fullText;
                viewMoreButton.textContent = 'View Less';
            } else {
                // Show only the first 10 words
                reviewMessage.textContent = first10Words;
                viewMoreButton.textContent = 'View More';
            }
        });
    });
});