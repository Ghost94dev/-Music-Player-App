// script.js - Clean version
var audio = {
    init: function() {
        var $that = this;
        $(function() {
            $that.components.media();
            $that.setupAutoPlay();
            $that.setupMobileNavigation();
        });
    },
    components: {
        media: function(target) {
            var media = $("audio.fc-media", (target !== undefined) ? target : "body");
            if (media.length) {
                media.mediaelementplayer({
                    audioHeight: 40,
                    features : ["playpause", "current", "duration", "progress", "volume", "tracks", "fullscreen"],
                    alwaysShowControls: true,
                    timeAndDurationSeparator: "<span></span>",
                    iPadUseNativeControls: true,
                    iPhoneUseNativeControls: true,
                    AndroidUseNativeControls: true
                });
            }
        }
    },

    setupAutoPlay: function() {
        var audioElement = document.getElementById("fc-media");

        if (audioElement) {
            // Add event listener for when the song ends
            audioElement.addEventListener("ended", function() {
                audio.playNext();
            });
        }
    },

    playNext: function() {
        // Get current page from URL parameters
        var urlParams = new URLSearchParams(window.location.search);
        var currentPage = parseInt(urlParams.get("page")) || 1;

        // Get total pages from the data attribute on the music-player div
        var totalPagesElement = document.querySelector(".music-player");
        var totalPages = parseInt(totalPagesElement ? totalPagesElement.dataset.totalPages : 1);

        var nextPage;

        // If we're at the last page, loop back to the first page
        if (currentPage >= totalPages) {
            nextPage = 1;
        } else {
            nextPage = currentPage + 1;
        }

        // Navigate to the next page
        window.location.href = "?page=" + nextPage;
    },

    playPrevious: function() {
        // Get current page from URL parameters
        var urlParams = new URLSearchParams(window.location.search);
        var currentPage = parseInt(urlParams.get("page")) || 1;

        // Get total pages from the data attribute on the music-player div
        var totalPagesElement = document.querySelector(".music-player");
        var totalPages = parseInt(totalPagesElement ? totalPagesElement.dataset.totalPages : 1);

        var previousPage;

        // If we're at the first page, loop to the last page
        if (currentPage <= 1) {
            previousPage = totalPages;
        } else {
            previousPage = currentPage - 1;
        }

        // Navigate to the previous page
        window.location.href = "?page=" + previousPage;
    },

    setupMobileNavigation: function() {
        const hamburger = document.getElementById('hamburger');
        const navMenu = document.getElementById('navMenu');

        if (hamburger && navMenu) {
            hamburger.addEventListener('click', (e) => {
                e.stopPropagation();
                navMenu.classList.toggle('active');
                hamburger.classList.toggle('active');
            });

            // Close menu when clicking outside
            document.addEventListener('click', (e) => {
                if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
                    navMenu.classList.remove('active');
                    hamburger.classList.remove('active');
                }
            });
        }
    }
};

audio.init();

// Enhanced lyrics handling with better error checking
document.addEventListener("DOMContentLoaded", function() {
    const audio = document.getElementById("fc-media");
    const lyricsContainer = document.getElementById("song-lyrics");

    if (!audio || !lyricsContainer) {
        console.error("Audio element or lyrics container not found");
        return;
    }

    try {
        // Get and clean the lyrics data
        const rawLyrics = lyricsContainer.dataset.lyrics || "[]";

        // Better cleaning of escaped quotes and HTML entities
        const cleanedLyrics = rawLyrics
            .replace(/&quot;/g, "\"")
            .replace(/&#x27;/g, "'")
            .replace(/&amp;/g, "&")
            .replace(/&lt;/g, "<")
            .replace(/&gt;/g, ">");

        console.log("Raw lyrics:", rawLyrics);
        console.log("Cleaned lyrics:", cleanedLyrics);

        let lyricsData;
        try {
            lyricsData = JSON.parse(cleanedLyrics);
        } catch (parseError) {
            console.error("JSON parse error:", parseError);
            // Try to extract lyrics from a different format if JSON parsing fails
            lyricsData = [];
        }

        if (!Array.isArray(lyricsData) || lyricsData.length === 0) {
            console.warn("No valid lyrics data found");
            lyricsContainer.textContent = "Now playing: " + (document.querySelector(".titre h1")?.textContent || "Unknown");
            return;
        }

        // Convert time formats and validate data
        const normalizedLyrics = lyricsData
            .filter(item => item && item.time && item.lyrics) // Filter out invalid entries
            .map(item => {
                let timeStr = item.time;

                // Handle different time formats
                if (timeStr.includes(".")) {
                    const timeParts = timeStr.split(".");
                    timeStr = timeParts[0]; // Keep only MM:SS part
                }

                return {
                    time: timeStr,
                    lyrics: item.lyrics.trim(),
                    timeInSeconds: convertToSeconds(timeStr)
                };
            })
            .sort((a, b) => a.timeInSeconds - b.timeInSeconds); // Sort by time

        console.log("Normalized lyrics:", normalizedLyrics);

        let currentLyricIndex = 0;

        // Update time display
        function updateTimeDisplay() {
            const currentTimeSpan = document.querySelector(".current-time");
            const durationSpan = document.querySelector(".duration");

            if (currentTimeSpan) {
                currentTimeSpan.textContent = formatTime(audio.currentTime);
            }

            if (durationSpan && !isNaN(audio.duration)) {
                durationSpan.textContent = formatTime(audio.duration);
            }
        }

        audio.addEventListener("timeupdate", function() {
            const currentTime = audio.currentTime;

            updateTimeDisplay();

            if (normalizedLyrics.length === 0) return;

            // Find current lyric with better logic
            let newLyricIndex = currentLyricIndex;

            // Look for the appropriate lyric line
            for (let i = 0; i < normalizedLyrics.length; i++) {
                if (currentTime >= normalizedLyrics[i].timeInSeconds) {
                    newLyricIndex = i;
                } else {
                    break;
                }
            }

            // Update display only if the lyric changed
            if (newLyricIndex !== currentLyricIndex) {
                currentLyricIndex = newLyricIndex;
                lyricsContainer.textContent = normalizedLyrics[currentLyricIndex].lyrics;
            }
        });

        // Initialize with first lyric
        if (normalizedLyrics.length > 0) {
            lyricsContainer.textContent = normalizedLyrics[0].lyrics;
        }

        function convertToSeconds(timeStr) {
            try {
                const parts = timeStr.split(":");
                if (parts.length === 2) {
                    const mins = parseInt(parts[0]) || 0;
                    const secs = parseFloat(parts[1]) || 0;
                    return mins * 60 + secs;
                }
                return 0;
            } catch (e) {
                console.error("Time conversion error:", e);
                return 0;
            }
        }

        function formatTime(seconds) {
            if (isNaN(seconds)) return "00:00";
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
        }

    } catch (e) {
        console.error("Lyrics initialization error:", e);
        lyricsContainer.textContent = "Now playing: " + (document.querySelector(".titre h1")?.textContent || "Unknown");
    }
});