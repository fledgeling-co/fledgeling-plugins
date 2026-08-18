// trips: live-region-created-with-text (warn)
function announce(msg) {
  const host = document.querySelector('#form');
  host.insertAdjacentHTML('beforeend', `<p role="status">${msg}</p>`);
}
