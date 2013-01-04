from please.command_line.template import Template


def add_import_opertions(matcher, active):
        from please.import_from_polygon import create_contest
        from please.import_from_polygon import create_problem
        from please.import_from_polygon import import_problem_from_polygon
        matcher.add_handler(
                Template(["import", "polygon", "contest", "#name"]),
                create_contest,
                active)
        matcher.add_handler(
                Template(["import", "polygon", "problem", "#problem_letter",
                    "from", "contest", "#contest_id"]),
                import_problem_from_polygon, active)
        matcher.add_handler(Template(["import", "polygon", "package", "#package"]),
                create_problem, active)


def add_export_operations(matcher):
    from please.exporter.exporter import export
    matcher.add_handler(
        Template(["export", "to", "#server_name",
            "contest", "#contest_id",
            "problem|problems",
            "@problems"]),
        export,
        True)
