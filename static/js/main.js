(function () {
  var root = document.documentElement;

  var toggle = document.getElementById("theme-toggle");
  if (toggle) toggle.addEventListener("click", function () {
    var next = root.dataset.theme === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    try { localStorage.setItem("theme", next); } catch (e) {}
  });

  var input = document.getElementById("search-input");
  var box = document.getElementById("search-results");
  if (input && box) {
    var timer;
    var hide = function () { box.hidden = true; box.textContent = ""; };
    input.addEventListener("input", function () {
      clearTimeout(timer);
      var q = input.value.trim();
      if (!q) return hide();
      timer = setTimeout(function () {
        fetch(input.dataset.url + "?q=" + encodeURIComponent(q))
          .then(function (r) { return r.json(); })
          .then(function (d) {
            box.textContent = "";
            if (!d.results.length) {
              var p = document.createElement("p");
              p.textContent = "No matches. Press Enter to search again.";
              box.appendChild(p);
            }
            d.results.forEach(function (x) {
              var a = document.createElement("a");
              a.href = x.url;
              a.textContent = x.title;
              box.appendChild(a);
            });
            box.hidden = false;
          })
          .catch(hide);
      }, 200);
    });
    input.addEventListener("keydown", function (e) { if (e.key === "Escape") hide(); });
    document.addEventListener("click", function (e) { if (!e.target.closest(".search")) hide(); });
  }

  var copy = document.getElementById("copy-link");
  if (copy) copy.addEventListener("click", function () {
    navigator.clipboard.writeText(copy.dataset.url).then(function () {
      var old = copy.textContent;
      copy.textContent = "Copied";
      setTimeout(function () { copy.textContent = old; }, 1500);
    });
  });
})();
