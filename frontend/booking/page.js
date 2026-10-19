// Booking page markup.
// Fields mirror backend/schemas/booking_schema.py (BookingRequest / BookingView).
// Elements that JS needs to read or update have an id; repeated items use data-* attributes.

export const bookingPageTemplate = `
<main class="booking-page" id="booking-page">
  <header class="booking-header">
    <h1>Randevu Oluştur</h1>
    <p class="booking-subtitle">İşleminizi, uzmanınızı ve size uygun saati seçin.</p>
  </header>

  <!-- Shown while procedures/staff are being fetched -->
  <div class="booking-loading" id="booking-loading" hidden>Yükleniyor...</div>

  <!-- Error banner (validation errors, booking conflict, staff not found, network errors) -->
  <div class="booking-alert booking-alert--error" id="booking-error" role="alert" hidden>
    <p id="booking-error-message"></p>
  </div>

  <form class="booking-form" id="booking-form" novalidate>
    <!-- Step 1: Procedure (filled from GET /procedures) -->
    <fieldset class="booking-step" id="step-procedure">
      <legend>1. İşlem</legend>
      <label for="procedure-select">İşlem seçin</label>
      <select id="procedure-select" name="procedure_id" required>
        <option value="" disabled selected>İşlem seçin</option>
        <!-- <option value="{procedure.id}">{procedure.operation}</option> -->
      </select>
      <small class="field-error" id="procedure-error" hidden></small>
    </fieldset>

    <!-- Step 2: Staff (filled from GET /staff/list-by-procedure?procedure_id={id}) -->
    <fieldset class="booking-step" id="step-staff" disabled>
      <legend>2. Uzman</legend>
      <label for="staff-select">Uzman seçin</label>
      <select id="staff-select" name="staff_id" required>
        <option value="" disabled selected>Önce bir işlem seçin</option>
        <!-- <option value="{staff.id}">{staff.first_name} {staff.last_name} – {staff.title}</option> -->
      </select>
      <small class="field-error" id="staff-error" hidden></small>
    </fieldset>

    <!-- Step 3: Date and time -->
    <fieldset class="booking-step" id="step-datetime" disabled>
      <legend>3. Tarih ve Saat</legend>

      <label for="booking-date">Tarih</label>
      <input type="date" id="booking-date" name="date" required>
      <small class="field-error" id="date-error" hidden></small>

      <!-- Every booking lasts 30 minutes; the backend sets end_time -->
      <label for="start-time">Saat <span class="field-hint">(30 dakika)</span></label>
      <input type="time" id="start-time" name="start_time" step="1800" required>
      <small class="field-error" id="time-error" hidden></small>

      <!-- Optional: clickable 30-minute slot buttons, if you later add an availability endpoint -->
      <div class="time-slots" id="time-slots" hidden>
        <!-- <button type="button" class="time-slot" data-start="10:00">10:00</button> -->
      </div>
    </fieldset>

    <!-- Step 4: Customer details -->
    <fieldset class="booking-step" id="step-customer">
      <legend>4. Bilgileriniz</legend>

      <label for="first-name">Ad</label>
      <input type="text" id="first-name" name="first_name" autocomplete="given-name" required>
      <small class="field-error" id="first-name-error" hidden></small>

      <label for="last-name">Soyad</label>
      <input type="text" id="last-name" name="last_name" autocomplete="family-name" required>
      <small class="field-error" id="last-name-error" hidden></small>

      <label for="phone-number">Telefon</label>
      <input type="tel" id="phone-number" name="phone_number" autocomplete="tel"
             inputmode="numeric" placeholder="5XX XXX XX XX" required>
      <small class="field-error" id="phone-error" hidden></small>
    </fieldset>

    <!-- Summary before submitting -->
    <section class="booking-summary" id="booking-summary" hidden>
      <h2>Randevu Özeti</h2>
      <dl>
        <dt>İşlem</dt>   <dd id="summary-procedure"></dd>
        <dt>Uzman</dt>   <dd id="summary-staff"></dd>
        <dt>Tarih</dt>   <dd id="summary-date"></dd>
        <dt>Saat</dt>    <dd id="summary-time"></dd>
        <dt>Ad Soyad</dt><dd id="summary-name"></dd>
        <dt>Telefon</dt> <dd id="summary-phone"></dd>
      </dl>
    </section>

    <div class="booking-actions">
      <button type="reset" id="booking-reset" class="btn btn--secondary">Temizle</button>
      <button type="submit" id="booking-submit" class="btn btn--primary">Randevu Al</button>
    </div>
  </form>

  <!-- Shown after POST /booking/ succeeds (filled from BookingView) -->
  <section class="booking-confirmation" id="booking-confirmation" hidden>
    <h2>Randevunuz oluşturuldu</h2>
    <p>Onay mesajı <strong id="confirm-phone"></strong> numarasına SMS olarak gönderildi.</p>
    <dl>
      <dt>Ad Soyad</dt><dd id="confirm-name"></dd>
      <dt>İşlem</dt>   <dd id="confirm-procedure"></dd>
      <dt>Uzman</dt>   <dd id="confirm-staff"></dd>
      <dt>Başlangıç</dt><dd id="confirm-start"></dd>
      <dt>Bitiş</dt>   <dd id="confirm-end"></dd>
    </dl>
    <button type="button" id="booking-new" class="btn btn--primary">Yeni Randevu</button>
  </section>
</main>
`;
