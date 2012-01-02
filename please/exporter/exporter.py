from .. import globalconfig

def export(server_name, problems):
    server = globalconfig.servers[server_name]
    server.set_problems(problems)
    server.create_archive()
    server.upload_file()
    server.run_script()
