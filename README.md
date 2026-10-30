# Crônicas de Arvandor — compilação Android

Este repositório prepara a compilação Android do projeto aberto **Guardian Monsters**, adaptado inicialmente com o nome **Crônicas de Arvandor**.

## Projeto original e código-fonte

O código-fonte completo e os assets do jogo estão no repositório de trabalho:

https://github.com/Pedra12/-pokemon-rpg-android

O jogo original é **Guardian Monsters**, de Georg Eckert:
https://github.com/lucidtanooki/guardian_monsters

A compilação deste repositório baixa o repositório de trabalho acima, incluindo o submódulo com o jogo e seus recursos gráficos. Assim, não é necessário copiar manualmente os arquivos binários do jogo para este repositório.

## Gerar o APK

1. Abra a aba **Actions**.
2. Escolha **Build Guardian Monsters Android APK**.
3. Toque em **Run workflow** ou abra uma execução automática concluída.
4. Na seção **Artifacts**, baixe `cronicas-de-arvandor-android-debug`.
5. Extraia o ZIP e instale o APK no Android.

O APK Debug é destinado a testes. Ainda não é uma versão final de publicação.

## Estado atual e limitações

- A compilação Android foi executada com sucesso no repositório de trabalho original.
- O nome do aplicativo foi alterado para **Crônicas de Arvandor** e foi adicionada uma primeira camada de textos em Português do Brasil.
- A tradução ainda é parcial.
- A base original usa orientação paisagem e resolução lógica 428×240. A interface ainda não foi adaptada para retrato 9:16.
- A história, mapas, diálogos e identidade visual ainda precisam de adaptação para formar o RPG original planejado.
- Os pacotes Clover Valley enviados anteriormente ainda precisam ser integrados e validados dentro do jogo; não considere que já estejam aplicados só porque os arquivos ZIP estão no outro repositório.

## Licenças e atribuições

O código de Guardian Monsters está sob **Apache License 2.0** e as artes principais indicadas pelo projeto estão sob **Creative Commons Attribution 3.0 (CC BY 3.0)**. Alguns recursos de terceiros usam licenças próprias, incluindo CC-BY-SA, BSD, MIT, CC0 e OFL. É obrigatório preservar os avisos e atribuições correspondentes antes de redistribuir o jogo.

Consulte os arquivos de licença e créditos no repositório de trabalho original e no projeto upstream:
https://github.com/lucidtanooki/guardian_monsters
