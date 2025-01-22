/**
 * Finds episodes based on the user's description.
 * Hides the main container, shows the results container,
 * and displays a loading spinner while searching.
 */

async function findEpisode() {
    const description = document.getElementById('episode-description').value;
    if (!description) {
        alert("Please, enter a description first!");
        return;
    }

    // Hide the main container
    document.querySelector('.main-container').style.display = 'none';
    // Show the results container
    const resultsContainer = document.getElementById('results');
    resultsContainer.classList.add('visible');
    
    // Display loading spinner and text
    const resultsGrid = document.querySelector('.results-grid');
    resultsGrid.innerHTML = `
        <div class="loading-container">
            <div class="spinner"></div>
            <p class="loading-text">Searching for the best episodes...</p>
        </div>
    `;

    try {
        // Send a POST request to the server with the description
        const response = await fetch('/find_episode?' + new URLSearchParams({
            description: description
        }), {
            method: 'POST',
        });
        
        // Parse the JSON response
        const data = await response.json();
        
        // Display the search results
        resultsContainer.innerHTML = `
            <div class="user-description-container">
                <p class="search-icon">🔎</p>
                <p class="user-description">"${description}"</p>
            </div>
            <h2 class="results-title">Maybe you are looking for one of these 3 episodes...</h2>
            <div class="results-grid">
                ${data.results.map(episode => {
                    // Convert episode title to wiki format
                    const wikiTitle = episode.title.replace(/ /g, '_');
                    const wikiUrl = `https://simpsons.fandom.com/wiki/${wikiTitle}`;
                    
                    return `
                        <div class="episode-card">
                                <div class="episode-title">${episode.title}</div>
                                <div class="episode-details">
                                    Season ${episode.season}<br>
                                    Episode ${episode.episode}
                                </div>
                            <a href="${wikiUrl}" target="_blank" class="more-info-btn">
                                More Info
                            </a>
                        </div>
                    `;
                }).join('')}
            </div>
            <div class="search-again-container">
                <button id="search-again-btn" class="search-again-btn">Search Again</button>
            </div>
        `;
        
        document.getElementById('search-again-btn').addEventListener('click', () => {
            location.reload();
        });
    } catch (error) {
        resultsGrid.innerHTML = '<p>Error finding episode. Please try again.</p>';
    }
}