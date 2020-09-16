monitor_dtime()
function monitor_dtime(){
var mydtimeHolder = document.querySelector("#showdtime")
// Set the date we're counting down to
var mydate = new Date()
var next30min = mydate.getMinutes() + 5
mydate.setMinutes(next30min)
var mydtime = mydate.getTime()

var x = setInterval(function() {

  var now = new Date().getTime();
    
  var distance = mydtime - now;
  
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    
  // Output the result in an element with id="demo"
  // mydtimeHolder.innerHTML =  minutes + "m " + seconds + "s ";
  // If the count down is over, write some text 
  if (distance < 0) {
    window.location.replace("connectdjango.com")
  }
}, 1000);
}

