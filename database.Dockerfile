# Which base image is used (in this case a simple python image)
FROM python:3.12.2-slim as base

# The workdirectory where all files will be copied.
WORKDIR /Database

# copy all from source to destination
COPY Database .


# install all required modules described in requirements.txt
RUN pip install -r requirements.txt


# Run the application.
ENTRYPOINT ["python"]
CMD ["create_db.py"]