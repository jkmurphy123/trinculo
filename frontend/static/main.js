const form = document.getElementById('form');
const out = document.getElementById('out');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const fd = new FormData(form);
  const files = form.querySelector('input[name="files"]').files;
  if (files.length === 0 || files.length > 4) {
    out.textContent = "Please select 1–4 images.";
    return;
  }
  for (let i = 0; i < files.length; i++) fd.append('files', files[i]);

  const res = await fetch('/api/submit', { method: 'POST', body: fd });
  const json = await res.json();
  out.textContent = JSON.stringify(json, null, 2);
});
