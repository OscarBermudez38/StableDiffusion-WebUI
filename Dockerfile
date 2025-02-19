FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install streamlit -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "streamlit_app.py"]
