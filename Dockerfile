FROM python:3.10.4-slim-bullseye as base

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /fashion_classifier_django

# Install dependencies
COPY ./requirements.txt .
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt

# Development stage
FROM base as dev
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Production stage (optional)
# FROM base as prod
# COPY . .
# RUN python manage.py collectstatic --no-input
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project.wsgi:application"]