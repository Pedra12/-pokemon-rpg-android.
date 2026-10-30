# Aventura Elemental — Android

Este repositório compila o projeto Android vertical **Aventura Elemental** que está no arquivo `pokemon-rpg-android-clover-valley-map.zip` do repositório de origem.

## Gerar o APK pelo celular

1. Abra a aba **Actions**.
2. Escolha **Build Aventura Elemental Android APK**.
3. Aguarde a execução terminar com sucesso.
4. Abra a execução e baixe o artefato `aventura-elemental-android-debug`.
5. Extraia o ZIP e instale o APK no Android. Se necessário, permita a instalação pelo navegador ou gerenciador de arquivos.

## Base atual

- Android nativo com Kotlin e Jetpack Compose.
- Orientação retrato e interface imersiva.
- Cenário desenhado com os tiles e sprites do pacote Clover Valley V2 Free.
- Personagem com animações direcionais e caminhada.
- Movimento por controles na tela, colisões simples e encontros aleatórios.
- Batalhas por turnos, tipos elementais, poções, experiência e níveis.
- Salvamento local de posição, direção, vida, poções e progresso.

## O que ainda está em desenvolvimento

Esta é uma base jogável inicial, não a versão final do RPG planejado. Ainda faltam:

- Captura, equipe e evolução de criaturas.
- Mais mapas e áreas desbloqueadas por progresso.
- NPCs, diálogos, missões e história com começo, meio e fim.
- Animações de ataque e efeitos de batalha.
- Menu de idioma Português (Brasil) / English.
- Controles por arrasto/toque no cenário e refinamento da interface.
- Testes no aparelho Android real.

## Recursos e licenças

O pacote Clover Valley V2 Free foi fornecido pelo usuário. Seu arquivo de leitura está preservado nos assets. A página do autor informa que a versão gratuita pode ser usada em projetos não comerciais e não pode ser revendida nem redistribuída como pacote de assets. Antes de publicar ou distribuir o jogo, confira os termos atuais e mantenha os créditos/avisos exigidos.

O jogo usa criaturas, nomes e identidade originais. Não utiliza sprites ou nomes oficiais de Pokémon.

## Estrutura

- `source/pokemon-rpg-android-clover-valley-map.zip`: projeto Android de origem.
- `.github/workflows/build-android.yml`: compilação automática do APK.
