let lift_width = 80;
let lift_height = 100;
let x,y;

function setup(){
    createCanvas(windowWidth,windowHeight);
    x = width/2-lift_width/2;
    y = height*0.1;
}

function draw(){
    background(255,255,20);

    // simulate a free falling rectangle ( lift )
    y += height*0.01;
    if(y>height-(lift_height)){
        y = height-(lift_height);
    }

    fill(255);
    
    rect(x,y,lift_width,lift_height);

    
}
