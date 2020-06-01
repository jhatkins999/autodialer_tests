$(function() {

  var numbers = ['651-492-2091', '917-613-4279']; // FROM API CALL
  var n = 1; // FROM API CALL

  var speakerDevices = document.getElementById("speaker-devices");
  var ringtoneDevices = document.getElementById("ringtone-devices");
  var outputVolumeBar = document.getElementById("output-volume");
  var inputVolumeBar = document.getElementById("input-volume");
  var volumeIndicators = document.getElementById("volume-indicators");

  var device;
  var devices = [device];
  for(i = 0; i < n; i ++)
  {
      log("Requesting Access Token...");
      console.log("requesting access token");
      // Using a relative link to access the Voice Token function
      $.getJSON("./voice-token") // Each generation of a token is unique, probs store tokens to api to be sure anyways
        .then(function(data) {
          log("Got a token.");
          console.log("Token: " + data.token);

          // Setup Twilio.Device
          device = new Twilio.Device(data.token, {
            codecPreferences: ["opus", "pcmu"],
            fakeLocalDTMF: true,
            enableRingingState: true
          });

          device.on("ready", function(device) {
            log("Twilio.Device Ready!");
            document.getElementById("call-controls").style.display = "block";
          });

          device.on("error", function(error) {
            log("Twilio.Device Error: " + error.message);
          });

          device.on("connect", function(conn) {
            log("Successfully established call!");
            document.getElementById("button-call").style.display = "none";
            document.getElementById("button-hangup").style.display = "inline";
            volumeIndicators.style.display = "block";
            bindVolumeIndicators(conn);
          });

          device.on("disconnect", function(conn) {
            log("Call ended.");
            document.getElementById("button-call").style.display = "inline";
            document.getElementById("button-hangup").style.display = "none";
            volumeIndicators.style.display = "none";
          });

          device.on("incoming", function(conn) {
            log("Incoming connection from " + conn.parameters.From);
            var archEnemyPhoneNumber = "+12093373517";

            if (conn.parameters.From === archEnemyPhoneNumber) {
              conn.reject();
              log("It's your nemesis. Rejected call.");
            } else {
              // accept the incoming connection and start two-way audio
              conn.accept();
            }
          });

          setClientNameUI(data.identity);
          device.audio.on("deviceChange", updateAllDevices.bind(device));
          if (device.audio.isOutputSelectionSupported) {
            document.getElementById("output-selection").style.display = "block";
          }
        })
        .catch(function(err) {
          console.log(err);
          log("Could not get a token from server!");
        });
      }

///////////////////////////////////////////////////////////////
  // Bind button to make call
  document.getElementById("button-call").onclick = function()
  {

    for(i = 0; i < n; i++)
    {
        call(numbers[i], device, speakerDevices, ringtoneDevices);
        log("call number : "+numbers[i]);
    }
  };

  // Bind button to hangup call
  document.getElementById("button-hangup").onclick = function() {
    hangup(device);
  };

  document.getElementById("get-devices").onclick = function() {
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      //.then(updateAllDevices.bind(device));
  };

  /*
  speakerDevices.addEventListener("change", function() {
    var selectedDevices = [].slice
      .call(speakerDevices.children)
      .filter(function(node) {
        return node.selected;
      })
      .map(function(node) {
        return node.getAttribute("data-id");
      });


    //device.audio.speakerDevices.set(selectedDevices);
  });

  ringtoneDevices.addEventListener("change", function() {
    var selectedDevices = [].slice
      .call(ringtoneDevices.children)
      .filter(function(node) {
        return node.selected;
      })
      .map(function(node) {
        return node.getAttribute("data-id");
      });

    device.audio.ringtoneDevices.set(selectedDevices);
  });
  */

  function bindVolumeIndicators(connection) {
    connection.on("volume", function(inputVolume, outputVolume) {
      var inputColor = "red";
      if (inputVolume < 0.5) {
        inputColor = "green";
      } else if (inputVolume < 0.75) {
        inputColor = "yellow";
      }

      inputVolumeBar.style.width = Math.floor(inputVolume * 300) + "px";
      inputVolumeBar.style.background = inputColor;

      var outputColor = "red";
      if (outputVolume < 0.5) {
        outputColor = "green";
      } else if (outputVolume < 0.75) {
        outputColor = "yellow";
      }

      outputVolumeBar.style.width = Math.floor(outputVolume * 300) + "px";
      outputVolumeBar.style.background = outputColor;
    });
  }
  function setSoundDevices(device, speakerDevices, ringtoneDevices)  {

    var selectedDevices = [].slice
      .call(speakerDevices.children)
      .filter(function(node) {
        return node.selected;
      })
      .map(function(node) {
        return node.getAttribute("data-id");
      });

    device.audio.speakerDevices.set(selectedDevices);

    var selectedDevices = [].slice
      .call(ringtoneDevices.children)
      .filter(function(node) {
        return node.selected;
      })
      .map(function(node) {
        return node.getAttribute("data-id");
      });

    device.audio.ringtoneDevices.set(selectedDevices);

    device.audio.availableOutputDevices.forEach(function(device, id) {
      var isActive = selectedDevices.size === 0 && id === "default";
      selectedDevices.forEach(function(device) {
        if (device.deviceId === id) {
          isActive = true;
        }
      });

      var option = document.createElement("option");
      option.label = device.label;
      option.setAttribute("data-id", id);
      if (isActive) {
        option.setAttribute("selected", "selected");
        console.log(id+" will be active")
      }

  });
  }

  function updateAllDevices() {
    updateDevices(speakerDevices, device.audio.speakerDevices.get());
    updateDevices(ringtoneDevices, device.audio.ringtoneDevices.get());

    // updateDevices(speakerDevices, );
    // updateDevices(ringtoneDevices, device);
  }

  // Update the available ringtone and speaker devices
  function updateDevices(selectEl, selectedDevices) {
    selectEl.innerHTML = "";

    device.audio.availableOutputDevices.forEach(function(device, id) {
      var isActive = selectedDevices.size === 0 && id === "default";
      selectedDevices.forEach(function(device) {
        if (device.deviceId === id) {
          isActive = true;
        }
      });

      var option = document.createElement("option");
      option.label = device.label;
      option.setAttribute("data-id", id);
      if (isActive) {
        //option.setAttribute("selected", "selected");
        console.log(id+" will be active");
      }
      selectEl.appendChild(option);
    });
  }

  // Activity log
  function log(message) {
    var logDiv = document.getElementById("log");
    logDiv.innerHTML += "<p>&gt;&nbsp;" + message + "</p>";
    logDiv.scrollTop = logDiv.scrollHeight;
  }

  // Set the client name in the UI
  function setClientNameUI(clientName) {
    var div = document.getElementById("client-name");
    div.innerHTML = "Your client name: <strong>" + clientName + "</strong>";
  }

  //New Functions: Call and Hangup
  function call(number, device, speakerDevices, ringtoneDevices)
  {
    // get the phone number to connect the call to
    var params = {
      To: number
    };

    console.log("Calling " + number + "...");
    if (device) {
      var outgoingConnection = device.connect(params);

      if(outgoingConnection.status() == 'connecting')
      {
        console.log("Ringing");
      }
      outgoingConnection.on("accept", function()
      {
        //for device in devices
        //device.disconnectAll()
        console.log("Connected babey(:");
        setSoundDevices(device, speakerDevices, ringtoneDevices);
        console.log("turned audio on");
      });
    }
    else
    {
        console.log("Device is not recognized");
    }

  }

  function hangup(device)
  {
    console.log("Hanging up...");
    if (device) {
      device.disconnectAll();
    }
  }

});
