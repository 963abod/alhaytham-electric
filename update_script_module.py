with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_tag = '<script type="module">'
end_tag = '</script>'

start_pos = html.find(start_tag)
end_pos = html.find(end_tag, start_pos)

if start_pos != -1 and end_pos != -1:
    new_script = r"""<script type="module">
  import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

  const SUPABASE_URL = 'https://eftlniajfnvvzmxswgtj.supabase.co';
  const SUPABASE_KEY = 'sb_publishable_6ypXec8dblC0ZHq7ERXUuw_TzXAZTnu';
  const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

  // Icons
  const ICONS = {
    solar: '<path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/><circle cx="12" cy="12" r="5"/>',
    maintenance: '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    wiring: '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
    inverter: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 12h10"/><path d="M12 7v10"/>',
    pump: '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
    camera: '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
    battery: '<rect x="2" y="6" width="17" height="12" rx="2"/><path d="M22 10v4"/><path d="M6 10v4"/><path d="M10 10v4"/><path d="M14 10v4"/>',
    video: '<polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>',
    default: '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>'
  };

  const svgIcon = (key) => `<div class="ic-wrap"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">${ICONS[key]||ICONS.default}</svg></div>`;
  const waLink = (phone, msg) => `https://wa.me/${(phone||'').replace(/[^0-9]/g,'')}${msg?('?text='+encodeURIComponent(msg)):''}`;

  /* =========================================
     VIDEO HELPER UTILITIES
     ========================================= */
  function getVideoEmbedInfo(url) {
    if (!url || typeof url !== 'string') return null;
    url = url.trim();
    if (!url) return null;

    // YouTube
    let ytMatch = url.match(/(?:youtube\.com\/(?:[^/]+\/.+\/|(?:v|e(?:mbed)?|shorts)\/|.*[?&]v=)|youtu\.be\/)([^"&?/\s]{11})/i);
    if (ytMatch && ytMatch[1]) {
      return {
        type: 'youtube',
        id: ytMatch[1],
        embedUrl: `https://www.youtube.com/embed/${ytMatch[1]}?autoplay=1&muted=1&playsinline=1`
      };
    }

    // Vimeo
    let vimeoMatch = url.match(/vimeo\.com\/(?:channels\/(?:\w+\/)?|groups\/[^/]*\/videos\/|album\/\d+\/video\/|video\/|)(\d+)/i);
    if (vimeoMatch && vimeoMatch[1]) {
      return {
        type: 'vimeo',
        id: vimeoMatch[1],
        embedUrl: `https://player.vimeo.com/video/${vimeoMatch[1]}?autoplay=1&muted=1`
      };
    }

    // Direct MP4 / WebM / Generic Video URL
    if (/\.(mp4|webm|ogg|mov)(\?.*)?$/i.test(url) || url.startsWith('http://') || url.startsWith('https://')) {
      return {
        type: 'direct',
        url: url
      };
    }

    return null;
  }

  function renderVideoPlayerHTML(videoUrl, options = {}) {
    const info = getVideoEmbedInfo(videoUrl);
    if (!info) return '';

    const controls = options.controls !== false;
    const autoplay = options.autoplay !== false;
    const muted = options.muted !== false;

    if (info.type === 'youtube' || info.type === 'vimeo') {
      return `
        <div class="responsive-video-wrap">
          <iframe
            src="${info.embedUrl}"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          ></iframe>
        </div>
      `;
    } else if (info.type === 'direct') {
      return `
        <div class="responsive-video-wrap">
          <video
            src="${info.url}"
            ${controls ? 'controls' : ''}
            ${autoplay ? 'autoplay' : ''}
            ${muted ? 'muted' : ''}
            loop
            playsinline
          ></video>
        </div>
      `;
    }
    return '';
  }

  /* =========================================
     TOAST NOTIFICATIONS
     ========================================= */
  window.showToast = function(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>${type === 'success' ? '✅' : '⚠️'}</span> <span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3200);
  };

  /* =========================================
     GLOBAL DATA STATE
     ========================================= */
  let productsData = [];
  let galleryData = [];

  /* =========================================
     PRODUCT PAGE & DETAIL MODAL
     ========================================= */
  let productPageOpen = false;
  let productHistoryAdded = false;

  window.openProduct = function(p) {
    const detail = document.getElementById('product-detail');
    const imageWrap = document.getElementById('pd-img-wrap');
    const name = document.getElementById('pd-name');
    const desc = document.getElementById('pd-desc');
    const whatsapp = document.getElementById('pd-wa');

    if (p.video_url && getVideoEmbedInfo(p.video_url)) {
      imageWrap.innerHTML = renderVideoPlayerHTML(p.video_url, { controls: true, autoplay: true, muted: true });
    } else if (p.image_url) {
      imageWrap.innerHTML = `<img src="${p.image_url}" alt="${p.name}" loading="eager">`;
    } else {
      imageWrap.innerHTML = `
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true">
          <rect x="3" y="4" width="18" height="16" rx="1"/>
          <path d="M3 9h18M3 14h18M9 4v16M15 4v16"/>
        </svg>
      `;
    }

    name.textContent = p.name || '';
    desc.textContent = p.description || 'لا يوجد وصف لهذا المنتج حالياً.';

    whatsapp.href = waLink(
      window.__phone,
      p.whatsapp_message || (`مرحباً، بدي أستفسر عن ${p.name}`)
    );

    productPageOpen = true;
    document.body.classList.add('product-view-open');
    detail.classList.add('open');

    if (!productHistoryAdded) {
      history.pushState({ productPage: true, productId: p.id || null }, '', '#product');
      productHistoryAdded = true;
    }

    window.scrollTo({ top: 0, behavior: 'instant' });
  };

  window.closeProduct = function(fromPopState = false) {
    const detail = document.getElementById('product-detail');
    productPageOpen = false;

    document.body.classList.remove('product-view-open');
    detail.classList.remove('open');

    if (!fromPopState && productHistoryAdded) {
      productHistoryAdded = false;
      if (location.hash === '#product') {
        history.back();
      }
    } else {
      productHistoryAdded = false;
    }

    setTimeout(() => {
      if (!productPageOpen) {
        document.getElementById('pd-img-wrap').innerHTML = '';
        document.getElementById('pd-name').textContent = '';
        document.getElementById('pd-desc').textContent = '';
      }
    }, 350);
  };

  window.addEventListener('popstate', function() {
    if (productPageOpen) closeProduct(true);
  });

  /* =========================================
     WORKS GALLERY LIGHTBOX
     ========================================= */
  let worksLightboxOpen = false;

  window.openWorksLightbox = function(itemOrUrl, captionText, videoUrl) {
    const overlay = document.getElementById('works-lightbox');
    const imgWrap = overlay ? overlay.querySelector('.gw-img-wrap') : null;
    const caption = document.getElementById('gw-caption');

    if (!overlay || !imgWrap || !caption) return;

    let imageUrl = '';
    let itemVideo = '';
    let title = '';

    if (typeof itemOrUrl === 'object' && itemOrUrl !== null) {
      imageUrl = itemOrUrl.image_url || '';
      itemVideo = itemOrUrl.video_url || '';
      title = itemOrUrl.caption || itemOrUrl.description || '';
    } else {
      imageUrl = itemOrUrl || '';
      title = captionText || '';
      itemVideo = videoUrl || '';
    }

    if (itemVideo && getVideoEmbedInfo(itemVideo)) {
      imgWrap.innerHTML = renderVideoPlayerHTML(itemVideo, { controls: true, autoplay: true, muted: true });
    } else {
      imgWrap.innerHTML = `<img id="gw-img" src="${imageUrl}" alt="${title}">`;
    }

    caption.textContent = title;
    overlay.classList.add('open');
    worksLightboxOpen = true;
    document.body.style.overflow = 'hidden';
  };

  window.closeWorksLightbox = function() {
    const overlay = document.getElementById('works-lightbox');
    if (!overlay) return;

    overlay.classList.remove('open');
    worksLightboxOpen = false;
    document.body.style.overflow = '';

    setTimeout(() => {
      if (!worksLightboxOpen) {
        const imgWrap = overlay.querySelector('.gw-img-wrap');
        const caption = document.getElementById('gw-caption');
        if (imgWrap) imgWrap.innerHTML = '<img id="gw-img" src="" alt="">';
        if (caption) caption.textContent = '';
      }
    }, 300);
  };

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && worksLightboxOpen) closeWorksLightbox();
  });

  document.addEventListener('DOMContentLoaded', function() {
    const worksOverlay = document.getElementById('works-lightbox');
    if (worksOverlay) {
      worksOverlay.addEventListener('click', function(e) {
        if (e.target === worksOverlay) closeWorksLightbox();
      });
    }
  });

  /* =========================================
     PRODUCTS CAROUSEL RENDERING
     ========================================= */
  function renderProductsCarousel() {
    const carousel = document.getElementById('products-carousel');
    const dotsContainer = document.getElementById('carousel-dots');
    if (!carousel) return;

    carousel.innerHTML = '';
    if (dotsContainer) dotsContainer.innerHTML = '';

    if (!productsData || !productsData.length) {
      carousel.innerHTML = '<p style="color:var(--ink-muted);padding:20px;">لا توجد منتجات حالياً.</p>';
      return;
    }

    productsData.forEach((p, idx) => {
      const card = document.createElement('div');
      card.className = 'p-card-carousel';
      card.style.cursor = 'pointer';

      const hasVideo = p.video_url && getVideoEmbedInfo(p.video_url);
      const videoBadgeHTML = hasVideo ? `<div class="video-badge"><svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg> فيديو</div>` : '';

      let thumbContent = '';
      if (hasVideo) {
        thumbContent = renderVideoPlayerHTML(p.video_url, { controls: false, autoplay: false, muted: true });
      } else if (p.image_url) {
        thumbContent = `<img src="${p.image_url}" alt="${p.name}">`;
      } else {
        thumbContent = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3"><rect x="3" y="4" width="18" height="16" rx="1"/><path d="M3 9h18M3 14h18M9 4v16M15 4v16"/></svg>`;
      }

      card.innerHTML = `
        ${videoBadgeHTML}
        <div class="p-thumb">${thumbContent}</div>
        <div class="p-body">
          ${p.category ? `<span style="font-size:0.75rem;color:var(--gold-bright);font-weight:700;">${p.category}</span>` : ''}
          <h3>${p.name}</h3>
          <p>${p.description || ''}</p>
          <a class="btn-outline" target="_blank" rel="noopener" href="${waLink(window.__phone, p.whatsapp_message || ('مرحباً، بدي أستفسر عن ' + p.name))}">استفسر الآن</a>
        </div>
      `;

      card.querySelector('.btn-outline').addEventListener('click', e => e.stopPropagation());
      card.addEventListener('click', () => openProduct(p));
      carousel.appendChild(card);

      if (dotsContainer) {
        const dot = document.createElement('div');
        dot.className = `carousel-dot ${idx === 0 ? 'active' : ''}`;
        dot.addEventListener('click', () => {
          card.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' });
        });
        dotsContainer.appendChild(dot);
      }
    });

    setupCarouselControls();
  }

  function setupCarouselControls() {
    const carousel = document.getElementById('products-carousel');
    const prevBtn = document.getElementById('carousel-prev');
    const nextBtn = document.getElementById('carousel-next');
    const dotsContainer = document.getElementById('carousel-dots');

    if (!carousel) return;

    if (prevBtn) {
      prevBtn.onclick = () => {
        carousel.scrollBy({ left: -300, behavior: 'smooth' });
      };
    }
    if (nextBtn) {
      nextBtn.onclick = () => {
        carousel.scrollBy({ left: 300, behavior: 'smooth' });
      };
    }

    carousel.onscroll = () => {
      if (!dotsContainer) return;
      const cards = carousel.querySelectorAll('.p-card-carousel');
      const dots = dotsContainer.querySelectorAll('.carousel-dot');
      const scrollLeft = Math.abs(carousel.scrollLeft);

      cards.forEach((card, i) => {
        if (card.offsetLeft <= scrollLeft + 150 && card.offsetLeft + card.offsetWidth > scrollLeft) {
          dots.forEach(d => d.classList.remove('active'));
          if (dots[i]) dots[i].classList.add('active');
        }
      });
    };
  }

  /* =========================================
     WORKS GALLERY RENDERING
     ========================================= */
  function renderGallery() {
    const wGrid = document.getElementById('works-grid');
    if (!wGrid) return;
    wGrid.innerHTML = '';

    if (galleryData && galleryData.length) {
      galleryData.forEach(g => {
        const div = document.createElement('div');
        div.className = 'w-tile';
        div.style.cursor = 'pointer';
        div.style.position = 'relative';

        const hasVideo = g.video_url && getVideoEmbedInfo(g.video_url);
        const videoBadge = hasVideo ? `<div class="video-badge"><svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg> فيديو</div>` : '';

        if (g.image_url) {
          div.innerHTML = `${videoBadge}<img src="${g.image_url}" alt="${g.caption || ''}">`;
        } else if (hasVideo) {
          div.innerHTML = `${videoBadge}${renderVideoPlayerHTML(g.video_url, { controls: false, autoplay: false, muted: true })}`;
        } else {
          div.innerHTML = `${videoBadge}<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="m3 16 5-5 4 4 4-6 5 7"/></svg>${g.caption || ''}`;
        }

        div.addEventListener('click', () => openWorksLightbox(g));
        wGrid.appendChild(div);
      });
    } else {
      const div = document.createElement('div');
      div.className = 'w-tile';
      div.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="m3 16 5-5 4 4 4-6 5 7"/></svg>سيتم إضافة صور الأعمال قريباً`;
      wGrid.appendChild(div);
    }
  }

  /* =========================================
     ADMIN PANEL MANAGEMENT LOGIC
     ========================================= */
  let activeAdminTab = 'products';
  let editingItem = null;
  let editingMode = 'add'; // 'add' or 'edit'

  window.openAdminModal = function() {
    const overlay = document.getElementById('admin-overlay');
    if (overlay) {
      overlay.classList.add('open');
      renderAdminList();
    }
  };

  window.closeAdminModal = function() {
    const overlay = document.getElementById('admin-overlay');
    if (overlay) overlay.classList.remove('open');
  };

  window.switchAdminTab = function(tab) {
    activeAdminTab = tab;
    document.getElementById('tab-btn-products').classList.toggle('active', tab === 'products');
    document.getElementById('tab-btn-projects').classList.toggle('active', tab === 'projects');
    document.getElementById('admin-add-item-btn').textContent = tab === 'products' ? '+ إضافة منتج جديد' : '+ إضافة عمل جديد';
    renderAdminList();
  };

  function renderAdminList() {
    const listContainer = document.getElementById('admin-list-container');
    const searchVal = (document.getElementById('admin-search-input')?.value || '').toLowerCase();
    if (!listContainer) return;

    listContainer.innerHTML = '';
    const items = activeAdminTab === 'products' ? productsData : galleryData;

    const filtered = items.filter(item => {
      const title = (item.name || item.caption || item.title || '').toLowerCase();
      const desc = (item.description || '').toLowerCase();
      const cat = (item.category || '').toLowerCase();
      return title.includes(searchVal) || desc.includes(searchVal) || cat.includes(searchVal);
    });

    if (!filtered.length) {
      listContainer.innerHTML = '<p style="color:var(--ink-muted);padding:20px;text-align:center;">لا توجد عناصر لعرضها.</p>';
      return;
    }

    filtered.forEach(item => {
      const card = document.createElement('div');
      card.className = 'admin-item-card';

      const title = item.name || item.caption || 'بدون عنوان';
      const sub = item.category ? `الفئة: ${item.category}` : (item.description || '');
      const thumb = item.image_url ? `<img src="${item.image_url}" alt="">` : (item.video_url ? '🎥' : '📷');
      const hasVideo = item.video_url && getVideoEmbedInfo(item.video_url);

      card.innerHTML = `
        <div class="admin-item-info">
          <div class="admin-item-thumb">
            ${typeof thumb === 'string' && thumb.startsWith('<img') ? thumb : `<span style="font-size:1.4rem;">${thumb}</span>`}
          </div>
          <div class="admin-item-details">
            <h4>${title} ${hasVideo ? '<span style="color:var(--gold-bright);font-size:0.75rem;">(🎥 فيديو)</span>' : ''}</h4>
            <p>${sub}</p>
          </div>
        </div>
        <div class="admin-item-actions">
          <button class="btn-action-edit" type="button"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg> تعديل</button>
          <button class="btn-action-delete" type="button"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg> حذف</button>
        </div>
      `;

      card.querySelector('.btn-action-edit').addEventListener('click', () => openItemEditor('edit', item));
      card.querySelector('.btn-action-delete').addEventListener('click', () => deleteAdminItem(item));
      listContainer.appendChild(card);
    });
  }

  /* =========================================
     ITEM EDITOR MODAL & LIVE PREVIEW
     ========================================= */
  window.openItemEditor = function(mode = 'add', item = null) {
    editingMode = mode;
    editingItem = item;

    const overlay = document.getElementById('editor-modal-overlay');
    const titleEl = document.getElementById('editor-title');

    const isProduct = activeAdminTab === 'products';

    document.getElementById('editor-item-type').value = activeAdminTab;
    document.getElementById('editor-item-id').value = item ? item.id : '';

    titleEl.textContent = mode === 'edit'
      ? (isProduct ? '✏️ تعديل المنتج' : '✏️ تعديل العمل / المشروع')
      : (isProduct ? '➕ إضافة منتج جديد' : '➕ إضافة عمل جديد');

    document.getElementById('label-name').textContent = isProduct ? 'اسم المنتج *' : 'عنوان العمل / الصورة *';
    document.getElementById('group-category').style.display = isProduct ? 'block' : 'none';
    document.getElementById('group-wa').style.display = isProduct ? 'block' : 'none';

    document.getElementById('editor-name').value = item ? (item.name || item.caption || '') : '';
    document.getElementById('editor-category').value = item ? (item.category || '') : '';
    document.getElementById('editor-desc').value = item ? (item.description || '') : '';
    document.getElementById('editor-image').value = item ? (item.image_url || '') : '';
    document.getElementById('editor-video').value = item ? (item.video_url || '') : '';
    document.getElementById('editor-wa').value = item ? (item.whatsapp_message || '') : '';
    document.getElementById('editor-sort').value = item ? (item.sort_order || 0) : 0;

    updateFormVideoPreview();
    overlay.classList.add('open');
  };

  window.closeItemEditor = function() {
    const overlay = document.getElementById('editor-modal-overlay');
    if (overlay) overlay.classList.remove('open');
  };

  window.updateFormVideoPreview = function() {
    const videoUrl = document.getElementById('editor-video')?.value;
    const previewContainer = document.getElementById('form-video-preview');
    if (!previewContainer) return;

    if (videoUrl && getVideoEmbedInfo(videoUrl)) {
      previewContainer.innerHTML = renderVideoPlayerHTML(videoUrl, { controls: true, autoplay: false, muted: true });
    } else {
      previewContainer.innerHTML = '<span style="color:var(--ink-muted);">أدخل رابط فيديو صحيح (YouTube, Vimeo, أو MP4) للمعاينة المباشرة</span>';
    }
  };

  window.handleItemSave = async function(e) {
    e.preventDefault();
    const saveBtn = document.getElementById('editor-save-btn');
    saveBtn.disabled = true;
    saveBtn.textContent = 'جاري الحفظ...';

    const itemType = document.getElementById('editor-item-type').value;
    const itemId = document.getElementById('editor-item-id').value;
    const nameVal = document.getElementById('editor-name').value.trim();
    const categoryVal = document.getElementById('editor-category').value.trim();
    const descVal = document.getElementById('editor-desc').value.trim();
    const imageVal = document.getElementById('editor-image').value.trim();
    const videoVal = document.getElementById('editor-video').value.trim();
    const waVal = document.getElementById('editor-wa').value.trim();
    const sortVal = parseInt(document.getElementById('editor-sort').value) || 0;

    const tableName = itemType === 'products' ? 'products' : 'gallery';

    let payload = {};
    if (itemType === 'products') {
      payload = {
        name: nameVal,
        category: categoryVal,
        description: descVal,
        image_url: imageVal,
        whatsapp_message: waVal,
        sort_order: sortVal
      };
      if (videoVal) payload.video_url = videoVal;
    } else {
      payload = {
        caption: nameVal,
        description: descVal,
        image_url: imageVal,
        sort_order: sortVal
      };
      if (videoVal) payload.video_url = videoVal;
    }

    try {
      if (editingMode === 'edit' && itemId) {
        let { data, error } = await supabase.from(tableName).update(payload).eq('id', itemId).select();
        if (error && error.code === 'PGRST204' && 'video_url' in payload) {
          delete payload.video_url;
          const retry = await supabase.from(tableName).update(payload).eq('id', itemId).select();
          data = retry.data;
          error = retry.error;
        }
        if (error) console.error('Supabase update error:', error);

        const list = itemType === 'products' ? productsData : galleryData;
        const index = list.findIndex(i => String(i.id) === String(itemId));
        if (index !== -1) {
          list[index] = { ...list[index], ...payload, video_url: videoVal };
        }
        showToast(itemType === 'products' ? 'تم تعديل المنتج بنجاح!' : 'تم تعديل المشروع بنجاح!');
      } else {
        let { data, error } = await supabase.from(tableName).insert([payload]).select();
        if (error && error.code === 'PGRST204' && 'video_url' in payload) {
          delete payload.video_url;
          const retry = await supabase.from(tableName).insert([payload]).select();
          data = retry.data;
          error = retry.error;
        }
        if (error) console.error('Supabase insert error:', error);

        const newRecord = (data && data[0]) ? data[0] : { id: String(Date.now()), ...payload, video_url: videoVal };
        if (itemType === 'products') {
          productsData.push(newRecord);
        } else {
          galleryData.push(newRecord);
        }
        showToast(itemType === 'products' ? 'تم إضافة المنتج بنجاح!' : 'تم إضافة المشروع بنجاح!');
      }

      renderProductsCarousel();
      renderGallery();
      renderAdminList();
      closeItemEditor();
    } catch (err) {
      console.error('Save error:', err);
      showToast('حدث خطأ أثناء الحفظ، يرجى المحاولة مرة أخرى', 'error');
    } finally {
      saveBtn.disabled = false;
      saveBtn.textContent = 'حفظ التعديلات';
    }
  };

  async function deleteAdminItem(item) {
    if (!confirm(`هل أنت تأكد من حذف "${item.name || item.caption}"؟`)) return;

    const itemType = activeAdminTab;
    const tableName = itemType === 'products' ? 'products' : 'gallery';

    try {
      const { error } = await supabase.from(tableName).delete().eq('id', item.id);
      if (error) console.error('Delete error:', error);

      if (itemType === 'products') {
        productsData = productsData.filter(i => String(i.id) !== String(item.id));
      } else {
        galleryData = galleryData.filter(i => String(i.id) !== String(item.id));
      }

      renderProductsCarousel();
      renderGallery();
      renderAdminList();
      showToast('تم حذف العنصر بنجاح!');
    } catch (err) {
      console.error('Delete failed:', err);
      showToast('تعذر حذف العنصر', 'error');
    }
  }

  /* =========================================
     SITE INITIALIZATION & DATA LOADING
     ========================================= */
  async function loadSite() {
    try {
      const { data: settings } = await supabase.from('site_settings').select('*').eq('id', 1).single();
      if (settings) {
        document.title = settings.workshop_name + ' | كهرباء وطاقة شمسية في حمص';
        const seoDescription = (settings.description || 'خدمات الكهرباء والطاقة الشمسية والتركيب والصيانة في حمص وضواحيها.') + ' | حمص وضواحيها';
        const metaDesc = document.querySelector('meta[name="description"]');
        if (metaDesc) metaDesc.setAttribute('content', seoDescription);

        document.getElementById('brand-name').innerHTML = `${settings.workshop_name}<small>حمص وضواحيها</small>`;
        document.getElementById('hero-title').textContent = settings.tagline || '';
        document.getElementById('hero-desc').textContent = settings.description || '';
        document.getElementById('about-text').textContent = settings.about_text || '';
        document.getElementById('contact-phone-label').textContent = 'الهاتف وواتساب: ' + (settings.phone || '');
        document.getElementById('contact-tel').href = 'tel:' + (settings.phone || '');
        const wa = waLink(settings.whatsapp || settings.phone || '');
        document.getElementById('contact-wa').href = wa;
        document.getElementById('nav-whatsapp').href = wa;
        document.getElementById('footer-copyright').textContent = `© ${new Date().getFullYear()} ${settings.workshop_name} — جميع الحقوق محفوظة`;

        const whyGrid = document.getElementById('why-grid');
        if (whyGrid) {
          whyGrid.innerHTML = '';
          (settings.why_us || []).forEach(text => {
            const div = document.createElement('div');
            div.className = 'why-item';
            div.innerHTML = `${svgIcon('default')}<h3>${text}</h3>`;
            whyGrid.appendChild(div);
          });
        }

        window.__phone = settings.whatsapp || settings.phone || '';
      }
    } catch (e) {
      console.warn('Settings load error:', e);
    }

    try {
      const { data: services } = await supabase.from('services').select('*').order('sort_order');
      const sGrid = document.getElementById('services-grid');
      if (sGrid) {
        sGrid.innerHTML = '';
        (services || []).forEach(s => {
          const div = document.createElement('div');
          div.className = 'card';
          div.innerHTML = `${svgIcon(s.icon)}<h3>${s.title}</h3><p>${s.description || ''}</p>`;
          sGrid.appendChild(div);
        });
      }
    } catch (e) {
      console.warn('Services load error:', e);
    }

    try {
      const { data: products, error: pError } = await supabase.from('products').select('*').order('category').order('sort_order');
      if (pError) console.warn('Products DB fetch error:', pError);
      if (products && products.length > 0) {
        productsData = products;
      } else {
        productsData = typeof DEFAULT_PRODUCTS !== 'undefined' ? DEFAULT_PRODUCTS : [];
      }
      renderProductsCarousel();
    } catch (e) {
      console.warn('Products load exception:', e);
      productsData = typeof DEFAULT_PRODUCTS !== 'undefined' ? DEFAULT_PRODUCTS : [];
      renderProductsCarousel();
    }

    try {
      const { data: gallery, error: gError } = await supabase.from('gallery').select('*').order('sort_order');
      if (gError) console.warn('Gallery DB fetch error:', gError);
      if (gallery && gallery.length > 0) {
        galleryData = gallery;
      } else {
        galleryData = typeof DEFAULT_GALLERY !== 'undefined' ? DEFAULT_GALLERY : [];
      }
      renderGallery();
    } catch (e) {
      console.warn('Gallery load exception:', e);
      galleryData = typeof DEFAULT_GALLERY !== 'undefined' ? DEFAULT_GALLERY : [];
      renderGallery();
    }

    document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
    renderAdminList();
  }

  function checkAdminRoute() {
    const path = window.location.pathname.toLowerCase();
    const hash = window.location.hash.toLowerCase();
    if (hash === '#admin' || hash === '#dashboard' || path.endsWith('/admin') || path.endsWith('/dashboard')) {
      openAdminModal();
    }
  }

  window.addEventListener('hashchange', checkAdminRoute);

  // Bind Event Listeners
  document.addEventListener('DOMContentLoaded', () => {
    checkAdminRoute();
    document.getElementById('open-admin-btn')?.addEventListener('click', openAdminModal);
    document.getElementById('close-admin-btn')?.addEventListener('click', closeAdminModal);

    document.getElementById('tab-btn-products')?.addEventListener('click', () => switchAdminTab('products'));
    document.getElementById('tab-btn-projects')?.addEventListener('click', () => switchAdminTab('projects'));

    document.getElementById('admin-search-input')?.addEventListener('input', renderAdminList);
    document.getElementById('admin-add-item-btn')?.addEventListener('click', () => openItemEditor('add'));

    document.getElementById('close-editor-btn')?.addEventListener('click', closeItemEditor);
    document.getElementById('cancel-editor-btn')?.addEventListener('click', closeItemEditor);
    document.getElementById('editor-form')?.addEventListener('submit', handleItemSave);
    document.getElementById('editor-video')?.addEventListener('input', updateFormVideoPreview);
  });

  loadSite();
</script>"""
    updated_html = html[:start_pos] + new_script + html[end_pos + len(end_tag):]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(updated_html)
    print("Successfully replaced script module.")
else:
    print("Error: Could not locate script tag.")
