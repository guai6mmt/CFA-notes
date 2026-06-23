// 在"文字版"页面顶部自动插入一个音频播放器，播放对应的本地音频。
// 音频由 scripts/generate_audio.py 预先生成（公式已用 AI 转成口语讲解）。
// 没有对应音频时不显示任何东西。

(function () {
  var checked = {}; // 缓存探测结果，避免重复请求

  function baseFromPath(pathname) {
    var p = pathname.replace(/\/+$/, ""); // 去掉结尾斜杠
    p = p.replace(/\.html$/i, ""); // 去掉 .html（如有）
    p = p.replace(/\/index$/i, ""); // 去掉 /index
    var decoded;
    try {
      decoded = decodeURIComponent(p);
    } catch (e) {
      decoded = p;
    }
    if (!/文字版$/.test(decoded)) return null; // 只在文字版页面显示
    return p;
  }

  function findAudio(base) {
    var candidates = [base + ".mp3", base + ".wav"];
    return candidates.reduce(function (chain, url) {
      return chain.then(function (found) {
        if (found) return found;
        if (url in checked) return checked[url] ? url : null;
        return fetch(url, { method: "HEAD" })
          .then(function (r) {
            checked[url] = r.ok;
            return r.ok ? url : null;
          })
          .catch(function () {
            checked[url] = false;
            return null;
          });
      });
    }, Promise.resolve(null));
  }

  function injectPlayer(url) {
    if (document.getElementById("tts-player")) return;
    var article = document.querySelector(".md-content__inner");
    if (!article) return;
    var box = document.createElement("div");
    box.id = "tts-player";
    box.className = "tts-player";
    box.innerHTML =
      '<div class="tts-player__label">🎧 听这篇笔记（公式已转成讲解）</div>' +
      '<audio controls preload="none" src="' + url + '"></audio>';
    var h1 = article.querySelector("h1");
    if (h1 && h1.nextSibling) {
      article.insertBefore(box, h1.nextSibling);
    } else {
      article.insertBefore(box, article.firstChild);
    }
  }

  function run() {
    var base = baseFromPath(window.location.pathname);
    if (!base) return;
    findAudio(base).then(function (url) {
      if (url) injectPlayer(url);
    });
  }

  // 兼容 Material 的即时加载（navigation.instant）
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(run);
  } else {
    document.addEventListener("DOMContentLoaded", run);
  }
})();
