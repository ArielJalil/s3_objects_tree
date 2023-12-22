# -*- coding: utf-8 -*-
"""
Usage: s3_tree_new.py [OPTIONS]

  S3 objects tree output.

Options:

  -c, --cli_profile TEXT  AWS cli profile name set in ~/.aws/config file.
                          [default: default]
  -b, --bucket_name TEXT  S3 bucket name.
  -p, --prefix TEXT       S3 prefix where the tree will begin.
  --help                  Show this message and exit.


i.e.

> python3 s3_tree.py -b s3_bucket_name -c CLI_PROFILE

Bucket Metrics:

s3_bucket_name: 123 Bytes
s3_bucket_name: 123 Object/s

WARNING!!! - Running this script on buckets with large amonunt of
objects could be expensive and might take a while till finish.

Please confirm if you want to proceed [Y/n]:

< s3_bucket_name/ >
│
├── PREFIX - folderA/
|   ├── size - object_1
|   └── size - object_2
├── PREFIX - folderB/
|   ├── size - object_3
|   └── size - object_4
└── PREFIX - FolderC/
    ├── size - object_5
    └── size - object_6
"""

import click  # pylint: disable=import-error
from classes.session import AwsSession
from classes.cw_metric import CwMetric

ELBOW = "└── "
TEE = "├── "
PIPE = "│   "
SPACE = "    "


def paginate(client: object, method: str, **kwargs) -> list:
    """Paginate boto3 client methods."""
    paginator = client.get_paginator(method)

    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result


@click.command()
@click.option(
    '-c',
    '--cli_profile',
    default='default',
    show_default=True,
    nargs=1,
    type=str,
    help='AWS cli profile name set in ~/.aws/config file.'
)
@click.option(
    '-b',
    '--bucket_name',
    show_default=False,
    nargs=1,
    type=str,
    help='S3 bucket name.'
)
@click.option(
    '-p',
    '--prefix',
    default='',
    show_default=False,
    nargs=1,
    type=str,
    help='S3 prefix where the tree will begin.'
)
def s3_tree(cli_profile: str, bucket_name: str, prefix: str) -> None:
    """S3 objects tree output."""
    session_obj = AwsSession(cli_profile)
    session = session_obj.cli()

    cw = session.client('cloudwatch')
    metric = CwMetric(cw)
    print("\nBucket Metrics:\n")
    metric.display_bucket_size(bucket_name)
    metric.display_object_count(bucket_name)

    print("\nWARNING!!! - Running this script on buckets with many")
    print("objects could be expensive and might take a while till finish.\n")

    if click.confirm('Please confirm if you want to proceed', default=True):
        s3 = session.client('s3')
        print(f"\n< {bucket_name}/{prefix} >\n{PIPE}")
        tree(s3, bucket_name, prefix, '')
    else:
        print('Abort action.')


def tree(s3, bucket, prefix, identation):
    """Recursively display s3 objects as a directory tree."""
    objects = list(
        paginate(
            s3,
            'list_objects_v2',
            Bucket=bucket,
            Delimiter='/',
            Prefix=prefix
        )
    )
    while objects:
        # Fetch first object to display
        obj = objects.pop(0)

        # Set flags
        is_prefix = bool('Prefix' in obj.keys())
        more_objs = bool(objects)

        display_obj(is_prefix, more_objs, identation, obj)

        if is_prefix:  # If it is a prefix we want a new branch
            tree(
                s3,
                bucket, obj['Prefix'],
                next_identation(identation, more_objs)
            )


def get_object(obj: str, idx: int) -> str:
    """Get object to display."""
    obj_split = obj.split('/')
    return obj_split[idx]


def display_obj(prefix: bool, more_obj: bool, identation: str, obj: dict) -> None:  # pylint: disable=line-too-long # noqa: E501
    """Grab the object to display and choose the right fork type."""
    if prefix:
        obj_to_display = f"PREFIX - {get_object(obj['Prefix'], -2)}/"
    else:
        obj_to_display = f"{obj['Size']} - {get_object(obj['Key'], -1)}"

    if more_obj:
        fork = TEE
    else:
        fork = ELBOW

    print(f"{identation}{fork}{obj_to_display}")


def next_identation(identation: str, more_obj: bool) -> str:
    """Calculate identation for next branch."""
    if more_obj:
        line_prefix = PIPE
    else:
        line_prefix = SPACE

    return identation + line_prefix


if __name__ == '__main__':
    s3_tree()  # pylint: disable=no-value-for-parameter
