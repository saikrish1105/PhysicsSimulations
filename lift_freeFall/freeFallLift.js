let lift_width = 80; // width of lift
let lift_height = 100; // height of lift
let lift_x,lift_y; // coordinates of lift
let vy_lift = 0; // velocity of the lift

let ball_x,ball_y; // coordinates of ball
let ball_d = 15; // diamter of ball inside
let vy_ball = 0; // velocity of the ball

let g = 0.98; // gravity (makes the lift fall slow or)
let e_ball = 0.9; // elasticity of the ball

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
        // lift free fall and displacement
        vy_lift += g;
        lift_y += vy_lift;

        // ball free fall and displaceent
        vy_ball += g;
        ball_y += vy_ball;

        // lift boundaries - ceiling and floor
        let lift_floor = lift_y + lift_height - ball_d/2;
        let lift_ceiling = lift_y + ball_d/2;

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
