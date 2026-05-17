FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1 
 
RUN pip install --upgrade pip 
 
COPY  moodMusicPlayer/requirements.txt  .
 
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn uvicorn 

COPY  moodMusicPlayer/ . 
 
EXPOSE 8000

# RUN python manage.py 

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

