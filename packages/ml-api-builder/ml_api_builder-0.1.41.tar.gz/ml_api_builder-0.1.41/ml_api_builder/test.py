from ml_api import ModelAPI
from config import api_config
from jenkins_job import JenkinsJob
import jenkins
import json
import re


config = api_config(
    jenkins_job_name='dbx_daipe_demo_1',
    Jenkins_url='http://18.185.104.16:8080/',
    jenkins_user="m",
    jenkins_pwd='mlopsdbx1020',
    buildWithParameters=True,
    jenkins_params={'model_run_id': 'mh_run_id', 'model_name': 'test value 2'},
    aws_stack_name="iris_model_mh_1",
)

model_api = ModelAPI(config)

model_api.set_model_name("iris_model")
model_api.set_model_run_id("d3b92192816c4f17b8aa6bfb19fd2d79")
model_api.set_inference_definition_notebook_path(
    "src/model_development/serving/inference_definition")

# job_output, api_url = model_api.deploy_code()
# print('job_output ', job_output)
# print('api_url ', api_url)


jenkins_server = jenkins.Jenkins('http://18.185.104.16:8080/',
                                 username='m',
                                 password='mlopsdbx1020')

current_build_num = jenkins_server.get_job_info('dbx_daipe_demo_1')[
    'nextBuildNumber'] - 2

# # print('current_build_num ', current_build_num)
# # print('jenkins_server ', jenkins_server.get_info())
data = jenkins_server.get_build_console_output(
    name='dbx_daipe_demo_1',
    number=current_build_num)


print(data[-1500:])

# jj = JenkinsJob(config)


# def get_url(output):
#     '''
#     Takes Jenkins job output as argument
#     and find API url address in it.
#     '''
#     complete_url = ''

#     try:
#         found_url = re.search(
#             "YOU CAN CALL YOUR API IN THIS URL:\'(.+?)\' RUNNING ON AWS LAMBDA", output).group(1)
#         complete_url = str(found_url+'/predict')
#         return complete_url
#     except AttributeError:
#         not_found = 'Not able to find API url inside Jenkins job output log file'
#         return not_found


# data, url = jj.jenkins_console_output_succed_job()
# print(data)

# print(get_url(jj.jenkins_console_output_succed_job()))
