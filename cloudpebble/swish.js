//Run at https://cloudpebble.net/ide/project/274001

var UI = require('ui');
var Vibe = require('ui/vibe');
var ajax = require('ajax');
var Accel = require('ui/accel');
Accel.init();

var resistance = 600;
var resetRatio = 2;
var currentSetting = 'resistance';
var prev = {x:0, y:0, z:0, vibe:0, time:0};
var racketReset = true;

var main = new UI.Card({
  title: 'Welcome to Swing Detector',
  subtitle: 'Resistance: ' + resistance,
  body: 'Changing ' + currentSetting
});
main.show();

var react = function(title, commentary) {
  Vibe.vibrate('short');

  console.log(title + ' - ' + commentary);
  main.title(title);
  main.body(commentary);

  racketReset = title.indexOf('Reset') > -1; //check the commentary contains 'Reset'
};

var wakeUpServer = function() {
  //TODO: indicate connection status in GUI
  ajax(
    {
      url: 'https://swish-swing-detector.herokuapp.com/ping',
      method: 'get'
    },
    function(data, status, request) {
      console.log(data); //Probably want to indicate connection status in GUI
    },
    function(error, status, request) {
      console.log('The ajax request failed: ' + error + ' : ' + status + ' : ' + request);
    }
  );
};
wakeUpServer();

var sendDataToServer = function(accelData) {
  console.log('Accel data: ' + JSON.stringify(accelData));

  ajax(
    {
      url: 'https://swish-swing-detector.herokuapp.com/collect',
      method: 'post',
      type: 'json',
      data: accelData,
    },
    function(data, status, request) {
      console.log(data);
    },
    function(error, status, request) {
      console.log('The ajax request failed: ' + error + ' : ' + status + ' : ' + request);
    }
  );
};

Accel.on('data', function(e) {
  sendDataToServer(e.accels);

  if(e.accel.x < prev.x - resistance && racketReset) {
    react('Shot Played', 'Change: ' + (e.accel.x - prev.x));
  } else if(e.accel.x > prev.x + (resistance / resetRatio) && !racketReset) {
    react('Racket Reset', 'Change: ' + (e.accel.x - prev.x));
    prev = e.accel;
  } else {
    prev = e.accel;
  }
});

main.on('click', 'select', function(e) {
  if(currentSetting === 'resistance') {
    currentSetting = 'reset ratio';
    main.subtitle('Reset Ratio: ' + resetRatio);
  } else {
    currentSetting = 'resistance';
    main.subtitle('Resistance: ' + resistance);
  }
  main.body('Changing ' + currentSetting);
  console.log('Current setting changed to ' + currentSetting);
});

main.on('click', 'down', function(e) {
  if(currentSetting === 'resistance') {
    resistance -= 50;
    main.subtitle('Resistance: ' + resistance);
    console.log('Reduced resistance to ' + resistance);
  } else {
    resetRatio -= 0.25;
    main.subtitle('Reset Ratio: ' + resetRatio);
    console.log('Reduced reset ratio to ' + resetRatio);
  }
});

main.on('click', 'up', function(e) {
  if(currentSetting === 'resistance') {
    resistance += 50;
    main.subtitle('Resistance: ' + resistance);
    console.log('Increased resistance to ' + resistance);
  } else {
    resetRatio += 0.25;
    main.subtitle('Reset Ratio: ' + resetRatio);
    console.log('Increased reset ratio to ' + resetRatio);
  }
});

