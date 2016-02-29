## Docker and Marathon/Mesos and Jenkins ecosystem

This is continuation integration system of docker, marathon, jenkins


### Usage

####test phase
./task.py test

####build phase
./task.py build

####deploy phase
./task.py deploy  --slack_token={token} --slack_channel={channel}  

#### required build.yml
```
Projects:
    Name:
        - yusukefurukawa 
    SubName:
        - test
    Version:
        - 0.0.6
Tests:
    From:
        - 'python:latest'
    Run: 
        >
        ADD requirements.txt .\n
        ADD app.py .\n
        ADD app_test.py .\n
        RUN pip install -r requirements.txt\n
    Phase:
        - tests
    Volume:
        - volume1
    RUN_COMMAND: 
        - 'python app_test.py'
Build:
    From:
        - 'python:latest'
    Run:
        >
        ADD requirements.txt .\n
        ADD app.py .\n
        ADD app_test.py .\n
        RUN pip install -r requirements.txt\n
        CMD ["python", "app.py"]\n
    Phase:
        - build
    Volume:
        - null
    ToMarathon:
        - deploy-ops.json
    ENV:
        ENV1:
            - hoge1
        ENV2:
            - hoge2
        DJANGO_SETTINGS_MODULE:
            - hogehoge.setting

    ARGS: 
        - '["python", "app.py"]'

Deploy:
    Ignore:
        -- true
Source:
    - getting-started-python
```

##### config.py
```
MARATHON_URL = 'http://10.141.141.10:8080/'
DOCKER_REPOGITORY = 'https://docker.io/'
DOCKER_REPOGITORY_HOST = 'docker.io'
SIMPLE_INCREMENTER = 'http://hogehoge.com'
SOURCE="git@github.com:frkwy/start_python_web.git"
```
