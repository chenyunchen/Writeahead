window.onload = init;
var profile, email;
var accessagree = "";
function init(){
  var button1 = document.getElementById("buttonclick1");
  button1.onclick = handleButtonClick1;
  var button2 = document.getElementById("buttonclick2");
  button2.onclick = handleButtonClick2;
  var button3 = document.getElementById("buttonclick3");
  button3.onclick = handleButtonClick3;
  var save = document.getElementById("save");
  save.onclick = handleSave;
  var load = document.getElementById("load");
  load.onclick = handleLoad;
}
function handleButtonClick1(){
  var transarea = document.getElementById("click1");
  var button = document.getElementById("buttonclick1");
  var divtitle = document.createElement("div");
  divtitle.setAttribute("id", "title");
  var textarea = document.createElement("textarea");
  textarea.setAttribute("class", "edit");
  textarea.setAttribute("id","clickevent1");
  transarea.removeChild(button);
  transarea.appendChild(divtitle);
  transarea.appendChild(textarea);
  tinymce.EditorManager.execCommand('mceAddEditor', true, "clickevent1");
}
function handleButtonClick2(){
  var transarea = document.getElementById("click2");
  var button = document.getElementById("buttonclick2");
  var divtitle = document.createElement("div");
  divtitle.setAttribute("id", "title");
  var textarea = document.createElement("textarea");
  textarea.setAttribute("class", "edit");
  textarea.setAttribute("id","clickevent2");
  transarea.removeChild(button);
  transarea.appendChild(divtitle);
  transarea.appendChild(textarea);
  tinymce.EditorManager.execCommand('mceAddEditor', true, "clickevent2");
}
function handleButtonClick3(){
  var transarea = document.getElementById("click3");
  var button = document.getElementById("buttonclick3");
  var divtitle = document.createElement("div");
  divtitle.setAttribute("id", "title");
  var textarea = document.createElement("textarea");
  textarea.setAttribute("class", "edit");
  textarea.setAttribute("id","clickevent3");
  transarea.removeChild(button);
  transarea.appendChild(divtitle);
  transarea.appendChild(textarea);
  tinymce.EditorManager.execCommand('mceAddEditor', true, "clickevent3");
}
function handleSave(){
  var first = document.getElementById("firstparagraph").value;
  var second = document.getElementById("secondparagraph").value;
  var third = document.getElementById("thirdparagraph").value;
  var content1 = tinyMCE.get("clickevent1").getContent();
  var content2 = tinyMCE.get("clickevent2").getContent();
  var content3 = tinyMCE.get("clickevent3").getContent();
  var article = {
    "accessagree": accessagree,
    "firstparagraph": first,
    "secondparagraph": second,
    "thirdparagraph": third,
    "clickevent1": content1,
    "clickevent2": content2,
    "clickevent3": content3
  }
  var req = new XMLHttpRequest();
  var url = "/articlesave";
  req.open("POST", url);
  req.setRequestHeader("Content-Type", "application/json");
  req.send(JSON.stringify(article));
  alert("Save Success!!");
}
function destroyClickedElement(event)
{
  document.body.removeChildmoveChild(event.target);
}
function handleLoad()
{
  var fileToLoad = document.getElementById("filename").files[0];

  var fileReader = new FileReader();
  fileReader.onload = function(fileLoadedEvent)
  {
  var textFromFileLoaded = fileLoadedEvent.target.result;
  document.getElementById("firstparagraph").value = textFromFileLoaded;
  };
  fileReader.readAsText(fileToLoad, "UTF-8");
}

function loginFinishedCallback(authResult) {
    if (authResult) {
      if (authResult['error'] == undefined){
        toggleElement('signinButton'); // Hide the sign-in button after successfully signing in the user.
        gapi.client.load('plus','v1', loadProfile);  // Trigger request to get the email address.
        var xmlhttp = new XMLHttpRequest();
        var url = "/request";
        xmlhttp.open("POST", url);
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        accessagree = authResult['access_token'];
        var clientdata = {
          "id": authResult['access_token']
        };
        xmlhttp.onload = function(){
            handleButtonClick1();
            handleButtonClick2();
            handleButtonClick3();
          if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
            jsoncontent = JSON.parse(xmlhttp.responseText);
            document.getElementById("time").innerHTML = "上次最後存檔時間: "+jsoncontent.time;
            document.getElementById("firstparagraph").value = jsoncontent.firstparagraph;
            document.getElementById("secondparagraph").value = jsoncontent.secondparagraph;
            document.getElementById("thirdparagraph").value = jsoncontent.thirdparagraph;
            document.getElementById("clickevent1").value = jsoncontent.clickevent1;
            document.getElementById("clickevent2").value = jsoncontent.clickevent2;
            document.getElementById("clickevent3").value = jsoncontent.clickevent3;
          }
        };
        xmlhttp.send(JSON.stringify(clientdata));
      } else {
        console.log('An error occurred');
      }
    } else {
      console.log('Empty authResult');  // Something went wrong
    }
  }

  /**
   * Uses the JavaScript API to request the user's profile, which includes
   * their basic information. When the plus.profile.emails.read scope is
   * requested, the response will also include the user's primary email address
   * and any other email addresses that the user made public.
   */
  function loadProfile(){
    var request = gapi.client.plus.people.get( {'userId' : 'me'} );
    request.execute(loadProfileCallback);
  }

  /**
   * Callback for the asynchronous request to the people.get method. The profile
   * and email are set to global variables. Triggers the user's basic profile
   * to display when called.
   */
  function loadProfileCallback(obj) {
    profile = obj;

    // Filter the emails object to find the user's primary account, which might
    // not always be the first in the array. The filter() method supports IE9+.
    email = obj['emails'].filter(function(v) {
        return v.type === 'account'; // Filter out the primary email
    })[0].value; // get the email from the filtered results, should always be defined.
    displayProfile(profile);
  }

  /**
   * Display the user's basic profile information from the profile object.
   */
  function displayProfile(profile){
    document.getElementById('name').innerHTML = profile['displayName'];
    document.getElementById('pic').innerHTML = '<img src="' + profile['image']['url'] + '" />';
    toggleElement('profile');
  }

  /**
   * Utility function to show or hide elements by their IDs.
   */
  function toggleElement(id) {
    var el = document.getElementById(id);
    if (el.getAttribute('class') == 'hide') {
      el.setAttribute('class', 'show');
    } else {
      el.setAttribute('class', 'hide');
    }
  }
