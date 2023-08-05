from dataclasses import dataclass

@dataclass
class api_config:
    jenkins_job_name: str        
    Jenkins_url: str
    jenkins_user: str
    jenkins_pwd: str
    buildWithParameters: bool
    jenkins_params: dict
    aws_stack_name: str
    model_name: str = 'default'
    model_run_id: str = 'default'