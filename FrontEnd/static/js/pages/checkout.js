/**
 * CHECKOUT PAGE JAVASCRIPT - Sài Gòn Côn Đảo Resort
 * Synchronized with Draw.io Architecture (UC-01 & SD-01 BCE Pattern)
 * Real-time 15-Minute Hold Countdown, Live Extra Services & Breakdown
 */

document.addEventListener('DOMContentLoaded', function() {
    // ── 1. Parse Initial Checkout Data ──
    var dataNode = document.getElementById('checkout-data');
    var viewData = {};
    if (dataNode) {
        try {
            viewData = JSON.parse(dataNode.textContent);
        } catch (e) {
            console.error('Error parsing checkout data:', e);
        }
    }

    var currentDiscountPercent = parseFloat(viewData.discountPercent || 0);
    var currentPromoCode = viewData.promoCode || '';

    function formatVnd(val) {
        var num = Math.round(Number(val) || 0);
        return num.toLocaleString('vi-VN').replace(/,/g, '.') + ' đ';
    }

    // ── 2. Real-time Live 15-Minute Countdown Timer ──
    var countdownEl = document.getElementById('live-countdown-clock');
    var lockedUntilStr = viewData.lockedUntil;
    var targetTime;

    if (lockedUntilStr && lockedUntilStr.trim() !== '') {
        var isoStr = lockedUntilStr.replace(' ', 'T');
        var parsedDate = new Date(isoStr);
        if (!isNaN(parsedDate.getTime())) {
            targetTime = parsedDate.getTime();
        }
    }

    if (!targetTime || targetTime <= Date.now()) {
        targetTime = Date.now() + 15 * 60 * 1000;
    }

    function updateCountdown() {
        if (!countdownEl) return;
        var now = Date.now();
        var remainingMs = targetTime - now;

        if (remainingMs <= 0) {
            countdownEl.textContent = '00:00';
            countdownEl.classList.add('timer-warning');
            clearInterval(timerInterval);
            
            setTimeout(function() {
                alert('Thời hạn giữ phòng 15 phút đã kết thúc. Phòng đã được mở lại cho khách khác trên hệ thống.');
                var releaseForm = document.getElementById('release-form');
                if (releaseForm) {
                    releaseForm.submit();
                } else {
                    window.location.href = '/booking';
                }
            }, 1000);
            return;
        }

        var totalSeconds = Math.floor(remainingMs / 1000);
        var minutes = Math.floor(totalSeconds / 60);
        var seconds = totalSeconds % 60;

        var minStr = minutes < 10 ? '0' + minutes : minutes;
        var secStr = seconds < 10 ? '0' + seconds : seconds;

        countdownEl.textContent = minStr + ':' + secStr;

        if (totalSeconds < 180) {
            countdownEl.classList.add('timer-warning');
        } else {
            countdownEl.classList.remove('timer-warning');
        }
    }

    updateCountdown();
    var timerInterval = setInterval(updateCountdown, 1000);

    // ── 3. Payment Method Card Active Style ──
    window.updatePaymentCardStyle = function() {
        var cards = document.querySelectorAll('.payment-method-card');
        cards.forEach(function(card) {
            var radio = card.querySelector('input[type="radio"]');
            if (radio && radio.checked) {
                card.classList.add('active');
            } else {
                card.classList.remove('active');
            }
        });
    };

    var methodRadios = document.querySelectorAll('input[name="payment_method"]');
    methodRadios.forEach(function(r) {
        r.addEventListener('change', window.updatePaymentCardStyle);
    });
    window.updatePaymentCardStyle();

    // ── 4. Live Stay Duration, Extra Services & Itemized Recalculation ──
    var checkinStr = viewData.checkinDate;
    var checkoutStr = viewData.checkoutDate;
    var basePrice = parseFloat(viewData.basePrice || 0);
    var nights = 1;

    if (checkinStr && checkoutStr) {
        var t1 = new Date(checkinStr).getTime();
        var t2 = new Date(checkoutStr).getTime();
        var diff = Math.ceil((t2 - t1) / 86400000);
        if (diff > 0) nights = diff;
    }

    var rawNights = viewData.selectedNights;
    if (rawNights && rawNights.trim() !== '') {
        var parts = rawNights.split(',').filter(function(n) { return n.trim() !== ''; });
        if (parts.length > 0) nights = parts.length;
    }

    var stayDurationEl = document.getElementById('stay-duration-summary');
    if (stayDurationEl) {
        stayDurationEl.textContent = nights + ' đêm lưu trú';
    }
    var recapNightsCount = document.getElementById('recap-nights-count');
    if (recapNightsCount) {
        recapNightsCount.textContent = nights;
    }

    var roomTotal = basePrice * nights;

    // Elements for breakdown
    var recapRoomCost = document.getElementById('recap-room-cost');
    var recapServicesBlock = document.getElementById('recap-services-block');
    var recapServicesCost = document.getElementById('recap-services-cost');
    var recapServicesList = document.getElementById('recap-services-list');
    var recapPromoBlock = document.getElementById('recap-promo-block');
    var recapPromoCodeLabel = document.getElementById('recap-promo-code-label');
    var recapPromoCost = document.getElementById('recap-promo-cost');
    var recapTaxCost = document.getElementById('recap-tax-cost');
    var totalPriceDisplay = document.getElementById('total-price-display');
    var totalPriceLabel = document.getElementById('total-price-label');
    var depositRemainingNote = document.getElementById('deposit-remaining-note');

    function recalculateTotal() {
        // 1. Dịch vụ gia tăng đã chọn
        var servicesTotal = 0;
        var selectedServices = [];
        var serviceCheckboxes = document.querySelectorAll('.extra-service-checkbox:checked');
        serviceCheckboxes.forEach(function(cb) {
            var price = parseFloat(cb.getAttribute('data-price') || 0);
            var name = cb.getAttribute('data-name') || '';
            servicesTotal += price;
            selectedServices.push('• ' + name + ' (+' + formatVnd(price) + ')');
        });

        // 2. Chiết khấu mã ưu đãi (nếu có)
        var discountAmount = 0;
        if (currentDiscountPercent > 0) {
            discountAmount = Math.round(roomTotal * (currentDiscountPercent / 100.0));
        }

        var netRoomCost = Math.max(0, roomTotal - discountAmount);
        var subtotal = netRoomCost + servicesTotal;
        var vatTax = Math.round(subtotal * 0.1);
        var grandTotal = subtotal + vatTax;

        // 3. Hình thức thanh toán (100% vs Đặt cọc 50%)
        var paymentTypeNode = document.querySelector('input[name="payment_type"]:checked');
        var paymentType = paymentTypeNode ? paymentTypeNode.value : 'full';

        var amountToPay = grandTotal;
        var displayLabel = 'Tổng cộng thanh toán (100%):';

        if (paymentType === 'deposit') {
            amountToPay = Math.round(grandTotal * 0.5);
            displayLabel = 'Đặt cọc thanh toán ngay (50%):';
            var remaining = grandTotal - amountToPay;
            if (depositRemainingNote) {
                depositRemainingNote.style.display = 'block';
                depositRemainingNote.textContent = 'Còn lại quyết toán khi Check-out: ' + formatVnd(remaining);
            }
        } else {
            if (depositRemainingNote) {
                depositRemainingNote.style.display = 'none';
            }
        }

        // 4. Cập nhật DOM
        if (recapRoomCost) recapRoomCost.textContent = formatVnd(roomTotal);

        if (recapServicesBlock) {
            if (servicesTotal > 0) {
                recapServicesBlock.style.display = 'block';
                if (recapServicesCost) recapServicesCost.textContent = '+' + formatVnd(servicesTotal);
                if (recapServicesList) recapServicesList.innerHTML = selectedServices.join('<br>');
            } else {
                recapServicesBlock.style.display = 'none';
            }
        }

        if (recapPromoBlock) {
            if (discountAmount > 0) {
                recapPromoBlock.style.display = 'block';
                if (recapPromoCodeLabel) recapPromoCodeLabel.textContent = currentPromoCode;
                if (recapPromoCost) recapPromoCost.textContent = '-' + formatVnd(discountAmount);
            } else {
                recapPromoBlock.style.display = 'none';
            }
        }

        if (recapTaxCost) recapTaxCost.textContent = formatVnd(vatTax);
        if (totalPriceLabel) totalPriceLabel.textContent = displayLabel;
        if (totalPriceDisplay) totalPriceDisplay.textContent = formatVnd(amountToPay);
    }

    // Lắng nghe thay đổi dịch vụ gia tăng
    var serviceCheckboxes = document.querySelectorAll('.extra-service-checkbox');
    serviceCheckboxes.forEach(function(cb) {
        cb.addEventListener('change', recalculateTotal);
    });

    // Lắng nghe thay đổi hình thức thanh toán (100% vs cọc 50%)
    var paymentTypeRadios = document.querySelectorAll('input[name="payment_type"]');
    paymentTypeRadios.forEach(function(r) {
        r.addEventListener('change', recalculateTotal);
    });

    // ── 5. Promo Code Live Validation in Checkout ──
    var btnCheckoutPromo = document.getElementById('btn_checkout_promo');
    var inputCheckoutPromo = document.getElementById('checkout_promo_code');
    var feedbackCheckoutPromo = document.getElementById('checkout_promo_feedback');

    if (btnCheckoutPromo && inputCheckoutPromo) {
        btnCheckoutPromo.addEventListener('click', async function() {
            var code = inputCheckoutPromo.value.trim().toUpperCase();
            if (!code) {
                if (feedbackCheckoutPromo) {
                    feedbackCheckoutPromo.innerHTML = '<span class="text-danger"><i class="fas fa-exclamation-circle me-1"></i>Vui lòng nhập mã ưu đãi.</span>';
                }
                currentDiscountPercent = 0;
                currentPromoCode = '';
                recalculateTotal();
                return;
            }

            btnCheckoutPromo.disabled = true;
            btnCheckoutPromo.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Đang kiểm tra...';

            try {
                var resp = await fetch('/booking/validate-promo', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        promo_code: code,
                        checkin_date: checkinStr || ''
                    })
                });
                var data = await resp.json();

                if (data && data.valid && data.promo) {
                    currentDiscountPercent = parseFloat(data.promo.discount_percent || 0);
                    currentPromoCode = code;
                    if (feedbackCheckoutPromo) {
                        feedbackCheckoutPromo.innerHTML = '<span class="text-success fw-bold"><i class="fas fa-check-circle me-1"></i>Đã áp dụng ' + code + ' (-' + currentDiscountPercent + '%: ' + (data.promo.description || '') + ')</span>';
                    }
                    btnCheckoutPromo.innerHTML = '<i class="fas fa-check me-1"></i>Đã nhận';
                } else {
                    currentDiscountPercent = 0;
                    currentPromoCode = '';
                    if (feedbackCheckoutPromo) {
                        feedbackCheckoutPromo.innerHTML = '<span class="text-danger"><i class="fas fa-times-circle me-1"></i>' + (data.message || 'Mã không hợp lệ hoặc đã hết hạn.') + '</span>';
                    }
                    btnCheckoutPromo.innerHTML = 'Kiểm tra';
                }
            } catch (err) {
                if (feedbackCheckoutPromo) {
                    feedbackCheckoutPromo.innerHTML = '<span class="text-danger"><i class="fas fa-times-circle me-1"></i>Lỗi kiểm tra mã.</span>';
                }
                btnCheckoutPromo.innerHTML = 'Kiểm tra';
            }

            btnCheckoutPromo.disabled = false;
            recalculateTotal();
        });
    }

    recalculateTotal();

    // ── 6. Form Submit Guard & Spinner ──
    var checkoutForm = document.getElementById('checkout-form');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', function(e) {
            var payMethod = checkoutForm.querySelector('input[name="payment_method"]:checked');
            var payType = checkoutForm.querySelector('input[name="payment_type"]:checked');
            var errDiv = document.getElementById('checkout-error');

            if (!payMethod || !payType) {
                e.preventDefault();
                if (errDiv) {
                    errDiv.textContent = 'Vui lòng chọn phương thức và hình thức thanh toán.';
                    errDiv.classList.remove('d-none');
                }
                return;
            }

            if (errDiv) errDiv.classList.add('d-none');
            var btn = document.getElementById('confirm-btn');
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>ĐANG XỬ LÝ KHÓA GIỮ PHÒNG...';
            }
        });
    }
});
