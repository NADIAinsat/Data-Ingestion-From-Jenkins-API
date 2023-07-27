import jenkinsAPI

# Saving artifacts.
# artifacts is a dict representing the artifact filenames and the instances
server = jenkinsAPI.server


def save_build_artifacts(job_name, build_number, artifact_name):
    job = server.get_job(job_name)
    build = job.get_build(build_number)
    artifacts = list(build.get_artifacts())
    for artifact in artifacts:
        if artifact.filename == artifact_name:
            artifact_url = artifact.url
            print(artifact_url)
            artifact.save(f"C:/Users/nadia/PycharmProjects/DataIngestion/jenkins_api/{artifact_name}")
            break


# save_build_artifacts('TestPipeline', 4, 'hello.txt')
