let lift_width = 80; // width of lift
let lift_height = 100; // height of lift
let lift_x,lift_y; // coordinates of lift
let ay_lift; // acceleration on lift
let vy_lift = 0; // velocity of the lift

let ball_x,ball_y; // coordinates of ball
let ball_d = 15; // diamter of ball inside
let ay_ball; // accelearation on ball
let vy_ball = 0; // velocity of the ball

let g = 0.15; // gravity (makes the lift fall slow or)
let e_ball = 0.9; // elasticity of the ball depends inversely on weight
let mass_lift = 100; // Heavy!
let mass_ball = 1;   // Light!
let drag_coeff = 0.05; // 'k' - How thick the air is

let falling = false;
let impact = false;
let startBtn;

function startFall(){
    falling = true;
    impact = false;

    lift_y = height*0.1; // initialise back to top
    vy_lift = 0;

    ball_x = lift_x;
    ball_y = lift_y + lift_height - ball_d / 2; // put ball to floor of lift
    vy_ball = 0;
}

function setup(){
    createCanvas(windowWidth*0.9,windowHeight*0.9);
    
    // creating a button to start free fall
    startBtn = createButton("Start Free-Fall");
    startBtn.mousePressed(startFall);
    startBtn.position(10,10);

    // initiating the coordinates
    lift_x = width/2-lift_width/2; // centre of screen no matetr what
    lift_y = height*0.1; // 10% top of screen
    ball_x = lift_x;    
    ball_y = lift_y + lift_height - ball_d / 2;
}

function draw(){
    background(255,255,20);

    // simulate a free falling rectangle (lift)
    if(falling){
        if (impact) {
            // If lift hit ground 
            ay_lift = 0; // lift no acceleration
            ay_ball = g; // ball normal acceleration without dragg 
        } else {
        // If falling, calculate the drag physics
        // Drag Force = k * v^2
            let dragForceLift = drag_coeff * (vy_lift * vy_lift);
            let dragForceBall = drag_coeff * (vy_ball * vy_ball);

            ay_lift = g - (dragForceLift / mass_lift);
            ay_ball = g - (dragForceBall / mass_ball);
        }

        // lift free fall and displacement
        vy_lift += ay_lift; // diff values of air resistance
        lift_y += vy_lift;

        // ball free fall and displaceent
        vy_ball += ay_ball; // more affected by air resistance
        ball_y += vy_ball;
 
        // lift boundaries - ceiling and floor
        let lift_floor = lift_y + lift_height - ball_d/2;
        let lift_ceiling = lift_y + ball_d/2;

        // when ball gets pushed to ceiling and moves as fast as lift
        if(!impact && ball_y<=lift_ceiling){
            ball_y = lift_ceiling;
            vy_ball = vy_lift;
        }

        // lift hit ground        
        if(lift_y>height-(lift_height)){
            lift_y = height-(lift_height);
            vy_lift = 0;
            impact = true;
        }


        // ball bouncing after impact
        if(impact){
            if(ball_y > lift_floor){
                ball_y = lift_floor;
                vy_ball = -vy_ball * e_ball;
            }
            if(ball_y < lift_ceiling){
                ball_y = lift_ceiling;
                vy_ball = -vy_ball * e_ball;
            }
        }
    }

    fill(255);
    rect(lift_x,lift_y,lift_width,lift_height);
    fill(0);
    circle(ball_x+(lift_width/2),ball_y,ball_d);
}
