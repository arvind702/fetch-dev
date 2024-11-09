# fetch-dev
A solution to https://github.com/fetch-rewards/receipt-processor-challenge

### Running this code:

_Please note that this server is hosted on all available addresses on port 5000. This means it may be exposed externally (port 5000 on your machine's local IP)._


* Download the contents of this repo and navigate to its containing folder.

* Then, create a Docker image:

  `docker build -t fetch-dev .`

* Create a container and run:

  `docker run -d -p 5000:5000 fetch-dev`

Make requests to `localhost:5000`.
