import click

from uniprotkb import uniprotkb


@click.group()
def cli():
    pass


cli.add_command(uniprotkb)


if __name__ == '__main__':
    cli()
