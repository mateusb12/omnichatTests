import {urlList} from './test_url.js';

document.getElementById('csvFileInput').addEventListener('change', loadCSV);
document.getElementById('sendButton').addEventListener('click', sendData);
document.addEventListener('DOMContentLoaded', function () {
    populateDropdownWithUrls();
});

function populateDropdownWithUrls() {
    const urlDropdown = document.getElementById('urlDropdown');
    urlList.forEach(url => {
        const option = document.createElement('option');
        option.value = url;
        option.textContent = url;
        urlDropdown.appendChild(option);
    });
}

function checkServerStatus() {
    const port = 4608;
    const url = `http://localhost:${port}/`;

    fetch(url)
        .then((response) => {
            if (!response.ok) {
                throw new Error('Server returned a non-200 response: ' + response.status);
            }
            return response.text(); // or response.json() if you are returning JSON
        })
        .then((data) => {
            console.log('Server is running:', data);
        })
        .catch((error) => {
            if (error.message.includes('NetworkError') || error.message.includes('Failed to fetch')) {
                console.error('Server is offline or blocked by CORS.');
                alert('Please start the server using START.BAT and try again.');
            } else {
                console.error('Error:', error.message);
            }
        });
}


function sanitizeContent(content) {
    // Replace \n with <br> for line breaks
    return content.replace(/\\n/g, '<br>');
}

function loadCSV(event) {
    const file = event.target.files[0];
    if (!file) return;

    // checkServerStatus();

    const reader = new FileReader();
    reader.onload = function (e) {
        const content = e.target.result;
        const lines = content.split('\n').map(line => line.split(';'));

        // Populate table
        const table = document.getElementById('csvTable');
        table.innerHTML = '';  // Clear existing content

        const tbody = document.createElement('tbody'); // Create a single tbody outside the loop

        lines.forEach((line, index) => {
            if (index === 0) {  // header
                const thead = document.createElement('thead');
                line.forEach(header => {
                    const th = document.createElement('th');
                    th.textContent = header;
                    thead.appendChild(th);
                });

                const thActual = document.createElement('th'); // ActualOutput column
                thActual.textContent = 'ActualOutput';
                thead.appendChild(thActual);

                const thTestResult = document.createElement('th'); // TestResult column
                thTestResult.textContent = 'TestResult';
                thead.appendChild(thTestResult);

                table.appendChild(thead);
            } else {  // data rows
                const tr = document.createElement('tr');
                line.forEach(cell => {
                    const td = document.createElement('td');
                    console.log("Before sanitize: " + cell);
                    const sanitizedContent = sanitizeContent(cell);
                    console.log("After sanitize: " + sanitizedContent);
                    td.innerHTML = sanitizedContent;
                    tr.appendChild(td);
                });

                const tdActual = document.createElement('td'); // ActualOutput cell placeholder
                tr.appendChild(tdActual);

                const tdTestResult = document.createElement('td'); // TestResult cell placeholder
                tr.appendChild(tdTestResult);

                tbody.appendChild(tr); // Append the row to tbody
            }
        });

        table.appendChild(tbody); // Append the tbody to the table after the loop
    };
    reader.readAsText(file);
}


async function sendData() {
    console.log("Button clicked");
    const urlDropdown = document.getElementById('urlDropdown');
    const selectedUrl = urlDropdown.value;
    await fillColumnsWithBotResponse(selectedUrl);
    compareOutputsAndPlaceEmojis();
}

async function getBotResponseFromFlask(inputCellValue, selectedUrl) {
    try {
        // Send the POST request
        const response = await fetch(selectedUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'ProfileName': 'Mateus',
                'From': 'whatsapp:+558599171902',
                'WaId': '558599171902',
                'Body': inputCellValue
            },
            body: JSON.stringify(inputCellValue)  // Send the string directly
        });

        // Check if the request was successful
        if (!response.ok) {
            throw new Error('Server returned a non-200 response: ' + response.status);
        }

        // Check the response content type
        const contentType = response.headers.get('content-type');

        let data;

        if (contentType && contentType.includes('application/json')) {
            // Process JSON response
            const jsonData = await response.json();
            data = jsonData.message; // Extracting the 'message' field from JSON
        } else {
            // Process text/plain response
            data = await response.text();
        }

        console.log('Received response from server:', data);
        return data;
    } catch (error) {
        console.error('Error calling the Flask endpoint:', error);
        throw error; // Re-throwing the error so that it can be caught outside this function if needed
    }
}



async function fillColumnsWithBotResponse(selectedUrl) {
    const table = document.getElementById('csvTable');
    const responseTextArea = document.getElementById('responseTextArea');

    if (table.rows.length === 0) {
        console.error("No data in the table. Please upload a CSV file first.");
        return;
    }

    for (let i = 0; i < table.rows.length; i++) {
        const row = table.rows[i];
        const inputCellValue = row.cells[1].textContent;
        console.log("Input cell value: " + inputCellValue);
        let result = await getBotResponseFromFlask(inputCellValue, selectedUrl);
        row.cells[row.cells.length - 2].innerHTML = sanitizeContent(result).replace(/"/g, '');
    }
}


function compareOutputsAndPlaceEmojis() {
    const table = document.getElementById('csvTable');
    const positiveEmoji = "🆗"; // OK emoji
    const negativeEmoji = "❌"; // X emoji

    // Helper function to normalize a string by removing whitespaces and newline characters
    const normalizeString = (str) => str.replace(/\s|\n/g, '');

    // Start from 1 to skip the header row
    for (let i = 0; i < table.rows.length; i++) {
        const row = table.rows[i];
        const expectedOutput = normalizeString(row.cells[2].textContent);
        const actualOutput = normalizeString(row.cells[3].textContent);

        const testResultCell = row.cells[4];

        // Compare the normalized expected and actual outputs
        if (expectedOutput === actualOutput) {
            testResultCell.textContent = positiveEmoji;
        } else {
            testResultCell.textContent = negativeEmoji;
        }
    }
}



