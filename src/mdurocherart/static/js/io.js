async function makePostRequest(url, payload){
    let response = await fetch(
        url = url,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload)
        }
    )

    if (response.ok && response.status === 200){
        return response
    }
    throw(
        new Error(`There was an issue loading the request, ${response.statusText} exited with code: ${response.status}`)
    )
}


async function makeGetRequest(url, payload){
    let response = await fetch(
        url = url,
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        }
    )

    if (response.ok && response.status === 200){
        return response
    }
    throw(
        new Error(`There was an issue loading the request, ${response.statusText} exited with code: ${response.status}`)
    )
}


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