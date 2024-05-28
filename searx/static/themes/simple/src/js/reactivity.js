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

// Watch for new #filters-btn & #infobox-more-btn elements and add event listener
const observer = new MutationObserver((mutationsList) => {
  for (const mutation of mutationsList) {
    if (mutation.type === 'childList') {
      mutation.addedNodes.forEach((node) => {
        if (node.nodeType === Node.ELEMENT_NODE) {
          if (node.id === 'filters-btn') {
            node.onclick = function() {
              toggleBtn(this, 'filters-visible', '.search_filters', 'invisible');
            };
          } else if (node.id ==='infobox-more-btn') {
            const {parentNode} = node;
            if (parentNode && parentNode.classList && parentNode.classList.contains('infobox')) {
              node.onclick = function() {
                parentNode.classList.toggle("collapse-open");
              };
            }
          }
          const filtersBtnDescendants = node.querySelectorAll && node.querySelectorAll('#filters-btn');
          if (filtersBtnDescendants && filtersBtnDescendants.forEach) {
            filtersBtnDescendants.forEach((descendant) => {
              descendant.onclick = function() {
                toggleBtn(this, 'filters-visible', '.search_filters', 'invisible');
              };
            });
          }
        }
      });
    }
  }
});
observer.observe(document.body, { childList: true, subtree: true });