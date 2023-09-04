function $(selector) {
    return document.querySelector(selector);
}

function toggleBtn(thisEl, activeClass, targetSelector, targetClass) {
    if (activeClass) {
        thisEl.classList.toggle(activeClass);
    }
    $(targetSelector).classList.toggle(targetClass);
}

function addBtn(thisEl, activeClass, targetSelector, targetClass) {
    if (activeClass) {
        thisEl.classList.add(activeClass);
    }
    $(targetSelector).classList.add(targetClass);
}

function removeBtn(thisEl, activeClass, targetSelector, targetClass) {
    if (activeClass) {
        thisEl.classList.remove(activeClass);
    }
    $(targetSelector).classList.remove(targetClass);
}

function resultsPreview(target) {
    $(target).classList.add("collapse-open");
    $(target).addEventListener("click", () => {
        $("#checkbox_images").checked = true;
    });
}
