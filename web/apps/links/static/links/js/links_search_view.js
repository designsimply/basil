function initializeLinksSearchForm() {
	let searchParams = new URLSearchParams(window.location.search);

	let s = searchParams.get('s')
	if ( s !== null ) {
		s = decodeURI(s);
	}
	document.getElementById('linksSearchFormText').value = s

	page = linksSearchState.page;
	document.getElementById('linksSearchFormPage').value = page;
	if ( page > 1) {
		document.getElementById('linksSearchSubmitPreviousId').hidden = false;		
	}
	if ( linksSearchState.end < linksSearchState.total ) {
		document.getElementById('linksSearchSubmitNextId').hidden = false;		
	}
}

function linksSearchSubmit() {
	console.log('search');
	var searchQueryString = encodeURI(document.getElementById('linksSearchFormText').value);
	document.getElementById('linksSearchFormS').value = searchQueryString;
}

function linksSearchSubmitPrevious() {
	console.log('prev page');
	let page = linksSearchState.page;
	page = Math.max(1, page - 1);
	document.getElementById('linksSearchFormPage').value = page;
	linksSearchSubmit();
}

function linksSearchSubmitNext() {
	console.log('next page');
	let page = linksSearchState.page;
	page++;
	document.getElementById('linksSearchFormPage').value = page;
	linksSearchSubmit();	
}

window.addEventListener('load', function(event) {
  // console.log("window.onload", event, Date.now() ,window.tdiff);	
	console.log('load page');
	initializeLinksSearchForm();
})
