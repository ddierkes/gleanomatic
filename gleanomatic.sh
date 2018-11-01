#!/bin/bash  

airflowType="CeleryExecutor"

startme() {
    echo "Starting ...\n"
    echo "running docker-compose with docker-compose-$airflowType.yml\n\n"
    #docker-compose -f docker-compose.yml -f docker-compose-ELK.yml -f docker-compose-$airflowType.yml up -d
    docker-compose -f docker-compose.yml -f docker-compose-$airflowType.yml up -d
}

stopme() {
    echo "Stopping ..."
    echo "stopping docker-compose with docker-compose-$airflowType.yml\n\n"
    #docker-compose -f docker-compose.yml -f docker-compose-ELK.yml -f docker-compose-$airflowType.yml stop
    docker-compose -f docker-compose.yml -f docker-compose-$airflowType.yml stop
}

showinfo() {
    echo "Showing info for docker-compose.yml and docker-compose-$airflowType.yml\n"
    #docker-compose -f docker-compose.yml -f docker-compose-ELK.yml -f docker-compose-$airflowType.yml ps
    docker-compose -f docker-compose.yml -f docker-compose-$airflowType.yml ps

}

case "$1" in 
    start)   startme ;;
    stop)    stopme ;;
    restart) stopme; startme ;;
    status) showinfo ;;
    *) echo "usage: $0 start|stop|restart" >&2
       exit 1
       ;;
esac
