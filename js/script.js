document.addEventListener('DOMContentLoaded', () => {
  // --- Mobile Menu Toggle ---
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  const mobileMenuLinks = document.querySelectorAll('.mobile-menu-link');

  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
      const isOpen = !mobileMenu.classList.contains('hidden');
      mobileMenuBtn.innerHTML = isOpen 
        ? `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>`
        : `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>`;
    });

    mobileMenuLinks.forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.add('hidden');
        mobileMenuBtn.innerHTML = `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>`;
      });
    });
  }

  // --- Active Navigation Link on Scroll ---
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');

  window.addEventListener('scroll', () => {
    let currentSectionId = '';
    const scrollPosition = window.scrollY + 150; // Offset for header height

    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;
      if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
        currentSectionId = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('text-purple-400', 'font-semibold');
      if (link.getAttribute('href') === `#${currentSectionId}`) {
        link.classList.add('text-purple-400', 'font-semibold');
      }
    });
  });

  // --- Interactive AI Preventivo Calculator ---
  const projectTypeSelect = document.getElementById('calc-project-type');
  const calcFeaturesList = document.getElementById('calc-features');
  const calcUrgencySelect = document.getElementById('calc-urgency');
  
  const traditionalCostEl = document.getElementById('traditional-cost');
  const bwsCostEl = document.getElementById('bws-cost');
  const savingsEl = document.getElementById('calc-savings');
  const bwsMonthlyEl = document.getElementById('bws-monthly');
  const bwsTimeEl = document.getElementById('bws-time');
  const traditionalTimeEl = document.getElementById('traditional-time');
  const calculatorCta = document.getElementById('calculator-cta');

  // Define data for calculation
  const projectTypes = {
    'landing': { name: 'Landing Page Professionale', baseCost: 1500, bwsCost: 399, bwsMonthly: 19, traditionalDays: 14, bwsDays: 3, features: ['Moduli di contatto', 'Integrazioni Analytics', 'SEO di base', 'Responsive Design'] },
    'website': { name: 'Sito Vetrina o Aziendale', baseCost: 3500, bwsCost: 699, bwsMonthly: 29, traditionalDays: 30, bwsDays: 6, features: ['Fino a 5 pagine', 'Blog / Notizie', 'Moduli contatti avanzati', 'Copywriting AI', 'Responsive Design', 'SEO Avanzata'] },
    'webapp': { name: 'Applicazione Web Su Misura', baseCost: 8000, bwsCost: 1490, bwsMonthly: 59, traditionalDays: 60, bwsDays: 12, features: ['Database dedicato', 'Pannello di amministrazione', 'Autenticazione utenti', 'Integrazione API esterne', 'Interfaccia reattiva'] },
    'automation': { name: 'Automazione Processi / AI Agent', baseCost: 6000, bwsCost: 990, bwsMonthly: 49, traditionalDays: 45, bwsDays: 8, features: ['Integrazione ChatGPT/LLM', 'Sincronizzazione DB/CRM', 'Automazione email/lead', 'Analisi automatica dati', 'Notifiche Slack/Telegram'] }
  };

  const extraFeatures = {
    'chatbot': { name: 'Assistente Virtuale AI (Chatbot)', cost: 299, time: 1 },
    'multilang': { name: 'Supporto Multilingua automatico', cost: 199, time: 1 },
    'payments': { name: 'Integrazione Pagamenti (Stripe)', cost: 249, time: 1 },
    'seo-premium': { name: 'Pacchetto SEO Premium + Copywriting AI', cost: 249, time: 1 }
  };

  function updateCalculator() {
    if (!projectTypeSelect || !traditionalCostEl) return;

    const selectedType = projectTypeSelect.value;
    const projectData = projectTypes[selectedType];
    
    if (!projectData) return;

    let traditionalCost = projectData.baseCost;
    let bwsCost = projectData.bwsCost;
    let traditionalDays = projectData.traditionalDays;
    let bwsDays = projectData.bwsDays;

    // Check selected features
    const checkboxes = calcFeaturesList.querySelectorAll('input[type="checkbox"]:checked');
    checkboxes.forEach(checkbox => {
      const featureKey = checkbox.value;
      if (extraFeatures[featureKey]) {
        traditionalCost += extraFeatures[featureKey].cost * 2.5; // Traditional development costs more for features too
        bwsCost += extraFeatures[featureKey].cost;
        traditionalDays += extraFeatures[featureKey].time * 3;
        bwsDays += extraFeatures[featureKey].time;
      }
    });

    // Check urgency
    const urgency = calcUrgencySelect.value;
    if (urgency === 'urgent') {
      traditionalCost = Math.round(traditionalCost * 1.3);
      bwsCost = Math.round(bwsCost * 1.15); // BWS handles urgency with less surcharge due to AI speed
      traditionalDays = Math.round(traditionalDays * 0.7);
      bwsDays = Math.round(bwsDays * 0.6);
    }

    // Format costs
    traditionalCostEl.textContent = `€${traditionalCost.toLocaleString('it-IT')}`;
    bwsCostEl.textContent = `€${bwsCost.toLocaleString('it-IT')}`;
    
    const savings = traditionalCost - bwsCost;
    savingsEl.textContent = `Risparmi €${savings.toLocaleString('it-IT')} (${Math.round((savings / traditionalCost) * 100)}%)`;
    
    bwsTimeEl.textContent = `${bwsDays} ${bwsDays === 1 ? 'giorno' : 'giorni'}`;
    bwsMonthlyEl.textContent = `da €${projectData.bwsMonthly}/mese`;
    traditionalTimeEl.textContent = `${traditionalDays} giorni`;

    // Save calculation description for pre-filling the contact form
    const featuresList = Array.from(checkboxes).map(cb => extraFeatures[cb.value].name).join(', ');
    const calculatorSummary = `Preventivo Calcolato: ${projectData.name}. Caratteristiche extra: [${featuresList || 'Nessuna'}]. Urgenza: ${urgency === 'urgent' ? 'Alta (Prioritario)' : 'Normale'}. Costo stimato: €${bwsCost} in ${bwsDays} giorni.`;
    calculatorCta.setAttribute('data-summary', calculatorSummary);
  }

  // Set up event listeners for calculator
  if (projectTypeSelect) {
    projectTypeSelect.addEventListener('change', updateCalculator);
    calcUrgencySelect.addEventListener('change', updateCalculator);
    
    // Generate feature checkboxes
    if (calcFeaturesList) {
      calcFeaturesList.innerHTML = '';
      Object.entries(extraFeatures).forEach(([key, feature]) => {
        const div = document.createElement('div');
        div.className = 'flex items-center space-x-3 bg-purple-950/20 p-2.5 rounded-lg border border-purple-900/30 hover:border-purple-500/30 transition-colors';
        div.innerHTML = `
          <input type="checkbox" id="feature-${key}" value="${key}" class="w-4 h-4 text-purple-600 bg-gray-900 rounded border-purple-900 focus:ring-purple-500 focus:ring-2">
          <label for="feature-${key}" class="text-sm text-gray-300 cursor-pointer select-none flex-grow">
            ${feature.name} <span class="text-xs text-purple-400 block">+€${feature.cost}</span>
          </label>
        `;
        calcFeaturesList.appendChild(div);
        
        // Add event listener to checkbox
        div.querySelector('input').addEventListener('change', updateCalculator);
      });
    }

    // Connect Calculator CTA to Contact Form
    if (calculatorCta) {
      calculatorCta.addEventListener('click', (e) => {
        const summary = e.currentTarget.getAttribute('data-summary');
        const messageField = document.getElementById('message');
        if (messageField && summary) {
          messageField.value = `Salve BWS, vorrei richiedere una consulenza basata sul mio preventivo personalizzato:\n\n${summary}\n\nGrazie!`;
          
          // Scroll smoothly to contact form
          const contactSection = document.getElementById('contatti');
          if (contactSection) {
            contactSection.scrollIntoView({ behavior: 'smooth' });
            
            // Add a temporary subtle glow highlight to the form
            const contactForm = document.querySelector('#contatti form');
            if (contactForm) {
              contactForm.classList.add('ring-2', 'ring-purple-500');
              setTimeout(() => {
                contactForm.classList.remove('ring-2', 'ring-purple-500');
              }, 3000);
            }
          }
        }
      });
    }

    // Initial calculation
    updateCalculator();
  }

  // --- Interactive AI Chatbot Assistant ---
  const chatMessagesContainer = document.getElementById('chat-messages');
  const chatInput = document.getElementById('chat-input');
  const chatSendBtn = document.getElementById('chat-send-btn');
  const quickRepliesContainer = document.getElementById('chat-quick-replies');

  const botResponses = {
    'default': "Scusa, non ho capito bene la domanda. Posso darti informazioni sui nostri servizi, sui nostri prezzi o su come l'AI può accelerare lo sviluppo aziendale!",
    'chi_siamo': "BWS (Bogdan Web Services) è un'agenzia digitale di nuova generazione. Usiamo l'Intelligenza Artificiale per progettare e sviluppare siti web, app, automazioni e software su misura. Questo ci permette di consegnare i progetti 5 volte più velocemente della concorrenza e con costi ridotti fino al 60%, mantenendo una qualità eccellente.",
    'servizi': "Realizziamo:\n1. 🤖 **Sistemi AI & Automazioni**: chatbot intelligenti, automazione dei processi aziendali ripetitivi, integrazione LLM.\n2. 🌐 **Siti Web & Landing Pages**: siti web moderni, veloci, SEO-friendly con copywriting ottimizzato.\n3. 📱 **App Web & Mobile**: software gestionali, applicazioni personalizzate e piattaforme SaaS su misura.",
    'prezzi': "I nostri prezzi partono da soli €399 per una Landing Page e €699 per un sito aziendale completo. Grazie all'AI, eliminiamo le inefficienze dello sviluppo tradizionale. Vuoi fare una prova? Usa il nostro **Calcolatore di Preventivi** qui sopra per stimare il costo del tuo progetto!",
    'contatti': "Puoi scriverci direttamente compilando il modulo qui a fianco oppure inviarci un'email a **info@bws.it**. Offriamo una prima consulenza strategica gratuita di 30 minuti per analizzare le tue necessità e capire come l'AI può aiutarti!",
    'funzionamento_ai': "L'AI non sostituisce i nostri programmatori e designer, ma ne moltiplica la produttività. Usiamo strumenti avanzati di AI generativa per la scrittura del codice, la generazione di asset grafici, la traduzione automatica e la creazione di contenuti SEO. Il risultato? Software senza bug, scritti in tempi record e testati in modo impeccabile."
  };

  const quickReplies = [
    { text: "⚡ Chi è BWS?", intent: 'chi_siamo' },
    { text: "🛠️ Che servizi offrite?", intent: 'servizi' },
    { text: "💰 Quanto costa un sito?", intent: 'prezzi' },
    { text: "🦾 Come usate l'AI?", intent: 'funzionamento_ai' },
    { text: "📬 Come posso contattarvi?", intent: 'contatti' }
  ];

  function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'typing-indicator';
    indicator.className = 'chat-bubble bot text-sm flex items-center space-x-1 py-2 px-3';
    indicator.innerHTML = `
      <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
      <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
      <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
    `;
    chatMessagesContainer.appendChild(indicator);
    chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
  }

  function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
      indicator.remove();
    }
  }

  function addMessage(text, sender) {
    if (!chatMessagesContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-bubble ${sender} text-sm`;
    
    // Handle simple markdown-style bolding and list numbers in bot answers
    let formattedText = text
      .replace(/\n/g, '<br>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      
    messageDiv.innerHTML = formattedText;
    
    chatMessagesContainer.appendChild(messageDiv);
    chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
  }

  function handleBotResponse(intent) {
    showTypingIndicator();
    
    // Simulate natural thinking delay
    setTimeout(() => {
      removeTypingIndicator();
      const responseText = botResponses[intent] || botResponses['default'];
      addMessage(responseText, 'bot');
    }, 1000 + Math.random() * 800);
  }

  function handleUserMessage(messageText) {
    if (!messageText.trim()) return;
    
    addMessage(messageText, 'user');
    
    // Determine intent from message keywords
    let matchedIntent = 'default';
    const textLower = messageText.toLowerCase();
    
    if (textLower.includes('chi') || textLower.includes('cosa è') || textLower.includes('bws') || textLower.includes('presentat') || textLower.includes('bogdan')) {
      matchedIntent = 'chi_siamo';
    } else if (textLower.includes('serviz') || textLower.includes('cosa fat') || textLower.includes('realizzat') || textLower.includes('svilupp')) {
      matchedIntent = 'servizi';
    } else if (textLower.includes('cost') || textLower.includes('prezz') || textLower.includes('tariff') || textLower.includes('preventiv') || textLower.includes('quant')) {
      matchedIntent = 'prezzi';
    } else if (textLower.includes('contat') || textLower.includes('scriv') || textLower.includes('email') || textLower.includes('telefono') || textLower.includes('appuntament')) {
      matchedIntent = 'contatti';
    } else if (textLower.includes('come usat') || textLower.includes('intelligenza') || textLower.includes('funziona') || textLower.includes('come possibil') || textLower.includes('perch')) {
      matchedIntent = 'funzionamento_ai';
    }
    
    handleBotResponse(matchedIntent);
  }

  function setupQuickReplies() {
    if (!quickRepliesContainer) return;
    quickRepliesContainer.innerHTML = '';
    
    quickReplies.forEach(reply => {
      const button = document.createElement('button');
      button.className = 'text-xs bg-purple-950/40 text-purple-300 border border-purple-900/60 hover:bg-purple-900/50 hover:border-purple-500 hover:text-white px-3 py-1.5 rounded-full transition-all duration-200 text-left shrink-0';
      button.textContent = reply.text;
      button.addEventListener('click', () => {
        addMessage(reply.text, 'user');
        handleBotResponse(reply.intent);
      });
      quickRepliesContainer.appendChild(button);
    });
  }

  if (chatMessagesContainer) {
    // Initial bot message
    setTimeout(() => {
      addMessage("Ciao! Sono l'assistente virtuale di **BWS (Bogdan Web Services)** 🤖. Come posso aiutarti oggi? Scegli una delle domande frequenti qui sotto o scrivimi direttamente!", 'bot');
      setupQuickReplies();
    }, 500);

    // Send button event
    if (chatSendBtn && chatInput) {
      chatSendBtn.addEventListener('click', () => {
        const text = chatInput.value;
        if (text.trim()) {
          handleUserMessage(text);
          chatInput.value = '';
        }
      });

      chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          const text = chatInput.value;
          if (text.trim()) {
            handleUserMessage(text);
            chatInput.value = '';
          }
        }
      });
    }
  }

  // --- Contact Form Submission & Feedback ---
  const contactForm = document.querySelector('#contatti form');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      const originalBtnText = submitBtn ? submitBtn.innerHTML : 'Invia Messaggio';
      
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg> Elaborazione in corso...
        `;
      }

      // Simulate network request delay (1.5 seconds)
      setTimeout(() => {
        // Create modern elegant notification modal/box
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-sm transition-opacity duration-300';
        modal.innerHTML = `
          <div class="bg-gray-900 border border-purple-900 p-8 rounded-2xl max-w-md w-full text-center shadow-2xl relative overflow-hidden animate-float">
            <!-- Background glows -->
            <div class="absolute -top-10 -right-10 w-32 h-32 bg-purple-500/20 rounded-full filter blur-xl"></div>
            <div class="absolute -bottom-10 -left-10 w-32 h-32 bg-pink-500/10 rounded-full filter blur-xl"></div>
            
            <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-purple-950/50 border border-purple-500/30 text-purple-400 mb-6">
              <svg class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            
            <h3 class="text-2xl font-bold text-white mb-2 font-display">Messaggio Inviato!</h3>
            <p class="text-gray-300 mb-6 text-sm">
              Grazie per averci contattato. Abbiamo ricevuto la tua richiesta e un nostro consulente ti risponderà entro le prossime 24 ore. Benvenuto nel futuro digitale!
            </p>
            
            <button id="close-modal-btn" class="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white font-medium py-3 px-6 rounded-xl transition-all duration-300 shadow-lg shadow-purple-950/50 hover:shadow-purple-500/20">
              Chiudi finestra
            </button>
          </div>
        `;
        
        document.body.appendChild(modal);
        
        // Reset form
        contactForm.reset();
        
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalBtnText;
        }

        // Close modal logic
        const closeModalBtn = document.getElementById('close-modal-btn');
        if (closeModalBtn) {
          closeModalBtn.addEventListener('click', () => {
            modal.remove();
          });
        }
      }, 1500);
    });
  }
});
