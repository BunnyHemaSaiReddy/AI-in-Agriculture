// Toggle the video search bar visibility
function toggleVideoSearch() {
    let videoSection = document.getElementById("video-search-section");
    videoSection.style.display = videoSection.style.display === "none" ? "block" : "none";
}

// Fetch and display YouTube videos inside the page
async function searchVideos() {
    let query = document.getElementById("query").value.trim();
    if (query === "") {
        alert("Please enter a search term.");
        return;
    }

    try {
        let response = await fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: query })
        });

        let data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        displayVideos(data.links);
    } catch (error) {
        console.error("Error fetching videos:", error);
        alert("Failed to load videos. Please try again later.");
    }
}

// Display video results inside the website
function displayVideos(videoLinks) {
    let container = document.getElementById("video-container");
    container.innerHTML = ""; // Clear previous results

    videoLinks.forEach(link => {
        let videoId = extractVideoId(link);

        if (videoId) {
            let videoElement = document.createElement("div");
            videoElement.classList.add("video-item");
            videoElement.innerHTML = `
                <iframe width="100%" height="200" 
                    src="https://www.youtube.com/embed/${videoId}" 
                    frameborder="0" allow="encrypted-media" allowfullscreen>
                </iframe>
            `;

            container.appendChild(videoElement);
        }
    });
}

// Extract the YouTube video ID from a URL
function extractVideoId(url) {
    let match = url.match(/(?:v=|\/embed\/|\/\d\/|\/vi\/|\/v\/|youtu.be\/|\/e\/|watch\?v=)([^#\&\?]*)/);
    return match && match[1] ? match[1] : null;
}
