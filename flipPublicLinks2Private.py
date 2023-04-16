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
#print('Enter the email address of the user you wish to remove sharelinks for:')
userEmail = 'gibberish'
print('Enter the org id that you wish to act upon:')
orgId = input()
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

#Get org info
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

#dataList.append(encode(userEmail))
dataList.append(encode('--'+boundary+'--'))
dataList.append(encode(''))
body = b'\r\n'.join(dataList)
payload = body
headers = {
  'Authorization': str(bearerToken),
  'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
}
conn.request("GET", "/api/2/organization/"+ str(orgId) +"/persons", payload, headers)
res = conn.getresponse()
data = res.read()
orgInfo = data.decode("utf-8")
orgInfoFormatted = json.loads(orgInfo)
#print(orgInfoFormatted)

personIds = []

for result in orgInfoFormatted['results']:
  #print(result['id'])
  current = str(result['id'])
  personIds.append(current)

#DEBUG
print('List of persons:')
print(personIds)

#Get user sharelinks
personPosition = 0
totalLinks = []

for i in personIds[personPosition]:
    try:

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
        conn.request("GET", "/api/2/person/" + str(personIds[personPosition]) + "/sharelinks", payload, headers)
        res = conn.getresponse()
        data = res.read()
        sharelinks = data.decode("utf-8")
        sharelinksFormatted = json.loads(sharelinks)

        for result in sharelinksFormatted['results']:
            if result['login_required'] == False:
                current = str(result['id'])
                totalLinks.append(current)
        
        personPosition += 1
        time.sleep(1.5)
    
    except IndexError:
        break

print('total links are:')
print(totalLinks)
    
    
#unwantedLinks = []



#for result in sharelinksFormatted['results']:
#  print(result['id'])
#  current = str(result['id'])
#  unwantedLinks.append(current)

linkPosition = 0
#Deactivating share links

for i in totalLinks[linkPosition]:
    try:

        conn = http.client.HTTPSConnection("syncedtool.com")
        dataList = []
        boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=login_required;'))

        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))

        dataList.append(encode("true"))
        dataList.append(encode('--'+boundary+'--'))
        dataList.append(encode(''))
        body = b'\r\n'.join(dataList)
        payload = body
        headers = {
        'Authorization': str(bearerToken),
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
        }
        conn.request("PUT", "/api/2/sharelinks/" + str(totalLinks[linkPosition]), payload, headers)
        res = conn.getresponse()
        data = res.read()
    #print(data.decode("utf-8"))
        linkPosition += 1
        time.sleep(1.5)
    except IndexError:
        break


print('All done!')
time.sleep(2)
print('Application closing in 30 seconds...')
time.sleep(30)



