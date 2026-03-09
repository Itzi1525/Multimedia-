function listen() {
  let inputArea = document.getElementById('input-area')
  let outputArea = document.getElementById('output-area')

  var recognition = new webkitSpeechRecognition();
  recognition.lang = "es-ES";  // idioma español
  recognition.start();

  recognition.onresult = function(event) {
    let transcript = event.results[0][0].transcript.toLowerCase();

    if (transcript.includes("que hora es") || 
        transcript.includes("que hora son") || 
        transcript.includes("dame la hora")) {

        let ahora = new Date();
        let hora = ahora.toLocaleTimeString();
        outputArea.innerHTML = "La hora es: " + hora;

    } else {
        outputArea.innerHTML = "No entendí lo que dijiste.";
    }
  }
}