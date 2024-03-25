// Make an AJAX request to fetch recent titles with URLs from Django backend
fetch('/get_titles/')
    .then(response => response.json())
    .then(titles => {
        // Code to display clickable titles using your typing bot
        const typingBot = document.getElementById('typing-bot'); // Replace with your actual bot element

        function createClickableTitle(titleData) {
            const titleLink = document.createElement('a');
            titleLink.textContent = titleData.title;
            titleLink.href = titleData.url;
            titleLink.target = '_blank'; // Open in a new tab
            return titleLink;
        }

        const recentTitles = titles.slice(-2); // Get the last two titles (most recent)
        const limit = 10; // Set the desired number of titles to display

        let currentIndex = 0;

        function typeNextTitle() {
            if (currentIndex < recentTitles.length && currentIndex < limit) {
                typingBot.innerHTML = ''; // Clear the typing bot element

                const titleElement = createClickableTitle(recentTitles[currentIndex]);
                typingBot.appendChild(titleElement);

                currentIndex++;
                setTimeout(typeNextTitle, 2000); // Change the typing speed as needed
            }
        }

        typeNextTitle();
    })
    .catch(error => console.error('Error fetching titles:', error));
