    FROM python:3.8.2

    ENV PYTHONBUFFERED 1
    ENV PYTHONWRITEBYTECODE 1

    RUN apt-get update \
        && apt-get install -y netcat

    ENV APP=/app
    RUN export DEALER_SERVICE_URL=https://feiwencheng-3000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai
    RUN export REVIEW_SERVICE_URL=https://feiwencheng-5000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai
    # Change the workdir.
    WORKDIR $APP

    # Install the requirements
    COPY requirements.txt $APP

    RUN pip3 install -r requirements.txt

    # Copy the rest of the files
    COPY . $APP

    EXPOSE 8000

    RUN chmod +x /app/entrypoint.sh

    ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]

    CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]