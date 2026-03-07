let stars = [];

function setup() {
    let canvas = createCanvas(windowWidth, windowHeight);

    // Make canvas behave like a background layer
    canvas.position(0, 0);
    canvas.style("position", "fixed");
    canvas.style("z-index", "-1");
    canvas.style("pointer-events", "none");

    noStroke();
}

function draw() {
    // Black background with slight fade for trail effect
    fill(0, 40);
    rect(0, 0, width, height);

    // Randomly spawn shooting stars
    if (random(1) < 0.08) {
        stars.push(new Star());
    }

    // Update and draw stars
    for (let i = stars.length - 1; i >= 0; i--) {
        stars[i].update();
        stars[i].show();

        if (stars[i].offscreen()) {
            stars.splice(i, 1);
        }
    }
}

class Star {
    constructor() {
        this.x = random(width);
        this.y = random(height);

        // Random velocity (shooting speed)
        this.speed = random(3, 12);

        // Random star size
        this.size = random(2, 4);

        // Random color between red, pink, and purple
        let colors = [
            color(255, 50, 80),   // red-pink
            color(255, 90, 160),  // pink
            color(160, 70, 255)   // purple
        ];

        this.col = random(colors);
    }

    update() {
        this.x += this.speed;
    }

    show() {
        fill(this.col);
        ellipse(this.x, this.y, this.size, this.size);
    }

    offscreen() {
        return this.x > width + 50;
    }
}

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}