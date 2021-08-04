# Alpha-Client server project
Project to track SSH attempt that failed on every node on client side and centralized the results in S3. 

This project has been fully tested on Ubuntu 18.03.

`client.py` is for client node that send the failed SSH attempt to S3 bucket. 

`master.py` is for master node to view the failerd SSH attempt of client nodes from S3 bucket.

## Setup
Kindly ensure that you have Python3, pip3, and awscli installed properly.

This project requires additional Python packages as per below. 

a) boto3 package

   ```bash 
   pip3 install boto3
   ```
b) pandas package

   ```bash 
   pip3 install pandas
   ```
### Code requirement to work properly
Kindly run `aws configure` to authenticate the AWS account that will be used for download/upload the file to S3.
- for client (client.py)

  Kindly change line number 68 to your bucket name. 
  
- for master (master.py)

  Kindly change line number 15 to your bucket name.

### Additional info
In order to execute this script at your preference time frame, you may add the client script (client.py) to your crontab list. 

Below is the example. 

```bash
crontab -e
```

`* * * * * /usr/bin/python3 /home/ubuntu/client.py`

configuration above shows that this script will be executed every minute.




  
