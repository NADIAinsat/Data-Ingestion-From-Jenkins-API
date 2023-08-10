from jenkins_api import jenkinsAPI
from data_processing import database_connection, data_modeling, data_integration


def main():
    server = jenkinsAPI.server
    session = database_connection.session
    engine = database_connection.engine
    data_modeling.Base.metadata.create_all(engine)
    data_integration.insert_new_jobs_and_builds(server)
    data_integration.update_changed_status(server)
    data_integration.update_dequeued_jobs(server)
    session.close()


if __name__ == "__main__":
    main()
