function trigger(event) {
    const leftBtn = document.getElementById('left-slider-btn');
    // function to determine which side of the screen the mouse is and
    // highlight a scroll button for users who do not have a touchpad
    const rightBtn = document.getElementById('right-slider-btn');
    const mouseX = event.clientX;
    const centerOfSlider = (slider_rect.right + slider_rect.left) / 2;

    if ((mouseX <= centerOfSlider)) {
        if (!leftBtn.disabled) {
            leftBtn.focus();
            setTimeout(() => {
                leftBtn.blur();
            }, 1000);
        } else {
            rightBtn.focus();
            setTimeout(() => {
                rightBtn.blur();
            }, 1000);
        }

    } else {
        if (!rightBtn.disabled) {
            rightBtn.focus();
            setTimeout(() => {
                rightBtn.blur();
            }, 1000);
        } else {
            leftBtn.focus();
            setTimeout(() => {
                leftBtn.blur();
            }, 1000);
        }
    }
}

function disableSliderBtn() {
    // disables slider buttons when they
    // is nothing to scroll to
    const centerImageId = getCenterImage();
    if (`${centerImageId}` == 0){
        document.getElementById('left-slider-btn').disabled = true;
    } else {
        document.getElementById('left-slider-btn').removeAttribute("disabled");
    }

    if (`${centerImageId}` == (imagesList.length-1)){
        document.getElementById('right-slider-btn').disabled = true;
    } else {
        document.getElementById('right-slider-btn').removeAttribute("disabled");
    }
}

function slideLeft() {
    // Slide image slider left
    const centerImageId = getCenterImage();
    const targetImage = document.getElementById(`${centerImageId-1}`);
    targetImage.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
        inline: 'center'
    });

    disableSliderBtn();
}

function slideRight() {
    // Slide image slider right
    const centerImageId = parseInt(getCenterImage());
    const targetImage = document.getElementById(`${centerImageId+1}`);
    targetImage.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
        inline: 'center'
    });

    disableSliderBtn();
}

function arrowSlider(event) {
    // arrow key slider
    const centerImageId = parseInt(getCenterImage());

    if ((event.which == 37) && (`${centerImageId}` !=0)){
        /*left key code*/
        slideLeft()
    }
    if ((event.which == 39) && (`${centerImageId}` != (imagesList.length-1))){
        /*right key code*/
        slideRight();
    }

}


function Onload(imageList) {
    resizeSlider()
    imagesList.forEach(image => {
        image.addEventListener("click", function(event) {
            openImage(event);
            event.stopPropagation();
        });
    });
    leftSliderBtn.addEventListener("click", slideLeft);
    rightSliderBtn.addEventListener("click", slideRight);
    document.addEventListener('keydown', arrowSlider);
    disableSliderBtn();
}

function checkImages(imageList){
    // Function that takes the list of images being shown
    // and uses the window to distinguish which ones are in view
    let in_view = [];
    imagesList.forEach(image => {
        const rect = image.getBoundingClientRect();
        if((rect.right > slider_rect.left) && (rect.left < slider_rect.right)){
            in_view.push(image)
        } else{
            image.setAttribute("style", "scale: 0.01;")
        }
    });
    return in_view;
}

function getCenterImage(imageList) {
    // function that returns the center image given
    // a list of images on screen
    const in_view = checkImages(imageList);
    let max = 0;
    let id;
    in_view.forEach(image => {
        if (image.style.scale > max){
            max = image.style.scale;
            id = image.id;
        }
    })
    return id;
}

function scaleImages(imageList){
    // function that scales images as they are scrolled through
    // making them smaller if they move to the left or to the
    // right
    const in_view = checkImages(imageList);
    const center = (slider_rect.right + slider_rect.left)/2;
    in_view.forEach(image => {
        const rect = image.getBoundingClientRect();
        if(((rect.right + rect.left)/2) > center){
            image.style.scale = `${1 - (( rect.right -((rect.right-rect.left)/2) - center)/(center))}`;
        } else if(((rect.right + rect.left)/2) < center){
            image.style.scale = `${((rect.right - ((rect.right-rect.left)/2))/(center))}`;
        }
    });

    requestAnimationFrame(scaleImages)
}
