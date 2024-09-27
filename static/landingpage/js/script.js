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

  // Project gallery
  $('.project-card').each(function() {
    var $card = $(this);
    var $gallery = $card.find('.project-gallery');
    var $images = $gallery.find('.project-image');
    var $prevBtn = $gallery.find('.gallery-nav.prev');
    var $nextBtn = $gallery.find('.gallery-nav.next');
    var $closeBtn = $gallery.find('.gallery-close');
    var currentIndex = 0;

    function showImage(index) {
      $images.removeClass('active').eq(index).addClass('active');
    }

    function nextImage() {
      currentIndex = (currentIndex + 1) % $images.length;
      showImage(currentIndex);
    }

    function prevImage() {
      currentIndex = (currentIndex - 1 + $images.length) % $images.length;
      showImage(currentIndex);
    }

    function openGallery() {
      $gallery.css('display', 'flex');
      showImage(0);
      $('body').css('overflow', 'hidden'); // Prevent page scrolling
    }

    function closeGallery() {
      $gallery.hide();
      currentIndex = 0; // Reset index
      $('body').css('overflow', ''); // Restore page scrolling
      $images.removeClass('active'); // Remove 'active' class from all images
    }

    $card.on('click', function(e) {
      if (!$(e.target).closest('.project-gallery').length) {
        openGallery();
      }
    });

    $closeBtn.on('click', function(e) {
      e.stopPropagation();
      closeGallery();
    });

    $gallery.on('click', function(e) {
      if (e.target === this) {
        closeGallery();
      }
    });

    $nextBtn.on('click', function(e) {
      e.stopPropagation();
      nextImage();
    });

    $prevBtn.on('click', function(e) {
      e.stopPropagation();
      prevImage();
    });

    $(document).keydown(function(e) {
      if ($gallery.is(':visible')) {
        if (e.which === 37) {
          prevImage();
        } else if (e.which === 39) {
          nextImage();
        } else if (e.which === 27) {
          closeGallery();
        }
      }
    });
  });
});