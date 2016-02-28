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
