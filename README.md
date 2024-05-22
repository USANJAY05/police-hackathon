<h1>Karnataka Police Hackathon Crime Analysis Project</h1>
<a href="http://172.188.97.56:8080"><img src="https://drive.usercontent.google.com/download?id=16SAt9JdWOdr2fRX3zN0FjqQoosCZYgNC"></a>
<h2>Click the image to view the website 👆</h2>
<h2>Download the CSV and include in this folder</h2>
<a href="https://drive.google.com/file/d/1iCvyzlVHNSP6cdhdMkhvkIVy3OP3tFBA/view?usp=sharing">Click here to download CSV</a>
<br>
  <h2>Install the packages</h2>
<ul>
  <li> flask</li>
  <li>numpy</li>
  <li>pandas</li>
  <li>scipy</li>
  <li>scikit-learn</li>
  <li>matplotlib</li>
  <li>seaborn</li>
  <li>statsmodels</li>
</ul>
<h3>You can run the app locally using docker</h3>
    <p id="textToCopy" onclick="copyText('docker pull usanjay05/crimexsura-kph:latest')">docker pull usanjay05/crimexsura-kph:latest</p>
<p>use (python3 app.py) to run the app</p>

<script>
    function copyText() {
        // Get the element by its ID or any other selector
        var element = document.getElementById("textToCopy");

        // Create a range to select the text
        var range = document.createRange();
        range.selectNode(element);

        // Select the text inside the range
        window.getSelection().removeAllRanges(); // Clear previous selections
        window.getSelection().addRange(range);

        // Copy the selected text
        document.execCommand("copy");

        // Deselect the text to avoid further complications
        window.getSelection().removeAllRanges();
    }
</script>
