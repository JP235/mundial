function change_option(next_group, team, opt) {
  try {
    console.log(next_group, team, opt)
    console.log(`.options_${opt}.${next_group}`)
    $(`.options_${opt}.${next_group}`).children().remove()
    $(`.options_${opt}.${next_group}`).append($(`.${team}:first`).clone())
    $(`#${next_group}${opt}`)[0].innerText = team
  } catch {
    console.log(next_group, team, opt)
    // }
  }
}
function remove_not(g,opt){
  $(g).parent().parent().siblings().children().removeClass(`not_${opt}`)
}
/** **/

$(group_A1).change(function () {
  const selected_team = $("#group_A1 option:selected").val()
  change_option("A1B2", selected_team, 1)
});

$(group_A2).change(function () {
  const selected_team = $("#group_A2 option:selected").val()
  change_option("B1A2", selected_team, 2)
});

$(group_B1).change(function () {
  const selected_team = $("#group_B1 option:selected").val()
  change_option("B1A2", selected_team, 1)
});

$(group_B2).change(function () {
  const selected_team = $("#group_B2 option:selected").val()
  change_option("A1B2", selected_team, 2)
});

$(group_C1).change(function () {
  const selected_team = $("#group_C1 option:selected").val()
  change_option("C1D2", selected_team, 1)
});

$(group_C2).change(function () {
  const selected_team = $("#group_C2 option:selected").val()
  change_option("D1C2", selected_team, 2)
});

$(group_D1).change(function () {
  const selected_team = $("#group_D1 option:selected").val()
  change_option("D1C2", selected_team, 1)
});

$(group_D2).change(function () {
  const selected_team = $("#group_D2 option:selected").val()
  change_option("C1D2", selected_team, 2)
});

$(group_E1).change(function () {
  const selected_team = $("#group_E1 option:selected").val()
  change_option("E1F2", selected_team, 1)
});

$(group_E2).change(function () {
  const selected_team = $("#group_E2 option:selected").val()
  change_option("F1E2", selected_team, 2)
});

$(group_F1).change(function () {
  const selected_team = $("#group_F1 option:selected").val()
  change_option("F1E2", selected_team, 1)
});

$(group_F2).change(function () {
  const selected_team = $("#group_F2 option:selected").val()
  change_option("E1F2", selected_team, 2)
});

$(group_G1).change(function () {
  const selected_team = $("#group_G1 option:selected").val()
  change_option("G1H2", selected_team, 1)
});

$(group_G2).change(function () {
  const selected_team = $("#group_G2 option:selected").val()
  change_option("H1G2", selected_team, 2)
});

$(group_H1).change(function () {
  const selected_team = $("#group_H1 option:selected").val()
  change_option("H1G2", selected_team, 1)
});

$(group_H2).change(function () {
  const selected_team = $("#group_H2 option:selected").val()
  change_option("G1H2", selected_team, 2)
});

/** 
 * 
*/
$(match_A1B2).change(function () {
  const selected_team = $("#A1B2 option:selected")[0].innerText
  change_option("AD", selected_team, 1)
});

$(match_C1D2).change(function () {
  const selected_team = $("#C1D2 option:selected")[0].innerText
  change_option("AD", selected_team, 2)
});

$(match_E1F2).change(function () {
  const selected_team = $("#E1F2 option:selected")[0].innerText
  change_option("EH", selected_team, 1)
});

$(match_G1H2).change(function () {
  const selected_team = $("#G1H2 option:selected")[0].innerText
  change_option("EH", selected_team, 2)
});

$(match_B1A2).change(function () {
  const selected_team = $("#B1A2 option:selected")[0].innerText
  change_option("BC", selected_team, 1)
});

$(match_D1C2).change(function () {
  const selected_team = $("#D1C2 option:selected")[0].innerText
  change_option("BC", selected_team, 2)
});

$(match_F1E2).change(function () {
  const selected_team = $("#F1E2 option:selected")[0].innerText
  change_option("FG", selected_team, 1)
});

$(match_H1G2).change(function () {
  const selected_team = $("#H1G2 option:selected")[0].innerText
  change_option("FG", selected_team, 2)
});

/**
 * 
 * 
 */

$(match_AD).change(function () {
  const selected_team = $("#AD option:selected")[0].innerText
  change_option("AH", selected_team, 1)
});

$(match_EH).change(function () {
  const selected_team = $("#EH option:selected")[0].innerText
  change_option("AH", selected_team, 2)
});

$(match_BC).change(function () {
  const selected_team = $("#BC option:selected")[0].innerText
  change_option("BG", selected_team, 1)
});

$(match_FG).change(function () {
  const selected_team = $("#FG option:selected")[0].innerText
  change_option("BG", selected_team, 2)
})

/**
 * 
 * 
 */

$(match_AH).change(function () {
  const selected_team = $("#AH option:selected")[0].innerText
  change_option("winner", selected_team, 1)
});

$(match_BG).change(function () {
  const selected_team = $("#BG option:selected")[0].innerText
  change_option("winner", selected_team, 2)
})

