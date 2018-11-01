# gleanomatic with RSEngine to write to and read from ResourceSync endpoints.


# Start up
With docker already installed and set up for your system, navigate to the directory and run
```
docker build -t gleanomatic_core .
```
Then run this
```
  ./gleanomatic.sh start
```  

## Deploy with a custom project

This repository comes with example project directories 'dags' and 'transformServices'.  To deploy Gleanomatic, you need to develop your own 'dags' and 'transforServices' directories.
For example, to get started you could create a new project direct outside of gleanomatic called 'myProject'.  Copy gleanomatic/dags and gleanomatic/transformServices into 'myProject'.  
Finally, in the .env file, change TRANSFORM_PATH and DAGS_PATH to those directories inside myProject (see example.env).

NOTE: For the time being, you will need to copy the gleanomatic library directory to the tranformServices directory to use the gleanomatic library.  TODO: Make gleanomatic a python library that can be installed with requirements.txt

## Named volume backup

If you have a volume named 'gleanomatic_rs-static', you could create a backup with this:

docker run -v gleanomatic_rs-static:/volume -v /tmp:/backup --rm loomchild/volume-backup backup rs-static_archive 
