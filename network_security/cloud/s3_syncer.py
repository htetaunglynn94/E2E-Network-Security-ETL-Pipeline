import subprocess

class s3_sync:
    def sync_folder_to_s3(self, folder, aws_bucket_url):
        """Upload local data to cloud."""
        command = f"aws s3 sync {folder} {aws_bucket_url}"
        subprocess.run(command,    # AWS CLI command
                       shell=True, # run command through the shell
                       check=True) # raise CalledProcessError id command fails

    def sync_folder_from_s3(self, folder, aws_bucket_url):
        """Download cloud data to local"""
        command = f"aws s3 sync {aws_bucket_url} {folder}"
        subprocess.run(command,    # AWS CLI command
                       shell=True, # run command through the shell
                       check=True) # raise CalledProcessError id command fails