FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -e .
EXPOSE 7860
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
