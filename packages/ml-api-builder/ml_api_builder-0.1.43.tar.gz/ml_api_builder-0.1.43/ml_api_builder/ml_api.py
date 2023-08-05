import requests
import pandas as pd
import time
import logging


from .jenkins_job import JenkinsJob
from .config import api_config

# from jenkins_job import JenkinsJob
# from config import api_config


class ModelAPI():
    '''
    Main class for API creation and deployment
    '''

    def __init__(self, api_config) -> None:
        self.api_config = api_config
        self.jenkins_job = JenkinsJob(self.api_config)

    def deploy_code(self):
        '''
        Managing model deploy.
        Printing job's status while job is building.
        Gives user output log from Jenkins job
        and if deployment is successfull API's url
        where user can test it with her custom data.
        '''

        data = self.jenkins_job.trigger()
        logging.info('Jenkins job trigger')
        status = data.get('status')
        time.sleep(10)

        while 'Job is building' in status or 'Trigger Jenkins job' in status:
            status = self.get_jenkins_job_status()['state']
            logging.info(status)
            time.sleep(5)

        status = self.jenkins_job.jenkins_job_status()
        output_log, url = self.jenkins_job.get_output_and_url()

        if status['result'] == 'SUCCESS':
            logging.info(
                f'API is succesfully deployed, you can call it with in {url}')
        else:
            logging.error(
                f"Your API deploy failed, look at job_output to get more detailed info")

        return output_log, url

    def test_api(self, df: pd.DataFrame, api_url):
        '''
        User can test her API with custom
        data with this method. It's simple post request
        to API's url.
        '''

        dfj = df.to_json()
        r = requests.post(url=api_url, data=dfj)
        data = r.content

        if 'Endpoint request timed out' in r:
            logging.error('Endpoint time out, try to call it again.')
            return {
                'statusCode': 500,
                'error': 'Endpoint request timed out, try to call it again.'
            }

        else:

            data = r.content
            return {
                'statusCode': 200,
                'predictions': data
            }

    def get_jenkins_job_status(self):
        '''
        Gives user current status of Jenkins job.
        It comes handy if user wants to check if job is
        still build or is done.
        '''
        status = self.jenkins_job.jenkins_job_status()
        return status

    def get_jenkins_job_output_and_url(self):
        '''
        Gives user end of Jenkins job output log
        and API's url where user can test it.
        '''
        output = self.jenkins_job.job_output_log
        url = self.jenkins_job.api_url
        return output, url

    def set_model_name(self, model_name):
        self.jenkins_job.model_name = model_name

    def set_model_run_id(self, model_run_id):
        self.jenkins_job.model_run_id = model_run_id

    def set_inference_definition_notebook_path(self, inference_definition_notebook_path):
        self.jenkins_job.inference_definition_notebook_path = inference_definition_notebook_path


if __name__ == "__main__":
    pass
