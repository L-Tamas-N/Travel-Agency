$(document).ready(function(){
    $('.hotel-carousel').slick({
        infinite: false,  // Prevents looping issues
        slidesToShow: 3,  // Always show exactly 3 slides
        slidesToScroll: 1,  // Move 1 slide at a time
        prevArrow: '<button type="button" class="slick-prev">Previous</button>',
        nextArrow: '<button type="button" class="slick-next">Next</button>',
        adaptiveHeight: false, 
        centerMode: false,  
        responsive: [
            {
                breakpoint: 1024,
                settings: { slidesToShow: 2, slidesToScroll: 1 }
            },
            {
                breakpoint: 768,
                settings: { slidesToShow: 1, slidesToScroll: 1 }
            }
        ]
    });
});