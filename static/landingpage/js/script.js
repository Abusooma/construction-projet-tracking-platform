$(document).ready(function () {
  // Smooth scroll for anchor links
  $('a[href*="#"]').on("click", function (e) {
    e.preventDefault();
    $("html, body").animate(
      {
        scrollTop: $($(this).attr("href")).offset().top,
      },
      500,
      "linear"
    );
  });

  // Animation on scroll
  $(window).scroll(function () {
    $(".animated-img").each(function () {
      var imagePos = $(this).offset().top;
      var windowHeight = $(window).height();
      var topOfWindow = $(window).scrollTop();
      if (imagePos < topOfWindow + windowHeight - 100) {
        $(this).addClass("fadeIn");
      }
    });

    $(".animated-box").each(function () {
      var boxPos = $(this).offset().top;
      var windowHeight = $(window).height();
      var topOfWindow = $(window).scrollTop();
      if (boxPos < topOfWindow + windowHeight - 100) {
        $(this).addClass("slideIn");
      }
    });
  });

  // Project slider
  $(".project-slider").each(function () {
    var $slider = $(this);
    var $images = $slider.find(".project-image");
    var currentIndex = 0;

    function showImage(index) {
      $images.removeClass("active").eq(index).addClass("active");
    }

    function nextImage() {
      currentIndex = (currentIndex + 1) % $images.length;
      showImage(currentIndex);
    }

    setInterval(nextImage, 3000); // Change image every 3 seconds
  });
});
