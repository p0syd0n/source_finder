function checkForErrorPage() {
  var iframe = document.getElementById('iFrame');
  var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
  
  if (iframeDoc.body.classList.contains('neterror')) {
      // If the iframe loads an error page, redirect to the iframe's source URL
      window.location.href = iframe.src;
  }
}

// Check every 500 milliseconds (0.5 seconds)
setInterval(checkForErrorPage, 500);
