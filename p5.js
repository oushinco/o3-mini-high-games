let balls = [];
const numBalls = 100;
const containerRadius = 300;
let rotationAngle = 0;

function setup() {
  createCanvas(windowWidth, windowHeight, WEBGL);
  // Create 100 balls with random positions, velocities, and colors.
  for (let i = 0; i < numBalls; i++) {
    balls.push(new Ball());
  }
}

function draw() {
  // Clear the background each frame.
  background(0);

  // Slowly rotate the entire scene.
  rotationAngle += 0.005;
  rotateY(rotationAngle);
  rotateX(rotationAngle * 0.3);

  // Draw the container sphere in wireframe style.
  noFill();
  stroke(255, 150);
  strokeWeight(1);
  sphere(containerRadius);

  // Update and display each ball.
  for (let b of balls) {
    b.update();
    b.display();
  }
}

class Ball {
  constructor() {
    // Give each ball a radius between 5 and 10.
    this.r = random(5, 10);

    // Pick a random position inside the container sphere,
    // making sure the ball is fully inside.
    let pos = p5.Vector.random3D();
    pos.mult(random(0, containerRadius - this.r));
    this.pos = pos;

    // Give the ball a random velocity.
    this.vel = p5.Vector.random3D();
    this.vel.mult(random(1, 3));

    // Choose a random, bright color.
    this.c = color(random(50, 255), random(50, 255), random(50, 255));

    // Initialize the trail (an array of previous positions).
    this.trail = [];
    this.maxTrail = 20;
  }

  update() {
    // Add a copy of the current position to the trail.
    this.trail.push(this.pos.copy());
    if (this.trail.length > this.maxTrail) {
      this.trail.shift();
    }

    // Update the position.
    this.pos.add(this.vel);

    // Check for collision with the container sphere.
    // If the distance from the origin plus the ball’s radius exceeds the container radius,
    // we reflect the ball’s velocity off the inner surface.
    let d = this.pos.mag();
    if (d + this.r > containerRadius) {
      // Get the normal (a unit vector pointing from the center to the ball).
      let normal = this.pos.copy().normalize();
      // Reposition the ball exactly at the inner surface.
      this.pos = normal.copy().mult(containerRadius - this.r);
      // Reflect the velocity: v = v - 2*(v · n)*n
      let dot = this.vel.dot(normal);
      let reflection = normal.copy().mult(2 * dot);
      this.vel.sub(reflection);
    }
  }

  display() {
    // Draw the trail as a series of line segments with fading opacity.
    noFill();
    for (let i = 0; i < this.trail.length - 1; i++) {
      let a = this.trail[i];
      let b = this.trail[i + 1];
      // Map the alpha from nearly transparent (old positions) to fully opaque (recent ones).
      let alphaVal = map(i, 0, this.trail.length - 1, 0, 255);
      stroke(red(this.c), green(this.c), blue(this.c), alphaVal);
      line(a.x, a.y, a.z, b.x, b.y, b.z);
    }

    // Draw the ball itself.
    push();
    translate(this.pos.x, this.pos.y, this.pos.z);
    noStroke();
    fill(this.c);
    sphere(this.r);
    pop();
  }
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}
