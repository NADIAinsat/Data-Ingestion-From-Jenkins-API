import jenkinsAPI


def print_console(job_name, build_number):
    server = jenkinsAPI.server
    job = server.get_job(job_name)
    build = job.get_build(build_number)
    console_output = build.get_console()
    print(console_output)


# print_console('TestPipeline', 4)
