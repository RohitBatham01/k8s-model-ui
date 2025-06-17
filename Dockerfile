FROM python:3.10-slim

# Set working dir
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Streamlit
EXPOSE 3000

# Entrypoint
CMD ["streamlit", "run", "app.py", "--server.port=3000", "--server.address=0.0.0.0"]

