<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import Sidebar from '../../components/layout/Sidebar.vue'
import InactivityOverlay from '../../components/layout/InactivityOverlay.vue'
import { useJournalStore } from '../../stores/journal'

const journalStore = useJournalStore()

// ── State ─────────────────────────────────────────────────────────────────────
const activeTab = ref('private') // 'private' | 'shared'
const view = ref('list') // 'list' | 'editor' | 'reader'

const currentNotebook = ref(null)
const editorContent = ref('')
const editorTitle = ref('')
const showNewNotebook = ref(false)
const newNotebookTitle = ref('')
const showDeleteConfirm = ref(false)
const notebookToDelete = ref(null)
const showShareConfirm = ref(false)
const notebookToShare = ref(null)
const showConvertConfirm = ref(false)
const notebookToConvert = ref(null)

// ── Computed ──────────────────────────────────────────────────────────────────
const notebooks = computed(() => {
  return activeTab.value === 'private' 
    ? journalStore.privateJournals 
    : journalStore.sharedJournals
})

const isLoading = computed(() => journalStore.isLoading)
const isSaving = computed(() => journalStore.isSaving)

const filteredNotebooks = computed(() => notebooks.value)

const breadcrumbs = computed(() => {
  const crumbs = [{ label: 'Journals', action: () => { view.value = 'list'; currentNotebook.value = null } }]
  if (view.value === 'list') {
    crumbs.push({ label: activeTab.value === 'private' ? 'Private' : 'Shared', action: null })
  } else if (currentNotebook.value) {
    crumbs.push({ label: activeTab.value === 'private' ? 'Private' : 'Shared', action: () => { view.value = 'list'; currentNotebook.value = null } })
    crumbs.push({ label: currentNotebook.value.title, action: null })
  }
  return crumbs
})

const isEdited = computed(() => {
  if (!currentNotebook.value) return false
  return editorTitle.value !== currentNotebook.value.title || editorContent.value !== currentNotebook.value.content
})

// ── API Calls ─────────────────────────────────────────────────────────────────
const fetchJournals = async () => {
  try {
    if (activeTab.value === "private") {
      await journalStore.fetchPrivateJournals(1, 10)
    } else {
      await journalStore.fetchSharedJournals(1, 10)
    }
  } catch (err) {
    console.error("Failed to fetch journals:", err)
  }
}

// ── Lifecycle ─────────────────────────────────────────────────────────────────
onMounted(() => {
  fetchJournals()
})

// Watch tab changes
watch(activeTab, async () => {
  view.value = "list"
  currentNotebook.value = null
  await fetchJournals()
})

// ── Markdown helpers ──────────────────────────────────────────────────────────
const renderMarkdown = (text) => {
  if (!text) return ''
  return text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/~~(.+?)~~/g, '<del>$1</del>')
    .replace(/^### (.+)$/gm, '<h3 class="md-h3">$1</h3>')
    .replace(/^## (.+)$/gm, '<h2 class="md-h2">$1</h2>')
    .replace(/^# (.+)$/gm, '<h1 class="md-h1">$1</h1>')
    .replace(/^- (.+)$/gm, '<li class="md-li">$1</li>')
    .replace(/^---$/gm, '<hr class="md-hr"/>')
    .replace(/\n/g, '<br/>')
}

const renderMarkdownWithMarkers = (text) => {
  if (!text) return ''
  return text
    .replace(/(\*\*)(.+?)(\*\*)/g, '<span class="md-marker">$1</span><strong>$2</strong><span class="md-marker">$3</span>')
    .replace(/(\*)(.+?)(\*)/g, '<span class="md-marker">$1</span><em>$2</em><span class="md-marker">$3</span>')
    .replace(/(~~)(.+?)(~~)/g, '<span class="md-marker">$1</span><del>$2</del><span class="md-marker">$3</span>')
    .replace(/^(###) (.+)$/gm, '<span class="md-marker">$1 </span><h3 class="md-h3-inline">$2</h3>')
    .replace(/^(##) (.+)$/gm, '<span class="md-marker">$1 </span><h2 class="md-h2-inline">$2</h2>')
    .replace(/^(#) (.+)$/gm, '<span class="md-marker">$1 </span><h1 class="md-h1-inline">$2</h1>')
    .replace(/^(-) (.+)$/gm, '<span class="md-marker">$1</span> <span class="md-li-inline">$2</span>')
    .replace(/^---$/gm, '<hr class="md-hr"/>')
    .replace(/\n/g, '<br/>')
}

// ── Formatting helpers ────────────────────────────────────────────────────────
const textareaRef = ref(null)

const applyFormat = (type) => {
  const textarea = textareaRef.value
  if (!textarea) return
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const selectedText = editorContent.value.substring(start, end)
  let formatted = ''

  switch(type) {
    case 'bold':
      formatted = `**${selectedText}**`
      break
    case 'italic':
      formatted = `*${selectedText}*`
      break
    case 'strike':
      formatted = `~~${selectedText}~~`
      break
    case 'h1':
      formatted = `# ${selectedText}`
      break
    case 'h2':
      formatted = `## ${selectedText}`
      break
    case 'h3':
      formatted = `### ${selectedText}`
      break
    case 'bullet':
      formatted = `- ${selectedText}`
      break
    case 'hr':
      formatted = '---'
      break
  }

  editorContent.value = editorContent.value.substring(0, start) + formatted + editorContent.value.substring(end)
  setTimeout(() => {
    textarea.focus()
    textarea.setSelectionRange(start + formatted.length, start + formatted.length)
  }, 10)
}

// ── Actions ───────────────────────────────────────────────────────────────────
const openNotebook = (notebook) => {
  currentNotebook.value = notebook
  editorTitle.value = notebook.title
  editorContent.value = notebook.content
  view.value = notebook.visibility === 'private' ? 'editor' : 'reader'
  journalStore.setCurrentJournal(notebook)
}

const createNotebook = async () => {
  if (!newNotebookTitle.value.trim()) return

  try {
    const newJournal = await journalStore.createJournal({
      title: newNotebookTitle.value,
      content: "express what you wish",
      visibility: "private"
    })

    showNewNotebook.value = false
    newNotebookTitle.value = ""

    openNotebook(newJournal)
  } catch (err) {
    console.error("Failed to create journal:", err)
  }
}

const saveNotebook = async () => {
  if (!currentNotebook.value) return

  try {
    const updated = await journalStore.updateJournal(currentNotebook.value.id, {
      title: editorTitle.value,
      content: editorContent.value
    })

    currentNotebook.value = updated
  } catch (err) {
    console.error("Failed to update journal:", err)
  }
}

const shareNotebook = async (notebook) => {
  try {
    await journalStore.updateJournal(notebook.id, {
      visibility: "shared"
    })

    await fetchJournals()

    showShareConfirm.value = false
    notebookToShare.value = null
    view.value = "list"
    currentNotebook.value = null
  } catch (err) {
    console.error("Failed to share journal:", err)
  }
}

const deleteNotebook = async (notebook) => {
  try {
    await journalStore.deleteJournal(notebook.id)

    showDeleteConfirm.value = false
    notebookToDelete.value = null
    view.value = "list"
    currentNotebook.value = null
  } catch (err) {
    console.error("Failed to delete journal:", err)
  }
}

const convertToMemory = async (notebook) => {
  try {
    await journalStore.convertToMemory(notebook.id)
    await fetchJournals()

    showConvertConfirm.value = false
    notebookToConvert.value = null
  } catch (err) {
    console.error("Failed to convert journal:", err)
  }
}

const formatDate = (iso) => new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
const truncate = (text, max = 80) => !text ? '' : text.length > max ? text.slice(0, max) + '…' : text
const stripMarkdown = (text) => text.replace(/[*#~\-_]/g, '').replace(/\n/g, ' ')
</script>

<template>
  <InactivityOverlay>
    <Sidebar>
    <div class="journal-page">
      <component :is="'style'">
        @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');
      </component>

      <!-- Background -->
      <div class="pointer-events-none select-none absolute inset-0 overflow-hidden" aria-hidden="true">
        <div class="absolute top-0 right-0 w-80 h-80 rounded-full opacity-20" style="background:radial-gradient(circle,#ddd6fe 0%,transparent 70%);"></div>
        <div class="absolute bottom-0 left-0 w-64 h-64 rounded-full opacity-15" style="background:radial-gradient(circle,#fce7f3 0%,transparent 70%);"></div>
        <svg class="absolute top-12 left-8 w-32 opacity-[0.04]" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="40" fill="#7c3aed"/>
          <circle cx="30" cy="40" r="15" fill="#a855f7"/>
          <circle cx="70" cy="60" r="12" fill="#c084fc"/>
        </svg>
      </div>

      <!-- Content -->
      <div class="relative z-10 max-w-4xl mx-auto px-4 sm:px-8 py-10">

        <!-- Breadcrumbs -->
        <div class="flex items-center gap-4 mb-6">
          <div class="flex gap-1" v-for="(crumb, idx) in breadcrumbs" :key="idx">
            <button v-if="crumb.action" @click="crumb.action"
                    class="journal-breadcrumb journal-breadcrumb--link">
              {{ crumb.label }}
            </button>
            <span v-else class="journal-breadcrumb">{{ crumb.label }}</span>
            <svg v-if="idx < breadcrumbs.length - 1" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#c4b5fd" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading && view === 'list'" class="flex items-center justify-center min-h-[400px]">
          <div class="flex flex-col items-center gap-3">
            <div class="flex gap-1">
              <span class="w-2 h-2 rounded-full bg-purple-400 loading-dot" style="animation-delay:0s"></span>
              <span class="w-2 h-2 rounded-full bg-purple-400 loading-dot" style="animation-delay:0.2s"></span>
              <span class="w-2 h-2 rounded-full bg-purple-400 loading-dot" style="animation-delay:0.4s"></span>
            </div>
            <p class="journal-body text-sm text-purple-400 tracking-wide">Loading journals…</p>
          </div>
        </div>

        <!-- ══════════════════ LIST VIEW ══════════════════ -->
        <div v-else-if="view === 'list'">

          <!-- Header -->
          <div class="mb-8">
            <div class="flex items-end justify-between mb-4">
              <div>
                <p class="journal-sub">Your notebooks</p>
                <h1 class="journal-display">Journals</h1>
              </div>
              <button @click="showNewNotebook = true" class="journal-btn journal-btn--primary">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                New Notebook
              </button>
            </div>
            <!-- Divider -->
            <div class="flex items-center gap-3">
              <div class="h-px flex-1" style="background:linear-gradient(90deg,#7c3aed,#c084fc,transparent);"></div>
              <svg width="10" height="10" viewBox="0 0 24 24" fill="#a855f7" stroke="none"><rect x="3" y="2" width="18" height="20" rx="2"/><line x1="8" y1="2" x2="8" y2="22" stroke="white" stroke-width="1"/></svg>
              <div class="h-px w-8" style="background:#c084fc;"></div>
            </div>
          </div>

          <!-- Tabs -->
          <div class="flex gap-2 mb-6">
            <button @click="activeTab = 'private'"
                    :class="['journal-tab', activeTab === 'private' ? 'journal-tab--active' : '']">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              Private
            </button>
            <button @click="activeTab = 'shared'"
                    :class="['journal-tab', activeTab === 'shared' ? 'journal-tab--active' : '']">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
              Shared
            </button>
          </div>

          <!-- Notebooks grid -->
          <div v-if="filteredNotebooks.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <article v-for="(notebook, idx) in filteredNotebooks" :key="notebook.id"
                     class="journal-card"
                     :style="`animation-delay: ${idx * 50}ms`">

              <!-- Card body (clickable) -->
              <div @click="openNotebook(notebook)" class="cursor-pointer flex-1">
                <div class="flex items-start gap-3 mb-3">
                  <div class="journal-card-icon">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
                  </div>
                  <div class="flex-1 min-w-0">
                    <h3 class="journal-card-title">{{ notebook.title }}</h3>
                    <p class="journal-card-date">{{ formatDate(notebook.edited_at) }}</p>
                  </div>
                </div>
                <p class="journal-card-preview">{{ truncate(stripMarkdown(notebook.content), 90) }}</p>
              </div>

              <!-- Actions (only for private) -->
              <div v-if="activeTab === 'private'" class="journal-card-actions">
                <button @click.stop="notebookToConvert = notebook; showConvertConfirm = true"
                        class="journal-action-btn journal-action-btn--convert"
                        title="Convert to Memory">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
                </button>
                <button @click.stop="notebookToShare = notebook; showShareConfirm = true"
                        class="journal-action-btn journal-action-btn--share"
                        title="Share with Partner">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
                </button>
                <button @click.stop="notebookToDelete = notebook; showDeleteConfirm = true"
                        class="journal-action-btn journal-action-btn--delete"
                        title="Delete Notebook">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>
                </button>
              </div>
            </article>
          </div>

          <!-- Empty state -->
          <div v-else class="text-center py-20">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#ddd6fe" stroke-width="1.5" class="mx-auto mb-4">
              <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
            </svg>
            <p class="journal-body text-gray-400 text-sm">No {{ activeTab }} notebooks yet.</p>
            <button @click="showNewNotebook = true" class="journal-btn journal-btn--secondary mt-4">Create One</button>
          </div>
        </div>

        <!-- ══════════════════ EDITOR VIEW ══════════════════ -->
        <div v-else-if="view === 'editor'" class="journal-editor-wrapper">

          <!-- Toolbar -->
          <div class="journal-toolbar">
            <div class="flex items-center gap-1">
              <button @click="applyFormat('bold')" class="toolbar-btn" title="Bold">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 4h8a4 4 0 0 1 4 4 4 4 0 0 1-4 4H6z"/><path d="M6 12h9a4 4 0 0 1 4 4 4 4 0 0 1-4 4H6z"/></svg>
              </button>
              <button @click="applyFormat('italic')" class="toolbar-btn" title="Italic">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="19" y1="4" x2="10" y2="4"/><line x1="14" y1="20" x2="5" y2="20"/><line x1="15" y1="4" x2="9" y2="20"/></svg>
              </button>
              <button @click="applyFormat('strike')" class="toolbar-btn" title="Strikethrough">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M17.3 4.9c-2.3-.6-4.4-1-6.2-.9-2.7.1-5.3 1.1-6.6 3.1-.5.8-.9 1.7-.9 2.6 0 .7.3 1.4.7 1.9l10.8-.2"/><path d="M4 11.5h16"/><path d="M6.7 19.1c2.3.6 4.4 1 6.2.9 2.7-.1 5.3-1.1 6.6-3.1.5-.8.9-1.7.9-2.6 0-.7-.3-1.4-.7-1.9l-10.8.2"/></svg>
              </button>
              <div class="w-px h-5 bg-purple-100 mx-1"></div>
              <button @click="applyFormat('h1')" class="toolbar-btn" title="Heading 1">H1</button>
              <button @click="applyFormat('h2')" class="toolbar-btn" title="Heading 2">H2</button>
              <button @click="applyFormat('h3')" class="toolbar-btn" title="Heading 3">H3</button>
              <div class="w-px h-5 bg-purple-100 mx-1"></div>
              <button @click="applyFormat('bullet')" class="toolbar-btn" title="Bullet">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
              </button>
              <button @click="applyFormat('hr')" class="toolbar-btn" title="Divider">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="3" y1="12" x2="21" y2="12"/></svg>
              </button>
            </div>
            <div class="flex items-center gap-2">
              <span v-if="isEdited" class="journal-body text-xs text-purple-400 flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-purple-400 animate-pulse"></span>
                Unsaved
              </span>
              <button @click="saveNotebook" :disabled="isSaving || !isEdited" class="journal-btn journal-btn--primary journal-btn--sm">
                <svg v-if="isSaving" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="animate-spin"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
                {{ isSaving ? 'Saving…' : 'Save' }}
              </button>
            </div>
          </div>

          <!-- Title input -->
          <input v-model="editorTitle" type="text" placeholder="Notebook title…"
                 class="journal-editor-title"/>

          <!-- Editor textarea -->
          <textarea ref="textareaRef" v-model="editorContent"
                    placeholder="Start writing…"
                    class="journal-editor-textarea"></textarea>

          <!-- Live preview with faint markers -->
          <div class="journal-editor-preview">
            <div class="journal-editor-preview-label">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
              Live Preview
            </div>
            <div class="journal-editor-preview-content" v-html="renderMarkdownWithMarkers(editorContent)"></div>
          </div>

          <!-- Markdown guide hint -->
          <div class="journal-editor-hint">
            <p class="journal-body text-xs text-gray-400">
              <strong>Markdown tips:</strong> **bold** · *italic* · ~~strike~~ · # Heading · - List · --- Divider
            </p>
          </div>
        </div>

        <!-- ══════════════════ READER VIEW ══════════════════ -->
        <div v-else-if="view === 'reader'" class="journal-reader">
          <div class="journal-reader-header">
            <h1 class="journal-reader-title">{{ currentNotebook.title }}</h1>
            <p class="journal-reader-date">Last edited {{ formatDate(currentNotebook.edited_at) }}</p>
            <div class="journal-reader-badge">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
              Shared with your partner
            </div>
          </div>
          <div class="journal-reader-content" v-html="renderMarkdown(currentNotebook.content)"></div>
        </div>

      </div>

      <!-- ══════════════════ MODALS ══════════════════ -->

      <!-- New Notebook Modal -->
      <Transition name="modal-fade">
        <div v-if="showNewNotebook" class="journal-modal-overlay" @click.self="showNewNotebook = false">
          <div class="journal-modal">
            <h3 class="journal-modal-title">New Notebook</h3>
            <div class="mt-4">
              <label class="journal-label">Notebook Title</label>
              <input v-model="newNotebookTitle" type="text" placeholder="Untitled" class="journal-input"
                     @keyup.enter="createNotebook"/>
            </div>
            <div class="flex gap-2 mt-5">
              <button @click="createNotebook" :disabled="!newNotebookTitle.trim()" class="journal-btn journal-btn--primary">Create</button>
              <button @click="showNewNotebook = false; newNotebookTitle = ''" class="journal-btn journal-btn--ghost">Cancel</button>
            </div>
          </div>
        </div>
      </Transition>

      <!-- Delete Confirm -->
      <Transition name="modal-fade">
        <div v-if="showDeleteConfirm" class="journal-modal-overlay" @click.self="showDeleteConfirm = false">
          <div class="journal-modal journal-modal--danger">
            <h3 class="journal-modal-title text-red-600">Delete Notebook?</h3>
            <p class="journal-body text-sm text-gray-600 mt-2">This will permanently delete <strong>{{ notebookToDelete?.title }}</strong>. This cannot be undone.</p>
            <div class="flex gap-2 mt-5">
              <button @click="deleteNotebook(notebookToDelete)" class="journal-btn journal-btn--danger">Delete</button>
              <button @click="showDeleteConfirm = false; notebookToDelete = null" class="journal-btn journal-btn--ghost">Cancel</button>
            </div>
          </div>
        </div>
      </Transition>

      <!-- Share Confirm -->
      <Transition name="modal-fade">
        <div v-if="showShareConfirm" class="journal-modal-overlay" @click.self="showShareConfirm = false">
          <div class="journal-modal">
            <h3 class="journal-modal-title">Share Notebook?</h3>
            <p class="journal-body text-sm text-gray-600 mt-2">Your partner will be able to read <strong>{{ notebookToShare?.title }}</strong>. You won't be able to edit it after sharing.</p>
            <div class="flex gap-2 mt-5">
              <button @click="shareNotebook(notebookToShare)" class="journal-btn journal-btn--primary">Share</button>
              <button @click="showShareConfirm = false; notebookToShare = null" class="journal-btn journal-btn--ghost">Cancel</button>
            </div>
          </div>
        </div>
      </Transition>

      <!-- Convert Confirm -->
      <Transition name="modal-fade">
        <div v-if="showConvertConfirm" class="journal-modal-overlay" @click.self="showConvertConfirm = false">
          <div class="journal-modal">
            <h3 class="journal-modal-title">Convert to Memory?</h3>
            <p class="journal-body text-sm text-gray-600 mt-2">This will create a new memory from <strong>{{ notebookToConvert?.title }}</strong>. The notebook will remain in your journals.</p>
            <div class="flex gap-2 mt-5">
              <button @click="convertToMemory(notebookToConvert)" class="journal-btn journal-btn--primary">Convert</button>
              <button @click="showConvertConfirm = false; notebookToConvert = null" class="journal-btn journal-btn--ghost">Cancel</button>
            </div>
          </div>
        </div>
      </Transition>
    </div>
    </Sidebar>
  </InactivityOverlay>

</template>

<!-- <style scoped>
.journal-page {
  background: linear-gradient(160deg, #faf5ff 0%, #ffffff 50%, #f8f9ff 100%);
  min-height: 100vh;
  position: relative;
}

/* Typography */
.journal-display { font-family: 'Crimson Pro', Georgia, serif; font-size: 2.5rem; font-weight: 600; color: #1e293b; line-height: 1.2; }
.journal-sub { font-family: 'DM Sans', sans-serif; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: #9333ea; margin-bottom: 0.25rem; }
.journal-body { font-family: 'DM Sans', sans-serif; }

/* Breadcrumbs */
.journal-breadcrumb {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8125rem;
  color: #94a3b8;
}
.journal-breadcrumb--link {
  color: #7c3aed;
  cursor: pointer;
  transition: color 0.15s;
}
.journal-breadcrumb--link:hover {
  color: #a855f7;
}

/* Buttons */
.journal-btn {
  font-family: 'DM Sans', sans-serif;
  padding: 0.625rem 1.25rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.15s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}
.journal-btn--primary {
  background: linear-gradient(135deg, #7c3aed, #9333ea);
  color: white;
  box-shadow: 0 2px 8px rgba(124,58,237,0.2);
}
.journal-btn--primary:hover { background: linear-gradient(135deg, #6d28d9, #7e22ce); }
.journal-btn--primary:disabled { opacity: 0.5; cursor: not-allowed; }
.journal-btn--secondary {
  background: #f3f4f6;
  color: #374151;
}
.journal-btn--secondary:hover { background: #e5e7eb; }
.journal-btn--ghost {
  background: transparent;
  border: 1px solid #e5e7eb;
  color: #6b7280;
}
.journal-btn--ghost:hover { background: #f9fafb; }
.journal-btn--danger {
  background: #ef4444;
  color: white;
}
.journal-btn--danger:hover { background: #dc2626; }
.journal-btn--sm {
  padding: 0.5rem 1rem;
  font-size: 0.8125rem;
}

/* Tabs */
.journal-tab {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.625rem 1.25rem;
  border-radius: 0.75rem;
  transition: all 0.15s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
}
.journal-tab:hover { background: #f1f5f9; color: #475569; }
.journal-tab--active {
  background: linear-gradient(135deg, #7c3aed, #9333ea);
  color: white;
  box-shadow: 0 2px 8px rgba(124,58,237,0.2);
}

/* Cards */
.journal-card {
  background: white;
  border-radius: 1rem;
  padding: 1.25rem;
  border: 1px solid #f1f5f9;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  animation: cardReveal 0.4s cubic-bezier(0.22,1,0.36,1) both;
}
.journal-card:hover {
  box-shadow: 0 8px 24px rgba(124,58,237,0.1);
  transform: translateY(-2px);
}

@keyframes cardReveal {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.journal-card-icon {
  width: 2rem;
  height: 2rem;
  border-radius: 0.5rem;
  background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
}

.journal-card-title {
  font-family: 'Crimson Pro', Georgia, serif;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  line-height: 1.3;
}

.journal-card-date {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  color: #94a3b8;
}

.journal-card-preview {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.875rem;
  color: #64748b;
  line-height: 1.5;
}

.journal-card-actions {
  display: flex;
  gap: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid #f1f5f9;
}

.journal-action-btn {
  width: 2rem;
  height: 2rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}

.journal-action-btn--convert {
  background: #fef3c7;
  color: #f59e0b;
}
.journal-action-btn--convert:hover { background: #fef3c7; color: #d97706; }

.journal-action-btn--share {
  background: #dbeafe;
  color: #3b82f6;
}
.journal-action-btn--share:hover { background: #bfdbfe; color: #2563eb; }

.journal-action-btn--delete {
  background: #fee2e2;
  color: #ef4444;
}
.journal-action-btn--delete:hover { background: #fecaca; color: #dc2626; }

/* Editor */
.journal-editor-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.journal-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background: white;
  border-radius: 0.75rem;
  border: 1px solid #f1f5f9;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  flex-wrap: wrap;
  gap: 0.75rem;
}

.toolbar-btn {
  width: 2rem;
  height: 2rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  transition: all 0.15s ease;
}
.toolbar-btn:hover {
  background: #f1f5f9;
  color: #475569;
}

.journal-editor-title {
  font-family: 'Crimson Pro', Georgia, serif;
  font-size: 2rem;
  font-weight: 600;
  padding: 1.25rem;
  border: 2px solid #f1f5f9;
  border-radius: 0.75rem;
  background: white;
  transition: border 0.15s ease;
}
.journal-editor-title:focus {
  outline: none;
  border-color: #c084fc;
}

.journal-editor-textarea {
  font-family: 'DM Sans', sans-serif;
  font-size: 1rem;
  line-height: 1.75;
  padding: 1.25rem;
  border: 2px solid #f1f5f9;
  border-radius: 0.75rem;
  background: white;
  min-height: 20rem;
  resize: vertical;
  transition: border 0.15s ease;
}
.journal-editor-textarea:focus {
  outline: none;
  border-color: #c084fc;
}

.journal-editor-preview {
  background: white;
  border: 2px solid #f1f5f9;
  border-radius: 0.75rem;
  padding: 1.25rem;
}

.journal-editor-preview-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #94a3b8;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.journal-editor-preview-content {
  font-family: 'DM Sans', sans-serif;
  font-size: 1rem;
  line-height: 1.75;
  color: #334155;
}

.journal-editor-hint {
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.75rem;
}

/* Markdown styles */
.md-marker {
  color: #cbd5e1;
  font-size: 0.875em;
}

.md-h1, .md-h1-inline { font-size: 2rem; font-weight: 700; color: #1e293b; margin: 1rem 0; }
.md-h2, .md-h2-inline { font-size: 1.5rem; font-weight: 700; color: #334155; margin: 0.875rem 0; }
.md-h3, .md-h3-inline { font-size: 1.25rem; font-weight: 700; color: #475569; margin: 0.75rem 0; }
.md-li, .md-li-inline { margin-left: 1.5rem; color: #64748b; }
.md-hr { border: none; border-top: 2px solid #e2e8f0; margin: 1.5rem 0; }

/* Reader */
.journal-reader {
  background: white;
  border-radius: 1rem;
  padding: 2.5rem;
  border: 1px solid #f1f5f9;
  box-shadow: 0 4px 16px rgba(0,0,0,0.04);
}

.journal-reader-header {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 2px solid #f1f5f9;
}

.journal-reader-title {
  font-family: 'Crimson Pro', Georgia, serif;
  font-size: 2.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.journal-reader-date {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.875rem;
  color: #94a3b8;
  margin-bottom: 1rem;
}

.journal-reader-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #faf5ff;
  border: 1px solid #e9d5ff;
  border-radius: 0.5rem;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #7c3aed;
}

.journal-reader-content {
  font-family: 'DM Sans', sans-serif;
  font-size: 1.125rem;
  line-height: 1.75;
  color: #334155;
}

/* Modals */
.journal-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15,23,42,0.6);
  backdrop-filter: blur(4px);
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.journal-modal {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  max-width: 28rem;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.journal-modal--danger {
  border: 2px solid #fee2e2;
}

.journal-modal-title {
  font-family: 'Crimson Pro', Georgia, serif;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
}

.journal-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
  display: block;
  margin-bottom: 0.5rem;
}

.journal-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #f1f5f9;
  border-radius: 0.75rem;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.875rem;
  transition: border 0.15s ease;
}
.journal-input:focus {
  outline: none;
  border-color: #c084fc;
}

/* Loading dots */
.loading-dot {
  animation: dotPulse 1.2s ease-in-out infinite;
}
@keyframes dotPulse {
  0%,100% { opacity: 0.3; transform: scale(0.8); }
  50% { opacity: 1; transform: scale(1.2); }
}

/* Modal transitions */
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.2s ease;
}
.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}
</style> -->

<style scoped>
/* ── Page ────────────────────────────────────────────────────────── */
.journal-page {
  min-height: 100vh;
  position: relative;
  background: linear-gradient(160deg, #fefbff 0%, #ffffff 50%, #fdf4ff 100%);
}

/* ── Typography ──────────────────────────────────────────────────── */
.journal-display { font-family: 'Crimson Pro', Georgia, serif; font-size: clamp(2.5rem, 5vw, 3rem); font-weight: 600; color: #1f2937; line-height: 1.1; }
.journal-body    { font-family: 'DM Sans', sans-serif; }
.journal-sub     { font-family: 'DM Sans', sans-serif; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: #a855f7; font-weight: 500; margin-bottom: 4px; }

/* ── Breadcrumbs ─────────────────────────────────────────────────── */
.journal-breadcrumb {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  color: #9ca3af;
  font-weight: 500;
}
.journal-breadcrumb--link {
  color: #7c3aed;
  transition: color 0.15s;
  cursor: pointer;
}
.journal-breadcrumb--link:hover { color: #6d28d9; }

/* ── Tabs ────────────────────────────────────────────────────────── */
.journal-tab {
  display: flex; align-items: center; gap: 6px;
  padding: 8px 16px;
  border-radius: 10px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8125rem;
  font-weight: 500;
  color: #6b7280;
  background: white;
  border: 1.5px solid #f0ebff;
  cursor: pointer;
  transition: all 0.15s ease;
}
.journal-tab--active {
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  color: white;
  border-color: transparent;
  box-shadow: 0 4px 14px rgba(124,58,237,0.25);
}

/* ── Cards ───────────────────────────────────────────────────────── */
.journal-card {
  background: white;
  border: 1.5px solid #f3e8ff;
  border-radius: 16px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: 0 2px 12px rgba(124,58,237,0.04);
  transition: all 0.25s cubic-bezier(0.22,1,0.36,1);
  animation: cardSlideIn 0.4s cubic-bezier(0.22,1,0.36,1) both;
}
.journal-card:hover {
  border-color: #e9d5ff;
  box-shadow: 0 8px 24px rgba(124,58,237,0.12);
  transform: translateY(-2px);
}

@keyframes cardSlideIn {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

.journal-card-icon {
  width: 32px; height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #f3e8ff, #fdf4ff);
  display: flex; align-items: center; justify-content: center;
  color: #7c3aed;
  flex-shrink: 0;
}
.journal-card-title {
  font-family: 'Crimson Pro', Georgia, serif;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.3;
  margin: 0;
}
.journal-card-date {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.7rem;
  color: #9ca3af;
  margin-top: 2px;
}
.journal-card-preview {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8125rem;
  color: #6b7280;
  line-height: 1.6;
  display: -webkit-box;
  line-clamp: 2;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.journal-card-actions {
  display: flex;
  gap: 6px;
  padding-top: 8px;
  border-top: 1px solid #f3e8ff;
}
.journal-action-btn {
  width: 30px; height: 30px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  border: 1.5px solid;
  cursor: pointer;
  transition: all 0.18s ease;
}
.journal-action-btn--convert {
  border-color: #fce7f3;
  color: #db2777;
  background: white;
}
.journal-action-btn--convert:hover { background: #fdf2f8; border-color: #fbcfe8; }
.journal-action-btn--share {
  border-color: #ddd6fe;
  color: #7c3aed;
  background: white;
}
.journal-action-btn--share:hover { background: #f5f3ff; border-color: #c4b5fd; }
.journal-action-btn--delete {
  border-color: #fee2e2;
  color: #ef4444;
  background: white;
}
.journal-action-btn--delete:hover { background: #fef2f2; border-color: #fecaca; }

/* ── Editor ──────────────────────────────────────────────────────── */
.journal-editor-wrapper {
  background: white;
  border: 1.5px solid #f3e8ff;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 4px 24px rgba(124,58,237,0.08);
}
.journal-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 12px;
  border-bottom: 1.5px solid #f3e8ff;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 10px;
}
.toolbar-btn {
  width: 30px; height: 30px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: #6b7280;
  background: transparent;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.15s;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.7rem;
  font-weight: 600;
}
.toolbar-btn:hover {
  background: #faf5ff;
  color: #7c3aed;
  border-color: #e9d5ff;
}
.journal-editor-title {
  width: 100%;
  font-family: 'Crimson Pro', Georgia, serif;
  font-size: 2rem;
  font-weight: 600;
  color: #1f2937;
  border: none;
  outline: none;
  padding: 12px 0;
  margin-bottom: 8px;
}
.journal-editor-title::placeholder { color: #d1d5db; }
.journal-editor-textarea {
  width: 100%;
  min-height: 400px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9375rem;
  line-height: 1.8;
  color: #374151;
  border: none;
  outline: none;
  resize: vertical;
  padding: 8px 0;
}
.journal-editor-textarea::placeholder { color: #d1d5db; font-style: italic; }
.journal-editor-preview {
  border-top: 1.5px solid #f3e8ff;
  margin-top: 20px;
  padding-top: 20px;
}
.journal-editor-preview-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #a855f7;
  font-weight: 500;
  margin-bottom: 12px;
}
.journal-editor-preview-content {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9375rem;
  line-height: 1.8;
  color: #374151;
  min-height: 80px;
  padding: 16px;
  background: #faf5ff;
  border-radius: 12px;
  border: 1px solid #f3e8ff;
}
/* Faint markdown markers in preview */
.journal-editor-preview-content :deep(.md-marker) {
  color: #d1d5db;
  font-weight: 400;
  opacity: 0.4;
}
/* Inline heading styles for preview */
.journal-editor-preview-content :deep(.md-h1-inline) {
  font-family: 'Crimson Pro', serif;
  font-size: 1.75rem;
  font-weight: 600;
  color: #1f2937;
  display: inline;
}
.journal-editor-preview-content :deep(.md-h2-inline) {
  font-family: 'Crimson Pro', serif;
  font-size: 1.4rem;
  font-weight: 600;
  color: #1f2937;
  display: inline;
}
.journal-editor-preview-content :deep(.md-h3-inline) {
  font-family: 'Crimson Pro', serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: #374151;
  display: inline;
}
.journal-editor-preview-content :deep(.md-li-inline) {
  margin-left: 4px;
}
.journal-editor-preview-content :deep(strong) { font-weight: 600; color: #1f2937; }
.journal-editor-preview-content :deep(em) { font-style: italic; color: #6b7280; }
.journal-editor-preview-content :deep(del) { text-decoration: line-through; opacity: 0.6; }
.journal-editor-preview-content :deep(.md-hr) {
  border: none;
  height: 1px;
  background: linear-gradient(90deg, transparent, #e9d5ff, transparent);
  margin: 16px 0;
  display: block;
}
.journal-editor-hint {
  padding-top: 12px;
  border-top: 1.5px solid #f3e8ff;
  margin-top: 12px;
}

/* ── Reader ──────────────────────────────────────────────────────── */
.journal-reader {
  background: white;
  border: 1.5px solid #f3e8ff;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 4px 24px rgba(124,58,237,0.08);
  max-width: 720px;
  margin: 0 auto;
}
.journal-reader-header {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1.5px solid #f3e8ff;
}
.journal-reader-title {
  font-family: 'Crimson Pro', Georgia, serif;
  font-size: 2.5rem;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.2;
  margin-bottom: 8px;
}
.journal-reader-date {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8125rem;
  color: #9ca3af;
  margin-bottom: 12px;
}
.journal-reader-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 8px;
  background: #fdf4ff;
  border: 1px solid #f0ebff;
  color: #7c3aed;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  font-weight: 500;
}
.journal-reader-content {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9375rem;
  line-height: 1.8;
  color: #374151;
}
.journal-reader-content :deep(.md-h1) {
  font-family: 'Crimson Pro', serif;
  font-size: 2rem;
  font-weight: 600;
  color: #1f2937;
  margin: 24px 0 12px;
  line-height: 1.2;
}
.journal-reader-content :deep(.md-h2) {
  font-family: 'Crimson Pro', serif;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 20px 0 10px;
  line-height: 1.3;
}
.journal-reader-content :deep(.md-h3) {
  font-family: 'Crimson Pro', serif;
  font-size: 1.2rem;
  font-weight: 600;
  color: #374151;
  margin: 16px 0 8px;
}
.journal-reader-content :deep(.md-li) {
  margin-left: 20px;
  list-style-type: disc;
  margin-bottom: 4px;
}
.journal-reader-content :deep(.md-hr) {
  border: none;
  height: 1px;
  background: linear-gradient(90deg, transparent, #e9d5ff, transparent);
  margin: 24px 0;
}
.journal-reader-content :deep(strong) { font-weight: 600; color: #1f2937; }
.journal-reader-content :deep(em) { font-style: italic; color: #6b7280; }
.journal-reader-content :deep(del) { text-decoration: line-through; opacity: 0.6; }

/* ── Buttons ─────────────────────────────────────────────────────── */
.journal-btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 9px 18px;
  border-radius: 12px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.18s ease;
  border: 1.5px solid transparent;
}
.journal-btn--sm { padding: 7px 14px; font-size: 0.75rem; }
.journal-btn--primary {
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  color: white;
  box-shadow: 0 4px 14px rgba(124,58,237,0.25);
}
.journal-btn--primary:hover:not(:disabled) {
  box-shadow: 0 6px 20px rgba(124,58,237,0.35);
  transform: translateY(-1px);
}
.journal-btn--primary:disabled { opacity: 0.5; cursor: not-allowed; }
.journal-btn--secondary {
  background: white;
  color: #7c3aed;
  border-color: #e9d5ff;
}
.journal-btn--secondary:hover { background: #faf5ff; border-color: #c084fc; }
.journal-btn--ghost {
  background: transparent;
  color: #6b7280;
  border-color: #e5e7eb;
}
.journal-btn--ghost:hover { background: #f9fafb; }
.journal-btn--danger {
  background: white;
  color: #ef4444;
  border-color: #fecaca;
}
.journal-btn--danger:hover { background: #fef2f2; border-color: #f87171; }

/* ── Modals ──────────────────────────────────────────────────────── */
.journal-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  background: rgba(10,5,25,0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.journal-modal {
  background: white;
  border-radius: 20px;
  padding: 24px;
  max-width: 400px;
  width: 100%;
  border: 1.5px solid #f3e8ff;
  box-shadow: 0 20px 60px rgba(124,58,237,0.2);
}
.journal-modal--danger {
  border-color: #fee2e2;
}
.journal-modal-title {
  font-family: 'Crimson Pro', Georgia, serif;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
}
.journal-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  display: block;
  margin-bottom: 6px;
}
.journal-input {
  width: 100%;
  padding: 10px 14px;
  border-radius: 12px;
  border: 1.5px solid #e9d5ff;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.875rem;
  color: #1f2937;
  background: white;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.journal-input:focus {
  border-color: #a855f7;
  box-shadow: 0 0 0 3px rgba(168,85,247,0.1);
}
.journal-input::placeholder { color: #d1d5db; }

/* ── Transitions ─────────────────────────────────────────────────── */
.modal-fade-enter-active, .modal-fade-leave-active { transition: all 0.25s ease; }
.modal-fade-enter-from, .modal-fade-leave-to       { opacity: 0; }
.modal-fade-enter-from .journal-modal,
.modal-fade-leave-to .journal-modal { transform: scale(0.95) translateY(12px); }

.animate-spin { animation: spin 1s linear infinite; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
</style>
