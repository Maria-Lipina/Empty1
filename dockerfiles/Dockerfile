FROM ubuntu:22.04
RUN apt update && \
	apt install -y nginx && \
	rm -rf /var/lib/apt/lists/*
EXPOSE 9000
CMD ["nginx", "-g", "daemon off;"]
