# Handlebars

A templating language to generate dynamic HTML code. As we have seen before, all the HTMLcode are hard-coded in a file. The webpage is static that only display a fixed content. What if we want to dynamically show different contents?  Handlebars can help!

Hnadlebars have two main parts: The template and the context. Template is a description of HTML code that used to dynamically generate HTML code. As shown in the below, the simplest template is hard-coded html code which means that the template can only generate a specific HTML code.

![image-20210915093754007](%E6%96%B0%E5%BB%BA%20MD_AUTO_FILE%20%E6%96%87%E4%BB%B6.assets/image-20210915093754007.png)

For a general template, inside each tag, there are some variables that refer to different contents. 

As shown in the below, the h1 tag contain a title variables that can be midified to show different content. Note that use double curly bracket to cover the variable.

```html
<h1>
    {{title}}
</h1>
```

Everything seems pretty good, but have you thought about where does variable `title` come from? - Context.

A context can be a javascript object that looks like this:

```js
const book = {
title: "The Da Vinci Code",
author: "Dan Brown",
pages: 359
}
```

​	Such a context combined with the following template:

```html
<h1>{{title}}</h1>
<div>Author: {{author.name}}</div>
<div>Pages: {{pages}}</div>
```

and generate the HTML code:

```html
<h1>The Da Vinci Code</h1>
<div>Author: Dan Brown</div>
<div>Pages: 359</div>
```

![image-20210915095645528](%E6%96%B0%E5%BB%BA%20MD_AUTO_FILE%20%E6%96%87%E4%BB%B6.assets/image-20210915095645528.png)

## The if block helper

```html
{{#if <condition> }}
<h1> 
    condition == True 
    </h1>
{{else}}
<h1>
    condition == Flase
    </h1>
{{/if}} 

```

## The Each Block Helper

The context is a javascript object that contains a human array. Each element of that array is another object with a name pair.

### context:

```
const context = {
humans: [
{name: "Alice"},
{name: "Bob"},
{name: "Claire"}
]
}
```

Inside the template, we traverse all the name use a unorder list to demostrate each name.

### Template:

```html
<h1>
    Context
</h1>
<ul>
    {{#each humans}}
    <li>
        <h2>
            {{name}}
        </h2>
    </li>
    {{/each}}
    
</ul>
```

## Escaping HTML Code

if your context is `<h1> Hello </h1>` then the generated html code would be <h1>Hello </h1> this is not good.  We want the code is rendered. How to fix?

Use `{{{ }}}`to display html content. E.g. `{{{<h1> Hello </h1>}}}`. So the browser would know that this context is in html format and automatically render it.

