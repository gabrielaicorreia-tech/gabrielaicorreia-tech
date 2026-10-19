# Guia visual — Dreamy × Neon (v2)

**Status:** em revisão na branch `claude/inspiring-wozniak-cv71gr`; publicação na `main` depende de aprovação.

## Conceito aprovado

- Duas versões da mesma identidade, escolhidas pelo tema de quem visita (`<picture>` com `prefers-color-scheme`):
  - **Clara — Dreamy gradient:** degradê rosa, lilás e pêssego, vidro, estrelas cromadas.
  - **Escura — Neon night:** fundo noturno com grade, brilho rosa, lilás e menta.
- Apresentação: **IA × Ciência de Dados × Desenvolvimento de Sistemas**, com a Psicologia como diferencial.
- Personalidade: gatinho preto, disco de vinil, flores, janela de código `gabi.js`.
- Animações leves (estrelas, vinil, cursor, equalizador), desligadas quando o visitante pede movimento reduzido.

## Paletas

| Token | Clara | Escura |
|---|---|---|
| Texto | `#2B1B3D` | `#F5EFFF` |
| Texto secundário | `#5B4A6E` | `#C9BEE6` |
| Rosa | `#E2408F` | `#FF4FB8` |
| Lilás | `#8A5CF6` | `#B57BFF` |
| Menta | `#1FA37A` | `#4FF0D0` |
| Pêssego | `#F28B5B` | `#FF9F6B` |

## Imagens

Todas são geradas por `assets/src/gerar_assets.py` (Python, sem dependências):

```
python assets/src/gerar_assets.py
```

Saída em `assets/light/` e `assets/dark/`: `banner`, `areas`, `stack`, `cards/*`, `musica` e `footer`. Para mudar textos ou cores, edite o script e gere de novo; não edite os SVGs à mão.

## Limites técnicos

- O GitHub mostra SVG como imagem: sem fontes externas (usamos fontes do sistema) e sem links dentro da imagem.
- Os textos de cada imagem estão também no `alt`, para leitores de tela.
- Cards de projeto são **categorias genéricas**, sem nomes, dados ou links de repositórios privados.
- O card de música é decorativo; quando houver playlist pública, adicionar um link comum abaixo dele.

## Segurança e publicação

- Não divulgar código, dados institucionais, informações de candidatos ou detalhes de projetos privados.
- Não inventar métricas, conquistas, tecnologias dominadas ou projetos públicos.
- Para o README aparecer no perfil, o repositório precisa ser público; isso é decisão da proprietária.
