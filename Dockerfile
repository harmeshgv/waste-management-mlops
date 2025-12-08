FROM python:3.12-slim

WORKDIR /app

COPY ./backend ./backend
COPY ./model ./model



RUN pip install --no-cache-dir \
        torch==2.4.1+cpu \
        torchvision==0.19.1+cpu \
        --index-url https://download.pytorch.org/whl/cpu && \
    pip install --prefer-binary -r backend/requirements.txt


EXPOSE 8001

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8001"]