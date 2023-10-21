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
    fadeOut(document.getElementById(`slide-${currentIndex}`));
    let activeSlide = document.getElementById(`slide-${index}`);
    removePreviousIndicator(index);
    updateIndicators(index);
    fadeOut(activeSlide);
    activeSlide.style.opacity = '0';

    activeSlide = document.getElementById(`slide-${index}`);

    if (index == 2 && !visitedBefore) {
        activeSlide.scrollIntoView({
            behavior: 'instant',
            block: 'center',
            inline: 'center'
        });

        onSlideLoad();
    } else {

        activeSlide.scrollIntoView({
            behavior: 'auto',
            block: 'center',
            inline: 'center'
        });

    }
    currentIndex = index;
    fadeIn(activeSlide);
}