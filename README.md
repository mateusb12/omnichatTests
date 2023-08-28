# TwilioPizza API Setup Guide 🍕

Follow the steps below to set up and test the TwilioPizza API.

## Getting Started

### 1. **TwilioPizza Repository** 📁
   Clone and open the `twilioPizza` repository.

![Step 1 Image](docs/pictures/step_1.png)

### 2. **Backend Configuration** 🐍
   Navigate to the Python backend and open `api.py`.

![Step 2 Image](docs/pictures/step_2.png)

### 3. **Start the Server** 🌐
   Run the server on port `3000`.

![Step 3 Image](docs/pictures/step_3.png)

### 4. **Setup Ngrok** 🚀
   - Open `ngrok`.
   - Execute the following command:
     ```
     ngrok http 3000
     ```
   - Copy the new `ngrok` URL.

![Step 4 Image](docs/pictures/step_4.png)

### 5. **Dialogflow Configuration** 🤖
   - Visit [Dialogflow Console](https://dialogflow.cloud.google.com).
   - Navigate to `fullfilment -> webhook`.
   - Paste the copied `ngrok` URL and save the changes.

![Step 5 Image](docs/pictures/step_5.png)
![Step 5B Image](docs/pictures/step_5_b.png)

## Running the Tests

### 6. **OmnichatTests Repository** 📊
   Open the `omnichatTests` repository.

![Step 6 Image](docs/pictures/step_6.png)

### 7. **Select Test Plan** 📝
   Under the `getCurrentPlan()` function, choose the `testPlan` you wish to run.

![Step 7 Image](docs/pictures/step_7.png)

### 8. **Edit Test Plan (optional)** 📝
   As you can see, the `getSignupPlan()` function basically loads a .csv file with the test plan.
   You can edit it if you want.

![Step Bonus Image](docs/pictures/signup_function.png)
![Step Bonus2 Image](docs/pictures/signup_csv.png)

### 9. **Run the Test** 🚀
   Execute the test.
![Step 8 Image](docs/pictures/step_8.png)

![Step 8B Image](docs/pictures/step_8_b.png)
---

**Happy Coding!** 🎉
