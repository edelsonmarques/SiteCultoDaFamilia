FROM python:3
WORKDIR /app
COPY requirements.txt ./
RUN python --version
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "app/app.py"]