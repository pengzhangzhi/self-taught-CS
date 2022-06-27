# Express Basics

Why write a lot of code in Node.js when we can write a little using Express?

Express is a framework for web app in Node.js.

 • Website: https://expressjs.com 

• Is distributed as an npm package. 

​			• npm install express

## Why not use the http module?

Requires lots of work.

## How express works?

Middlewares Architecture

Inside a web app, there are some middlewares in row. Each of them handle a specific request and return a reponse. When receiving a request, a middleware can process it and send a http reponse. Also, the middleware can pass the request to the next middleware.![image-20210915092729937](Express%20Basics.assets/image-20210915092729937.png)

## Example Code

### Example 1

here is a general example to show you how to use express.

```js
const express = require("express") // import express framework
const app = express() // web app object
// use middleware. takes function as the middleware.
app.use( 
    function(request, response, next){
        if(request.method == "GET" && request.uri == "/hello"){
            // send response.
            response.send("Hello. This is the body of HTTP response.") 
        }else{
 // if we can handle this request, then send it to the next middleware.
            next() 
        }
    }
)
app.listen(8080) // listen to a port
```

### Example 2

Instead of using `use` to refer to different http request, we can use a specific mthod. E.g. `app.get` to handle get request. Note that you do not have to pass the request to the next middleware in this case.

```js
app.get('/hello', function(request, response){ // handle get request
    // the first parameter refers to url the sencond refer to middleware.
const clientIp = request.ip
const queryStringObject = request.query
})
app.get('/hi', function(request, response){
response.send("Hi!")
})


```

### Example 3

Express is more powerful than vanilla HTTP module. Express is a superset of HTTP.

Express contains more APIs than HTTP.

```js
app.get("/hello",function(request,response){
    
    const ip = request.ip
    const query_dict = request.qurery
    
})
```

Except for regular attribute like `request.url`, Express can access other information of clients. Here we obtain the IP and query dict. For GET request that looks like this: 

`GET /the-uri?what=this&that=8 HTTP/1.1`.

The query is the string after ? mark.

`request.query = {what: "this", that: "8"}`

#### Considering response:

we can send file or download file to client.

```js
app.get("/hello",function(request,response){
	response.sendFile("file.html")
    response.download("file.html")
})
```

### Example 4: Routing parameters

Let is considering this case, cilents want to visit url that have the pattern `human/0`, `human/1`.... where 0,1.. is the id. How to handle such a request?

A simple solution is cover all the case.

```js
app.get("human/0",function(request, response){
	// ...
    const id = 0
})
app.get("human/1",function(request, response){
	// ...
    const id = 1
})

// ....
```

Toooo complicated right?

A better solution is using Routing parameters.  Use `:id` to denote parameter id. Routing parameters can match the url so that is in the format of `"human/:id"` can be handle by a single `get` method.

```js
app.get("human/:id",function(request, response){
		const id = request.param.id 
})
```

### Example 5

If a middleware **a** add an attribute to a request and send the request to the next middleware **b**. Then b can manipulate the attribute.

```js
app.use(function(request, response, next){
request.stupidExample = 15
next()
})
app.get('/hello', function(request, response){
// We can use request.stupidExample here!
})
```



## What remains to learn?

- • Different middleware functions you can use.
-  • Commonly used middleware functions: https://expressjs.com/en/resources/middleware.html 
- • Many other npm packages contains middleware functions.
-  • More advanced features in Express (i.e. response.render()).

## Recommended reading

- [Express' website](https://expressjs.com/en/guide/routing.html)
  - Guide
    - Routing

