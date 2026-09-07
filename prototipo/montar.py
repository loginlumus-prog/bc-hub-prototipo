# -*- coding: utf-8 -*-
"""
Funde landing.html + painel.html num arquivo só.

O problema real da fusão é COLISÃO DE CSS: as duas páginas usam os mesmos nomes
(.bt, .chapeu, .duas, .marca) com valores diferentes. Em vez de renomear na mão
— que quebra em silêncio — este script prefixa cada regra com o container dela:
as da landing viram `#site ...`, as do painel viram `#plataforma ...`.
"""
import re, io, sys

def bloco(arq, tag):
    h = open(arq, encoding='utf-8').read()
    m = re.search(r'<%s>(.*?)</%s>' % (tag, tag), h, re.S)
    return m.group(1) if m else ''

def markup(arq):
    """Tudo entre </style> e <script>."""
    h = open(arq, encoding='utf-8').read()
    ini = h.index('</style>') + len('</style>')
    fim = h.index('<script>')
    return h[ini:fim].strip()

def fatiar(css):
    """Quebra o CSS em pedaços de nível superior, preservando comentários."""
    out, buf, prof, i = [], '', 0, 0
    while i < len(css):
        if css[i:i+2] == '/*':
            j = css.index('*/', i) + 2
            buf += css[i:j]; i = j; continue
        c = css[i]; buf += c
        if c == '{': prof += 1
        elif c == '}':
            prof -= 1
            if prof == 0:
                out.append(buf); buf = ''
        i += 1
    if buf.strip(): out.append(buf)
    return out

def prefixar_sel(sel, P):
    saida = []
    for s in sel.split(','):
        s = s.strip()
        if not s: continue
        if s == 'body':
            saida.append('__PULAR__')
        elif s.startswith('body'):
            # `body[data-nivel] .mod-c` -> `body[data-nivel] #plataforma .mod-c`
            partes = s.split(' ', 1)
            saida.append(partes[0] + ' ' + P + (' ' + partes[1] if len(partes) > 1 else ''))
        else:
            saida.append(P + ' ' + s)
    return saida

def prefixar(css, P):
    fora = []
    for pedaco in fatiar(css):
        cru = pedaco.strip()
        if not cru: continue
        if cru.startswith('/*') and '{' not in cru:
            fora.append(pedaco); continue
        pre = ''
        if cru.startswith('/*'):
            corte = cru.index('*/') + 2
            pre, cru = cru[:corte] + '\n', cru[corte:].strip()
        if not cru:
            fora.append(pre); continue
        sel = cru[:cru.index('{')].strip()
        corpo = cru[cru.index('{')+1:cru.rindex('}')]
        if sel.startswith('@keyframes') or sel.startswith(':root'):
            fora.append(pre + cru); continue
        if sel.startswith('@media') or sel.startswith('@supports'):
            fora.append(pre + sel + '{\n' + prefixar(corpo, P) + '\n}'); continue
        novos = [s for s in prefixar_sel(sel, P) if s != '__PULAR__']
        if not novos:
            continue                      # regra `body{}` sai; a base cobre
        fora.append(pre + ', '.join(novos) + '{' + corpo + '}')
    return '\n'.join(fora)

BASE = """
/* ============================================================
   BASE COMPARTILHADA
   As duas metades do site vivem no mesmo arquivo: #site é a
   página pública, #plataforma é o sistema. O que muda entre
   elas (escala de texto) fica no container, não no body.
   ============================================================ */
*{box-sizing:border-box}
body{
  margin:0;background:var(--breu);color:var(--marfim);
  font-family:var(--sans);-webkit-font-smoothing:antialiased;overflow-x:hidden;
}
#site{font-size:15px;line-height:1.6}
#plataforma{font-size:13.5px;line-height:1.55}

/* ⚠️ NÃO REMOVER.
   Toda a navegação — trocar site/plataforma, entrar, montar o menu por
   perfil — esconde elemento com `el.hidden`. Mas o `[hidden]` do navegador
   é regra de UA, e QUALQUER `display` do nosso CSS ganha dela: como
   `.entrada` é `display:grid` e `.casca` é `display:flex`, marcar hidden
   não surtia efeito nenhum e a tela de entrada ficava colada por cima.
   Dentro do visualizador de artifact isso passou despercebido porque o
   host injeta esta mesma regra; em página servida sozinha, não existe. */
[hidden]{display:none!important}
"""

css_l = prefixar(bloco('landing.html', 'style'), '#site')
css_p = prefixar(bloco('painel.html',  'style'), '#plataforma')

js_l = bloco('landing.html', 'script')
js_p = bloco('painel.html',  'script')

TROCA = """
/* ── A troca entre o site e a plataforma ───────────────────── */
(function(){
  "use strict";
  var site = document.getElementById("site");
  var plat = document.getElementById("plataforma");

  function verSite(){
    plat.hidden = true; site.hidden = false;
    window.scrollTo({ top:0, behavior:"instant" });
  }
  function verPlataforma(){
    site.hidden = true; plat.hidden = false;
    window.scrollTo({ top:0, behavior:"instant" });
  }
  /* Merge, nunca substituir: o script do painel já pendurou
     abrirEntrada/abrirCadastro aqui antes deste bloco rodar. */
  window.BC = window.BC || {};
  window.BC.verSite = verSite;
  window.BC.verPlataforma = verPlataforma;

  document.querySelectorAll("[data-ir]").forEach(function(b){
    b.addEventListener("click", function(e){
      e.preventDefault();
      var onde = b.dataset.ir;
      if (onde === "site") return verSite();
      verPlataforma();
      if (onde === "cadastro") window.BC.abrirCadastro();
      else window.BC.abrirEntrada();
    });
  });

  if (location.hash === "#cadastro"){ verPlataforma(); window.BC.abrirCadastro(); }
  else if (location.hash === "#entrar"){ verPlataforma(); window.BC.abrirEntrada(); }
})();
"""

SAIDA = """<title>BC Hub</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,200;0,300;0,400;0,500;1,6..72,200;1,6..72,300&family=Manrope:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">

<style>
{base}

/* ══════════════════ PÁGINA PÚBLICA ══════════════════ */
{css_l}

/* ══════════════════ PLATAFORMA ══════════════════ */
{css_p}
</style>

<div id="site">
{mk_l}
</div>

<div id="plataforma" hidden>
{mk_p}
</div>

<script>
{js_l}
{js_p}
{troca}
</script>
""".format(base=BASE, css_l=css_l, css_p=css_p,
           mk_l=markup('landing.html'), mk_p=markup('painel.html'),
           js_l=js_l, js_p=js_p, troca=TROCA)

# imagens embutidas
for chave, arq in [('__IMG_HERO__','hero_w'), ('__IMG_REUNIAO__','reuniao_w'),
                   ('__IMG_DOCS__','docs_w'), ('__IMG_TEXTURA__','textura_w')]:
    SAIDA = SAIDA.replace(chave, open('img/%s.b64' % arq).read().strip())

io.open('bc-hub-completo.html', 'w', encoding='utf-8').write(SAIDA)

restos = [t for t in ('__IMG_', '__LINK_', '__PULAR__') if t in SAIDA]
print('placeholders nao substituidos:', restos or 'nenhum')
print('tamanho: %.2f MB' % (len(SAIDA.encode('utf-8'))/1024/1024))
