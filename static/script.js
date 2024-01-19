// Function to parse date strings into Date objects
function parseDate(dateString) {
  const parsedDate = new Date(dateString);
  return isNaN(parsedDate.getTime()) ? null : parsedDate;
}

// Wait for the DOM to be ready
document.addEventListener('DOMContentLoaded', function () {
  // Make a request to your Flask route
  fetch('/dictdata')
    .then(response => response.json())
    .then(data => {
      // Get the textarea element
      var textarea = document.getElementById('data');

      // Display the JSON data in the textarea
      textarea.value = JSON.stringify(data, null, 2);
      
      let longestStreakPlayer = "";
      let longestStreak = 0;
      let longestStreakDays = 0;
      let currentStreakPlayer = "";
      let currentStreak = 0;
      let currentStreakStart = "";
      
      for (let match in data) {
        let players = data[match]["Player Data"];
        for (let player of players) {
          if (player["Stat Name"] === "HIGHEST SCORE") {
            if (player["Player Name"] === currentStreakPlayer) {
              currentStreak += 1;
            } else {
              currentStreakPlayer = player["Player Name"];
              currentStreak = 1;
              currentStreakStart = new Date(data[match]["Date Scraped"]);
            }
            if (currentStreak > longestStreak) {
              longestStreak = currentStreak;
              longestStreakPlayer = currentStreakPlayer;
              let startDate = new Date(currentStreakStart.getFullYear(), currentStreakStart.getMonth(), currentStreakStart.getDate());
              let endDate = new Date(data[match]["Date Scraped"]);
              endDate = new Date(endDate.getFullYear(), endDate.getMonth(), endDate.getDate());
              longestStreakDays =Math.floor( (endDate - startDate) / (1000 * 60 * 60 * 24) + 1);
            }
          }
        }
      }
      
      //console.log(longestStreakPlayer, longestStreakDays);
      // Display the result on the page
      var resultDiv = document.getElementById('result');
      resultDiv.innerHTML = `
        <p>Player with HIGHEST SCORE held the stat the longest: ${longestStreakPlayer}</p>
        <p>Days held: ${longestStreakDays}</p>
      `;
    })
    .catch(error => console.error('Error fetching data:', error));
});
