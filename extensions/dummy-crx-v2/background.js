console.log("Background speaking...");

var xhr = new XMLHttpRequest();

// Configure the XHR request
xhr.open('GET', "https://example.org?source=bg", true);

xhr.onload = function () {
  if (xhr.status >= 200 && xhr.status < 300) {
    const responseData = xhr.responseText;
    console.log('Received data:', responseData);
  } else {
    console.error('Request failed with status:', xhr.status, xhr.statusText);
  }
};

xhr.onerror = function () {
  console.error('Network error occurred');
};

xhr.send();