import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's inspect CSS insertion point right before </style>
css_to_add = """
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

print("Script template ready")
