console.log("loaded tables")

// based on: D3 Table - F1 Leaderboard by: Jonathan 
// https://codepen.io/jonakirke94/pen/NWzreGM

// array describing the color for each team
// using camel case where the team names include a space
var colors = {
  mercedes: '#00D2BE',
  ferrari: '#DC0000',
  redBull: '#1E41FF',
  renault: '#FFF500',
  racingPoint: '#F596C8',
  alfaRomeo: '#9B0000',
  toroRosso: '#469BFF',
  haas: '#BD9E57',
  mclaren: '#FF8700',
  williams: '#FFFFFF'
}

// array describing the Jugadors, sorted by position and with a Puntos describing the distance from the leading Jugador
var leaderboard = [
  {
    name: 'P1',
    team: 'Argentina',
    Puntos: '10'
  },
  {
    name: 'P2',
    team: 'España',
    Puntos: '9'
  },
  {
    name: 'P3',
    team: 'España',
    Puntos: '9'
  },
  {
    name: 'P4',
    team: 'Francia',
    Puntos: '7'
  },
  {
    name: 'P5',
    team: 'Argentina',
    Puntos: '5'
  },
];

// target the table element in which to add one div for each Jugador
var main = d3
    .select('#leaderboardTable');

// for each Jugador add one table row
// ! add a class to the row to differentiate the rows from the existing one
// otherwise the select method would target the existing one and include one row less than the required amount
var Jugadors = main
  .selectAll('tr.Jugador')
  .data(leaderboard)
  .enter()
  .append('tr')
  .attr('class', 'Jugador');

// in each row add the information specified by the dataset in td elements
// specify a class to style the elements differently with CSS

// position using the index of the data points
Jugadors
  .append('td')
  .text((d, i) => i + 1)
  .attr('class', 'position');


// name followed by the team
Jugadors
  .append('td')
  // include the last name in a separate element to style it differently
  // include the team also in another element for the same reason
  .html (({name, team}) => `${name.split(' ').map((part, index) => index > 0 ? `<strong>${part}</strong>` : `${part}`).join(' ')} <span>- ${team}</span>`)
  .attr('class', 'Jugador');

// Puntos from the first Jugador
Jugadors
  .append('td')
  .attr('class', 'Puntos')
  .append('span')
  .text(({Puntos}) => Puntos);