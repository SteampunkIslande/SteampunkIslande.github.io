import click

import sys


@click.command()
@click.argument("file", type=click.File())
@click.option(
    "--separator",
    "-s",
    "sep",
    help="A string to match for separating columns",
    default=",",
)
def main(file, sep):
    head = """
    <link rel="stylesheet" href="tableau.css">
    <table id="tableau">
    """
    with file as f:
        print(head)
        first_line: str = next(f)
        print("<tr>")
        for col in first_line.split(sep):
            print("<th>", col, "</th>")
        print("</tr>")
        for line in f:
            print("<tr>")
            for col in line.split(sep):
                print("<td>")
                print(col)
                print("</td>")
            print("</tr>")
        print("</table>")


if __name__ == "__main__":
    exit(main())
