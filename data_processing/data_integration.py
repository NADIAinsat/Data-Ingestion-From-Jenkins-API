from jenkinsapi.custom_exceptions import NotFound
from jenkins_api import jenkinsAPI
from data_processing.data_modeling import Job, Build
from sqlalchemy import desc, update
from data_processing import database_connection
from sqlalchemy import inspect
import os

server = jenkinsAPI.server
session = database_connection.session
artifacts_path = "C:/Users/nadia/PycharmProjects/DataIngestion/Build Artifacts"


def save_build_artifacts(job_name, build_number):
    # This method saves each build's artifact in its specific path
    job = server.get_job(job_name)
    build = job.get_build(build_number)
    artifacts = list(build.get_artifacts())
    for artifact in artifacts:
        artifact_url = artifact.url
        print(artifact_url)
        directory_path = f"{artifacts_path}/{job_name}/{build_number}"
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        artifact.save(f"{directory_path}/{artifact.filename}")
        break


def insert_new_build(build_info):
    # Inserting one build info in the database as a new instance
    build_inst = {}
    for key, value in build_info.items():
        # Linking the build to its related job in Job table
        if key == 'job':
            existing_job = session.query(Job).filter_by(name=value).first()
            build_inst['job_id'] = existing_job.id
        else:
            build_inst[key] = value
    save_build_artifacts(build_info['job'], int(build_inst['number']))
    build = Build(**build_inst)
    session.add(build)
    session.commit()


def insert_all_builds(job_name, start, end):
    # Inserting all the builds of job_name of numbers between start and end integers
    for build_number in range(start, end):
        try:
            build_info = jenkinsAPI.get_build_info(job_name, build_number)
            insert_new_build(build_info)
        except NotFound:
            continue  # Skip this build number if it doesn't exist


engine = database_connection.engine


def update_builds_foreignkey(job_name):
    existing_job = session.query(Job).filter_by(name=job_name).order_by(desc(Job.Insert_Date)).first()
    session.execute(
        update(Build).
        where(Build.build.like(f"{job_name}%")).
        values(job_id=existing_job.id)
    )
    session.commit()


def update_job(existing_job):
    job_inst = jenkinsAPI.get_job_info(existing_job.name)
    inspector = inspect(engine)
    table_columns = inspector.get_columns('Job')
    is_updated = False
    # Iterate through the columns
    for column in table_columns:
        column_name = column['name']
        if column_name in job_inst and job_inst[column_name] != getattr(existing_job, column_name):
            # Update the attributes of the existing job instance
            setattr(existing_job, column_name, job_inst[column_name])
            is_updated = True
    if is_updated:
        session.commit()
        update_builds_foreignkey(existing_job.name)

    return job_inst


def insert_new_jobs_and_builds(server):
    # Insert all jobs into the 'job' table
    for job_name, job_instance in server.get_jobs():
        job_inst = jenkinsAPI.get_job_info(job_name)
        existing_job = session.query(Job).filter_by(name=str(job_instance.name)).first()
        if existing_job is None:  # the job does not already exist in the table
            job = Job(**job_inst)
            session.add(job)
            session.commit()
        else:
            job_inst = update_job(existing_job)
        last_build_number = job_inst['lastBuild']
        last_build_info = jenkinsAPI.get_build_info(job_name, int(last_build_number))
        table_last_build = session.query(Build). \
            filter(Build.build.like(f"{last_build_info['job']}%")). \
            order_by(desc(Build.Insert_Date)). \
            first()
        # print('last timestamp for job ', job_name, last_build_info['timestamp'])
        # print('table last insert date for job ', job_name, table_last_build.Insert_Date)
        if table_last_build is not None and last_build_info['timestamp'] > table_last_build.timestamp:
            # insert the added builds after last insertion
            insert_all_builds(job_name, int(table_last_build.number) + 1, int(last_build_number) + 1)
        elif table_last_build is None:
            # Insert all available builds
            insert_all_builds(job_name, 1, int(last_build_number) + 1)


def print_builds_after_timestamp(server, timestamp):
    # Insert all jobs into the 'job' table
    for job_name, job_instance in server.get_jobs():
        job_inst = jenkinsAPI.get_job_info(job_name)
        existing_job = session.query(Job).filter_by(name=str(job_instance.name)).first()
        if existing_job is None:  # the job does not already exist in the table
            job = Job(**job_inst)
            session.add(job)
            session.commit()
        else:
            job_inst = update_job(existing_job)
        last_build_number = job_inst['lastBuild']
        # Iterate through all the builds available in a job
        for build_number in range(1, int(last_build_number) + 1):
            try:
                build_info = jenkinsAPI.get_build_info(job_name, build_number)
                if build_info['timestamp'] > timestamp:
                    print(build_info)
            except NotFound:
                continue  # Skip this build number if it doesn't exist


def update_dequeued_jobs(server):
    for job_name, job_instance in server.get_jobs():
        existing_job = session.query(Job).filter_by(name=str(job_instance.name)).first()
        if existing_job is None:
            continue
        else:
            last_inserted_job = session.query(Job).order_by(desc(Job.Insert_Date)).first()
            if (last_inserted_job is not None) and (last_inserted_job.queued == 'True') and (
                    job_instance.is_queued() is False):
                update_job(existing_job)


def update_changed_status(server):
    for job_name, job_instance in server.get_jobs():
        job_inst = jenkinsAPI.get_job_info(job_name)
        last_build_number = job_inst['lastBuild']
        # Iterate through all the builds available in a job
        for build_number in range(1, int(last_build_number) + 1):
            try:
                build_info = jenkinsAPI.get_build_info(job_name, build_number)
            except NotFound:
                continue  # Skip this build number if it doesn't exist
            existing_build = session.query(Build).filter_by(build=str(build_info['build'])).first()
            if existing_build is None:
                continue
            elif build_info['status'] != existing_build.status:
                session.execute(
                    update(Build).
                    where(Build.build.like(existing_build.build)).
                    values(status=build_info['status'], duration=build_info['duration'], running=build_info['running'])
                )
                session.commit()


# insert_new_jobs_and_builds(server)
# update_changed_status(server)
# update_dequeued_jobs(server)

# Close the session
# session.close()
