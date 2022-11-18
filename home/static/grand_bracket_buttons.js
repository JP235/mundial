$("#start-button").click(function () {
  $("#start-button").addClass("hide")
  $(Grupos_h3).removeClass("hide")
  $(A).removeClass("hide")
})

$(next_A).click(function () {
  $(A).addClass("hide")
  $(B).removeClass("hide")
})
$(prev_A).click(function () {
  $(A).addClass("hide")
  $("#start-button").removeClass("hide")
})

$(next_B).click(function () {
  $(B).addClass("hide")
  $(C).removeClass("hide")
})
$(prev_B).click(function () {
  $(B).addClass("hide")
  $(A).removeClass("hide")
})

$(next_C).click(function () {
  $(C).addClass("hide")
  $(D).removeClass("hide")
})
$(prev_C).click(function () {
  $(C).addClass("hide")
  $(B).removeClass("hide")
})

$(next_D).click(function () {
  $(D).addClass("hide")
  $(E).removeClass("hide")
})
$(prev_D).click(function () {
  $(D).addClass("hide")
  $(C).removeClass("hide")
})

$(next_E).click(function () {
  $(E).addClass("hide")
  $(F).removeClass("hide")
})
$(prev_E).click(function () {
  $(E).addClass("hide")
  $(D).removeClass("hide")
})

$(next_F).click(function () {
  $(F).addClass("hide")
  $(G).removeClass("hide")
})
$(prev_F).click(function () {
  $(F).addClass("hide")
  $(E).removeClass("hide")
})

$(next_G).click(function () {
  $(G).addClass("hide")
  $(H).removeClass("hide")
})
$(prev_G).click(function () {
  $(G).addClass("hide")
  $(F).removeClass("hide")
})

$(next_H).click(function () {
  $(H).addClass("hide")
  $(match_A1B2).removeClass("hide")
  $(Grupos_h3).addClass("done")
})
$(prev_H).click(function () {
  $(H).addClass("hide")
  $(G).removeClass("hide")
})

/** -------------------------------------------------------*/

$(prev_A1B2).click(function () {
  $(Grupos_h3).removeClass("done")
  $(match_A1B2).addClass("hide")
  $(H).removeClass("hide")
})
$(next_A1B2).click(function () {
  $(match_A1B2).addClass("hide")
  $(match_C1D2).removeClass("hide")
})

$(prev_C1D2).click(function () {
  $(match_C1D2).addClass("hide")
  $(match_A1B2).removeClass("hide")
})
$(next_C1D2).click(function () {
  $(match_C1D2).addClass("hide")
  $(match_E1F2).removeClass("hide")
})


$(prev_E1F2).click(function () {
  $(match_E1F2).addClass("hide")
  $(match_C1D2).removeClass("hide")
})
$(next_E1F2).click(function () {
  $(match_E1F2).addClass("hide")
  $(match_G1H2).removeClass("hide")
})


$(prev_G1H2).click(function () {
  $(match_G1H2).addClass("hide")
  $(match_E1F2).removeClass("hide")
})
$(next_G1H2).click(function () {
  $(match_G1H2).addClass("hide")
  $(match_B1A2).removeClass("hide")
})


$(prev_B1A2).click(function () {
  $(match_B1A2).addClass("hide")
  $(match_G1H2).removeClass("hide")
})
$(next_B1A2).click(function () {
  $(match_B1A2).addClass("hide")
  $(match_D1C2).removeClass("hide")
})


$(prev_D1C2).click(function () {
  $(match_D1C2).addClass("hide")
  $(match_B1A2).removeClass("hide")
})
$(next_D1C2).click(function () {
  $(match_D1C2).addClass("hide")
  $(match_F1E2).removeClass("hide")
})


$(prev_F1E2).click(function () {
  $(match_F1E2).addClass("hide")
  $(match_D1C2).removeClass("hide")
})
$(next_F1E2).click(function () {
  $(match_F1E2).addClass("hide")
  $(match_H1G2).removeClass("hide")
})


$(prev_H1G2).click(function () {
  $(match_H1G2).addClass("hide")
  $(match_F1E2).removeClass("hide")
})
$(next_H1G2).click(function () {
  $(match_H1G2).addClass("hide")
  $(match_AD).removeClass("hide")
  $("#16_h3").addClass("done")
})

/** -------------------------------------------------------*/

$(prev_AD).click(function () {
  $("#16_h3").removeClass("done")
  $(match_AD).addClass("hide")
  $(match_H1G2).removeClass("hide")
})
$(next_AD).click(function () {
  $(match_AD).addClass("hide")
  $(match_EH).removeClass("hide")
})


$(prev_EH).click(function () {
  $(match_EH).addClass("hide")
  $(match_AD).removeClass("hide")
})
$(next_EH).click(function () {
  $(match_EH).addClass("hide")
  $(match_BC).removeClass("hide")
})

$(prev_BC).click(function () {
  $(match_BC).addClass("hide")
  $(EH).removeClass("hide")
})
$(next_BC).click(function () {
  $(match_BC).addClass("hide")
  $(match_FG).removeClass("hide")
})

$(prev_FG).click(function () {
  $(match_FG).addClass("hide")
  $(match_BC).removeClass("hide")
})
$(next_FG).click(function () {
  $(match_AH).removeClass("hide")
  $(match_FG).addClass("hide")
  $("#eight_h3").addClass("done")
})

/** -------------------------------------------------------*/

$(prev_AH).click(function () {
  $(match_AH).addClass("hide")
  $(match_FG).removeClass("hide")
  $("#eight_h3").removeClass("done")
})
$(next_AH).click(function () {
  $(match_AH).addClass("hide")
  $(match_BG).removeClass("hide")
})

$(prev_BG).click(function () {
  $(match_BG).addClass("hide")
  $(match_AH).removeClass("hide")
})
$(next_BG).click(function () {
  $(match_BG).addClass("hide")
  $(match_winner).removeClass("hide")
  $(semi_h3).addClass("done")
})

/** -------------------------------------------------------*/

$(prev_winner).click(function () {
  $("#submit-button").addClass("hide")
  $(match_winner).addClass("hide")
  $(Final_h3).removeClass("done")
  $(match_BG).removeClass("hide")
  $(semi_h3).removeClass("done")
})

$(next_winner).click(function () {
  $("#submit-button").removeClass("hide")
  $(next_winner).addClass("hide")
  $(Final_h3).addClass("done")
})

