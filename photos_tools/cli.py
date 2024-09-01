import click
import os

from photos_tools.defaults import PhotosToolsDefaults as PTD
from photos_tools.service import PhotosService

@click.group()
@click.pass_context
@click.option(
    "--photos-secrets-file",
    "photos_secrets_file",
    type=click.Path(),
    default=PTD.PHOTOS_SECRETS_FILE,
    show_default=True,
    help="Google Photos client secrets file.",
)
@click.option(
    "--photos-refresh-token",
    "photos_refresh_token",
    type=click.Path(),
    default=PTD.PHOTOS_REFRESH_TOKEN,
    show_default=True,
    help="Google Photos refresh file (if it exists).",
)
@click.option(
    "--enable-logging",
    "enable_logging",
    type=bool,
    default=PTD.ENABLE_LOGGING,
    show_default=True,
    help="Whether to enable logging.",
)
def cli(ctx: click.Context, photos_secrets_file, photos_refresh_token, enable_logging):
    """Manage Google Photos."""
    try:
        ctx.obj = PhotosService(photos_secrets_file=photos_secrets_file, photos_refresh_token=photos_refresh_token, enable_logging=enable_logging)
    except Exception as e:
        print(f"Program error: {e}")
        exit(1)

@cli.command()
@click.pass_context
@click.option(
    "--output-dir",
    "output_dir",
    type=click.Path(),
    help="Directory to download the media to.",
)
@click.option(
    "--dry-run",
    "dry_run",
    is_flag=True,
    help="Dry run only.",
)
def clean(ctx: click.Context, output_dir, dry_run):
    """Download favorited photos so that you can later delete them from the cloud."""
    favorited_photos = ctx.obj.getFavoritedPhotos()
    print(f"{len(favorited_photos)} Photos to extract:")
    for photo in favorited_photos:
        print(f"- {photo}")
    if not dry_run:
        print("\nDownloading...")
        for photo in favorited_photos:
            if not ctx.obj.downloadPhoto(photo, output_dir):
                print(f"  WARNING: Unable to download {photo}")

def main():
    cli()

if __name__ == "__main__":
    main()
