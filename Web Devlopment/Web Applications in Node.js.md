# Web Applications in Node.js

Implement Web APP in Node.js

## Introduction

As shown in the fig below, the clients sent a HTTP Requests to Node.js App throught port 80. The App receive the request and generate responses that send back to clients.

![image-20210914155523713](Web%20Applications%20in%20Node.js.assets/image-20210914155523713.png)

## Example Code

### Eaxmple 1

An introductary example to show how your code works in real web app.

```js
const http = require('http') // import http module
const myServer = http.createServer(function(request, response){ // create a server
// this function is a callback function that called every time the server receive a request.

    // write reponse head. 200 is status code, the second argument is header.
    response.writeHead(200, {"content-Type":"text/plain"}) 
    
   // write response body.
    reponse.end("Hello") 

})

myServer.listen(80) // sepcify port.
```

### Example 2

This example will show you how to read out request information.

Let is say we have received a request as shown in the beflow.

![image-20210914160516583](Web%20Applications%20in%20Node.js.assets/image-20210914160516583.png)

```js

const myServer = http.createServer(function(request, response){
	const method = request.method // "GET"
    const url = request.url 
    const verion = request.httpVersion 
    const headers = request.headers
    
    // read the body

})

myServer.listen(80) // sepcify port.
```

The most hard part is reading body content. The body often contains the main data of a request. If the data is too large like video, directly reading  the whole data will generate a extremely long string. To tackle this problem, we can read a fixed amount of data each time until it reachs the end. 

Here is the code:

```js
const bodyParts = []

// we use on method to register a event sepecified by the first parameter: data
// Then pass a callback function that is called each time we read a chunck of data. Here we simply store the chunck into a array "bodyParts".
request.on("data", (chunck)=>{bodyParts.push(chunck)})
// At last,  we register a end event, that detect if the data event is ended. If it is ended, the callback will be called.
request.on("end", ()=>{const body = Buffer.concat(bodyParts).toString()})
```

### Example 3

Example 3 will show you how you can create outgoing responses.

Let is say your output response is shown as below.

<img src="Web%20Applications%20in%20Node.js.assets/image-20210914164043375.png" alt="image-20210914164043375" style="zoom:50%;" />

You can specify the reponse value like this:

![image-20210914164318047](Web%20Applications%20in%20Node.js.assets/image-20210914164318047.png)

![image-20210914164335631](Web%20Applications%20in%20Node.js.assets/image-20210914164335631.png)

To specify the body, you can do:

```js
response.write(“text.”)

reponse.end()
```

Remeber to call the `reponse.end()` function at the end. If you forget, your reponse will never be send back to clients.

# npm

## What is it?

**package management tools.**

If you are formilar with pyton, npm is like pip but works in js.

As shown in the fig below, Alice have published her package X to npm registry and every can download and use it in their project like Bob and Claire. Bob aslo can download packages that other prorgammer unload in the registry.

![image-20210914174506597](Web%20Applications%20in%20Node.js.assets/image-20210914174506597.png)

### How to use?

install npm. 

**npm is installed by default if you have download node.js.**

### How to ceate your own package?

```bash
mkdir project

cd project

npm init --yes # intialize pacakge.

npm install <package-name> # install package.


```

`npm init --yes` will ceate a configureation file which looks like this:

```
{
  "name": "javascript_exerices",
  "version": "1.0.0",
  "description": "",
  "main": "exercises.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
    
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "dependencies": {
    "express": "^4.17.1"
  }
}
```

Here the `scripts` cinludes bash script that we can run by `npm run <sctipt-name>`.

For example, we have a script:`“start”:"node main.js"` that is for initialization purpose.

We can directly run command: `npm run start` to intialize our project.





