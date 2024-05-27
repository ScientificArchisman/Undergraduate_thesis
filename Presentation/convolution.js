// Define input signal and kernel
var input = [1, 2, 3, 4, 5, 6, 7, 8];
var kernel = [0.5, 0.5];

// Create canvas and get context
var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");

// Draw input signal
ctx.beginPath();
ctx.moveTo(50, 50);
for (var i = 0; i < input.length; i++) {
	ctx.lineTo(50 + i * 50, 50 + input[i] * 20);
}
ctx.stroke();

// Draw kernel
ctx.beginPath();
ctx.moveTo(300, 100);
ctx.lineTo(350, 100);
ctx.lineTo(350, 150);
ctx.lineTo(300, 150);
ctx.closePath();
ctx.stroke();
ctx.fillText(kernel[0], 305, 115);
ctx.fillText(kernel[1], 330, 115);

// Perform convolution
var output = [];
for (var i = 0; i < input.length - kernel.length + 1; i++) {
	var sum = 0;
	for (var j = 0; j < kernel.length; j++) {
		sum += input[i + j] * kernel[j];
	}
	output.push(sum);
}

// Draw output signal
var delay = 500;
var index = 0;
function drawOutputSignal() {
	setTimeout(function() {
		ctx.beginPath();
		ctx.moveTo(450, 50);
		for (var i = 0; i < output.length; i++) {
			if (i < index) {
				ctx.lineTo(450 + i * 50, 50 + output[i] * 20);
			} else {
				ctx.lineTo(450 + i * 50, 50);
			}
		}
		ctx.stroke();
		index++;
		if (index <= output.length) {
			drawOutputSignal();
		}
	}, delay);
}

drawOutputSignal();
