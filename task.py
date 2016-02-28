#!/usr/bin/env python

import os
import sys
import yaml
import requests
import config
def get_project_name(yml):
    project_name = yml['Projects']['Name'][0]
    sub_name = '/{}'.format(yml['Projects']['SubName'][0]) if yml['Projects']['SubName'][0] else ''
    id = '{project_name}{sub_name}'.format(project_name=project_name,
                                           sub_name=sub_name)
    try:
        version = requests.get("{}/app/{}-{}".format(config.SIMPLE_INCREMENTER, yml['Projects']['Name'][0], sub_name[1:]), timeout=1).json()["next_version"]
    except:
        version = "0.0.1"
    return {"name": yml['Projects']['Name'][0], "project_name": id, "sub_name": sub_name[1:], "source_path": yml['Source'][0], "version": version}

def generate_docker_file(destination="test", yml=None):
    TASK = {"test": "Tests", "build": "Build", "deploy": "Deploy"}
    TASK = yml[TASK[destination]]
    with open('{}/Dockerfile'.format(destination), 'w') as f:
        f.write("FROM {}\n".format(TASK["From"][0]))
        for d in TASK["Run"].split("\\n"):
            f.write (d+"\n")

def generate_build_task(destination="test", yml=None):
    TASK = {"test": "Tests", "build": "Build", "deploy": "Deploy"}

    project_name = get_project_name(yml)["project_name"]
    version = get_project_name(yml)["version"]
    source_path = get_project_name(yml)["source_path"]
    name = get_project_name(yml)["name"]
    sub_name = get_project_name(yml)["sub_name"]
    task = yml[TASK[destination]]

    with open('{}.sh'.format(destination), 'w') as f:
        f.write("#!/bin/bash\n")
        if destination == "deploy":
            f.write('cp latest_container_name.py {}\n'.format(destination))
            f.write('cp notice_container_name_to_slack.py {}\n'.format(destination))
            f.write('cp config.py {}\n'.format(destination))
        f.write ('cd {} && GIT_REVISION=`git rev-parse  --short HEAD` && cd ..\n'.format(source_path))
        for y in yml['Source']:
            f.write('cp -rf {}/* {}\n'.format(y, destination))
        f.write ('cd {}\n'.format(destination))
        build_string = 'docker build -t {project_name} .\n'.format(project_name=project_name)
        f.write (build_string)
        
        if destination in ("test", "deploy"):
            f.write('docker run -t {project_name} {args}\n'.format(project_name=project_name,
               args=task["RUN_COMMAND"][0].replace('"', '\\"') if task["RUN_COMMAND"][0] else ""))
        if destination == "build":
            f.write("docker tag {project_name} {repo_url}/{project_name}\n".format(project_name=project_name, 
                                                                                 repo_url=config.DOCKER_REPOGITORY_HOST))
            f.write("docker push {repo_url}/{project_name}\n".format(project_name=project_name, 
                                                                   repo_url=config.DOCKER_REPOGITORY_HOST))
            f.write("docker rmi {repo_url}/{project_name}\n".format(project_name=project_name, 
                                                                   repo_url=config.DOCKER_REPOGITORY_HOST))
                    
            f.write ('TO_MARATHON_JSON="{}"\n'.format(yml['Build']['ToMarathon'][0]))
            f.write ('SOURCE_PATH="{}"\n'.format(source_path))
            f.write ('NAME="{}-{}"\n'.format(name,sub_name))
            f.write ('TAG="{}"\n'.format(project_name))
            f.write ('PUSH_URL="{}"\n'.format(config.DOCKER_REPOGITORY_HOST+os.sep+project_name))
            f.write ('ID={}/{}\n'.format(project_name, version))
            f.write ('ARGS="{}"\n'.format(task["ARGS"][0].replace('"', '\\"') if task["ARGS"][0] else []))
            
            if "ENV" in task:
                for _env in task["ENV"]:
                    f.write ('{}={}\n'.format(_env, task["ENV"][_env][0]))
            else:
                task["ENV"] = []
            f.write ('VERSION={}\n'.format(version))
            f.write ('MARATHON_URL={}\n'.format(config.MARATHON_URL))
            f.write('''
    JSON=$(cat ${TO_MARATHON_JSON})\n
    JSON="${JSON//%%id%%/${ID}}"\n
    JSON="${JSON//%%name%%/${NAME}}"\n
    JSON="${JSON//%%tag%%/${PUSH_URL}}"\n
    JSON="${JSON//%%version%%/${VERSION}}"\n
    JSON="${JSON//%%args%%/${ARGS}}"\n
    JSON="${JSON//%%git_revision%%/${GIT_REVISION}}"\n''')

            for _env in task["ENV"]:
                _env_string = 'JSON="${JSON//%%' + _env.lower() + '%%/${' + _env +  '}}"\n'
                f.write(_env_string)

            f.write('''echo "$JSON"\n''')
            f.write('''curl -v -H "Content-Type: application/json" -H "Accept: application/json" -X POST -d "${JSON}" "${MARATHON_URL}v2/apps"''')



        #volume = "mkdir -p {}".format(TASK['Volume'][0]) if TASK['Volume'][0] else ''
        #f.write(volume + "\n")
        #if volume:
        #    volume_path = "-v {}:/{}".format(os.getcwd(), TASK['Volume'][0])
        #else:
        #    volume_path = ""
        #run_string = 'docker run {volume_path} {project_name}\n'.format(volume_path=volume_path,
        #                                                                project_name=project_name)
        #f.write (run_string)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        os.makedirs("test")
        os.makedirs("build")
        os.makedirs("deploy")
        yml = yaml.load(open('{}'.format(sys.argv[2], 'r')))
        generate_build_task(sys.argv[1], yml)
        generate_docker_file(sys.argv[1], yml)
        #print ("generate {}.sh".format(sys.argv[1]))
        #os.system("cat  {}.sh".format(sys.argv[1]))
        #os.system("sh {}.sh".format(sys.argv[1]))
        #print ("invalid task. Please input test or build or deploy")
    else:
        generate_build_task()
