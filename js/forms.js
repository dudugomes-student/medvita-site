// O navegador só monta a mensagem. Nada é enviado nem guardado pelo site:
// a pessoa revisa o texto e envia pelo próprio WhatsApp.
const WHATSAPP = '5511926264855';
const clean = (value, limit = 200) => String(value ?? '')
  .normalize('NFC')
  .replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g, '')
  .replace(/[ \t]+/g, ' ')
  .trim()
  .slice(0, limit);

const greetings = {
  instituicao: 'Olá, Medvita. Sou de uma instituição e preciso de profissionais de saúde.',
  profissional: 'Olá, Medvita. Sou profissional de saúde e quero deixar meu cadastro.',
  geral: 'Olá, Medvita. Gostaria de conversar.'
};

document.querySelectorAll('[data-whatsapp-form]').forEach(form => {
  const kind = form.dataset.whatsappForm;
  const result = form.querySelector('[data-form-result]');
  const link = result?.querySelector('a');
  const status = result?.querySelector('[role=status]');
  const submit = form.querySelector('button[type=submit]');
  if (!result || !link || !status || !submit) return;
  submit.disabled = false;

  form.addEventListener('input', () => { result.hidden = true; });
  form.addEventListener('submit', event => {
    event.preventDefault();
    // Montar equipe: pelo menos uma especialidade.
    const firstPick = form.querySelector('.picks input');
    if (firstPick && !form.querySelector('.picks input:checked')) {
      firstPick.setCustomValidity('Escolha pelo menos uma área.');
      firstPick.reportValidity();
      form.querySelector('.picks').addEventListener('change', () => firstPick.setCustomValidity(''), { once: true });
      return;
    }
    if (!form.reportValidity()) return;

    const lines = [greetings[kind] || greetings.geral, ''];
    // Cada campo com data-label vira uma linha; caixas marcadas do mesmo grupo viram uma lista.
    const groups = new Map();
    form.querySelectorAll('[data-label]').forEach(field => {
      const label = field.dataset.label;
      if (field.type === 'checkbox' || field.type === 'radio') {
        if (!field.checked) return;
        groups.set(label, [...(groups.get(label) || []), clean(field.value, 60)]);
        return;
      }
      const limit = field.tagName === 'TEXTAREA' ? 1200 : 160;
      const value = clean(field.value, limit);
      if (value) lines.push(`${label}: ${value}`);
    });
    groups.forEach((values, label) => lines.push(`${label}: ${values.join(', ')}`));

    // encodeURIComponent: espaço vira %20 (o WhatsApp não trata "+" como espaço em todos os aparelhos).
    link.href = `https://wa.me/${form.dataset.number || WHATSAPP}?text=${encodeURIComponent(lines.join('\n'))}`;
    result.hidden = false;
    status.textContent = 'Mensagem pronta. Confira o texto e envie no WhatsApp.';
    link.focus();
  });
});
