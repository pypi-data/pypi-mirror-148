"""Console script for images_to_pdf."""
import sys
import click
from typing import List

from PIL import Image, UnidentifiedImageError

from images_to_pdf.images_to_pdf import execute


def sanitize_output_name(ctx, param, value: str):
    if not value.endswith(".pdf"):
        return f"{value}.pdf"
    return value


def verify_images(ctx, param, value: List[str]):
    for image in value:
        try:
            Image.open(image).verify()
        except UnidentifiedImageError:
            raise click.BadParameter(
                message=f"The file {repr(image)} is corrupted/not a valid image file 😞, check your files and try again 😉."
            )
    return value


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument(
    "image_files",
    type=click.Path(exists=True),
    nargs=-1,
    required=True,
    callback=verify_images,
)
@click.option(
    "-n",
    "--name",
    show_default=True,
    required=True,
    help='Output name e.g. "out.pdf"',
    prompt="Output name",
    callback=sanitize_output_name,
)
def main(name, image_files):
    """Transforms a list of images into a single pdf"""
    execute(name, image_files)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
