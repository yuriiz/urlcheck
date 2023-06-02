(function () {
  function check() {
    function reqListener() {
      var result = JSON.parse(this.responseText)["result"];
      for (k in result) {
        document.getElementById("url-" + k).querySelector("td").className =
          199 < result[k] && result[k] < 300
            ? "bg-success-subtle"
            : "bg-danger-subtle";
      }
      document.getElementById("check-now").disabled = false;
      document.getElementById("check-now").innerText = "Check Now";
    }

    const req = new XMLHttpRequest();
    req.addEventListener("load", reqListener);
    req.open("POST", "check");
    req.setRequestHeader("content-type", "application/x-www-form-urlencoded");
    req.send(
      "csrfmiddlewaretoken=" + document.forms[0].csrfmiddlewaretoken.value,
    );
    document.getElementById("check-now").disabled = true;
    document.getElementById("check-now").innerText = "Checking...";
  }

  document.getElementById("check-now").addEventListener("click", function () {
    check();
  });
  var timerId;
  document.getElementById("schedule").addEventListener("click", function () {
    if (timerId) clearInterval(timerId);
    var minutes = document.getElementById("frequency").value;
    timerid = setInterval(check, minutes * 60 * 1000);
    alert("Will check every " + minutes + " minutes.");
  });
})();
