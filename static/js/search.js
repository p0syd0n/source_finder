const searchBox = document.getElementById("search");

document.addEventListener("keypress", (e) => {
	if (e.keyCode == 47) {
		searchBox.select();
	}
});

