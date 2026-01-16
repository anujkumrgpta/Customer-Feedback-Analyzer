# Feedback Hub - Customer Feedback Analyzer

Feedback Hub is a simple web application designed for Giva to collect, analyze, and visualize customer feedback for products like rings, necklaces, and earrings. It uses a Flask backend for data handling and a responsive HTML/JS frontend for the dashboard.

## Features

### Backend (`app.py`)
-   **Feedback API**: Endpoints to submit and retrieve feedback.
-   **Sentiment Analysis**: Rule-based logic to classify feedback as Positive or Negative based on keyword counts.
-   **Theme Detection**: Identifies themes (Comfort, Durability, Appearance) based on specific keywords.
-   **Data Persistence**: Stores feedback in `feedback_data.json` so data survives server restarts.

### Frontend (`templates/index.html`)
-   **Submission Form**: Easy-to-use form for customers to rate and review products.
-   **Interactive Dashboard**:
    -   **Sentiment Pie Chart**: Visualizes Positive (Green) vs Negative (Red) feedback.
    -   **Theme Bar Chart**: Shows the frequency of mentioned themes.
    -   **AI Insights**: Generates actionable insights (e.g., "Improve durability") based on negative feedback patterns.
    -   **Recent Reviews**: Displays the latest 5 reviews with a "Show More" option.

## Setup & Run

1.  **Prerequisites**: Python installed.
2.  **Install Dependencies**:
    ```bash
    pip install flask
    ```
3.  **Run the Application**:
    ```bash
    python app.py
    ```
4.  **Access the App**: Open your browser and go to `http://localhost:5000`.

## Logic Explanation

### Sentiment Analysis
We use a simple bag-of-words approach:
-   **Positive Words**: shiny, elegant, comfortable, premium, etc.
-   **Negative Words**: tarnish, dull, broke, uncomfortable, etc.
-   **Logic**: If `positive_count >= negative_count`, the sentiment is **Positive**. Otherwise, it is **Negative**.

### Theme Detection
We check for keywords associated with specific themes:
-   **Comfort**: light, heavy, fit, wearable...
-   **Durability**: broke, strong, quality, fragile...
-   **Appearance**: shiny, dull, design, polish...

### Insight Generation (Frontend)
Insights are generated client-side when you click "Generate Insights":
-   **"Improve durability"**: Triggered if >30% of reviews mention "Durability" with Negative sentiment.
-   **"Consider lighter designs"**: Triggered if >30% of reviews mention "Comfort" with Negative sentiment.
-   **"Revamp design aesthetics"**: Triggered if >30% of reviews mention "Appearance" with Negative sentiment.

## Project Structure

-   `app.py`: Flask backend application.
-   `templates/index.html`: Frontend HTML/CSS/JS.
-   `feedback_data.json`: Data storage file (created automatically).
