## Docker and Marathon/Mesos and Jenkins ecosystem

This is continuation integration system of docker, marathon, jenkins


### Usage

####test phase
./task.py test {yml.path}
sh test.sh

####build phase
./task.py build {yml.path}
sh build.sh

####deploy phase
./task.py deploy {yml.path}
sh deploy.sh
