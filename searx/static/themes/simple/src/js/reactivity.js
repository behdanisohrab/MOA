function $ (selector) {
  return document.querySelector(selector);
}

function $$ (selector) {
  return document.querySelectorAll(selector);
}

function toggleBtn (thisEl, activeClass, targetSelector, targetClass) {
  if (activeClass) {
    thisEl.classList.toggle(activeClass);
  }
  $(targetSelector).classList.toggle(targetClass);
}

function addBtn (thisEl, activeClass, targetSelector, targetClass) {
  if (activeClass) {
    thisEl.classList.add(activeClass);
  }
  $(targetSelector).classList.add(targetClass);
}

function removeBtn (thisEl, activeClass, targetSelector, targetClass) {
  if (activeClass) {
    thisEl.classList.remove(activeClass);
  }
  $(targetSelector).classList.remove(targetClass);
}

function imagesPreview() {
  $(".preview-images").classList.add("collapse-open");
  $(".media-more-btn").addEventListener("click", () => {
    $("#checkbox_images").checked = true;
  });
  $(".media-more-btn").onclick = null;
}

function videosPreview() {
  $("#checkbox_videos").checked = true;
}

function infoboxMore() {
  $$(".infobox").forEach((infobox) => {
    const moreBtn = infobox.querySelector(".infobox-more-btn")
    if (moreBtn) {
      moreBtn.addEventListener("click", () => {
        infobox.classList.toggle("collapse-open");
      })
    }
  })
}