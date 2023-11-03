from grohit.cli.commands.command import Command


class RenderCommand(Command):
    """
    Render a template
    render
        {template : The template file}
        {--o|output= : The output file}
        {--d|data= : The data file}
    """

    name = "render"
    description = "Renders Grafana dashboard by template"

    def handle(self):
        print("test")
        print(self.grohit.config.GRAFANA_URL)
