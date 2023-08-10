import jenkinsAPI

# Saving artifacts.
# artifacts is a dict representing the artifact filenames and the instances
server = jenkinsAPI.server
local_path = "C:/Users/nadia/PycharmProjects/DataIngestion/jenkins_api"


def save_build_artifacts(job_name, build_number):
    job = server.get_job(job_name)
    build = job.get_build(build_number)
    artifacts = list(build.get_artifacts())
    for artifact in artifacts:
        artifact_url = artifact.url
        print(artifact_url)
        artifact.save(f"{local_path}/{artifact.filename}")
        break


save_build_artifacts('TestPipeline', 16)
