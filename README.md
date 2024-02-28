# Link Shortener & click analytics

1. Clone and create, activate virtual environment
```
git clone https://github.com/nithin-gith/lsca
cd lsca/
python3 -m venv venv
source venv/bin/activate 
```

2. install the required libraries
```
pip install -r requirequirements.txt
```

3. Add the DB credentials to .env file
```
touch .env
```

4. Start the server
```
flask run
```

## Using Docker
1. clone the repo
```
git clone https://github.com/nithin-gith/lsca
```
2. build the image
```
docker build -t lsca:latest .
```
3. start the container
```
docker run -d -p source_port:dest_port lsca:latest
ex: docker run -d -p 8080:8080 lsca:latest
```
all the requests to localhost:source_port will be transfered to dest_port (which is port of container)

