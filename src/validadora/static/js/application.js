
function alerta(message) { 
	alert(message); 
}

function draganddrop(){
	window.Dropzone.options.myAwesomeDropzone = {
  	init: function() {
    		this.on("addedfile", function(file) { alert("Added file."); });
  		}
	};
}