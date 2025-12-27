let stars = [];
let factor = 100; // controls spreading of each particle from centre
let speed_slider;
function setup() {
  createCanvas(windowWidth, windowHeight);
  speed_slider = createSlider(0,20,8,0.1);
  for(let i=0;i<500;i++){
    stars[i] = createVector(
      random(-width*factor,width*factor),
      random(-height*factor,height*factor),
      random(width)
    );
    stars[i].pz = stars[i].z;
  }
}

function draw() {
  background(0);
  translate(width/2,height/2)

  for(let star of stars){
    let x = star.x/star.z;
    let y = star.y/star.z;
    let px = star.x/star.pz;
    let py = star.y/star.pz;
    let d = map(star.z,0,width,10,1); // near -> large far is small
    fill(255,0,255); // colour
    noStroke();
    circle(x,y,d);
    stroke(250,0,250); // outline
    line(x,y,px,py);

    star.pz = star.z;
    star.z -= speed_slider.value(); // kind of controls the speed
    if(star.z < 10){
      star.z = width;
      star.pz = width;
    }
  }
  
}
