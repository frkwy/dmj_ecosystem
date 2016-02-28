## Docker and Marathon/Mesos and Jenkins ecosystem

This is continuation integration system of docker, marathon, jenkins


### Usage

####test phase
pip install pyyaml requests
./task.py test --yaml={yml.path}  

####build phase
pip install pyyaml requests  
./task.py build --yaml={yml.path}  

####deploy phase
pip install pyyaml requests  
./task.py deploy  --yaml={yaml} --slack_token={token} --slack_channel={channel}  

