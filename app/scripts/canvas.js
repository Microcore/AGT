'use strict';
var stage = new createjs.Stage('canvas');
var shape = new createjs.Shape();
var shadow = new createjs.Shadow('black', 0, 0, 10);
var RAD_0 = - Math.PI / 2,
    ARC_PERCENT = Math.PI * 2 / 100,
    FRAMEDURATION_60 = 1000 / 60,
    FRAMEDURATION_30 = 1000 / 30,
    FRAME_COUNT = 0;
stage.addChild(shape);

createjs.Ticker.timingMode = createjs.Ticker.RAF;
createjs.Ticker.addEventListener('tick', tick);

function tick(evt) {
    shape.graphics.clear();
    shape.graphics.setStrokeStyle(5).beginStroke('black').arc(
        100, 100, 90, RAD_0, RAD_0 + ARC_PERCENT * FRAME_COUNT
    );
    shape.shadow = shadow;
    FRAME_COUNT = FRAME_COUNT + 1;
    if(FRAME_COUNT > 100){
        FRAME_COUNT = 0;
    }
    stage.update(evt);
}
