FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -e .
EXPOSE 7860
CMD ["server"]
