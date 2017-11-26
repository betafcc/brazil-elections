export const cycle = function* (arr) {
  let i = 0;

  while (true) {
    yield arr[i];
    i = (i + 1 + arr.length) % arr.length;
  }
};


export const toFront = (el) =>
  el
    .parentElement
    .appendChild(el);


export const toBack = (el) =>
  el
    .prependChild(el.parentElement, el);


export const getQuery = () =>
  window
    .location
    .search
    .slice(1)
    .split('&')
    .map(e => e.split('=').map(decodeURIComponent))
    .reduce((acc, [k, v]) =>
      (acc[k] = v, acc)
    , {});


export const setQuery = query => {
  if (window.history.pushState) {
    const queryString = Object
      .entries(query)
      .map(e => e.map(encodeURIComponent).join('='))
      .join('&');

    const newurl =
      window.location.protocol +
      "//" +
      window.location.host +
      window.location.pathname +
      '?' +
      queryString;

    window.history.pushState({path:newurl},'',newurl);
  }
}
