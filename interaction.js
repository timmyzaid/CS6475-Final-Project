function handleFileSelect(event){
	//var form = document.getElementById('file-form');
	//var fileSelect = document.getElementById('file-select');
	//var uploadButton = document.getElementById('upload-button');

	//form.onsubmit = function(event) {
		event.preventDefault();
		var files = event.target.files;
		if(!files.length)
			return;

		var formData = new FormData();
		//uploadButton.innerHTML = 'Uploading...';

		for(var i = 0; i < files.length; i++){
			var file = files[i];

			if(!file.type.match('image.*'))
				continue;

			formData.append('tilePhotos', file, file.name);
		}

		var xhr = new XMLHttpRequest();
		xhr.open('post', 'files', true);

		xhr.onload = function(){
			if(xhr.status === 200)
				console.log("Success!");
			else
				alert('Upload failed');
		};

		xhr.send(formData);
	//}
}