## Synopsis

This tool allows you to create angular projects running over a node.js server. 
All the pages created with `angular-node-easy-setup` are mapped to a route's configuration file.

In this tool, a view is a set with a `.html` and a `.controller.js` files.
All views, controllers and services are automatically mapped to the `index.html` and a new route is created for it.

Services can also be created and they are also automatically mapped to the `index.html`.


## Installation

```bash
$ ./install.sh
```

## API Reference

To start a new app, run: 

```bash
$ an-easy-setup gen app
```

and provide the needed information we ask.
After the npm install finishes running, from inside of your app's folder you can run npm start to run the server.

Make sure that every command below will be executed from inside `your_app_folder` or `your_app_folder/app`

To add a new view with its controller and a state, run:

```bash
$ an-easy-setup gen view
```

To add a new service, run:

```bash
$ an-easy-setup gen service
```
