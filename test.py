# Login with informations
payload = {'email': self.api_login, 'password': self.api_password}
headers = {'content-type': 'application/vnd.cycloid.io.v1+json'}
r = requests.get('%s/user/login' % self.api_url, data=payload, headers=headers)
r.json()

