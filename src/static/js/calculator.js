
function CalculateSlab(){
	var width = document.getElementById('slab-width').valueAsNumber;
	var length = document.getElementById('slab-length').valueAsNumber;
	var thickness = document.getElementById('slab-thickness').valueAsNumber;
	var quantity = document.getElementById('slab-quantity').valueAsNumber;
	thickness /= 12;

	var cubic_yards = (((thickness * width * length) / 27) * quantity).toFixed(2);
	var bags_80 = (((thickness * width * length) / .6) * quantity).toFixed(2);
	var bags_60 = (((thickness * width * length) / .45) * quantity).toFixed(2);

	document.getElementById("slab-cubic-yards").innerText = (" " + cubic_yards);
	document.getElementById("slab-80lb").innerText = (" " + bags_80);
	document.getElementById("slab-60lb").innerText = (" " + bags_60);
};

function CalculateRound(){
	var diameter = document.getElementById('round-diameter').valueAsNumber;
	var depth = document.getElementById('round-depth').valueAsNumber;
	var quantity = document.getElementById('round-quantity').valueAsNumber;
	var area = 3.14159265359 * Math.pow(((diameter / 12) / 2), 2);
	depth /= 12;

	var cubic_yards = ((area * depth * quantity) /27).toFixed(2);
	var bags_80 = ((area * depth * quantity) /.6).toFixed(2);
	var bags_60 = ((area * depth * quantity) /.45).toFixed(2);

	document.getElementById("round-cubic-yards").innerText = (" " + cubic_yards);
	document.getElementById("round-80lb").innerText = (" " + bags_80);
	document.getElementById("round-60lb").innerText = (" " + bags_60);
};

function CalculateTriangle(){
	var sideA = document.getElementById('triangle-sideA').valueAsNumber;
	var sideB = document.getElementById('triangle-sideB').valueAsNumber;
	var sideC = document.getElementById('triangle-sideC').valueAsNumber;
	var thickness = document.getElementById('triangle-thickness').valueAsNumber;
	thickness /= 12;
	var perimeter = (sideA + sideB + sideC) / 2;
	var area = Math.sqrt(perimeter * (perimeter - sideA) * (perimeter - sideB) * (perimeter - sideC));


	var cubic_yards = ((area * thickness) / 27).toFixed(2)
	var bags_80 = ((area * thickness) / .6).toFixed(2)
	var bags_60 = ((area * thickness) / .45).toFixed(2)

	document.getElementById("triangle-cubic-yards").innerText = (" " + cubic_yards);
	document.getElementById("triangle-80lb").innerText = (" " + bags_80);
	document.getElementById("triangle-60lb").innerText = (" " + bags_60);
};


document.getElementById("slab-calculate").addEventListener('click', CalculateSlab);
document.getElementById("round-calculate").addEventListener('click', CalculateRound);
document.getElementById("triangle-calculate").addEventListener('click', CalculateTriangle);
