/* Laboratório: mostra o conteúdo dos arquivos de exemplo dentro da página.
   Nada aqui envia dados para lugar nenhum: só lê arquivos estáticos do próprio site. */
(function () {
  var lang = (document.documentElement.lang || '').slice(0, 2);
  var abra = lang === 'en' ? 'Open the file directly: ' : lang === 'es' ? 'Abra el archivo directamente: ' : 'Abra o arquivo direto: ';
  document.querySelectorAll('pre[data-arquivo]').forEach(function (pre) {
    var url = pre.getAttribute('data-arquivo');
    fetch(url).then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
      .then(function (t) { pre.textContent = t; })
      .catch(function () { pre.textContent = abra + url; });
  });
})();
