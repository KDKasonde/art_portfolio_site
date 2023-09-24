function fadeIn(slide) {
    let id = null;
    let transformation = 0;
    id = setInterval(function (event){
        easeTextIn(event);
    }, 15)

    function easeTextIn() {
        if (transformation > 1){
            slide.style.opacity = `1`
            clearInterval(id)
        } else {
            transformation += 0.01;
            slide.style.opacity = `${transformation}`
        }
    }
}

function fadeOut(slide) {
    slide.style.opacity = `0`
}

function changeSlide(index) {
    let activeSlide = document.getElementById(`slide-${index+1}`);
    removePreviousIndicator(index);
    updateIndicators(index);
    fadeOut(activeSlide);
    activeSlide.style.opacity = 0;

    activeSlide = document.getElementById(`slide-${index+1}`);

    if (index+1 == 2 && !visitedBefore) {
        activeSlide.scrollIntoView({
            behavior: 'instant',
            block: 'center',
            inline: 'center'
        });

        onSlideLoad();
    } else {

        activeSlide.scrollIntoView({
            behavior: 'smooth',
            block: 'center',
            inline: 'center'
        });

    }
    currentIndex = index;
    fadeIn(activeSlide);
}