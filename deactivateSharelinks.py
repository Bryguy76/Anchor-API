import http.client
import json
import mimetypes
from codecs import encode
import time
import sys
#Choose user
print('Enter the email address of the API account to authenticate with:')
authEmail = input()
print('Please enter the account password:')
userPassword = input()
print('Enter the client id:')
clientId = input()
print('Enter the client secret:')
clientSecret = input()
print('Enter the email address of the user you wish to remove sharelinks for:')
userEmail = input()
bearerToken = ''
#Obtain Auth Token
conn = http.client.HTTPSConnection("syncedtool.com")
dataList = []
boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=grant_type;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("password"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=client_id;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(clientId))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=client_secret;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(clientSecret))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=username;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(authEmail))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=password;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(userPassword))
dataList.append(encode('--'+boundary+'--'))
dataList.append(encode(''))
body = b'\r\n'.join(dataList)
payload = body
headers = {
  'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
}
conn.request("POST", "/oauth/token", payload, headers)
res = conn.getresponse()
data = res.read()
tokenData = data.decode("utf-8")
tokenDataFormatted = json.loads(tokenData)
#print(tokenDataFormatted)
preBearerToken = tokenDataFormatted['access_token']
bearerToken = 'Bearer ' + preBearerToken

#Get user info
headers = {
  'Authorization': '',
  'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
}

headers['Authorization'] = bearerToken
conn = http.client.HTTPSConnection("syncedtool.com")
dataList = []
boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=email;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(userEmail))
dataList.append(encode('--'+boundary+'--'))
dataList.append(encode(''))
body = b'\r\n'.join(dataList)
payload = body
headers = {
  'Authorization': str(bearerToken),
  'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
}
conn.request("GET", "/api/2/person/" + str(userEmail), payload, headers)
res = conn.getresponse()
data = res.read()
userInfo = data.decode("utf-8")
userInfoFormatted = json.loads(userInfo)
print('User id is: ' + str(userInfoFormatted['id']))
print(userEmail)

#Store user id

userId = userInfoFormatted['id']

#Get user sharelinks

conn = http.client.HTTPSConnection("syncedtool.com")
dataList = []
boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=email;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(userEmail))
dataList.append(encode('--'+boundary+'--'))
dataList.append(encode(''))
body = b'\r\n'.join(dataList)
payload = body
headers = {
  'Authorization': str(bearerToken),
  'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
}
conn.request("GET", "/api/2/person/" + str(userId) + "/sharelinks", payload, headers)
res = conn.getresponse()
data = res.read()
sharelinks = data.decode("utf-8")
sharelinksFormatted = json.loads(sharelinks)

unwantedLinks = []

print('Found sharelinks are:')


for result in sharelinksFormatted['results']:
  print(result['id'])
  current = str(result['id'])
  unwantedLinks.append(current)

linkPosition = 0
#Deactivating share links

for i in unwantedLinks[linkPosition]:
  try:

    conn = http.client.HTTPSConnection("syncedtool.com")
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=email;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=Authorization : Bearer;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("yP4bvAXcQ2ARn2dMoTNdvdpcAaooQm"))
    dataList.append(encode('--'+boundary+'--'))
    dataList.append(encode(''))
    body = b'\r\n'.join(dataList)
    payload = body
    headers = {
    'Authorization': str(bearerToken),
    'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    conn.request("DELETE", "/api/2/sharelinks/" + str(unwantedLinks[linkPosition]), payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(data.decode("utf-8"))
    linkPosition += 1
    time.sleep(1.5)
  except IndexError:
    break


print('All done!')
time.sleep(2)
print('Application now closing...')
time.sleep(2)



