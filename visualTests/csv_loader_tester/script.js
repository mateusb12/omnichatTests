document.getElementById('csvFileInput').addEventListener('change', loadCSV);
document.getElementById('sendButton').addEventListener('click', sendData);

// let pyodideRuntime = null;
//
// languagePluginLoader.then(() => {
//     pyodideRuntime = pyodide;
// });

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
        startFlaskServer();
      } else {
        console.error('Error:', error.message);
      }
    });
}

function startFlaskServer() {
  const command = 'python csv_flask.py';
  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      return;
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
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

    if (pyodideRuntime === null) {
        console.error("Pyodide is not initialized yet.");
        return;
    }


    const table = document.getElementById('csvTable');
    const responseTextArea = document.getElementById('responseTextArea');

    if (table.rows.length === 0) {
        console.error("No data in the table. Please upload a CSV file first.");
        return;
    }

    // Start from 1 to skip the header row
    for (let i = 1; i < table.rows.length; i++) {
        const row = table.rows[i];
        const inputCellValue = row.cells[1].textContent;
        console.log("About to call Python function with input:", inputCellValue);

        const pythonCode = `
        from pyscript_interface import sendFirebaseLessRequest
        result = sendFirebaseLessRequest("${inputCellValue}")
        result
        `;

        try {
            let result = await pyodideRuntime.runPythonAsync(pythonCode);
            // ... rest of your code ...
        } catch (error) {
            console.error("Error calling Python function:", error);
        }
    }
}

