FROM python:3

# set a directory for the app
WORKDIR /usr/src/app

# ADD . /app.py

# copy all the files to the container
COPY . .

# install dependencies: --no-cache-dir
RUN pip install --no-cache-dir -r requirements.txt

# tell the port number the container should expose
EXPOSE 5000

# run the command
CMD ["python", "./app.py"]