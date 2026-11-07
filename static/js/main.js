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
    var thought = document.getElementById("thought");
  if (thought) {
    var menu = document.getElementById("dl-menu");
    var dlToggle = document.getElementById("dl-toggle");
    var body = thought.querySelector(".prose");
    var stamp = thought.querySelector("time").textContent.trim();
    var fname = "thought-" + thought.dataset.id;

    var closeMenu = function () { menu.hidden = true; dlToggle.setAttribute("aria-expanded", "false"); };
    dlToggle.addEventListener("click", function (e) {
      e.stopPropagation();
      menu.hidden = !menu.hidden;
      dlToggle.setAttribute("aria-expanded", String(!menu.hidden));
    });
    document.addEventListener("click", function (e) { if (!e.target.closest("#dl")) closeMenu(); });

    var save = function (blob, name) {
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = name;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    };
    var plain = function () { return body.innerText.trim(); };

    document.getElementById("dl-text").addEventListener("click", function () {
      save(new Blob([plain() + "\n\n" + stamp + "\n"], { type: "text/plain;charset=utf-8" }), fname + ".txt");
      closeMenu();
    });

    document.getElementById("dl-image").addEventListener("click", function () {
      closeMenu();
      (document.fonts ? document.fonts.ready : Promise.resolve()).then(function () {
        var W = 1080, pad = 90, lh = 58, font = "38px Manrope, system-ui, sans-serif";
        var c = document.createElement("canvas"), ctx = c.getContext("2d");
        ctx.font = font;
        var lines = [];
        plain().split(/\n+/).forEach(function (para, i) {
          if (i) lines.push("");
          var line = "";
          para.split(/\s+/).forEach(function (w) {
            var test = line ? line + " " + w : w;
            if (ctx.measureText(test).width > W - pad * 2 && line) { lines.push(line); line = w; }
            else line = test;
          });
          lines.push(line);
        });
        var H = pad * 2 + lines.length * lh + 130;
        c.width = W; c.height = H;
        ctx = c.getContext("2d");
        var g = ctx.createRadialGradient(W * 0.15, 0, 0, W * 0.15, 0, H);
        g.addColorStop(0, "#2b1a55"); g.addColorStop(0.6, "#0c0a14");
        ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
        ctx.fillStyle = "#8b5cf6"; ctx.fillRect(pad, pad - 30, 64, 6);
        ctx.fillStyle = "#ecebf5"; ctx.font = font; ctx.textBaseline = "top";
        lines.forEach(function (l, i) { ctx.fillText(l, pad, pad + i * lh); });
        var y = H - pad - 10;
        ctx.fillStyle = "#a09fb8"; ctx.font = "28px Manrope, system-ui, sans-serif";
        ctx.fillText(stamp, pad, y);
        ctx.textAlign = "right";
        ctx.fillText(thought.dataset.site, W - pad, y);
        c.toBlob(function (b) { save(b, fname + ".png"); }, "image/png");
      });
    });
  }
})();
