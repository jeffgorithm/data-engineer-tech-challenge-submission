# Screenshot
<p align="center">
    <img src="screenshot.png" alt="screenshot"/>
</p>

# Prerequisite
- Python 3
- Pip

# Technologies
- Requests
- Pandas
- Streamlit

# Setup
1. Create new Python virtual environment
    ```
    python -m venv venv
    ```
2. Activate Python virtual environment
    ```
    source venv/bin/activate
    ```
3. Install Python dependencies
    ```
    pip install -r requirements.txt
    ```

# Run
1. Invoke API to retrieve data and store as JSON
    ```
    python invoke_api.py
    ```
2. Start streamlit application
    ```
    streamlit run streamlit.py
    ```
3. Go to [127.0.0.1:8501](http://127.0.0.1:8501) on your browser to view interactive dashboard