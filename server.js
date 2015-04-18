var http = require('http'),
	fs = require('fs'),
	formidable = require('formidable');


var server = http.createServer(function(request, response) {
	console.log(request.url);
	if(request.method === "GET"){
		if(request.url === '/'){
			fs.readFile("./index.html", function(err, html){
				if(err)
					throw err;
				response.writeHeader(200, {"Content-Type": "text/html"});
				response.write(html);
				response.end();
			});
		}
		else if(request.url === "/layout.css"){
			fs.readFile("./layout.css", function(err, layout){
				if(err)
					throw err;
				response.writeHeader(200, {"Content-Type": "text/css"});
				response.write(layout);
				response.end();
			});
		}
		else if(request.url === "/interaction.js"){
			fs.readFile("./interaction.js", function(err, js){
				if(err)
					throw err;
				response.writeHeader(200, {"Content-Type": "text/javascript"});
				response.write(js);
				response.end();
			});
		}
	}
	else if(request.method === "POST"){
		console.log("received post");
		if(request.url === "/tilePhotos"){
			var form = new formidable.IncomingForm();
			form.uploadDir = './tilePhotos/';
			form.keepExtensions = true;
			form.parse(request);

			form.on('fileBegin', function(name, file) {
				file.path = './tilePhotos/' + file.name;
			});
			
			form.on('end', function(fields, files) {
				console.log("Upload comleted!");
				response.writeHead(200);
				response.end();
			});
		}
		else if(request.url === "/basePhoto"){
			var form = new formidable.IncomingForm();
			form.uploadDir = './basePhoto/';
			form.keepExtensions = true;
			form.parse(request);

			form.on('fileBegin', function(name, file) {
				file.path = './basePhoto/' + file.name;
			});
			
			form.on('end', function(fields, files) {
				console.log("Upload comleted!");
				response.writeHead(200);
				response.end();
			});
		}
	}
}).listen(8000);
console.log('Server running at http://127.0.0.1:8000/');