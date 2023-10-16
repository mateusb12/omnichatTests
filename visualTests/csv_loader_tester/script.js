document.getElementById('csvFileInput').addEventListener('change', loadCSV);
document.getElementById('sendButton').addEventListener('click', sendData);

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

function loadCSV(event) {
    const file = event.target.files[0];
    if (!file) return;

    checkServerStatus();

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
                table.appendChild(thead);
            } else {  // data rows
                const tr = document.createElement('tr');
                line.forEach(cell => {
                    const td = document.createElement('td');
                    td.textContent = cell;
                    tr.appendChild(td);
                });
                const tdActual = document.createElement('td'); // ActualOutput cell placeholder
                tr.appendChild(tdActual);
                tbody.appendChild(tr); // Append the row to tbody
            }
        });

        table.appendChild(tbody); // Append the tbody to the table after the loop
    };
    reader.readAsText(file);
}


async function sendData() {
    console.log("Button clicked");
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
        let result = await getBotResponseFromFlask(inputCellValue);
        // Assuming "ExpectedOutput" is the second column and "ActualOutput" is the third column
        // Set the content of the "ActualOutput" column
        row.cells[row.cells.length - 1].textContent = result;
    }
}

async function getBotResponseFromFlask(inputCellValue) {
    const port = 4608;
    const url = `http://localhost:${port}/getBotResponse`;

    // Prepare the request body
    const requestBody = {
        body: inputCellValue // assuming the server expects a "body" key with the value
    };

    try {
        // Send the POST request
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        // Check if the request was successful
        if (!response.ok) {
            throw new Error('Server returned a non-200 response: ' + response.status);
        }

        const data = await response.json(); // Assuming the server returns a JSON response
        console.log('Received response from server:', data);

        return data;
    } catch (error) {
        console.error('Error calling the Flask endpoint:', error);
        throw error; // Re-throwing the error so that it can be caught outside this function if needed
    }
}

