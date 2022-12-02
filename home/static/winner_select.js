
function change_winner(team) {
  try {
    $(`.winner`).children().remove()
    $(`.winner`).append($(`.${team}:first`).clone())
    $(".selected_winner")[0].value = team
  } catch {

  }
}

$(".flags_counties_octavos").click(function (e) {
  console.log(e.target.parentElement.id)
  if (e.target.parentElement.id.length === 3) {
    console.log($(`#${e.target.parentElement.id}`))
    $(".flags_counties_octavos * ").removeClass("selected")
    $(`#${e.target.parentElement.id}`).addClass("selected")
    change_winner(e.target.parentElement.id)
  }
});
