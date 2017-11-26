export default async function loadMaps(url) {
  // Raw <year:Number, map:GeoJSON> dict
  const dict = await (await fetch(url)).json()

  // List of map years
  const years = Object.keys(dict).map(el => +el).sort()

  // Get map by year
  const year = year =>
    dict[
      reversedYears
        .find(y => y <= year)
      || years[years.length - 1]
    ]

  // This helps a lot to find year between bounds
  const reversedYears = [...years].reverse()

  return {dict, years, year}
}
