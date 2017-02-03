#!/usr/bin/env python

import os
import sys

scopeServices, scopeControllers, scopeStates = "<!-- END SERVICES -->", "<!-- END CONTROLLERS -->", "//END SCOPES"
rootDirectory = '.rd_easy_setup'

def makedirs(name):
	try:
		os.makedirs(name)
	except:
		pass

def saveFile(filename, content):
	currentFile = open("%s/%s" % (os.getcwd(), filename), 'w')
	currentFile.write(content)

	currentFile.close()

def updateFile(filename, content, scope):
	currentFile = open("%s/%s" % (os.getcwd(), filename), 'r')
	currentFileContent = currentFile.read()

	newFileContent = currentFileContent.replace(scope, "%s\n\t\t%s" % (content, scope))

	saveFile(filename, newFileContent)

def generate_packages(name = "genApp", version = "1.0.0", description = "", main = "server.js", author = "Angular Generator"):
	content = """{
"name": "%s",
"version": "%s",
"description": "%s",
"main": "%s",
"author": "%s",
"license": "ISC",
"dependencies": {
	"angular": "^1.6.1",
	"angular-ui-router": "^0.4.2",
	"ejs": "^2.5.5",
	"express": "^4.14.1"
}
}""" % (name, version, description, main, author)

	saveFile("%s/package.json" % name, content)

def generate_main(name, main):

	content = """var express = require('express');
var app = express();

var port = process.env.PORT || 8080;

app.use(express.static(__dirname + '/app'));
app.use('/node_modules',  express.static(__dirname + '/node_modules'));

app.engine('html', require('ejs').renderFile);

app.set('view engine', 'ejs');

app.get('/', function(req, res) {
    res.render('index.html');
});

app.listen(port, function() {
    console.log('Our app is running on http://localhost:' + port);
});
	"""

	saveFile('%s/%s' % (name, main) , content)

def generate_index(name, description, author):
	contentIndex = """<html>
	<head>
		<script src="/node_modules/angular/angular.min.js"></script>
		<script src="/node_modules/angular-ui-router/release/angular-ui-router.min.js"></script>

		<script type="text/javascript" src="app.js"></script>

		%s

		%s
	</head>
	<body ng-app="%s">
		<div ui-view></div>
	</body>
</html>
""" % (scopeServices, scopeControllers, name)

	contentDescription = """<h1>%s</h1>
<h2>%s</h2>
<h3>Author: %s</h3>
	""" % (name, description, author)

	saveFile('%s/app/index.html' % name, contentIndex)
	saveFile('%s/app/about.html' % name, contentDescription)

def generate_app(name):
	content = """var app = angular.module('%s', ['ui.router']);


app.config(function($stateProvider, $urlRouterProvider){
	$urlRouterProvider.otherwise('about');

	$stateProvider.state('about', {
		templateUrl: "about.html",
		url: "/about"
	});

	%s
});
	""" % (name, scopeStates)

	saveFile('%s/app/app.js' % name, content)


def generate_view():
	if os.path.exists(rootDirectory):
		os.chdir('app')

	view_name = raw_input("View Name: ")
	controller_name = raw_input("Controller Name: ")
	state_name = raw_input("State Name: ")
	url = raw_input("URL: ")

	contentView = "<div>Hello, this is the view %s</div>" % view_name
	contentController = """app.controller('%s', function($scope){

});""" % (controller_name)

	contentState = """$stateProvider.state('%s', {
		templateUrl: "%s/%s.html",
		controller: "%s",
		url: "/%s"
	});
	""" % (state_name, view_name, view_name, controller_name, url)

	makedirs(view_name)

	saveFile('%s/%s.html' % (view_name, view_name), contentView)
	saveFile('%s/%s.controller.js' % (view_name, view_name), contentController)

	contentIndex = """<script src="%s/%s.controller.js"></script>""" % (view_name, view_name)
	updateFile('index.html', contentIndex, scopeControllers)
	updateFile('app.js', contentState, scopeStates)

def generate_service():
	if os.path.exists(rootDirectory):
		os.chdir('app')
		
	package_name = raw_input("Package Name: ")
	service_name = raw_input("Service Name: ")

	contentService = """app.service('%s', function(){
	this.getSample = function(){
		return "Angular Generator";
	};
});
	""" % (service_name)

	contentIndex = """<script src="%s/%s.service.js"></script>""" % (package_name, service_name)

	makedirs(package_name)

	saveFile('%s/%s.service.js' % (package_name, service_name), contentService)

	updateFile('index.html', contentIndex, scopeServices)

# --------------------- Getting project information ----------------------------
def generate_angular():
	name = raw_input("Project Name: ")
	version = "1.0.0"
	description = raw_input("Description: ")
	main = "server.js"
	author = raw_input("Author: ")

	# ---------------------- Preparing project folders ------------------------------

	makedirs(name)
	makedirs('%s/app' % name)

	saveFile('%s/%s' % (name, rootDirectory), '.')

	# ---------------------- Generate packages.json file ----------------------------

	generate_packages(name, version, description, main, author)

	# ---------------------- Generate "main".js file --------------------------------

	generate_main(name, main)

	# ---------------------- Generate index.html ------------------------------------

	generate_index(name, description, author)

	# ---------------------- Generate app.js ----------------------------------------

	generate_app(name)

	# ---------------------- Finishing ----------------------------------------------

	newcwd = '%s/%s/' % (os.getcwd(), name)
	os.chdir(newcwd)

	os.system("npm install")

	print("")
	print("---------------------------------------------------------------------------------------------")
	print("Your angular project named %s was created in %s/%s" % (name, os.getcwd(), name))
	print("Go to the folder and run npm install to install the dependencies and then npm start to run")
	print("---------------------------------------------------------------------------------------------")
	print("")


if 'gen' in sys.argv and 'app' in sys.argv:
	generate_angular()
elif 'gen' in sys.argv and 'view' in sys.argv:
	generate_view()
elif 'gen' in sys.argv and 'service' in sys.argv:
	generate_service()
else:
	print("Unknown Command")
