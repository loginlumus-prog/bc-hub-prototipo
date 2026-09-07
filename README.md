# BC Hub — protótipo

Protótipo de apresentação da plataforma de indicação da BC Consultoria &
Assessoria: recuperação de crédito tributário (CNPJ) e negociação de dívida
negativada (CPF), com rede de indicadores remunerada.

**No ar:** ver a aba Pages deste repositório.

## Como é montado

O site vive em dois arquivos que são editados separadamente e fundidos num só:

| Arquivo | O que é |
|---|---|
| `prototipo/landing.html` | página pública |
| `prototipo/painel.html`  | plataforma — 28 telas, 6 perfis |
| `prototipo/montar.py`    | funde os dois em `index.html` |

As duas metades usam os mesmos nomes de classe (`.bt`, `.chapeu`, `.duas`) com
valores diferentes, então o montador prefixa cada regra de CSS com o container
dela: `#site` para a página pública, `#plataforma` para o sistema. Sem isso uma
metade quebra a outra em silêncio.

As imagens ficam embutidas como data URI (`prototipo/img/*.b64`), geradas a
partir dos originais em `prototipo/img/`.

Para reconstruir depois de editar:

    cd prototipo && python montar.py && cp bc-hub-completo.html ../index.html

## Acessos de demonstração

Senha de todos os perfis: `bc2026`

| Perfil | E-mail |
|---|---|
| Indicador | ricardo@bchub.com.br |
| Comercial | camila@bchub.com.br |
| Jurídico | larissa@carvalhofontes.adv.br |
| Financeiro | financeiro@bchub.com.br |
| Administração | admin@bchub.com.br |
| Cliente | contato@valenorte.com.br |

Todos os dados são de demonstração. Nenhum cliente, processo ou valor é real.
