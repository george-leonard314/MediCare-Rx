# Which base image is used (in this case a simple python image)
FROM python:3.12.2-slim as base

# The workdirectory where all files will be copied.
WORKDIR /app

# copy all from source to destination
COPY Frontend_Customer .

# install all required modules described in requirements.txt
RUN pip install -r requirements.txt

# Expose the port that the application listens on.
EXPOSE 8081

# Run the application.
ENTRYPOINT ["python"]
CMD ["frontend_customer.py"]