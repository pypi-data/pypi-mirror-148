from cmath import inf
import json
import requests
import re
import jenkins
import logging


class JenkinsJob():
    '''
    Class to manage and interact with Jenkins job
    which deploying user's code to AWS
    '''

    def __init__(self, api_config) -> None:

        self.jenkins_job_name = api_config.jenkins_job_name
        self.buildWithParameters = api_config.buildWithParameters

        self.jenkins_server = jenkins.Jenkins(api_config.Jenkins_url,
                                              username=api_config.jenkins_user,
                                              password=api_config.jenkins_pwd)

        self.job_output_log = ''
        self.api_url = ''

        self.jenkins_user = api_config.jenkins_user
        self.jenkins_pwd = api_config.jenkins_pwd
        self.Jenkins_url = api_config.Jenkins_url

        self.aws_stack_name = api_config.aws_stack_name
        self.model_name = 'default'
        self.model_run_id = 'default'
        self.inference_definition_notebook_path = 'default'
        self.job_info = ''

    def trigger(self):
        '''
        Try to trigger Jenkins job
        and inform user about
        '''

        self.jenkins_server = self.refresh_jenkins_server_connection()

        jenkins_params = {
            'model_name': self.model_name,
            'model_run_id': self.model_run_id,
            'aws_stack_name': self.aws_stack_name,
            'inference_definition_notebook_path': self.inference_definition_notebook_path
        }

        try:
            if self.buildWithParameters:
                jenkins_job_status = f'Trigger Jenkins job with parameters: {jenkins_params}'
                logging.info(jenkins_job_status)

                self.jenkins_server.build_job(
                    self.jenkins_job_name, jenkins_params)


                return {
                    'statusCode': 200,
                    'status': jenkins_job_status
                }

            else:
                jenkins_job_status = 'Trigger Jenkins job without parameters'
                logging.info(jenkins_job_status)
                self.jenkins_server.build_job(self.jenkins_job_name)


                return {
                    'statusCode': 200,
                    'status': jenkins_job_status
                }

        except:
            jenkins_job_status = "Failed to trigger the Jenkins job, it could be wrong job name or wrong parameters."
            logging.error(jenkins_job_status)

            return {
                'statusCode': 404,
                'status': jenkins_job_status
            }

    def jenkins_job_status(self):
        '''
        gives user current status of
        running job
        '''

        self.jenkins_server = self.refresh_jenkins_server_connection()

        current_build_num = self.jenkins_server.get_job_info(self.jenkins_job_name)[
            'nextBuildNumber'] - 1

        self.job_info = self.jenkins_server.get_build_info(
            name=self.jenkins_job_name,
            number=current_build_num)

        if self.job_info['building']:
            return {
                'state': 'Job is building'
            }
        else:
            return{
                'state': 'Job is finished',
                'result': self.job_info['result']

            }

    def refresh_jenkins_server_connection(self):

        try:
            connection = jenkins.Jenkins(self.Jenkins_url,
                                         username=self.jenkins_user,
                                         password=self.jenkins_pwd)

            return connection

        except:
            logging.error('Cannot connect to jenkins server')

    def get_output_and_url(self):

        if self.job_info['result'] == "SUCCESS":
            self.job_output_log, self.api_url = self.jenkins_console_output_succed_job()
        else:
            self.job_output_log, self.api_url = self.jenkins_console_output_fail_job()

        return self.job_output_log, self.api_url

    def jenkins_console_output_succed_job(self):
        '''
        Jenkins job output for user if
        job ends up successfully.
        '''
        self.jenkins_server = self.refresh_jenkins_server_connection()

        current_build_num = self.jenkins_server.get_job_info(self.jenkins_job_name)[
            'nextBuildNumber'] - 1

        data = self.jenkins_server.get_build_console_output(
            name=self.jenkins_job_name,
            number=current_build_num)

        end_of_log = data[-1_500:]
        url = self.get_url(data)

        return end_of_log, url

    def jenkins_console_output_fail_job(self):
        '''
        Jenkins job output for user if
        job failed.
        '''
        self.jenkins_server = self.refresh_jenkins_server_connection()

        current_build_num = self.jenkins_server.get_job_info(self.jenkins_job_name)[
            'nextBuildNumber'] - 1

        data = self.jenkins_server.get_build_console_output(
            name=self.jenkins_job_name,
            number=current_build_num)

        end_of_log = data[-1_500:]
        url = 'Job deploy failed, API was not deployed'

        return end_of_log, url

    def get_url(self, output):
        '''
        Takes Jenkins job output as argument
        and find API url address in it.
        '''
        complete_url = ''

        try:
            found_url = re.search(
                "YOU CAN CALL YOUR API IN THIS URL:\'(.+?)\' RUNNING ON AWS LAMBDA", output).group(1)
            complete_url = str(found_url+'/predict')
            logging.info('Found API url inside Jenkins job output log')
            return complete_url
        except AttributeError:
            not_found = 'Not able to find API url inside Jenkins job output log file'
            logging.error('Cannot find API url inside Jenkins job output')
            return not_found


if __name__ == "main":
    pass
