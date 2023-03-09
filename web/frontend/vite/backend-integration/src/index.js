import mug from './mug.png';

window.onload = () => {
  const image = document.getElementById('image');
  const src = document.getElementById('src');

  image.src = mug;
  src.innerText = mug;
};
