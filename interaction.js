function handleBasePhotoFileSelect(event){
	event.preventDefault();
	var files = event.target.files;
	if(files && files.length !== 1)
		return;

	if(!files[0].type.match('image.*'))
		return;

	var formData = new FormData();
	formData.append('tilePhotos', files[0], files[0].name);

	var xhr = new XMLHttpRequest();
	xhr.open('post', 'basePhoto', true);

	xhr.onload = function(){
		if(xhr.status === 200)
			console.log("Success!");
		else
			alert('Upload failed');
	};

	xhr.send(formData);
}

function handleTilePhotosFileSelect(event){
	event.preventDefault();
	var files = event.target.files;
	if(!files.length)
		return;

	var formData = new FormData();

	for(var i = 0; i < files.length; i++){
		var file = files[i];

		if(!file.type.match('image.*'))
			continue;

		formData.append('tilePhotos', file, file.name);
	}

	var xhr = new XMLHttpRequest();
	xhr.open('post', 'tilePhotos', true);

	xhr.onload = function(){
		if(xhr.status === 200)
			console.log("Success!");
		else
			alert('Upload failed');
	};

	xhr.send(formData);
}