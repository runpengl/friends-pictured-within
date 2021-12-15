for (let i = 0; i < document.getElementsByTagName("input").length - 1; i++) {
  let elem = document.getElementsByTagName("input")[i];
  if (elem.maxLength !== 1) {
    continue;
  }
  elem.oninput = function () {
    if (
      "ABCDEFGHIJKLMNOPQRSTUVWXYZ".indexOf(this.value.toLocaleUpperCase()) ===
      -1
    ) {
      this.value = "";
      return;
    }
    if (this.value.length === 1) {
      try {
        document.getElementsByTagName("input")[i + 1].focus();
      } catch (e) {}
    }
  };
}
document.addEventListener("keydown", (e) => {
  if (e.key === "Delete" || e.key === "Backspace") {
    let activeIndex = -1;
    for (let i = 0; i < document.getElementsByTagName("input").length; i++) {
      if (document.getElementsByTagName("input")[i] == document.activeElement) {
        activeIndex = i;
      }
    }
    if (activeIndex > -1 && document.activeElement.maxLength === 1) {
      document.activeElement.value = "";
      try {
        let prevElement =
          document.getElementsByTagName("input")[activeIndex - 1];
        if (prevElement.maxLength === 1) {
          prevElement.focus();
        }
      } catch (e) {}
    }
  }
});

$(() => {
  const opts1 = [
    "I",
    "II",
    "III",
    "IV",
    "V",
    "VI",
    "VII",
    "VIII",
    "IX",
    "X",
    "XI",
    "XII",
  ];
  const opts2 = [
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",
  ];
  $(".col1 table").each(function (index) {
    const select1 = $("<select class=s1>");
    const select2 = $("<select class=s2>");
    select1.append(
      $("<option>")
        .attr("disabled", true)
        .attr("selected", true)
        .attr("value", "")
    );
    select2.append(
      $("<option>")
        .attr("disabled", true)
        .attr("selected", true)
        .attr("value", "")
    );
    for (let opt of opts1) {
      let option = $("<option>").attr("value", opt).text(opt);
      select1.append(option);
    }
    for (let opt of opts2) {
      let option = $("<option>")
        .attr("value", opt)
        .text(opt);
      select2.append(option);
    }
    $(this)
    .children("thead")
    .first()
    .children("tr")
    .first()
    .children("th")
    .first()
    .html(select1);
    const selectContainer = $("<div>").addClass("select-container");
    $(this).append(selectContainer.append(select2));
  });
  $("td.n div").click(function () {
    let notation = $(this).text();
    let modifier = 4;
    while (notation[notation.length - 1] === "'") {
      modifier += 1;
      notation = notation.slice(0, -1);
    }
    while (notation[notation.length - 1] === ",") {
      modifier -= 1;
      notation = notation.slice(0, -1);
    }
    let s1 = undefined;
    $(".s1").each(function (index) {
      if ($(this).val() === notation) {
        if (s1 === undefined) {
          s1 = index;
        } else {
          s1 = -1;
        }
      }
    });
    let s2 = undefined;
    $(".s2").each(function (index) {
      if (index === s1) {
        s2 = $(this).val();
      }
    });
    if (s2) {
      try {
        const audio = new Audio(`assets/tones/${s2.replace('#', '+')}${modifier}.wav`);
        audio.playbackRate = parseFloat($(this).data("r"));
        audio.play();
      } catch (e) {}
    }
  });
});
