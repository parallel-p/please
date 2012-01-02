from .. import export_servers

def export(server_name, problems):
    server = export_servers.servers[server_name]
    server.set_problems(problems)
    server.create_archive()
    server.upload_file()
    server.run_script()
