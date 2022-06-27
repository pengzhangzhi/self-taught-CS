# Cookies and Sessions explained

## Cookies 

HTTP is stateless, which means it can not remeber any information of previous request.

However, in some cases, we want to remeber what was happend.  e.g. In a web shop, you want to track the items that clients have put in the basket. 

That is why we use cookies.

 When clients send a request to the server with information that the server want to store,  the server will create a cookies (key/value pairs) to store such information and sent back to clients. For example you are using google to search for soccer. 

`Client send: GET /search?query=soccer`

`Server receive:200 Ok, create cookies: name: searches value: soccer, and return searched results and cookies.`

The cookies are stored in HTTP Header.

`GET /search?query=hockey HTTP/1.1 Accept: text/html Cookie: searches=soccer`

Note that cookies can be read and modified by clients. This said, servers can not trust the cookies from client even though them are created by servers.

## Sessions 

To handle the security problem, we can use Sessions.

Sessions are like a validation tools to verify if the cookies is valid (To put it simply, check if the cookies are created by the server itself).

For example, the client send a request to login in with an username and password. When the server receive the request, it will create a sesssion. Unlike cookies, the session has two items: id and loggedInAS. id is the session id, which can be a random string (e.g. wqeasdas). loggedInAs store the information of the account. If a user loggin in with this information, the server will recognize he/she as a valid user. Then the server will create a cookie that has two item:  name: sessionId, value: wqeasdas. Finally send the cookies and responses back to the client.

If the user modify the cookies, then the session will fail to recognize the session id. 

# Cookies and Sessions in Express

## Cookies

### Create cookies

`response.cookies(key,value)`

```js
const express = require('express')
const app = express()
app.get("/create-cookie", function(request, response){

response.cookies("lastVisit",Date.now())
    // ..
})

```

Header added to the response:

`Set-Cookie: lastVisit=1537889037157`

### Reading cookies

read cookies `Cookie: lastVisit=1537889037157`from client.

Use third party package cookies-parser

`npm install cookies-parser `

```js
const express = require('express')
const cookieParser = require('cookie-parser')
const app = express()
app.use(cookieParser())
app.get("/log-cookie", function(request, response){
	date = parseInt(request.cookies.lastVisit)
})

```

## Sessions

