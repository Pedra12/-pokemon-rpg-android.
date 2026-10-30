# Aventura Elemental — Android

Este repositório compila e aplica melhorias sobre o projeto Android vertical enviado no arquivo `pokemon-rpg-android-clover-valley-map.zip`.

## Gerar o APK pelo celular

1. Abra a aba **Actions**.
2. Escolha **Build Aventura Elemental Android APK**.
3. Aguarde a execução terminar com sucesso.
4. Abra a execução e baixe o artefato `aventura-elemental-android-debug`.
5. Extraia o ZIP e instale o APK no Android.

Se já houver uma versão Debug instalada e o Android recusar a atualização, desinstale a versão anterior antes de instalar a nova.

## Recursos já implementados nesta base

- Android nativo com Kotlin e Jetpack Compose.
- Orientação retrato e tela imersiva.
- Cenário com sprites e tiles originais do pacote Clover Valley V2 Free.
- Personagem com animações direcionais e controles por botões ou arrasto na área do mapa.
- Encontros aleatórios e batalhas por turnos.
- Vantagens elementais, poções, experiência e níveis.
- Captura de criaturas com chance variável conforme a vida do adversário.
- Tela de equipe com criaturas capturadas.
- Evolução de Brasa para Brasalume ao atingir o nível 5.
- Três regiões com layouts diferentes, desbloqueadas após 3 e 6 vitórias.
- Eventos de diálogo da história e salvamento local do progresso.
- Efeito visual de ataque e sprites de criaturas em pixel art.
- Seletor de idioma Português (Brasil) / English; parte da interface ainda está em tradução.

## O que ainda falta para a versão final

- História completa com começo, desenvolvimento, missões e final emocional.
- NPCs visuais, diálogos interativos e missões em cada região.
- Mapas maiores, interiores de casas e áreas secretas.
- Mais criaturas com sprites próprios, captura detalhada, equipe ativa e árvores de evolução.
- Animações individuais de ataques, efeitos elementais e ajustes finais de equilíbrio.
- Tradução completa de todas as mensagens e telas.
- Testes de instalação, desempenho e jogabilidade em aparelho Android real.

Esta versão é uma evolução jogável da base, mas ainda não deve ser considerada o RPG completo.

## Recursos e licenças

O pacote Clover Valley V2 Free foi fornecido pelo usuário. O arquivo de leitura que acompanha o pacote foi preservado nos assets. Antes de publicar ou distribuir o jogo, confira os termos atuais na página original do autor e mantenha os créditos exigidos. O pacote gratuito tem restrições de uso comercial e de redistribuição dos arquivos de arte.

O jogo usa criaturas, nomes e identidade originais. Não utiliza sprites ou nomes oficiais de Pokémon.

## Compilação

O workflow `.github/workflows/build-android.yml` extrai o projeto vertical, aplica as melhorias de `scripts/patch_vertical_game.py`, compila com Java 17 / Android SDK 35 / Gradle 8.9 e publica um APK Debug para teste.
