'use strict';
var stage = new createjs.Stage('canvas');
var shape = new createjs.Shape();
var shadow = new createjs.Shadow('black', 0, 0, 10);
var RAD_0 = - Math.PI / 2,
    ARC_PERCENT = Math.PI * 2 / 100,
    FPS = 60,
    FRAME_COUNT = 0;
shape.shadow = shadow;
stage.addChild(shape);

createjs.Ticker.timingMode = createjs.Ticker.RAF;
createjs.Ticker.framerate = FPS;
createjs.Ticker.addEventListener('tick', tick);
function tick(evt) {
    if (FRAME_COUNT >= FPS / 2) {
        FRAME_COUNT = 0;
        // fetch and redraw volume bar
        fetch('http://127.0.0.1:2016/volume').then(function(response){
            return response.json().then(function(json){
                shape.graphics.clear();
                shape.graphics.setStrokeStyle(5).beginStroke('black').arc(
                    100, 100, 90, RAD_0, RAD_0 + ARC_PERCENT * json.value
                );
            });
        });
    }else{
        FRAME_COUNT = FRAME_COUNT + 1;
    }
    stage.update(evt);
}
