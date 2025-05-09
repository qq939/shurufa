#执行Dockerfile
docker build -t ai_agent:1.0 .
docker run -d -p 8080:5111 --restart ai_agent:1.0
