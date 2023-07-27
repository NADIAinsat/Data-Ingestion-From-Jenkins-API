from jenkinsapi.jenkins import Jenkins
import os

# Jenkins server URL and credentials
jenkins_url = os.environ.get('jenkins_url')
jenkins_username = os.environ.get('jenkins_username')
jenkins_password = os.environ.get('jenkins_password')
server = Jenkins(jenkins_url, username=jenkins_username, password=jenkins_password)


def get_job_info(job_name):
    # Retrieve job information
    job = server.get_job(job_name)
    name = str(job.name)
    description = str(job.get_description())
    running = str(job.is_running())
    enabled = str(job.is_enabled())
    lastBuild = str(job.get_last_buildnumber())
    queued = str(job.is_queued())
    return dict(name=name, description=description, running=running,
                enabled=enabled, lastBuild=lastBuild, queued=queued)


# print(get_job_info('TestPipeline'))

def get_build_info(job_name, build_number):
    # Retrieve build information
    job = server.get_job(job_name)
    build = job.get_build(build_number)
    number = build.get_number()
    description = build.get_description()
    timestamp = build.get_timestamp()
    url = build.get_build_url()
    duration = build.get_duration()
    status = build.get_status()
    running = build.is_running()
    upstream_job_name = build.get_upstream_job_name()
    return dict(job=str(job), build=str(build), number=str(number), description=str(description),
                timestamp=timestamp, url=str(url), duration=str(duration), status=str(status),
                running=str(running), upstream_job_name=str(upstream_job_name))


# print(get_build_info('TestPipeline', 4))
