import re

# Read current index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Head / CSS - Insert before </style>
css_additions = """
  /* =========================================
     VIDEO PLAYER & BADGES
     ========================================= */
  .responsive-video-wrap {
    position: relative;
    width: 100%;
    aspect-ratio: 16/9;
    background: #000;
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--line);
  }
  .responsive-video-wrap iframe,
  .responsive-video-wrap video {
    width: 100%;
    height: 100%;
    border: 0;
    object-fit: contain;
  }
  .video-badge {
    position: absolute;
    top: 8px;
    right: 8px;
    background: rgba(10, 9, 8, 0.85);
    color: var(--gold-bright);
    border: 1px solid var(--line);
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 0.72rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    z-index: 3;
    backdrop-filter: blur(6px);
  }

  /* =========================================
     PRODUCTS HORIZONTAL CAROUSEL
     ========================================= */
  .products-carousel-container {
    position: relative;
    margin-top: 28px;
  }
  .products-carousel-wrap {
    display: flex;
    gap: 20px;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    scroll-behavior: smooth;
    padding: 12px 4px 24px 4px;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  .products-carousel-wrap::-webkit-scrollbar {
    display: none;
  }
  .p-card-carousel {
    flex: 0 0 clamp(270px, 78vw, 320px);
    scroll-snap-align: start;
    border: 1px solid var(--line);
    border-radius: var(--radius);
    overflow: hidden;
    background: linear-gradient(180deg, var(--bg-1), var(--bg-2));
    display: flex;
    flex-direction: column;
    transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease;
    position: relative;
  }
  .p-card-carousel:hover {
    transform: translateY(-6px);
    border-color: rgba(201,162,39,.5);
    box-shadow: 0 20px 40px -20px rgba(201,162,39,.6);
  }
  .carousel-controls {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 18px;
    padding: 0 8px;
  }
  .carousel-arrow {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: var(--bg-1);
    border: 1px solid var(--line);
    color: var(--gold-bright);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all .2s ease;
  }
  .carousel-arrow:hover:not(:disabled) {
    background: var(--gold-bright);
    color: var(--bg-0);
    border-color: var(--gold-bright);
  }
  .carousel-arrow:disabled {
    opacity: 0.35;
    cursor: not-allowed;
  }
  .carousel-dots {
    display: flex;
    gap: 8px;
    align-items: center;
    justify-content: center;
  }
  .carousel-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: rgba(201, 162, 39, 0.25);
    transition: all .25s ease;
    cursor: pointer;
  }
  .carousel-dot.active {
    width: 22px;
    border-radius: 999px;
    background: var(--gold-bright);
  }

  /* =========================================
     ADMIN PANEL & EDITOR MODAL
     ========================================= */
  .admin-trigger-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border-radius: 999px;
    background: rgba(201, 162, 39, 0.12);
    border: 1px solid var(--line);
    color: var(--gold-bright);
    font-size: 0.85rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: 'Almarai', sans-serif;
  }
  .admin-trigger-btn:hover {
    background: var(--gold-bright);
    color: var(--bg-0);
  }

  .admin-overlay {
    display: none;
    position: fixed;
    inset: 0;
    z-index: 200;
    background: rgba(10, 9, 8, 0.94);
    backdrop-filter: blur(14px);
    overflow-y: auto;
    padding: 24px 16px;
  }
  .admin-overlay.open {
    display: block;
  }
  .admin-container {
    max-width: 1000px;
    margin: 0 auto;
    background: var(--bg-1);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.8);
  }
  .admin-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 18px;
    border-bottom: 1px solid var(--line);
    margin-bottom: 20px;
    flex-wrap: wrap;
    gap: 12px;
  }
  .admin-header h2 {
    font-size: 1.4rem;
    margin: 0;
    color: var(--gold-bright);
  }
  .admin-tabs {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
    border-bottom: 1px solid var(--line);
    padding-bottom: 12px;
  }
  .admin-tab-btn {
    background: transparent;
    border: 1px solid transparent;
    color: var(--ink-muted);
    padding: 8px 18px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s;
    font-family: inherit;
  }
  .admin-tab-btn.active {
    background: var(--gold-dim);
    color: var(--gold-bright);
    border-color: var(--line);
  }
  .admin-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
    gap: 12px;
    flex-wrap: wrap;
  }
  .admin-search {
    flex: 1;
    min-width: 200px;
    padding: 10px 16px;
    background: var(--bg-2);
    border: 1px solid var(--line);
    border-radius: 999px;
    color: var(--ink);
    font-family: inherit;
    font-size: 0.9rem;
  }
  .admin-add-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 10px 20px;
    background: linear-gradient(180deg, var(--gold-bright), var(--gold));
    color: var(--bg-0);
    border: none;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.88rem;
    cursor: pointer;
    font-family: inherit;
    transition: transform 0.2s;
  }
  .admin-add-btn:hover {
    transform: translateY(-2px);
  }

  .admin-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .admin-item-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 18px;
    background: var(--bg-2);
    border: 1px solid var(--line);
    border-radius: 12px;
    gap: 16px;
    flex-wrap: wrap;
  }
  .admin-item-info {
    display: flex;
    align-items: center;
    gap: 14px;
    flex: 1;
    min-width: 240px;
  }
  .admin-item-thumb {
    width: 56px;
    height: 56px;
    border-radius: 8px;
    overflow: hidden;
    position: relative;
    background: var(--bg-0);
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--line);
  }
  .admin-item-thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  .admin-item-details h4 {
    margin: 0 0 4px;
    font-size: 0.98rem;
    font-weight: 700;
  }
  .admin-item-details p {
    margin: 0;
    font-size: 0.82rem;
    color: var(--ink-muted);
  }
  .admin-item-actions {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .btn-action-edit {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 7px 14px;
    border-radius: 8px;
    background: rgba(242, 201, 76, 0.15);
    color: var(--gold-bright);
    border: 1px solid rgba(201, 162, 39, 0.3);
    font-size: 0.82rem;
    font-weight: 700;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.2s;
  }
  .btn-action-edit:hover {
    background: var(--gold-bright);
    color: var(--bg-0);
  }
  .btn-action-delete {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 7px 14px;
    border-radius: 8px;
    background: rgba(235, 87, 87, 0.12);
    color: #eb5757;
    border: 1px solid rgba(235, 87, 87, 0.3);
    font-size: 0.82rem;
    font-weight: 700;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.2s;
  }
  .btn-action-delete:hover {
    background: #eb5757;
    color: #fff;
  }

  .editor-modal-overlay {
    display: none;
    position: fixed;
    inset: 0;
    z-index: 250;
    background: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(10px);
    overflow-y: auto;
    padding: 20px 16px;
  }
  .editor-modal-overlay.open {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .editor-modal {
    width: 100%;
    max-width: 650px;
    background: var(--bg-1);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 24px;
    margin: auto;
    position: relative;
    box-shadow: 0 20px 50px rgba(0,0,0,0.9);
  }
  .form-group {
    margin-bottom: 16px;
  }
  .form-group label {
    display: block;
    font-size: 0.86rem;
    font-weight: 700;
    margin-bottom: 6px;
    color: var(--ink);
  }
  .form-control {
    width: 100%;
    padding: 11px 14px;
    background: var(--bg-2);
    border: 1px solid var(--line);
    border-radius: 10px;
    color: var(--ink);
    font-family: inherit;
    font-size: 0.9rem;
    transition: border-color 0.2s;
  }
  .form-control:focus {
    outline: none;
    border-color: var(--gold-bright);
  }
  textarea.form-control {
    min-height: 80px;
    resize: vertical;
  }
  .form-actions {
    display: flex;
    gap: 12px;
    justify-content: flex-end;
    margin-top: 24px;
  }

  .toast-container {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 300;
    display: flex;
    flex-direction: column;
    gap: 10px;
    pointer-events: none;
  }
  .toast {
    pointer-events: auto;
    background: var(--bg-2);
    border: 1px solid var(--gold);
    color: var(--ink);
    padding: 12px 20px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 0.9rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    gap: 10px;
    animation: toastIn 0.3s ease forwards;
  }
  @keyframes toastIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }
"""

html = html.replace('</style>', css_additions + '\n</style>')

# 2. Add Admin button in Header
nav_button_html = """    <button class="admin-trigger-btn" id="open-admin-btn" type="button"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg> لوحة التحكم</button>
    <a class="cta-mini" id="nav-whatsapp" href="#" target="_blank" rel="noopener">واتساب</a>"""

html = html.replace('<a class="cta-mini" id="nav-whatsapp" href="#" target="_blank" rel="noopener">واتساب</a>', nav_button_html)

# 3. Replace Products Grid with Products Carousel HTML
carousel_html = """      <div class="products-carousel-container">
        <div class="products-carousel-wrap" id="products-carousel"></div>
        <div class="carousel-controls">
          <button class="carousel-arrow prev" id="carousel-prev" type="button" aria-label="السابق">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m9 18 6-6-6-6"/></svg>
          </button>
          <div class="carousel-dots" id="carousel-dots"></div>
          <button class="carousel-arrow next" id="carousel-next" type="button" aria-label="التالي">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m15 18-6-6 6-6"/></svg>
          </button>
        </div>
      </div>"""

html = html.replace('<div class="grid-products" id="products-grid"></div>', carousel_html)

# 4. Insert Admin Overlay and Editor Modals before </body>
modals_html = """
<!-- Admin Panel Modal -->
<div id="admin-overlay" class="admin-overlay" role="dialog" aria-modal="true" aria-label="لوحة التحكم">
  <div class="admin-container">
    <div class="admin-header">
      <h2>🛠️ لوحة تحكم ورشة الهيثم</h2>
      <button class="pd-close" type="button" id="close-admin-btn" style="margin:0;">✕ إغلاق</button>
    </div>
    <div class="admin-tabs">
      <button class="admin-tab-btn active" id="tab-btn-products" type="button">📦 إدارة المنتجات</button>
      <button class="admin-tab-btn" id="tab-btn-projects" type="button">🖼️ إدارة أعمالنا والمشاريع</button>
    </div>
    <div class="admin-toolbar">
      <input type="text" id="admin-search-input" class="admin-search" placeholder="بحث في العناصر...">
      <button class="admin-add-btn" id="admin-add-item-btn" type="button">+ إضافة منتج جديد</button>
    </div>
    <div id="admin-list-container" class="admin-list"></div>
  </div>
</div>

<!-- Item Editor Modal (Create / Edit) -->
<div id="editor-modal-overlay" class="editor-modal-overlay" role="dialog" aria-modal="true" aria-label="تعديل العنصر">
  <div class="editor-modal">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:18px;border-bottom:1px solid var(--line);padding-bottom:12px;">
      <h3 id="editor-title" style="margin:0;font-size:1.2rem;color:var(--gold-bright);">تعديل العنصر</h3>
      <button class="pd-close" type="button" id="close-editor-btn" style="margin:0;padding:6px 12px;min-height:auto;">✕</button>
    </div>
    <form id="editor-form">
      <input type="hidden" id="editor-item-id">
      <input type="hidden" id="editor-item-type">

      <div class="form-group">
        <label id="label-name" for="editor-name">اسم المنتج / العنوان *</label>
        <input type="text" id="editor-name" class="form-control" required placeholder="أدخل الاسم">
      </div>

      <div class="form-group" id="group-category">
        <label for="editor-category">الفئة / التصنيف</label>
        <input type="text" id="editor-category" class="form-control" placeholder="مثال: إنفرترات، بطاريات، ألواح">
      </div>

      <div class="form-group">
        <label for="editor-desc">الوصف</label>
        <textarea id="editor-desc" class="form-control" placeholder="أدخل تفاصيل الوصف..."></textarea>
      </div>

      <div class="form-group">
        <label for="editor-image">رابط الصورة (Image URL)</label>
        <input type="url" id="editor-image" class="form-control" placeholder="https://example.com/image.jpg">
      </div>

      <div class="form-group">
        <label for="editor-video">رابط الفيديو (Video URL - YouTube, Vimeo, or MP4)</label>
        <input type="url" id="editor-video" class="form-control" placeholder="https://www.youtube.com/watch?v=... أو https://example.com/video.mp4">
      </div>

      <div class="form-group">
        <label>معاينة الفيديو المباشرة:</label>
        <div id="form-video-preview" style="background:var(--bg-2);border:1px dashed var(--line);border-radius:12px;padding:12px;text-align:center;min-height:120px;display:flex;align-items:center;justify-content:center;color:var(--ink-muted);font-size:0.85rem;">
          أدخل رابط فيديو صحيح للمعاينة المباشرة
        </div>
      </div>

      <div class="form-group" id="group-wa">
        <label for="editor-wa">رسالة واتساب المخصصة (اختياري)</label>
        <input type="text" id="editor-wa" class="form-control" placeholder="مرحباً، بدي أستفسر عن هذا المنتج">
      </div>

      <div class="form-group">
        <label for="editor-sort">ترتيب العرض (Sort Order)</label>
        <input type="number" id="editor-sort" class="form-control" value="0">
      </div>

      <div class="form-actions">
        <button type="button" class="btn-ghost" id="cancel-editor-btn" style="padding:9px 20px;">إلغاء</button>
        <button type="submit" id="editor-save-btn" class="btn-primary" style="padding:9px 26px;">حفظ التعديلات</button>
      </div>
    </form>
  </div>
</div>

<div id="toast-container" class="toast-container"></div>
"""

if 'id="admin-overlay"' not in html:
    html = html.replace('</body>', modals_html + '\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('HTML updated with CSS, carousel markup, and Admin modals.')
