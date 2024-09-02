const statusIcon = {
  success: `circle-check`,
  danger: 'circle-xmark',
  info: 'circle-info',
  warning: 'circle-exclaimation'
}

export function notify(message, color = 'success', delay = 5000, loading = false) {
  document.querySelectorAll('.notification').forEach((i) => i.remove())

  const notification = document.createElement('div')
  notification.innerHTML = `
    <div class="d-flex justify-content-between gap-4">
      <p class="mb-0">
        <i class="fa-solid fa-${loading ? `circle-notch fa-spin` : statusIcon[color]} me-2"></i>
        <span>${message}</span>
      </p>
      <button type="button" class="btn-close" data-mdb-dismiss="alert"></button>
    </div>
  `
  notification.classList.add(
    'alert',
    'fade',
    'shadow-lg',
    'notification',
    'border-start',
    'border-5',
    `border-${color}`,
    'py-3'
  )

  document.body.appendChild(notification)

  const notificationInstance = new mdb.Alert(notification, {
    color: color,
    offset: 20,
    hidden: true,
    position: 'top-center',
    autohide: true,
    delay: delay,
    animation: true
  })

  notificationInstance.show()
}

export function initRipple(element, color = null) {
  var options = {}
  if (color) options['rippleColor'] = color
  new mdb.Ripple(element, options)
}

export function showModal(modal_id) {
  new mdb.Modal(document.getElementById(modal_id)).show()
}

export function hideModal(modal_id) {
  mdb.Modal.getInstance(document.getElementById(modal_id)).hide()
}

export function hideModalAll() {
  document.querySelectorAll('.modal.show').forEach((modal) => {
    mdb.Modal.getInstance(modal).hide()
  })
}

export function changeModalBackdrop(modal_id, backdrop) {
  const modal = mdb.Modal.getInstance(document.getElementById(modal_id))
  modal._config.backdrop = backdrop
  modal._config.mdbBackdrop = backdrop
}

export function initTooptip(
  element,
  title,
  placement = 'bottom',
  trigger = 'hover focus',
  delay_show = 0,
  delay_hide = 0
) {
  const options = {
    title: title,
    placement: placement,
    trigger: trigger,
    delay: { show: delay_show, hide: delay_hide }
  }
  return mdb.Tooltip.getOrCreateInstance(element, options)
}

export function initClipboard(element, target) {
  new mdb.Clipboard(element, { clipboardTarget: target })
  const copy = () => initTooptip(element, 'Copy', 'bottom', 'hover focus')
  var tooltip = copy()
  element.addEventListener('copied.mdb.clipboard', () => {
    tooltip.dispose()
    tooltip = initTooptip(element, 'Copied!', 'bottom', 'hover focus', 0, 500)
    tooltip.show()
    element.addEventListener('hidden.mdb.tooltip', () => {
      tooltip.dispose()
      tooltip = copy()
    })
  })
}
