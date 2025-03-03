var myVariable = "Shotgun Shotgun Ganja Ganja Buddha Buddha";
var placeholder = ""

function myFunction(aValue) {
    placeholder = document.getElementById("para").innerText;
    document.getElementById("para").innerHTML=aValue;
} 

function revertMyFunction(oldValue) {
    document.getElementById("para").innerHTML=oldValue;
}

var awesomeNum = 50;
var myString = "Hi Tehere"
var mySecondString = "THis is the seconds string"
var thisArray = ["Hello","World"]
var myBoolean = false
var iLikeObjects = {"Jane":33,"Timmy":"21","Phil":27}

function doAlert(inputVar) {
    alert(inputVar)
}

function doComparisonAlert() {
    alert(9==9)
}