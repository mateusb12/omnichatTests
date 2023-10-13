document.getElementById('csvFileInput').addEventListener('change', loadCSV);
document.getElementById('sendBtn').addEventListener('click', sendData);

function loadCSV(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        const content = e.target.result;
        const lines = content.split('\n').map(line => line.split(';'));

        // Populate table
        const table = document.getElementById('csvTable');
        table.innerHTML = '';  // Clear existing content
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
                const tbody = document.createElement('tbody');
                line.forEach(cell => {
                    const td = document.createElement('td');
                    td.textContent = cell;
                    tbody.appendChild(td);
                });
                const tdActual = document.createElement('td'); // ActualOutput cell placeholder
                tbody.appendChild(tdActual);
                table.appendChild(tbody);
            }
        });
    };
    reader.readAsText(file);
}

function sendData() {
    // For demonstration purposes, we'll mock the send function.
    const textArea = document.getElementById('responseTextArea');
    textArea.value = "Data sent successfully!";
}