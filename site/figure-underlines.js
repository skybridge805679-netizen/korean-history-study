/* Keep the source image intact; align underline marks with its rendered bounds. */
(() => {
  window.underlinedFigureImage = (key, src, imageHtml) => {
    const marks = window.QUESTION_UNDERLINES?.[key];
    if (!marks || marks.src !== src) return imageHtml;
    const lines = marks.lines.map(line => `<line x1="${line.x1}" x2="${line.x2}" y1="${line.y}" y2="${line.y}" stroke-width="${line.strokeWidth}"/>`).join('');
    return `<span class="figure-underline-frame" data-underline-key="${key}">${imageHtml}<svg class="figure-underline-layer" viewBox="0 0 ${marks.width} ${marks.height}" preserveAspectRatio="none" aria-hidden="true" focusable="false">${lines}</svg></span>`;
  };

  const watched = new Map();
  function align(frame) {
    const image = frame.querySelector('img');
    const layer = frame.querySelector('.figure-underline-layer');
    const bounds = image.getBoundingClientRect();
    const parent = frame.getBoundingClientRect();
    Object.assign(layer.style, {
      left: `${bounds.left - parent.left}px`, top: `${bounds.top - parent.top}px`,
      width: `${bounds.width}px`, height: `${bounds.height}px`
    });
  }
  function scan() {
    for (const [frame, observer] of watched) {
      if (!frame.isConnected) { observer.disconnect(); watched.delete(frame); }
    }
    document.querySelectorAll('.figure-underline-frame').forEach(frame => {
      if (watched.has(frame)) return;
      const image = frame.querySelector('img');
      const observer = new ResizeObserver(() => align(frame));
      observer.observe(image);
      image.addEventListener('load', () => align(frame), {once: true});
      watched.set(frame, observer);
      align(frame);
    });
  }
  new MutationObserver(scan).observe(document.body, {childList: true, subtree: true});
  scan();
})();
