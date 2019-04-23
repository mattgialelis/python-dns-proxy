# DNS to DNS-TLS-Proxy


## *Getting Started*
  
These instructions will get you a copy of the project up and running.

## **Prerequisites**

The main packages required to run the api are listed below.

- Docker

- Python3


## **Getting it Running**

-  Build the docker image

```Bash
Docker build -t dnsproxy .
```

-  Create a docker network 
```bash
Docker network create --subnet 10.0.0.0/24  proxy-network
```

- Launch Docker container into network
```bash
docker run --net proxy-network  -id dnsproxy
```

**Note**

The below steps do not work on MAC OSX as the network passthru does not work.

https://docs.docker.com/docker-for-mac/networking/#i-cannot-ping-my-containers



- Find Ip of container
```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' CONTAINER ID
```

- Use Dig to hit the DNS proxy for testing
```bash
dig @10.0.0.1 -p 53 +tcp  www.google.com
```


## **Development Notes and Decisions**

- Python 3 was the coding language of choice to build this proxy
- Threading was implemented to allow processing of multiple requests simultaneously 
- A queue length of 5 was added to python socket to allow queuing if required   
- Cloduflare's 1.1.1.1 was used as the TLS DNS server 
- Everything has been moved off the main thread in case you want to import the module later
- Listens on 0.0.0.0 on TCP/53 


## **Improvements Needed**

- Listen on UDP as well 
- DNS caching implemented with TTL 
- DDOS protection and rate limiting to ensure no abuse
- Rewriting proxy in GOlang due to the better handling of sockets and crossplatfrom support
- Using a Serverless architure over a microsevices
- Use other DNS over TLS providers in a round robin or based on response times
- Logging of transactions for monintoring as well as preformance metrics
- DNS filtering to remove ad's and Malious content based of global black lists and Internal ones
- Coverage and unit and intergration tests