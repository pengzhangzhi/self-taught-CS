## What is the MVC Pattern?

A design pattern common in implementation of GUIs.

Sperate your code into three part.

- Model: data to be visualized

- View: Visualizing Model

- Controler: making it all happen

  - Create/fetches Model
  - instantialize View 
  - handle user interations with the view

  ## MVC For Web APP

  The model (data) is typically stored in a database.

  The view generates HTML Code.

  The controler:

  1. receives incoming requests.
  
  2. fetches the model from database.
  
  3. ask view to generate HTML Code for the fetched data.
  
  4. send back reponse.
  
     ![image-20210915182342276](Web%20Applications%20in%20Express.assets/image-20210915182342276.png)
  
  ## MVC Express Example
  
  ```js
  const express = require("express")
  const app = express()
  // model(data) 
  const human = {id:0, name:"Alice"}
  // controler
  app.get("/hello",function(request, response){
      // render the view with model. 
      // The view is human.hbs
      response.render("human.hbs",human)
  })
  ```
  
  `  response.render("human.hbs",human)` is part of controler. `views/human.hbs` is a handlebar template here is called **view** that looks like this:
  
  ```html
  <h1>
  {{name}}
  </h1>
  ```
  
  Note that all the `.hbl` files is stored in `views` folder. The `human` is the context. 

Finally, our app will retrun a reponse body that is rendered like this:

```js
<h1>
Alice
</h1>
```

## Using handlebars in express

1. `npm install express-handlebars`

```js
const express = require("express")
const expressHnadlebars = require("express-handlebars")

const app = express()
// register a view implemented in hbs.
app.engine("hbs",expressHandlebars()
           {
           extname:".hbs"
           })
```

You can use `response.render("<name-of-your-view>.hbs",model)` in your callbacks to render view.  The view is in the path:` views/<name-of-your-view>.hbs`.

## Layouts In Express-handlebars

Lets say you have two view:

1. `views/about.hbs`

```html
<!DOCTYPE html>
<html>
<head>
<title>Website</title>
</head>
<body>
<h1>About</h1>
<p>About us...</p>
</body>
</html>

```

2. `views/contact.hbs`

```html
<!DOCTYPE html>
<html>
<head>
<title>Website</title>
</head>
<body>
<h1>Contact</h1>
<p>Contact us...</p>
</body>
</html>

```

The only different is:

```html
<body>
<h1>  </h1>
<p>  </p>
</body>
```

The layout is the same.

To get rid of dupilication, we can use a layout handlebar.

In the layout blue.hbs `/views/layouts/blue.hbs`,  use the `{{{body}}}` to refer to different content. Other parts is the layout.

```html
<!DOCTYPE html>
<html>
<head>
<title>Webite</title>
</head>
<body>
{{{body}}}
</body>
</html>
```

In the about view (`/views/about.hbs`), simply wirte:

```html
<h1>About</h1>
<p>About us...</p>
```

In the contact view,

```html
<h1>Contact</h1>
<p>Contact us...</p>
```

and register the layout view:

```js
app.engine("hbs", expressHandlebars({
    extname:".hbs",
    defaultLayout:"blue", // specify the defalut layout: views/layouts/blue.hbs
}))
app.get("/about",function(request, response){
    response.render("about.hbs",{}) // render the about view that is based on the blue layout.
})
```

## Partials in express-handlebars

Let is say the layout of your web app looks like this:

![image-20210915183426928](Web%20Applications%20in%20Express.assets/image-20210915183426928.png)

You want to implement two login module, how to do it? copy and paste? That is duplication!

You can implement a login.hbs file that contains the login view code. And use the code in other view.

For example,

File `/views/partials/login.hbs` is :

```html
<h1>Login</h1>
<form>
...
</form>
```

In `/views/home.hbs`:

```html
<h1>Home</h1>
<p>Login using the form below.</p>
{{> login}}

```

Here the syntax is `{{> login}}` to use a login handlebar in the path: `/views/partials/login.hbs`.

## Handling HTML Form

Here is a standrd HTML Form for login. 

```html
<form method="GET" action="http://www.mi6.com/login">
Username: <input type="text" name="un"><br>
Password: <input type="password" name="pw"><br>
<input type="submit" value="Login!">
</form>
```

How our app handle a Form request?

Here the form use GET method. So the request would be like this: `GET /login?un=JamesBond&pw=missMP HTTP/1.1`. The url `un=JamesBond&pw=missMP `indicates the username and password.

In express, to access the information ,we can use: `request.query.un`  and `request.query.pw`.

**What if the form use POST method?**

This is a little different. The URL would not indicate any information about the content. There is a attribute: `Content-Type: application/x-www-form-urlencoded` tells that this is url-encoded. The content is encoded into the request body.

Things get complicated. We need to use a pacakage. `npm install body-parser` to decode body content.

```js
const exprss = require("express")
const app = express()
const bodyparser = require("body-parser")
// bodyparser is a object that has a function urlencoded. the parameter {extened:false} is defalut value in most cases.
// bodyparser is a midlleware that deal with the post query.
app.use(bodyparser.urlencoded({extended:false}))

// after the bodyparser is used as the middleware, the body content of post will be parsed as qurey format.

app.post("/login",function(request, response){
    const name = request.body.un
    const password = request.body.pw
})
```

## The static middleware

There are some static file in our web app. For example the `layout.css`.

![image-20210915185301632](Web%20Applications%20in%20Express.assets/image-20210915185301632.png)

If we want users to access to those file by url like: `/layout.css`, we have to write a peice of control code for each ffiles. NO! It is duplication.

A better solution is this. 

```js
const express = require("express")
const app = express()
app.use(epxress.static("public")) // public is the folder that store all the static file.

```

If a user ask to access  layout.css file, out app will first traverse the file to see if there is a file named layout.css. If so, it will directly return the file.

