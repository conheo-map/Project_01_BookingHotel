// Filter Room Status
function filterRooms(status, btn) {
  document.querySelectorAll('.sodophong-loc-cuc').forEach(function(c) { c.classList.remove('active'); });
  btn.classList.add('active');
  document.querySelectorAll('.sodophong-phong-the').forEach(function(card) {
    if (status === 'all') {
      card.style.display = '';
    } else {
      card.style.display = card.dataset.status === status ? '' : 'none';
    }
  });
}

// Filter Wing (City Hotel vs Resort Hotel)
function filterWing(wing, btn) {
  document.querySelectorAll('.wing-filter-btn').forEach(function(b) {
    b.classList.remove('active', 'btn-heritage-gold');
    b.classList.add('btn-outline-secondary');
  });
  btn.classList.remove('btn-outline-secondary');
  btn.classList.add('active', 'btn-heritage-gold');

  document.querySelectorAll('.sodophong-loai-phan').forEach(function(sec) {
    if (wing === 'all') {
      sec.style.display = '';
    } else {
      sec.style.display = (sec.dataset.hotelId === wing) ? '' : 'none';
    }
  });
}

// Grid columns
function changeGridCols(n) {
  document.querySelectorAll('.sodophong-phong-luoi').forEach(function(grid) {
    grid.style.gridTemplateColumns = 'repeat(' + n + ', 1fr)';
  });
}

// Walk-in modal
function openWalkinModal(physId, roomName, rtId, hotelId, rtCode, basePrice) {
  document.getElementById('wk-physical-room-id').value = physId;
  document.getElementById('wk-room-type-id').value = rtId;
  document.getElementById('wk-hotel-id').value = hotelId;
  document.getElementById('wk-room-badge').innerHTML =
    '<span><i class="fas fa-door-open me-2"></i>' + roomName + ' — ' + rtCode + '</span>' +
    '<span class="text-warning">' + basePrice.toLocaleString('vi-VN') + ' ₫/đêm</span>';
  document.getElementById('wk-price-display').textContent = basePrice.toLocaleString('vi-VN') + ' ₫';

  // Default dates: today → tomorrow
  var today = new Date();
  var tomorrow = new Date(today);
  tomorrow.setDate(today.getDate() + 1);
  document.getElementById('wk-checkin').value = today.toISOString().split('T')[0];
  document.getElementById('wk-checkout').value = tomorrow.toISOString().split('T')[0];

  document.getElementById('walkin-backdrop').style.display = 'block';
  document.getElementById('walkin-modal').style.display = 'block';
}

function closeWalkinModal() {
  document.getElementById('walkin-backdrop').style.display = 'none';
  document.getElementById('walkin-modal').style.display = 'none';
}
