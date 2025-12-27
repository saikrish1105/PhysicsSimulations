let x,y; // x and y coordinates of the 
let vy = 0; // the initial velocity
let e = 0.8; // coefficient of restitution
let g = 0.98; // acceleration due to gravity
let falling = false; // to simulate at button click
let startBtn;

function setup(){
    createCanvas(500,500);
    // create slider to get input of ball
    x = width/2;
    y = 50;

    // start button
    startBtn = createButton("Start Free-Fall");
    startBtn.mousePressed(startFall);

    // reset button
    resetBtn = createButton("Reset");
    startBtn.mousePressed(reset);
}

function startFall(){
    falling = true;
}
function reset(){
    falling = false;
    y = 50;
    vy = 0;
}
function draw(){
    // remember the canvas start (0,0) from top left (x,y)
    background(0);
    let d = 15;
    if(falling){
        vy += g; // accelerate velocity based on gravity
        y += vy; // change position based on velocity
        // x -= 1; changing this x can add a factor of windw moves it left/right
        
        if(y>height-d/2){ // when it reaches the ground
            y = height-d/2; // so it doesnt fall below the canvas  -
            vy = -vy*e; // makes velocity go up once it comes down
        }
    }

    fill(255,255,0); // everything below this line gets this colour
    circle(x,y,d); // create circle at point x,y, with radius d
}
