var http = require('http'),
	fs = require('fs');


http.createServer(function(request, response) {
	//console.log(request.url);
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
}).listen(8000);
console.log('Server running at http://127.0.0.1:8000/');