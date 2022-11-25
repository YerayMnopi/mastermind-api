import typer

from .init_db import InitDBCommand

app = typer.Typer()


@app.command()
def create_db():
    typer.echo('Creating DB')
    InitDBCommand().handle()
    typer.echo('DB created')


if __name__ == "__main__":
    app()
