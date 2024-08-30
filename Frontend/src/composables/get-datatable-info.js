export function getDataTableInfo(dataset_length, per_page, current_page, total, filtered, label = 'data') {
  const start = dataset_length > 0 ? per_page * (current_page - 1) + 1 : 0
  var end = start - 1 + dataset_length
  end = end < 0 ? 0 : end
  var info = `Showing ${start} to ${end} of ${filtered} ${label}`
  if (total != filtered) info += ` (filtered from ${total} ${label})`
  return info
}