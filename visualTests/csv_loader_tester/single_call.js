async function sendRequest() {
    const url = 'http://localhost:3000/twilioSandbox'; // Endpoint URL
    const bodyContent = "oiiii"; // Body content

    try {
        // Prepare the headers
        const headers = new Headers();
        headers.append('Content-Type', 'application/json; charset=utf-8');
        headers.append('Body', encodeURIComponent('Kkkkk'));
        headers.append('From', encodeURIComponent('guaraná'));
        headers.append('ProfileName', encodeURIComponent('guarané'));
        headers.append('WaId', '85985743958473');

        // Send the POST request
        const response = await fetch(url, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(bodyContent) // Send the body as a JSON string
        });

        // Check if the request was successful
        if (!response.ok) {
            throw new Error('Server returned a non-200 response: ' + response.status);
        }

        // Process the response
        const data = await response.text();
        console.log('Received response:', data);
        return data;
    } catch (error) {
        console.error('Error in sending request:', error);
        throw error;
    }
}

sendRequest();
