const xParseDemoHref =
  "https://www.textin.com/console/recognition/robot_markdown?service=pdf_to_markdown";
const billDemoHref =
  "https://www.textin.com/console/recognition/robot_bills?service=bill_recognize_v2";

function isBillPage() {
  var pathname = window.location.pathname;
  return pathname.includes("bill");
}

function changeTrialButtonPC() {
  if (isBillPage()) {
    var primaryButtonPC = document.querySelector("#topbar-cta-button > a");

    if (
      primaryButtonPC &&
      primaryButtonPC.getAttribute("href") != billDemoHref
    ) {
      primaryButtonPC.setAttribute("href", billDemoHref);
    }
  }
}

function changeTrialButtonMobile() {
  if (isBillPage()) {
    var primaryButtonMobile = document.querySelector(
      "#headlessui-portal-root nav li:not(#topbar-cta-button):not(.navbar-link) a"
    );
    if (
      primaryButtonMobile &&
      primaryButtonMobile.getAttribute("href") != billDemoHref
    ) {
      primaryButtonMobile.setAttribute("href", billDemoHref);
    }
  }
}

function changePageTitle() {
  if (isBillPage()) {
    var title = document.title || "";
    var tileSections = title.split("-");
    var newTitle = tileSections[0] + "- Textin 票据识别";
    document.title = newTitle;
  }
}

function changeMetaInfo() {
  changeTrialButtonPC();
  changePageTitle();
}

changeMetaInfo();

var throttledChangeMetaInfo = throttle(changeMetaInfo, 500);

window.addEventListener("mousemove", throttledChangeMetaInfo);
window.addEventListener("touchmove", throttledChangeMetaInfo);

if (isMobile) {
  setInterval(() => {
    changeTrialButtonMobile();
    changePageTitle();
  }, 500);
}

function throttle(fn, delay) {
  var lastTime = 0; // 上一次执行的时间

  return function () {
    var context = this; // 保存上下文
    var currentTime = new Date().getTime(); // 当前时间

    // 如果距离上一次执行的时间超过 delay
    if (currentTime - lastTime >= delay) {
      fn.apply(context, arguments); // 执行函数
      lastTime = currentTime; // 更新上一次执行时间
    }
  };
}

function isMobile() {
  var userAgent = navigator.userAgent || navigator.vendor || window.opera;

  // 检查是否包含移动设备相关的关键字
  return /android|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(
    userAgent
  );
}
