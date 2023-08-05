# Boto3-result

Library that encapsulate Boto3 in option.Result

- One class for each AWS service
- Returning Result instead of throwing exception
- Tested with library versions in requirements.txt
- Source on [github](https://github.com/gilcu2/boto3-result)

## Requirements

- python3/pip
- A valid boto3 configuration as explained in
  [boto3 config](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html)

## Use

```shell
pip install boto3r
```

## Examples

```python
    from boto3r.s3 import S3
    import os

    s3=S3.create().unwrap()
    
    S3_BUCKET = os.environ['S3_TEST_BUCKET']
    key = 'test-key'
    s = 's3_test'
    
    r=s3.put_object(S3_BUCKET, key, s) \
        .flatmap(lambda _: s3.get_attributes(S3_BUCKET, key)).flatmap()
    
    print(r.unwrap()['LastModified'])
```

## Test running

Requirements:

- Env vars:
    - S3_TEST_BUCKET with writing permission

```shell
./bin/run_test.sh
```