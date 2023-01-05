 """
 Script to set environment variables, credentials needed for Docker and AWS Batch.
 According to best practices from AWS - credentials should be stored in .aws/credentials.txt under home location.
 """

import os
docker_path = "./Docker/.env"
batch_path = "AWSBatch/.env"
# get your home location from HOME env variable
home = os.environ.get("HOME")

os.remove(docker_path)
os.remove(batch_path)

with open(f"{home}/.aws/credentials.txt", "r") as f:
    text = f.read()
text_lines = text.splitlines()
# loop through read lines to get each of credentials
for line in text_lines:
    if "=" in line:
        lines = line.split("=")
        env_name = str(lines[0]).upper()
        env_line = f"{env_name}={lines[1]}"
        with open(docker_path, "a") as e:
            e.write(f"\n{env_line}")
        print(f"Variable name: {env_name} added")

print(".env file for Docker added")

# copy file to AWS Batch directory
os.popen(f"cp {docker_path} {batch_path}")
print(".env file for AWS Batch added")