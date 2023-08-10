# s3_objects_tree

CLI command to generate a directory tree like with S3 bucket objects

## Required Python modules

* boto3
* botocore
* click

## Pre-requisite

In order to run this script you'll need to configure your AWS cli credentials

## Usage

```txt
Usage: s3_tree_with_objs.py [OPTIONS]

  S3 objects tree output.

Options:
  -c, --cli_profile TEXT  AWS cli profile name set in ~/.aws/config file.
                          [default: default]
  -b, --bucket_name TEXT  S3 bucket name.
  -p, --prefix TEXT       S3 prefix where the tree will begin.
  --help                  Show this message and exit.


i.e.

$ python3 s3_tree.py -b s3_bucket_name -c CLI_PROFILE

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
```

## Author and Lincense

This script has been written by [Ariel Jall](https://github.com/ArielJalil) and it is released under [GNU 3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).