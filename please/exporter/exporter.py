from .. import export_servers

def export(server_name, contest_id, problems):
    server = export_servers.servers[server_name]
    server.set_problems(problems)
    server.set_contest_id(contest_id)
    server.create_archive()
    server.upload_file()
    server.run_script()
