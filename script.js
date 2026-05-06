// Year stamp
document.getElementById('year').textContent = new Date().getFullYear();

// Sticky-nav background toggle
const nav = document.getElementById('nav');
const onScroll = () => {
  if (window.scrollY > 40) nav.classList.add('scrolled');
  else nav.classList.remove('scrolled');
};
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// Reveal-on-scroll
const io = new IntersectionObserver((entries) => {
  for (const e of entries) {
    if (e.isIntersecting) {
      e.target.classList.add('in');
      io.unobserve(e.target);
    }
  }
}, { threshold: 0.15, rootMargin: '0px 0px -8% 0px' });

document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// Contact form — opens user's mail client with prefilled body.
// Swap action to a Formspree/Web3Forms endpoint when backend is set up.
const form = document.getElementById('contactForm');
const status = document.getElementById('formStatus');

if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;

    const data = new FormData(form);
    const name = (data.get('name') || '').toString().trim();
    const email = (data.get('email') || '').toString().trim();
    const company = (data.get('company') || '').toString().trim();
    const topic = (data.get('topic') || 'Anfrage').toString();
    const message = (data.get('message') || '').toString().trim();

    const subject = `[Enlivion] ${topic}`;
    const body =
      `Name: ${name}\n` +
      `E-Mail: ${email}\n` +
      (company ? `Unternehmen: ${company}\n` : '') +
      `Thema: ${topic}\n\n` +
      `Nachricht:\n${message}\n`;

    const mailto = `mailto:info@enlivion.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

    status.className = 'form-status success';
    status.textContent = 'Wir öffnen Ihr Mail-Programm — bitte Senden bestätigen.';
    window.location.href = mailto;
  });
}
