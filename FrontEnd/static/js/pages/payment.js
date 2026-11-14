/**
 * PAYMENT PAGE JAVASCRIPT - Sài Gòn Côn Đảo Resort
 * Synchronized with Draw.io Architecture (UC-01 & SD-01 BCE Pattern)
 * Real-time 15-Minute Countdown & Dynamic Payment Method Switching
 */

function switchPaymentMethod(method) {
  document.querySelectorAll('.thanhtoan-phuongthuc-chitiet').forEach(function(el) {
    el.classList.add('d-none');
  });
  var target = document.getElementById('form-' + method);
  if (target) target.classList.remove('d-none');

  document.querySelectorAll('.thanhtoan-phuongthuc-muc').forEach(function(el) {
    var radio = el.querySelector('input[type="radio"]');
    if (radio && radio.value === method) {
      el.classList.add('active');
    } else {
      el.classList.remove('active');
    }
  });
}

function formatCardNumber(input) {
  var v = input.value.replace(/\D/g, '').substring(0, 16);
  input.value = v.replace(/(\d{4})(?=\d)/g, '$1 ');
}

function formatExpiry(input) {
  var v = input.value.replace(/\D/g, '').substring(0, 4);
  if (v.length >= 3) {
    input.value = v.substring(0, 2) + ' / ' + v.substring(2);
  } else {
    input.value = v;
  }
}

document.addEventListener('DOMContentLoaded', function() {
  // ── 1. Live Countdown Timer ──
  var clockEl = document.getElementById('pay-countdown-clock');
  var dataNode = document.getElementById('payment-page-data');
  var targetTime;

  if (dataNode) {
    try {
      var d = JSON.parse(dataNode.textContent);
      if (d.lockedUntil && d.lockedUntil.trim() !== '') {
        var iso = d.lockedUntil.replace(' ', 'T');
        var parsed = new Date(iso);
        if (!isNaN(parsed.getTime())) {
          targetTime = parsed.getTime();
        }
      }
    } catch (e) {
      console.error('Error parsing payment page data:', e);
    }
  }

  if (!targetTime || targetTime <= Date.now()) {
    targetTime = Date.now() + 15 * 60 * 1000;
  }

  function updateClock() {
    if (!clockEl) return;
    var now = Date.now();
    var diffMs = targetTime - now;

    if (diffMs <= 0) {
      clockEl.textContent = '00:00';
      clearInterval(clockInterval);
      alert('Thời hạn giữ phòng 15 phút đã kết thúc. Phòng sẽ được mở lại cho khách khác trên hệ thống.');
      var releaseForm = document.getElementById('release-form');
      if (releaseForm) releaseForm.submit();
      else window.location.href = '/booking';
      return;
    }

    var totalSec = Math.floor(diffMs / 1000);
    var mins = Math.floor(totalSec / 60);
    var secs = totalSec % 60;

    var minStr = mins < 10 ? '0' + mins : mins;
    var secStr = secs < 10 ? '0' + secs : secs;
    clockEl.textContent = minStr + ':' + secStr;
  }

  updateClock();
  var clockInterval = setInterval(updateClock, 1000);

  // ── 2. Payment Form Validation & Processing State ──
  var form = document.getElementById('payment-form');
  if (form) {
    form.addEventListener('submit', function(e) {
      var activeMethod = document.querySelector('input[name="method_display"]:checked');
      if (!activeMethod) return;
      var method = activeMethod.value;
      var errDiv = document.getElementById('pay-error');

      if (method === 'credit_card') {
        var cardNum = document.querySelector('[name="card_number"]').value.trim();
        var cardExp = document.querySelector('[name="card_expiry"]').value.trim();
        var cardCvc = document.querySelector('[name="card_cvc"]').value.trim();
        var cardHolder = document.querySelector('[name="card_holder"]').value.trim();

        if (!cardNum || !cardExp || !cardCvc || !cardHolder) {
          e.preventDefault();
          if (errDiv) {
            errDiv.textContent = 'Vui lòng điền đầy đủ số thẻ, ngày hết hạn, mã CVC và tên chủ thẻ.';
            errDiv.classList.remove('d-none');
          }
          return;
        }
      } else if (method === 'bank_transfer') {
        var bankName = document.querySelector('[name="bank_name"]').value.trim();
        var transferName = document.querySelector('[name="transfer_name"]').value.trim();

        if (!bankName || !transferName) {
          e.preventDefault();
          if (errDiv) {
            errDiv.textContent = 'Vui lòng chọn ngân hàng và nhập họ tên người chuyển khoản.';
            errDiv.classList.remove('d-none');
          }
          return;
        }
      }

      if (errDiv) errDiv.classList.add('d-none');
      var btn = document.getElementById('btn-pay');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> ĐANG XÁC THỰC THANH TOÁN &amp; XUẤT VOUCHER...';
      }
    });
  }
});
