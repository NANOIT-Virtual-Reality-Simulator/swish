//Run at https://cloudpebble.net/ide/project/274001

var UI = require('ui');
var ajax = require('ajax');
var Accel = require('ui/accel');

var READY_TO_RECORD = 'Ready to record';
var RECORDING_ = 'Recording...';
var NO_CONNECTION = 'No connection';
var CONNECTING_ = 'Connecting...';

var status = CONNECTING_;
var selectedShot = 0;
var shots = ['FDrive', 'BDrive'];
var main = new UI.Card({
  title: 'Swish',
  subtitle: 'Swing Analysis',
  body: status
});

/*************************************
************* HELPER FNS *************
**************************************/
var setStatus = function(newStatus) {
  status = newStatus;
  main.body(status);
};

var pingServer = function() {
  setStatus(CONNECTING_);
  ajax(
    {
      url: 'https://swish-swing-detector.herokuapp.com/ping',
      method: 'get',
    },
    function(data, status, request) {
      main.subtitle(shots[selectedShot]);
      setStatus(READY_TO_RECORD);
    },
    function(error, status, request) {
      setStatus(NO_CONNECTION);
    }
  );
};

var sendDataToServer = function(accelData) {
  console.log('Sending accel data: ' + JSON.stringify(accelData));

  ajax(
    {
      url: 'https://swish-swing-detector.herokuapp.com/record',
      method: 'post',
      type: 'json',
      data: accelData,
    },
    function(data, status, request) {
      console.log(data);
    },
    function(error, status, request) {
      console.log('The ajax request failed: ' + error + ' : ' + status + ' : ' + request);
      setStatus(NO_CONNECTION);
    }
  );
};

var cycleSelectedShot = function(i) {
  selectedShot += i;
  if(selectedShot > shots.length) {
    selectedShot = 0;
  } else if(selectedShot < 0) {
    selectedShot = shots.length - 1;
  }

  main.subtitle(shots[selectedShot]);
};

/*************************************
************** START UP **************
**************************************/
Accel.init();
pingServer();
main.show();

/*************************************
*************** EVENTS ***************
**************************************/
Accel.on('data', function(e) {
  if(status == RECORDING_) sendDataToServer(e.accels);
});

main.on('click', 'select', function(e) {
  switch(status) {
    case RECORDING_:
      setStatus(READY_TO_RECORD);
      break;
    case READY_TO_RECORD:
      setStatus(RECORDING_);
      break;
    case NO_CONNECTION:
      pingServer();
      break;
  }
});

main.on('click', 'down', function(e) {
  cycleSelectedShot(-1);
});

main.on('click', 'up', function(e) {
  cycleSelectedShot(1);
});


