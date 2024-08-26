# LLM-Based RAG System

## Process Overview

1. **User Input via Streamlit Interface**:
   - The user interacts with a Streamlit-based front-end where they can input their query.

2. **Query Sent to Flask Backend**:
   - The query entered by the user is sent from the Streamlit interface to a Flask backend via an API call.

3. **Internet Search and Article Scraping**:
   - The Flask backend searches the internet for the query using a designated API. It retrieves the top relevant articles and scrapes their content, extracting only the useful text (headings and paragraphs).

4. **Content Processing**:
   - The scraped content is processed to create a coherent input, which is then passed to the LLM for generating a response.

5. **LLM Response Generation**:
   - The processed content and the user's query are used to generate a contextual answer using the LLM. The LLM is accessed via an API, specifically Ollama's Llama 3 model, and the generated response is returned to the Flask backend.

6. **Response Sent Back to Streamlit Interface**:
   - The Flask backend sends the generated answer back to the Streamlit interface, where it is displayed to the user.

## Prerequisites

- Python 3.10 or above

## Setup Instructions

### Step 1: Clone or Download the Repository (if emailed)

```bash
git clone https://github.com/your-repo-url.git
cd project_name
```

Or download it directly.

### Step 2: Set Up a Virtual Environment

You can use `venv` or `conda` to create an isolated environment for this project.

#### Using `venv`

```bash
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

#### Using `conda`

```bash
conda create --name project_env python=3.10
conda activate project_env
```

### Step 3: Install Requirements

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory and add your API keys in a way they can be accessed in the app.

### Step 5: Run the Flask Backend

Navigate to the `flask_app` directory and start the Flask server:

```bash
cd flask_app
python app.py
```

### Step 6: Run the Streamlit Frontend

In a new terminal, run the Streamlit app:

```bash
cd streamlit_app
streamlit run app.py
```

### Step 7: Open the Application

Open your web browser and go to `http://localhost:8501`. You can now interact with the system by entering your query.

## Project Structure

- **flask_app/**: Contains the backend Flask API and utility functions.
- **streamlit_app/**: Contains the Streamlit front-end code.
- **requirements.txt**: Lists the project dependencies.
![Screenshot 2024-08-26 203601](https://github.com/user-attachments/assets/e97b4fb7-194e-479c-91a4-7816abbaf80d)
![Screenshot 2024-08-26 203632](https://github.com/user-attachments/assets/2e2de089-8445-4a48-8cd8-096db4a00a47)





