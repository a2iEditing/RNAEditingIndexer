# Docker Usage

## Quick Introduction - What is a Docker? (and some terminology)
This is a short explanation about Docker and containers, for the full documentation please go to the [official site](https://docs.docker.com/).

Docker is a type of application runnning containers. Containers are conceptually similar to virtual machines, 
but are lighter and more fexbile.
We supply a __*docker file*__, which contains the instructions to build a container (henceforth refered to as __*"image"*__) that contains
the operating system and all dependencies for the tool, so the user doesn't have to to deal with installing and configurating them.
To use this, you must have Docker installed on your machine, and then create the image (__*build*__ it, done once), and then you may run the tool almost as if it was installed on the local machine. When you build the image you give it a name (a __*tag*__), that you refer to later when running it. 
Keep in mind that the image runs inside a virtual enviroment. Thus, to access your file system, you have to specify a 
connection (a __*volum*__, see below). This binding allows you to refer to an internal path linked to your local files (very similar
to to regular links).

## Building the Image
To build the image ("install" the tool), make sure your docker service is running and run a command as following (please kindly note
that these are basic parameters, you can further adjust the usage, see more about this in the [full Docker documentaion](https://docs.docker.com/)):
```
cd /your_git_dir

# ***Note*** this will download the needed dependencies *AND* information tables (14G of data)
# this may take some time.
docker image build  -t your_docker_rep_name/a_name_such_as_a2i_editing_index:a_tag .
```

## Running the Image

### Volum (file system interface)
To enalbe reading and writing to the file system you must specify a connection to the docker image.
You may do this globaly, but here we give example for a runtime command (therefore after the run, the connection will disappear).
The format is [path on your file system]:[path in the container]:[accession suffix] (this may change in a couple of Linux types, see Docker docemntation).
To access a directory with read permissions only, specify *'ro'*, for read\write (e.g. your output directory)- use the *'rw'* suffix.
Here is an example of the commad to __add__ to your command line (we will use this example through these instructions):
```
-v /the_path/to_your_bams:/data/some_dir_inside:ro -v /the_path/to_your_output_dir:/data/some_other_path:rw
```

### User Permissions
If you run the image without these paramters the files created will be with **root user permissions**.
To adjust the run to use your regular user permissions add the following line (yet again some OS may need a little adjustments):
```
-u $(id -u ${USER}):$(id -g ${USER})
```

### Full Command Line (2 examples)
The format of the command is:

docker run [Docker paramters: __\<defining user\>__ __\<volum definitions\>__] image_name RNAEditingIndex __\<paramters for the tool\>__
```
# Example 1:
dokcer run \
  -u $(id -u ${USER}):$(id -g ${USER})\
  -v /the_path/to_your_bams:/data/some_dir_inside:ro -v /the_path/to_your_output_dir:/data/some_other_path:rw\
  your_docker_rep_name/a_name_such_as_a2i_editing_index:a_tag RNAEditingIndex -d /data/some_dir_inside\
  -l /the_path/to_your_output_dir/logs_dir -o /the_path/to_your_output_dir/cmpileups\
  -os /the_path/to_your_output_dir/summary_dir\
  --genome hg38
  
 # Example 2:
dokcer run \
  -u $(id -u ${USER}):$(id -g ${USER})\
  -v /the_path/to_your_bams:/data/some_dir_inside:ro  -v /a_path_to_resources:/data/my_resources\
  -v /the_path/to_your_output_dir:/data/some_other_path:rw\
  your_docker_rep_name/a_name_such_as_a2i_editing_index:a_tag RNAEditingIndex -d /data/some_dir_inside\
  -l /the_path/to_your_output_dir/logs_dir -o /the_path/to_your_output_dir/cmpileups\
  -os /the_path/to_your_output_dir/summary_dir\
  --genome hg38 --rb /data/my_resources/my_custom_regions_file.bed.gz 
```
