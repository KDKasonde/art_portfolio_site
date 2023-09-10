function checkImages(imageList){
    // Function that takes the list of images being shown
    // and uses the window to distinguish which ones are in view
    let in_view = [];
    imagesList.forEach(image => {
        const rect = image.getBoundingClientRect();
        if((rect.right > slider_rect.left) && (rect.left < slider_rect.right)){
            in_view.push(image)
        } else{
            image.setAttribute("style", "scale: 0;")
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
