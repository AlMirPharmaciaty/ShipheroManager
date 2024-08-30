function convertUTCToLocal(date) {
  const utcDate = new Date(date)
  const localOffset = utcDate.getTimezoneOffset() * 60 * 1000
  const localDate = new Date(utcDate.getTime() - localOffset)
  return localDate
}

export function format_date(
  date,
  date_only = false,
  time_only = false,
  timelapse = false,
  wording = 'long'
) {
  var date_options = {
    weekday: wording,
    month: wording,
    day: '2-digit',
    year: 'numeric'
  }
  var time_options = {
    hour: '2-digit',
    minute: '2-digit'
  }

  date = convertUTCToLocal(date)
  var date_to_string = new Date(date).toLocaleString('en-US', date_options)
  var time_to_string = new Date(date).toLocaleString('en-US', time_options)
  var text = `${date_to_string} at ${time_to_string}`
  if (date_only) text = date_to_string
  else if (time_only) text = time_to_string
  if (timelapse) text = `${text} (${get_timelapse(date, true)})`
  return text
}

export function get_timelapse(date, utc_date = false) {
  if (!utc_date) {
    date = convertUTCToLocal(date)
  }
  var currentDateTime = new Date()
  var timelapse = Math.abs(currentDateTime - new Date(date))

  var mm = timelapse
  var sec = Math.floor(timelapse / 1000)
  var min = Math.floor(timelapse / (1000 * 60))
  var hr = Math.floor(timelapse / (1000 * 60 * 60))
  var day = Math.floor(timelapse / (1000 * 60 * 60 * 24))
  var month = Math.floor(timelapse / (1000 * 60 * 60 * 24 * 30))
  var year = Math.floor(timelapse / (1000 * 60 * 60 * 24 * 30 * 12))

  timelapse = mm + ' milliseconds ago'
  if (sec >= 1 && sec < 60) {
    let text = sec > 1 ? ' seconds ago' : ' second ago'
    timelapse = sec + text
  } else if (min >= 1 && min < 60) {
    let text = min > 1 ? ' minutes ago' : ' minute ago'
    timelapse = min + text
  } else if (hr >= 1 && hr < 24) {
    let text = hr > 1 ? ' hours ago' : ' hour ago'
    timelapse = hr + text
  } else if (day >= 1 && day < 30) {
    let text = day > 1 ? ' days ago' : ' day ago'
    timelapse = day + text
  } else if (month >= 1 && month < 12) {
    let text = month > 1 ? ' months ago' : ' month ago'
    timelapse = month + text
  } else if (year >= 1) {
    let text = year > 1 ? ' years ago' : ' year ago'
    timelapse = year + text
  }
  return timelapse
}
