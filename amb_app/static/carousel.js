// https://codepen.io/rkrc/pen/LEgKww

var slideSpeed = 5000;

var main = function(){
    //Carousel
   setInterval(function() {timedDelay()}, slideSpeed);
};

//timedDelay function
function timedDelay() {

    var currentSlide = $('.active-slide');
	var nextTimedSlide = currentSlide.next();
	
    if(nextTimedSlide.length === 0 ) {
		nextTimedSlide = $('.slide').first();
	}
   
	currentSlide.fadeOut(600, function() {
		$(this).removeClass('active-slide');
	    nextTimedSlide.fadeIn(600).addClass('active-slide');
	});
}

$(document).ready(main);