
#Licensed under the MIT License 

import subprocess

users= [5]
for user in users:
    print(f"Testing for {user} users")
    html_file = f"--html=m_log_{user}.html"
    subprocess.run(["locust", "-f", "locust_test.py", "--users", str(user), "--spawn-rate", str(user) , html_file, "--processes", "-1"])