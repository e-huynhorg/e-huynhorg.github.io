// Language management
class LanguageManager {
  constructor() {
    this.currentLang = 'en';
    this.fallbackLang = 'en';
    this.translations = {};
    this.loadedLanguages = new Set();
    
    // Initialize
    this.init();
  }
  
  async init() {
    // Get language from URL parameter, localStorage, or browser preference
    const urlParams = new URLSearchParams(window.location.search);
    const urlLang = urlParams.get('lang');
    const storedLang = localStorage.getItem('preferred-language');
    const browserLang = navigator.language.slice(0, 2);
    
    // Priority: URL > localStorage > browser > default
    this.currentLang = urlLang || storedLang || (browserLang === 'sv' || browserLang === 'vi' ? browserLang : 'en');
    
    // Set up language selector
    const langSelect = document.getElementById('language-select');
    langSelect.value = this.currentLang;
    langSelect.addEventListener('change', (e) => this.switchLanguage(e.target.value));
    
    // Load and apply initial language
    await this.loadLanguage(this.currentLang);
    this.updateContent();
    
    // Set up email (after language is loaded)
    this.setupEmail();
  }
  
  async loadLanguage(lang) {
    if (this.loadedLanguages.has(lang)) {
      return;
    }
    
    try {
      const response = await fetch(`lang/${lang}.json`);
      if (response.ok) {
        this.translations[lang] = await response.json();
        this.loadedLanguages.add(lang);
      } else {
        console.warn(`Failed to load language: ${lang}`);
        // Load fallback if not already loaded
        if (lang !== this.fallbackLang && !this.loadedLanguages.has(this.fallbackLang)) {
          await this.loadLanguage(this.fallbackLang);
        }
      }
    } catch (error) {
      console.error(`Error loading language ${lang}:`, error);
      // Load fallback if not already loaded
      if (lang !== this.fallbackLang && !this.loadedLanguages.has(this.fallbackLang)) {
        await this.loadLanguage(this.fallbackLang);
      }
    }
  }
  
  async switchLanguage(lang) {
    document.body.classList.add('loading');
    
    // Load language if not already loaded
    await this.loadLanguage(lang);
    
    this.currentLang = lang;
    this.updateContent();
    
    // Save preference
    localStorage.setItem('preferred-language', lang);
    
    // Update URL
    const url = new URL(window.location);
    url.searchParams.set('lang', lang);
    window.history.replaceState({}, '', url);
    
    // Update HTML lang attribute
    document.documentElement.lang = lang;
    
    document.body.classList.remove('loading');
  }
  
  getText(key) {
    const translation = this.translations[this.currentLang];
    const fallbackTranslation = this.translations[this.fallbackLang];
    
    // Navigate through nested object keys (e.g., "sections.whoami.title")
    const getNestedValue = (obj, path) => {
      return path.split('.').reduce((current, key) => current && current[key], obj);
    };
    
    const text = getNestedValue(translation, key);
    const fallbackText = getNestedValue(fallbackTranslation, key);
    
    return text || fallbackText || key;
  }
  
  updateContent() {
    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(element => {
      const key = element.getAttribute('data-i18n');
      const text = this.getText(key);
      
      if (text && text !== key) {
        element.innerHTML = text;
      }
    });
    
    // Update education list
    this.updateEducationList();
    
    // Update CV links
    this.updateCVLinks();
    
    // Update page title
    const name = this.getText('header.name');
    document.title = `${name} - Landing Page`;
  }
  
  updateEducationList() {
    const educationList = document.getElementById('education-list');
    const translation = this.translations[this.currentLang] || this.translations[this.fallbackLang];
    
    if (translation && translation.sections && translation.sections.education && translation.sections.education.items) {
      educationList.innerHTML = '';
      translation.sections.education.items.forEach(item => {
        const li = document.createElement('li');
        li.innerHTML = item;
        educationList.appendChild(li);
      });
    }
  }
  
  updateCVLinks() {
    const cvLinksContainer = document.getElementById('cv-links');
    const translation = this.translations[this.currentLang] || this.translations[this.fallbackLang];
    
    if (translation && translation.sections && translation.sections.cv && translation.sections.cv.links) {
      cvLinksContainer.innerHTML = '';
      translation.sections.cv.links.forEach(link => {
        const a = document.createElement('a');
        a.href = link.href;
        a.title = link.title;
        a.textContent = link.text;
        cvLinksContainer.appendChild(a);
      });
    }
  }
  
  setupEmail() {
    // Build email dynamically to avoid bots
    const user = "evan";
    const domain = "e-huynh.org";
    const email = `${user}@${domain}`;
    const emailSpan = document.getElementById("email");
    emailSpan.textContent = email;
  }
}

// Initialize language manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.langManager = new LanguageManager();
});
