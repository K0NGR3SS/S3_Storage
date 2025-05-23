import asyncio
from contextlib import asynccontextmanager
from aiobotocore.session import get_session

class S3Storage:
    def __init__(
        self,
        access_key = str,
        secret_key = str,
        endpoint_url = str,
        bucket_name = str,
    ):
         self.config ={
             "aws_access_key_id": access_key,
             "aws_secret_access_key": secret_key,
             "endpoint_url": endpoint_url,
         }
         self.bucket_name = bucket_name
         self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
        self,
        file_path: str,
        #This function can be changed to let user paste his own file, but in this case this function takes files locally from the file

    ):
        object_name = file_path.split('/')[-1]
        #Extracts just the file name from the full path to use as the S3 object key
        async with self.get_client() as client:
            with open(file_path, 'rb') as file:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file,
                )

async def main():
        s3_client = S3Storage(
            access_key="Whatever your access key token is",
            secret_key="Whatever your secret key token is",
            endpoint_url="https://s3.amazonaws.com", #Or other platform you use
        )

        await s3_client.upload_file("Whatever_File_You_Upload")

if __name__ == "__main__":
    asyncio.run(main())