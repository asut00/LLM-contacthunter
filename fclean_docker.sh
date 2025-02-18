docker images -f "dangling=true" -q | xargs -r docker rmi
docker ps -qa | xargs -r docker stop
docker ps -qa | xargs -r docker rm 
docker images -qa | xargs -r docker rmi -f
docker volume ls -q | xargs -r docker volume rm
docker network ls -q | xargs -r docker network rm
docker ps -a -q | xargs -r docker rm -f
docker images -q | xargs -r docker rmi
docker system prune -a --force
docker volume prune --force